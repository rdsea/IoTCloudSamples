import mongoose from 'mongoose';
import validUrl from 'valid-url';
const MONGODB_URL = process.env.MONGODB_URL;
if ((MONGODB_URL !=null) && validUrl.isUri(MONGODB_URL)) {
    mongoose.connect(MONGODB_URL,{ useNewUrlParser: true });
}
else
    console.log("MONGODB_URL is not set or not in a right form!")
mongoose.Promise = global.Promise;

export default mongoose;
