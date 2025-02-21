//mqtt topic 
var topic = process.argv[2];
//connection string of mqtt
//mqtt://username:password@hostname:port 
var url = process.argv[3];
var mqtt = require('mqtt');
//load mqtt configuration
var option = {
    //"clean":  false,
    "qos":2
    //"clientId":"6ccf573c-6074-11eb-8f98-f7b88ad5abed"
};


var mqttclient = mqtt.connect(url, option);
//connect to the gateway - what if it fails
mqttclient.on('connect', function () {
    console.log("connected");
    mqttclient.subscribe(topic);
    console.log("Wait for the message");
    //client.publish('presence', 'Hello mqtt');
});
//we must generalize the case, so thaht the client just write the transformation and the publish
mqttclient.on('message', function (topic, message) {
    console.log(topic, message.toString("utf-8"));
});
