// Used to sign in to Google Profile
function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	$(".g-signin2").css("display","none");
	$(".data").css("display","block");
	$("#pic").attr('src',profile.getImageUrl());
	$("#email").text(profile.getEmail());
	$('#name').text(profile.getName());
}


// Used to sign out of profile
function signOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function() {
		if (confirm('Are you sure you want to sign out?')) {
			$(".g-signin2").css("display","block");
			$(".data").css("display","none");
		} else {
			// Does nothing
		}
	})
}


function addL() {
	//First things first, we need our text:
	var text = document.getElementById("item").value; //.value gets input values

	//Now construct a quick list element
	var li = "<li>" + text + "</li>";

	//Now use appendChild and add it to the list!
	document.getElementById("list").appendChild(li);
}

/*(function($){
	$('#myform').submit(function(e){
		var val = $('#in').val();
		$('ul.list').append('<li>' + val + '</li>');
		e.preventDefault();
	});
})(jQuery);*/