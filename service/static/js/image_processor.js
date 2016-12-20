var original = document.getElementById('original')
var canvas = document.getElementById('canvas')
var output = document.getElementById('output')
var cCtx = canvas.getContext('2d')
var oCtx = output.getContext('2d')
var reader = new FileReader()

function setUpCanvas() {
	output.width = original.width
	output.height = original.height
	canvas.width = original.width
	canvas.height = original.height
	cCtx.drawImage(original, 0, 0)
}

function border() {
	var imagedata = cCtx.getImageData(0, 0, original.width, original.height)
	var newImage = grafi.sharpen(imagedata)
	oCtx.putImageData(newImage, 10, 10)
}

reader.onload = function() {
	original.src = reader.result
}

original.onload = function() {
	setUpCanvas()
	border()
}
