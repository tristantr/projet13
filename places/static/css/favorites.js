$(document).ready(function(){

	$('span[name="fav"]').on('click', (event) => {

		console.log('Coucou')

		let place_id = $(event.target).attr('id')
		let logo_class = $(event.target).attr('class')

		event.preventDefault();

		$.ajax({
			type: 'POST',
			url: '/places/favorites/',
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'place_id': place_id,

			},			
			success: function(response) {
				if (logo_class.indexOf('far') !== -1) {
					$(event.target).removeClass('far')
					$(event.target).addClass('fas')
				} else {
					$(event.target).removeClass('fas')
					$(event.target).addClass('far')			
				}
			},
		})


	})})