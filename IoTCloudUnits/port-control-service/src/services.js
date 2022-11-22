import db from './data/db.js';
class PortControlService {
    constructor(){

    }
registerVessel(vessel){
    return db.insert(vessel)
}

 findAllVessels(){
    return db.find({});
}

 findVesselsInTerminal(terminal){
    let query = {
        "Terminal":terminal
    }
    return db.find(query)
}
 registerTruck(truck){
    return db.insert(truck)
}
 findAllTrucks(){
    return db.find({});
}
 findTrucksInPort(licensePlate){
  let query = {
      licensePlate
  }
  return db.find(query)
}

 registerCrane(crane){
    return db.insert(crane)
}
 findAllCranes(){
    return db.find({});
}
 findCraneInPort(craneId){
  let query = {
      craneId
  }
  return db.find(query)
}
//TODO find cranes with geohash
}
export default PortControlService;