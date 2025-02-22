import Datastore from 'nedb';
import path from 'path';

let database = new Datastore({filename: './.db', autoload: true });

class DB {
    constructor() {

    }
    insert(doc) {
        return new Promise((resolve, reject) => {
            console.log(`inserting document ${JSON.stringify(doc)}`);
            database.insert(doc, (err) => {
                if (err) {
                    console.error(err);
                    reject(err);
                } else {
                    console.log(`successfully inserted document ${JSON.stringify(doc)}`);
                    resolve(doc);
                }
            })
        });
    }

    find(query) {
        return new Promise((resolve, reject) => {
            database.find(query, (err, docs) => {
                if (err) {
                    reject(err);
                } else {
                    console.log(`successfully found ${docs.length} results for ${query}`);
                    resolve(docs);
                }
            });
        });
    }

    findOne(query) {
        return new Promise((resolve, reject) => {
            console.log(`finding one documentof ${JSON.stringify(query)}`);
            database.findOne(query, (err, doc) => {
                if (err) {
                    console.error(err);
                    reject(err);
                } else {
                    if (doc === null) console.log(`no result found for ${JSON.stringify(query)}`);
                    resolve(doc);
                }
            });
        });
    }

    update(query, update, options) {
        return new Promise((resolve, reject) => {
            console.log(`updating documents ${JSON.stringify(query)} with ${JSON.stringify(update)}`);
            database.update(query, update, (err, numberOfUpdated, upsert) => {
                if (err) {
                    console.error(err);
                    reject(err);
                } else {
                    console.log(`successfully updated ${numberOfUpdated} docs with ${upsert} upserts`);
                    let res = {
                        numberOfUpdated,
                        upsert,
                    }
                    resolve(res);
                }
            });
        })
    }

    remove(query, options) {
        return new Promise((resolve, reject) => {
            database.remove(query, (err, numRemoved) => {
                if (err) {
                    console.error(er);
                    reject(err);
                } else {
                    console.log(`successfully removed ${numRemoved} entries from db`);
                    resolve();
                }
            })
        })
    }
}

export default DB;

