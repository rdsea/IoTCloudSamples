import mongoose from 'mongoose';
import validUrl from 'valid-url';
const MONGODB_URL = process.env.MONGODB_URL;

if ((MONGODB_URL !=null) && validUrl.isUri(MONGODB_URL)) {
    //console.log(MONGODB_URL);
mongoose.connect(MONGODB_URL,{ useNewUrlParser: true,connectWithNoPrimary: true }); 
}
else
    console.log("MONGODB_URL is not set or not in the right format! The service might not be executed properly!")


mongoose.Promise = global.Promise;

export default mongoose;
