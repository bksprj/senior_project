// Used to sign in to Google Profile
function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	$(".g-signin2").css("display","none");
	$(".data").css("display","block");
	$("#pic").attr('src',profile.getImageUrl());
	$("#email").text(profile.getEmail());
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