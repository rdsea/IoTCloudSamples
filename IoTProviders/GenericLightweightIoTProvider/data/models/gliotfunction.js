import mongoose from '../db.js';

var GLIoTFunction = mongoose.model('GLIoTFunction', {
    location: String,
    createdAt: Number,
    sliceId: String,
    local_pid: Number,
    gliotId: String,
    status: String
});

export default GLIoTFunction;
