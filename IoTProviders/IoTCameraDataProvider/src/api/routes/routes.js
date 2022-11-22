'use strict';
import  cameraController from '../controllers/camera-controller.js';

/**
* Created by Tran The Vu on 15/11/2017.
* Email: anhvaut@gmail.com/vu.tran@vnuk.edu.vn
*/

export default function(app) {
	

	app.route('/camera/list')
		.get(cameraController.listAllCameras);

	app.route('/camera/list/location')
		.get(cameraController.listAllCamerasByLocation);

	app.route('/camera/:cameraName')
		.post(cameraController.exportVideo);

	app.route('/camera/:cameraName/:videoId')
		.get(cameraController.getVideoById);

	app.route('/camera/:cameraName/list/all')
		.get(cameraController.listAllVideoFrames);

	app.route('/camera/:cameraName/list/:time')
		.get(cameraController.getVideoFrameByTime);

	app.route('/register')
		.post(cameraController.register);


};
