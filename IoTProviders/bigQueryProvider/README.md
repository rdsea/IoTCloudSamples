# Simple IoT Data as a Service based on Big Query

This provide acts as an IoT Data-as-a-Service with the backend of Google BigQuery. 

The idea is that the provider will create datasets and tables for customers. This provider expects a `service_account.json` which is a google service account for BigQuery admin. 

## Configuration

set MONGODB_URL environment to indicate the mongodb backend.

```
$export MONGODB_URL=
$export GOOGLE_APPLICATION_CREDENTIALS=
```
 

## Run

`$ npm start` will start the provider
