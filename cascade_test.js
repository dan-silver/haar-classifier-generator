var cv = require('opencv');

var color = [0, 255, 0];
var thickness = 2;
var cascadeFile = 'trained_classifiers/banana_classifier.xml';

var inputFiles = [ 'tests/test.jpg'];

inputFiles.forEach(function(fileName) {
	cv.readImage(fileName, function(err, im) {
		im.detectObject(cascadeFile, {neighbors: 2, scale: 2}, function(err, objects) {
			console.log(objects);
			for(var k = 0; k < objects.length; k++) {
				var object = objects[k];
				im.rectangle([object.x, object.y], [object.x + object.width, object.y + object.height], color, 2);
			}
			im.save(fileName.replace(/.jpg/, 'processed.jpg'));
		});
	});
});