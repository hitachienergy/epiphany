# Epiphany Platform Kafka authentication design document

Affected version: 0.5.x

## Goals

Provide authentication for Kafka clients and brokers using:
1). SSL
2). SASL-SCRAM

## Use cases

1). SSL - Kafka will be authorizing clients based on certificate, where certificate will be signed
by common CA root certificate and validated against .
2). SASL-SCRAM - Kafka will be authorizing clients based on credentials and validated using SASL and with SCRAM credentials stored in Zookeeper

## Design proposal

Add to Epiphany configuration/kafka field that will select authentication method - SSL or SASL with SCRAM. Based on this method of authentication will be selected with available settings (e.g. number of iterations for SCRAM).

For SSL option CA certificate will be fetched to machine where Epiphany has been executed, so the user can sign his client certificates with CA certificate and use them to connect to Kafka.

For SASL with SCRAM option Epiphany can create also additional SCRAM credentials creations, that will be used for client authentication.

