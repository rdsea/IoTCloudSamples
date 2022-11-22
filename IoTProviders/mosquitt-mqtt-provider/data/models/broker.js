import mongoose from '../db.js';

var Broker = mongoose.model('Broker', {
    location: String,
    url:String,
    port:Number,
    createdAt: Number,
    sliceId: String,
    qos: Number,
    brokerId: String,
});

export default Broker;
