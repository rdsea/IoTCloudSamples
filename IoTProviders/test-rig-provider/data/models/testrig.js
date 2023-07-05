import mongoose from '../db.js';

var Testrig = mongoose.model('Testrig', {
    location: String,
    createdAt: Number,
    sliceId: String,
    testrigId: String,
});

export default Testrig;
