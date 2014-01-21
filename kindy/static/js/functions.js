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
			$('textarea').summernote({ height: '250px' });
		});
	});
}

// SITE WIDE FUNCTIONS
$(function() {
	// SCROLLABLE SIDEBAR CONTENT
	if($(window).innerWidth() > 991) {
		$('#sidebar').jScrollPane();
		$(window).resize(function() { $('#sidebar').jScrollPane(); });
	}

	// SHOW SIDEBAR ON SMALLER SCREENS
	$('#header .sidebar-button').click(function() {
		$('#content').toggleClass('move');
	});

	$('#content').click(function() {
		if($(this).hasClass('move')) $('#content').toggleClass('move');
	});

	// DISABLE SUBMIT BUTTON WHEN FORM IS SUBMITED
	$('form').submit(function() {
		$(this).find(':input:submit').val('Loading...').prop('disabled', true);
	});
});