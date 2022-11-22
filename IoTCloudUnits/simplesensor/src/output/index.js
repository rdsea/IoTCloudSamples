import httpOutput from './httpOutput.js';
import mqttOutput from './mqttOutput.js';
import consoleOutput from './consoleOuput.js';

const outputs = {
    http: httpOutput,
    mqtt: mqttOutput,
    console: consoleOutput,
};

export default outputs;