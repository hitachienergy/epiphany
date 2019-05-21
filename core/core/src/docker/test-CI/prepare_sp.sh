mkdir -p tmp/sp
mkdir -p core/build/azure/infrastructure/$RESOURCE_GROUP

echo '{
  "appId": "{{ sp_client_id }}",
  "displayName": "epiphany-vsts",
  "name": "http://epiphany-vsts",
  "password": "{{ sp_client_secret }}",
  "tenant": "{{ sp_tenant_id }}"
}
' >> tmp/sp/az_ad_sp.json

sed "/set -e/q" core/core/src/templates/azure/env.sh.j2 > tmp/sp/env.sh

echo 'export ARM_SUBSCRIPTION_ID="{{ sp_subscription_id }}"
export ARM_CLIENT_ID="{{ sp_client_id }}"
export ARM_CLIENT_SECRET="{{ sp_client_secret }}"
export ARM_TENANT_ID="{{ sp_tenant_id }}"
' >> tmp/sp/env.sh

echo "
---
# Security.yaml

core:
  azure:
    terraform:
      # This version info is what version is being used at the moment. The version of Terraform in the manifest.yaml in the
      # root of the repo is for the initial install and the minum version
      version: 1.6
      service_principal:
        # Three files are required for SPs to work, az_ad_sp.json, env.sh and security.yaml. By default, these are created if the
        # 'create' attribute is true. If false then you will need to supply those two files. This allows you to create
        # a service_principal of your own instead of having one generated.
        # You will also need to override env.sh that contains the 'ARM_...' environment variables required.
        enable: True
        create: False # If you want to use an existing one then set this to false
      auth: pwd # Valid is 'pwd' and 'cert'. At this time Terraform only support 'pwd' for service principals
      # NOTE: Backend is a Terraform resource that stores the *.tfstate files used by Terraform to store state. The default
      # is to store the state file locally but this can cause issues if working in a team environment.
      backend:
        # Only used by Terraform
        # The backend storage account is '<resource_group_name>''backend' (combined name with suffix)
        # The storage container is generated as '<resource_group_name>'-'terraform'
        # NOTE: Known issue with backend tf when having different VM types below when enabled! So, only one VM entry with count set should be used. Set to false for now...
        enable: False

subscription_id: {{ sp_subscription_id }}
app_name: epiphany-vsts
app_id: {{ sp_client_id }}
tenant_id: {{ sp_tenant_id }}
role: Contributor
auth: {{ sp_client_secret }}
auth_type: pwd
" >> tmp/sp/security.yaml
sed -i "s/{{ sp_subscription_id }}/$SP_SUBSCRIPTION_ID/g; s/{{ sp_client_id }}/$SP_CLIENT_ID/g; s/{{ sp_tenant_id }}/$SP_TENANT_ID/g; s/{{ sp_client_secret }}/$SP_CLIENT_SECRET/g" tmp/sp/*
cp tmp/sp/* core/build/azure/infrastructure/$RESOURCE_GROUP
rm -rf tmp