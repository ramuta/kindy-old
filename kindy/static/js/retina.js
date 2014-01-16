/*
 * Retina.js - jQuery script for replacing basic images with retina images
 * Author: Davor Padovan
 * Copyright: (c) Davor Padovan - All Rights Reserved.
 */

if(window.devicePixelRatio > 1) {
	$('img').each(function(i, e) {
		if(!$(e).attr('src')) return;

		var oldImage = new Image();
		oldImage.src = $(e).attr('src');
		oldImage.onload = function () {
            $(e).attr({ height: this.height, width: this.width });
        };

		var newImage = $(e).attr('src').replace(/(.+)(\.\w{3,4})$/, '$1-2x$2');

		$.ajax({
			url: newImage,
			type: 'HEAD',
			success: function() {
				$(e).attr('src', newImage);
			}
		});
	});
}