import mongoose from './db.js';

var User = mongoose.model('user', {
   email: { type: String, index: { unique: true } },
   bucketName: String,     
});

export default User;