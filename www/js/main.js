$(function () {	

  var names = $.parseJSON($('#teachernames').text())
	$('.typeahead').typeahead({
		source: names,
	});

	$('#searchform').on('click', function(){
		$('#infoinst').fadeOut();
	});

	$('.submit').on('click', function(ev){
		ev.preventDefault();
		$('form').submit();
	});


});