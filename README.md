# Slack Alert

|                |                                 |
| -------------- | ------------------------------- |
| Name           | Slack Alert                     |
| Version        | v0.0.2                          |
| Dockerhub Link | [weevenetwork/weeve-slack-alert](https://hub.docker.com/r/weevenetwork/weeve-slack-alert)  |
| Authors        | Jakub Grzelak                   |



- [Slack Alert](#slack-alert)
  - [Description](#description)
  - [Features](#features)
  - [Sample Notifications](#sample-notifications)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)
  - [Docker Compose Example](#docker-compose-example)


## Description

Slack Alert is an alerting module responsible for sending notifications to Slack channels when triggered.
This module is containerized using Docker.


## Features

* Egress data from data service
* Send notification to Slack Channel


## Sample Notifications

| Type        | Text                  |
| ----------- | --------------------- |
| warning     | _WARNING for MachineName! Temperature reading shows 41.19 Celsius._               |
| alarming    | _ALARM from MachineName! Detected an alarming reading of Temperature: 100 Celsius._ |
| caution     | _CAUTION for MachineName! Temperature is 100 Celsius._                             |
| broken      | _BROKEN device MachineName! Detected Temperature reading is -1.1 Celsius._         |


## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:


| Name                | Environment Variables | Type    | Description                                            |
| ------------------- | --------------------- | ------- | ------------------------------------------------------ |
| Input Label         | INPUT_LABEL           | string  | The field to apply alert on, i.e: "temperature"        |
| Input Unit          | INPUT_UNIT            | string  | I.e: "Celsius"                                         |
| Alert Severity      | ALERT_SEVERITY        | string  | Alert type: warning, alarming, caution, broken         |
| Slack Webhook URL   | SLACK_WEBHOOK_URL     | string  | Webhook to the slack channel to put alerts on, format: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'         |


Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

### Set by the weeve Agent on the edge-node

| Environment Variables | type   | Description                            |
| --------------------- | ------ | -------------------------------------- |
| EGRESS_URL            | string | HTTP ReST endpoint for the next module |
| MODULE_NAME           | string | Name of the module                     |
| MODULE_TYPE           | string | Type of the module (ingress, processing, egress)  |


## Dependencies

```txt
Flask==1.1.1
requests
python-dotenv
python-decouple==3.4
```

## Input

Input to this module is JSON body single object:

Example:
```node
{
  temperature: 15,
}
```

## Output

This module does not produce any output except Slack notifications.

## Docker Compose Example

```yml
version: "3"
services:
  slack-alert:
    image: weevenetwork/weeve-slack-alert
    environment:
      MODULE_NAME: slack-alert
      MODULE_TYPE: EGRESS
      EGRESS_URL: https://hookb.in/DrrdzwQwXgIdNNEwggLo
      INPUT_LABEL: "temperature"
      INPUT_UNIT: "Celsius"
      ALERT_SEVERITY: "warning"
      SLACK_WEBHOOK_URL: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
    ports:
      - 5000:80
```
