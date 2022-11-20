import mongoose from 'mongoose';

const MONGODB_URL = process.env.MONGODB_URL;
if (MONGODB_URL !=null)
    mongoose.connect(MONGODB_URL, { useMongoClient: true });
else {
    console.log("MONGODB_URL is not set! The service might not be run")
}
mongoose.Promise = global.Promise;

export default mongoose;