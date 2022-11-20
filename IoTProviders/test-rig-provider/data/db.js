import mongoose from 'mongoose';

const MONGODB_URL = process.env.MONGODB_URL;

if (MONGODB_URL !=null)
    mongoose.connect(MONGODB_URL, { useMongoClient: true });
else
    console.count("MONGODB_URL is not set!")
mongoose.Promise = global.Promise;

export default mongoose;