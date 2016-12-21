var original = document.getElementById('original')
var canvas = document.getElementById('canvas')
var output = document.getElementById('output')
var imgProcess = document.getElementsByName('process')
var cropWidth = document.getElementById('cropWidth')
var cropHeight = document.getElementById('cropHeight')
var cCtx = canvas.getContext('2d')
var oCtx = output.getContext('2d')
var reader = new FileReader()

function setUpCanvas() {
	output.width = original.width
	output.height = original.height
	canvas.width = original.width
	canvas.height = original.height

	var wrh = original.width / original.height;
	var newWidth = canvas.width;
	var newHeight = newWidth / wrh;
	if (newHeight > canvas.height) {
		newHeight = canvas.height;
		newWidth = newHeight * wrh;
	}

	if (cropWidth.value != '' && cropHeight.value != '') {
		newWidth = cropWidth.value
		newHeight = cropHeight.value
	}

	cCtx.drawImage(original, 0, 0, newWidth, newHeight)
}

function border() {
	var imagedata = cCtx.getImageData(0, 0, output.width, output.height)
	var value = ''

	for (var i = 0; i < imgProcess.length; i++) {
		if (imgProcess[i].checked) {
			value = imgProcess[i].value;
		}
	}

	if (value == 'sharpen') {
		var newImage = grafi.sharpen(imagedata)
	} else if (value == 'solarize') {
		var newImage = grafi.solarize(imagedata)
	} else {
		var newImage = imagedata
	}

	oCtx.putImageData(newImage, 0, 0)
}

reader.onload = function() {
	original.src = reader.result
}

original.onload = function() {
	setUpCanvas()
	border()
}
