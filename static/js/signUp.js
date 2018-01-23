$(function(){
	$('#JoinInBtn').click(function(){
		
		$.ajax({
			url: '/joinIn',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				alert(response);
				window.location.herf = "intro.html";
			},
			error: function(error){
				alert(error);
			}
		});
	});
});
