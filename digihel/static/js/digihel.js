$(function() {

    $('#js-toggle-search, .navbar .drop-search .input-group-btn > .btn[type="reset"]').on('click', function(event) {
			event.preventDefault();
			$('.navbar .drop-search .input-group > input').val('');
			$('.navbar .drop-search').toggleClass('is-open');
			$('a[href="#toggle-search"]').closest('li').toggleClass('active');
			$('#js-toggle-search span').removeClass('glyphicon-remove');
			$('#js-toggle-search span').addClass('glyphicon-search');

			if ($('.navbar .drop-search').hasClass('is-open')) {
				setTimeout(function() {
					$('.navbar .drop-search .form-control').focus();
				}, 100);
				$('#js-toggle-search span').removeClass('glyphicon-search');
				$('#js-toggle-search span').addClass('glyphicon-remove');
			}
		});

		$(document).on('keyup', function(event) {
			if (event.which == 27 && $('.navbar .drop-search').hasClass('is-open')) {
				$('#js-toggle-search').trigger('click');
			}
		});

    $('.match-height').matchHeight();

});