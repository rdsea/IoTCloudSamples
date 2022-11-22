import yml from 'js-yaml';
import fs  from 'fs';
import logger from './src/logger.js';


let config = null;
try {
    config = yml.load(fs.readFileSync("config.yml", 'utf8'));
    logger.info("configuration accepted")
    logger.info(config);
} catch (e) {
    logger.error("failed to parse config !");
    logger.error(e);
}

export default config;

  