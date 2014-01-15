// FANCYBOX FOR IMAGE GALLERIES
function gallery(el) {
	$(function() {
		$.ajaxSetup({ cache: true });

		$.getScript('//getkindy.s3.amazonaws.com/js/fancybox.js', function() {
			$(el).fancybox({
				type: 'image', // NOT NECESSARY WHEN/IF URL IS IMAGE (.JPG, .PNG, ...)
				padding: 0,
				loop: false
			});
		});
	});
}

// WYSIWYG TEXT EDITOR
function texteditor(el) {
	$(function() {
		$.ajaxSetup({ cache: true });

		$.getScript('//getkindy.s3.amazonaws.com/js/texteditor.js', function() {
			$(el).cleditor({
				height: '350px',
				width: '250%',
				controls: 'bold italic underline style | color removeformat | bullets numbering | alignleft center alignright | undo redo | image link unlink | source',
				bodyStyle: 'font:normal 14px/1 Ubuntu, Helvetica, Arial, sans-serif; margin:10px;'
			});
		});
	});
}

// SITE WIDE FUNCTIONS
$(function() {
	// SCROLLABLE SIDEBAR CONTENT
	$('#sidebar').jScrollPane();
	$(window).resize(function() { $('#sidebar').jScrollPane(); });

	// DISABLE SUBMIT BUTTON WHEN FORM IS SUBMITED
	$('form').submit(function() {
		$(this).find('input[type="submit"]').val('Loading...').prop('disabled', true);
	});
});