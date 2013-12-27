// FANCYBOX FOR IMAGE GALLERIES
function gallery(el) {
	$(function() {
		$(el).fancybox({
			type: 'image', // NOT NECESSARY WHEN/IF URL IS IMAGE (.JPG, .PNG, ...)
			padding: 0,
			loop: false
		});
	});
}