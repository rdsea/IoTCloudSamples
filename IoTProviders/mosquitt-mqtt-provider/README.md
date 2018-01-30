# Test Rig provider
This REST server provides an API to provision instances of Mosquitto MQTT for your slice ID

# Usage

`GET /mosquittobroker`
    - provides a sample configuration to provision the broker

`POST /mosquittobroker`
    - creates a broker with the configuration provided from the GET call

`GET /mosquittobroker/:sliceId`
    - returns all the brokers associated with the slice id provided

`DELETE /mosquittobroker/:mosquittobrokerId`
    - deletes the mosquittobroker with the provided id

# Deployment

This server must be deployed somewhere with access to `gcloud` and `kubectl`. Easiest is a google compute VM which has these
components installed