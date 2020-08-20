# Troubleshooting

## Epicli container connection issues after hibernation/sleep on Windows

When running the Epicli container on Windows you might get such errors when trying to run the apply command:

Azure:
```
INFO cli.engine.terraform.TerraformCommand - Error: Error reading queue properties for AzureRM Storage Account "cluster": queues.Client#GetServiceProperties: Failure responding to request: StatusCode=403 -- Original Error: autorest/azure: error response cannot be parsed: "\ufeff<?xml version=\"1.0\" encoding=\"utf-8\"?><Error><Code>AuthenticationFailed</Code><Message>Server failed to authenticate the request. Make sure the value of Authorization header is formed correctly including the signature.\nRequestId:cba2935f-1003-006f-071d-db55f6000000\nTime:2020-02-04T05:38:45.4268197Z</Message><AuthenticationErrorDetail>Request date header too old: 'Fri, 31 Jan 2020 12:28:37 GMT'</AuthenticationErrorDetail></Error>" error: invalid character 'ï' looking for beginning of value
```

AWS:
```
ERROR epicli - An error occurred (AuthFailure) when calling the DescribeImages operation: AWS was not able to validate the provided access credentials
```

These issues might occur when the host machine you are running the Epicli container on was put to sleep or hybernated for an extended period of time. Hyper-V might have issues syncing the time between the container and the host after it wakes up or is resumed. You can confirm this by checking the date and time in your container by running:

```shell
Date
```

If the times are out of sync restarting the container will resolve the issue. If you do not want to restart the container you can also run the following 2 commands from an elevated Powershell prompt to force it during container runtime:

```shell
Get-VMIntegrationService -VMName DockerDesktopVM -Name "Time Synchronization" | Disable-VMIntegrationService

Get-VMIntegrationService -VMName DockerDesktopVM -Name "Time Synchronization" | Enable-VMIntegrationService
```

Common:

When public key is created by `ssh-keygen` sometimes it's necessary to convert it to utf-8 encoding.
Otherwise such error occurs:

```text
ERROR epicli - 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

## Kafka

When running the Ansible automation there is a verification script called `kafka_producer_consumer.py` which creates a topic, produces messages and consumes messages. If the script fails for whatever reason then Ansible verification will report it as an error. An example of an issue is as follows:

```text
ERROR org.apache.kafka.common.errors.InvalidReplicationFactorException: Replication factor: 1 larger than available brokers: 0.
```

This issue is saying the a replication of 1 is being attempted but there are no brokers '0'. This means that the kafka broker(s) are not running any longer. Kafka will start and attempt to establish connections etc. and if unable it will shutdown and log the message. So, when the verification script runs it will not be able to find a local broker (runs on each broker).

Take a look at syslog/dmesg and run `sudo systemctl status kafka`. Most likely it is related to security (TLS/SSL) and/or network but it can also be incorrect settings in the config file `/opt/kafka/config/server.properties`. Correct and rerun the automation.
