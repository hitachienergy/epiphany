# Troubleshooting

## Kubernetes

Sometimes Google has a connection issue with pulling down images. You may see something like below:

```text
TASK [master : kubeadm config images pull] **********************************************************************************************
fatal: [vm-epiphany-rhel-playground-master-001]: FAILED! => {"changed": true, "cmd": "kubeadm config images pull", "delta": "0:00:01.428562", "end": "2018-07-18 08:56:47.608629", "msg": "non-zero return code", "rc": 1, "start": "2018-07-18 08:56:46.180067", "stderr": "failed to pull image \"k8s.gcr.io/kube-apiserver-amd64:v1.11.1\": exit status 1", "stderr_lines": ["failed to pull image \"k8s.gcr.io/kube-apiserver-amd64:v1.11.1\": exit status 1"], "stdout": "", "stdout_lines": []}
```

Wait a little while and try again and it will usually resolve itself quickly. If it does not go away then it could be the version of Kubernetes. For example, in the error above, v1.11.1 did not have proper images in the google registry. Changing to v1.11.0 fixed it until Google fixed their issue.

## Kafka

When running the Ansible automation there is a verification script called `kafka_producer_consumer.py` which creates a topic, produces messages and consumes messages. If the script fails for whatever reason then Ansible verification will report it as an error. An example of an issue is as follows:

```text
ERROR org.apache.kafka.common.errors.InvalidReplicationFactorException: Replication factor: 1 larger than available brokers: 0.
```

This issue is saying the a replication of 1 is being attempted but there are no brokers '0'. This means that the kafka broker(s) are not running any longer. Kafka will start and attempt to establish connections etc. and if unable it will shutdown and log the message. So, when the verification script runs it will not be able to find a local broker (runs on each broker).

Take a look at syslog/dmesg and run `sudo systemctl status kafka`. Most likely it is related to security (TLS/SSL) and/or network but it can also be incorrect settings in the config file `/opt/kafka/config/server.properties`. Correct and rerun the automation.
