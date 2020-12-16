#!/usr/bin/env bash

# v1.0.1
# Tested with Kubernetes: 1.11

# This script reproduces what the kubelet does to calculate 'memory.available' relative to root cgroup.
# It also calculates and shows other memory related info which helps you choose values
# for kubelet configuration parameters (e.g. kubeReserved and systemReserved)

# The value for 'memory.available' is derived from the cgroupfs instead of tools like free.

# Docs:
# https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/
# https://kubernetes.io/docs/tasks/administer-cluster/out-of-resource/
# /proc/meminfo estimated available memory: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=34e431b0ae398fc54ea69ff85ec700722c9da773

set -e

## Functions

# params: [what_to_clear: 1 = page cache (default), 2 = reclaimable slab objects (includes dentries and inodes), 3 = all]
function clear_os_caches {
  local what_to_clear=${1}
  [[ -n $what_to_clear ]] || what_to_clear=1
  local what_to_clear_name
  case $what_to_clear in
    1) what_to_clear_name='page cache';;
    2) what_to_clear_name='reclaimable slab objects';;
    3) what_to_clear_name='page cache + reclaimable slab objects';;
    *) echo "Incorrect value"; exit 1;;
  esac
  local cmd="sync; sysctl -w vm.drop_caches=$what_to_clear"
  echo "Clearing OS caches ($what_to_clear_name): $cmd"
  sudo sh -c "$cmd"
  echo "---"
}

# params: number
function convert_number_to_mega {
  echo $((${1} / 1024 / 1024))
}

# params: string, format_code
function format_string {
  local format_code=${2}
  case $format_code in
    bold)   format_code='[1m';;
    yellow) format_code='[33m';;
  esac
  echo "\e${format_code}${1}\e[0m"
}

# params: name, value, [format_code] [only_value_formatted]
function print_value {
  local value=${2}
  if [[ -n ${3} ]] && ((${4})); then # format only value
    value=$(format_string "$value" "${3}")
  fi
  local output="${1}: $value"
  if [[ -n ${3} ]] && ! ((${4})); then # format whole output
    output=$(format_string "$output" "${3}")
  fi
  echo "$output"
}

# params: name, value, [format_code] [only_value_formatted]
function print_value_in_mb {
  local value
  value=$(convert_number_to_mega "${2}")
  if [[ -n ${3} ]] && ((${4})); then # format only value
    value=$(format_string "$value" "${3}")
    print_value "${1}" "$value MB"
  else
    print_value "${1}" "$value MB" "${3}"
  fi
}

# params: cgroup_path
function get_cgroup_memory_usage { # total_rss + total_cache + total_swap
  cat "${1}/memory.usage_in_bytes"
}

# params: cgroup_path
function get_cgroup_rss { # resident set size of cgroup = rss + mapped_file (more info: kernel-doc/Documentation/cgroup-v1/memory.txt)
  local total_rss
  local total_mapped_file
  total_rss=$(grep -w total_rss "${1}/memory.stat" | awk '{print $2}')
  total_mapped_file=$(grep -w total_mapped_file "${1}/memory.stat" | awk '{print $2}')
  echo $((total_rss + total_mapped_file))
}

# params: cgroup_path
function get_cgroup_memory_working_set {
  local memory_usage_in_bytes
  local memory_total_inactive_file
  local memory_working_set=0
  memory_usage_in_bytes=$(get_cgroup_memory_usage "${1}")
  memory_total_inactive_file=$(grep -w total_inactive_file "${1}/memory.stat" | awk '{print $2}')
  if ((memory_usage_in_bytes > memory_total_inactive_file)); then
    memory_working_set=$((memory_usage_in_bytes - memory_total_inactive_file))
  fi
  echo $memory_working_set
}

# params: pid
function get_memory_rss_for_pid {
  echo $(( $(grep VmRSS "/proc/${1}/status" | awk '{print $2}') * 1024 )) # kB to bytes
}

# params: arithmetic_expression, [scale_to_print: default = 0]
function calc_percent {
  local scale_to_print=${2}
  [[ -n $scale_to_print ]] || scale_to_print=0
  awk "BEGIN {printf(\"%.${scale_to_print}f\", ${1} * 100)}"
}

# params: threshold_type (hard|soft)
function get_memory_eviction_threshold_from_kubelet_config {
  local threshold_type=${1}
  local kubelet_config_path=/var/lib/kubelet/config.yaml
  local threshold_name
  case $threshold_type in
    hard) threshold_name='evictionHard';;
    soft) threshold_name='evictionSoft';;
    *) echo "Incorrect value"; exit 1;;
  esac
  local memory_threshold
  memory_threshold=$(sudo grep -v '^\s*#' $kubelet_config_path | grep -A4 ${threshold_name}: | grep -w memory.available | grep -v '[smh]$' | awk '{print $2}')
  if [[ ! $memory_threshold =~ ^[0-9]+([EPTGMKE]i?)?$ ]]; then
    memory_threshold=-1 # unexpected value or threshold not found
  fi
  echo $memory_threshold
}

## Cgroup data

readonly root_cgroup_memory_path=/sys/fs/cgroup/memory

declare -A cgroups; declare -a ordered_keys # associative arrays in Bash are unordered
cgroups[docker.service]=$root_cgroup_memory_path/system.slice/docker.service;   ordered_keys+=(docker.service)
cgroups[kubelet.service]=$root_cgroup_memory_path/system.slice/kubelet.service; ordered_keys+=(kubelet.service)
# on Ubuntu kubepods cgroup has different path (without '.slice'), i.e. '/sys/fs/cgroup/memory/kubepods'
kubepods_cgroup_name=kubepods
if [[ ! -e $root_cgroup_memory_path/$kubepods_cgroup_name ]]; then
  kubepods_cgroup_name=kubepods.slice
fi
cgroups[$kubepods_cgroup_name]=$root_cgroup_memory_path/$kubepods_cgroup_name; ordered_keys+=("$kubepods_cgroup_name")
cgroups[system.slice]=$root_cgroup_memory_path/system.slice;                   ordered_keys+=(system.slice)
cgroups[user.slice]=$root_cgroup_memory_path/user.slice;                       ordered_keys+=(user.slice)

## Options

os_caches_to_clear=0
short_mode=0
verbose_mode=0

for arg
do
  case "$arg" in
    --clear-all-caches|-a) os_caches_to_clear=3;; # clear page cache and reclaimable slab objects (not recommended in production)
    --clear-page-cache|-p) os_caches_to_clear=1;; # clear page cache only
    --short|-s)            short_mode=1;;
    --verbose|-v)          verbose_mode=1;;
    *) echo "Unknown argument: $arg"; exit 1;;
  esac
done

# clear OS caches
((os_caches_to_clear)) && clear_os_caches $os_caches_to_clear

## Root cgroup part, based on k8s script: https://kubernetes.io/docs/tasks/administer-cluster/memory-available.sh

memory_capacity=$(($(grep -w MemTotal /proc/meminfo | awk '{print $2}') * 1024)) # all values in bytes

# current memory usage
memory_usage_from_cgroup=$(cat $root_cgroup_memory_path/memory.usage_in_bytes)
memory_working_set_from_cgroup=$(get_cgroup_memory_working_set $root_cgroup_memory_path)
memory_available_from_cgroup=$((memory_capacity - memory_working_set_from_cgroup))

# print root part
print_value_in_mb 'memory capacity' "$memory_capacity"
echo "---"
echo "cgroup based memory info (used by k8s)"
echo -e "$(print_value_in_mb '  available' "$memory_available_from_cgroup" bold)"
           print_value_in_mb '  working set' "$memory_working_set_from_cgroup"
           print_value_in_mb '  usage' "$memory_usage_from_cgroup"

## Other cgroups part

# get and print data
for cgroup in "${ordered_keys[@]}"; do
  cgroup_path=${cgroups[$cgroup]}
  if [[ $cgroup == "${ordered_keys[0]}" ]]; then
    echo "---"
  else
    echo
  fi
  echo -e "cgroup: $(format_string "$cgroup" bold)"

  if [[ ! -e $cgroup_path ]]; then
    echo -e "  $(format_string skipped yellow) - path not found: $cgroup_path"
    cgroups[${cgroup}.memory.working_set]=0
    continue
  else
    cgroups[${cgroup}.memory.working_set]=$(get_cgroup_memory_working_set $cgroup_path)
  fi

  if [[ $cgroup == "$kubepods_cgroup_name" ]]; then
    echo -e "$(print_value_in_mb '  working set' "${cgroups[${cgroup}.memory.working_set]}" bold)"
  else
    echo -e "$(print_value_in_mb '  working set' "${cgroups[${cgroup}.memory.working_set]}" bold 1)"
  fi
  ((short_mode)) || print_value_in_mb '  resident set size' "$(get_cgroup_rss $cgroup_path)"
  ((short_mode)) || print_value_in_mb '  usage' "$(get_cgroup_memory_usage $cgroup_path)"

  if ((verbose_mode)) && [[ $cgroup == kubelet.service && -f  /sys/fs/cgroup/systemd/system.slice/${cgroup}/cgroup.procs ]]; then
    pid=$(head -1 "/sys/fs/cgroup/systemd/system.slice/${cgroup}/cgroup.procs")
    process_name=$(cat "/proc/$pid/comm")
    echo "process: $process_name (pid: $pid)"
    print_value_in_mb '  resident set size' "$(get_memory_rss_for_pid "$pid")"
  fi
done

## /proc/meminfo based part

# MemAvailable: An estimate of how much memory is available for starting new applications, without swapping.
# Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks in each zone.
# The estimate takes into account that the system needs some page cache to function well, and that not all reclaimable slab will be reclaimable, due to items being in use.

echo "---"
echo -e "/proc/meminfo based: $(format_string 'free -m' bold)"
free -m | grep -E -v 'Swap:[[:space:]]+0' # do not print about swap if zero

memory_available_from_meminfo=$(($(grep MemAvailable: /proc/meminfo | awk '{print $2}') * 1024)) # kB to bytes
memory_working_set_from_meminfo=$((memory_capacity - memory_available_from_meminfo))

if ((verbose_mode)); then
  echo "---"
  vm_min_free_bytes=$(($(cat /proc/sys/vm/min_free_kbytes) * 1024)) # kB to bytes
  low_watermarks_sum=$(awk '$1 == "low" {low_watermarks_sum += $2} END {print low_watermarks_sum * 4096}' /proc/zoneinfo)
  echo "$(print_value_in_mb /proc/sys/vm/min_free_kbytes "$vm_min_free_bytes")", "$(print_value_in_mb 'low watermarks from /proc/zoneinfo' "$low_watermarks_sum")"
fi

## Calculations"

echo
echo "--- calculations ---"
# for kubeReserved
echo -e "$(print_value_in_mb 'docker.service + kubelet.service cgroups working set' \
                             $((${cgroups[docker.service.memory.working_set]} + ${cgroups[kubelet.service.memory.working_set]})) bold)"

echo "$(print_value_in_mb 'meminfo working set' $memory_working_set_from_meminfo) ($(calc_percent "$memory_working_set_from_meminfo / $memory_capacity" 2)%)"

# for systemReserved
estimated_system_working_set=$((memory_working_set_from_meminfo - ${cgroups[docker.service.memory.working_set]} - ${cgroups[kubelet.service.memory.working_set]} \
                                - ${cgroups[${kubepods_cgroup_name}.memory.working_set]} - ${cgroups[user.slice.memory.working_set]}))
echo -e "$(print_value_in_mb 'estimated system working set' "$estimated_system_working_set" bold)"

echo -e "$(print_value_in_mb 'estimated system + docker + kubelet working set' \
                             $((estimated_system_working_set + ${cgroups[docker.service.memory.working_set]} + ${cgroups[kubelet.service.memory.working_set]})) bold 1)"
echo
echo -e "$(print_value_in_mb "memory available $(format_string delta bold) [cgroup - meminfo]" \
                             $((memory_available_from_cgroup - memory_available_from_meminfo)) bold 1)"

## Limits

echo
echo "--- limits ---"

# kubepods cgroup memory limit
if [[ -f ${cgroups[$kubepods_cgroup_name]}/memory.limit_in_bytes ]]; then
  kubepods_cgroup_memory_limit=$(cat "${cgroups[$kubepods_cgroup_name]}/memory.limit_in_bytes")
  if ((kubepods_cgroup_memory_limit > memory_capacity)); then
    echo -e "$(format_string "no memory limit set for $kubepods_cgroup_name cgroup" yellow)"
    kubepods_cgroup_memory_limit=0 # limit was not set
  else
    echo -e "$(print_value_in_mb "$(format_string $kubepods_cgroup_name bold) cgroup memory.limit" $kubepods_cgroup_memory_limit bold 1)"
  fi
else
  echo -e "$(format_string "cgroup $kubepods_cgroup_name not found" yellow) - path not found: ${cgroups[$kubepods_cgroup_name]}/memory.limit_in_bytes"
  kubepods_cgroup_memory_limit=0 # limit not found
fi

# kubelet hard eviction threshold
kubelet_hard_eviction_threshold=$(get_memory_eviction_threshold_from_kubelet_config hard)
if [[ $kubelet_hard_eviction_threshold != "-1" ]]; then # threshold found
  echo -e "$(print_value kubelet.evictionHard.memory.available "$kubelet_hard_eviction_threshold" bold 1)"
  # this script supports only 'Mi' unit (megabytes) for further calculation
  if [[ ! $kubelet_hard_eviction_threshold =~ Mi$ ]]; then
    kubelet_hard_eviction_threshold=-2 # unsupported unit
  else # convert to bytes
    kubelet_hard_eviction_threshold=${kubelet_hard_eviction_threshold/Mi/''}
    kubelet_hard_eviction_threshold=$((kubelet_hard_eviction_threshold * 1024 * 1024))
  fi
fi

# kubelet soft eviction threshold
kubelet_soft_eviction_threshold=$(get_memory_eviction_threshold_from_kubelet_config soft)
if [[ $kubelet_soft_eviction_threshold != "-1" ]]; then # threshold found
  echo -e "$(print_value kubelet.evictionSoft.memory.available "$kubelet_soft_eviction_threshold" bold 1)"
fi

# allocatable memory for pods - if exceeded and hard eviction threshold is set, pod eviction is triggered
if (( kubepods_cgroup_memory_limit && kubelet_hard_eviction_threshold >= 0 )); then
  pods_allocatable_memory=$((kubepods_cgroup_memory_limit - kubelet_hard_eviction_threshold))
  echo -e "$(print_value_in_mb "computed allocatable memory for pods" "$pods_allocatable_memory" bold 1)" \
          "($(calc_percent "${cgroups[${kubepods_cgroup_name}.memory.working_set]} / $pods_allocatable_memory" 2)% in use)"
fi

# load average
if ((! short_mode)); then
  echo "---"
  echo "Load average: $(< /proc/loadavg cut -d' ' -f1-3)"
fi
