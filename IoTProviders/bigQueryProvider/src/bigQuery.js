import BigQuery from '@google-cloud/bigquery';

let key_file =process.env.GOOGLE_APPLICATION_CREDENTIALS;
if (key_file == null) {
    console.log("GOOGLE_APPLICATION_CREDENTIALS is not set to the credential file");
}

let bigQuery = new BigQuery.BigQuery({
    keyFilename: key_file
});

export default bigQuery;