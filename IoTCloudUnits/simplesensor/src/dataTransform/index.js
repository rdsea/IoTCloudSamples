import csvTransform from './csvTransform.js';
import jsonTransform from './jsonTransform.js';

const transforms = {
    csv: csvTransform,
    json: jsonTransform,
};

export default transforms;