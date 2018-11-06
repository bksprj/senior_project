// When the user clicks on div, open the popup
function myFunction() {
	var popup = document.getElementById("myPopup");
	popup.classList.toggle("show");
}
			
// Used to sign in to Google Profile
function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	$(".g-signin2").css("display","none");
	$(".data").css("display","block");
	$(".goaway").css("display","none");
	$("#pic").attr('src',profile.getImageUrl());
	$.post( "/", profile.getEmail());
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
			$(".goaway").css("display","block");
		} else {
			// Does nothing
		}
	})
}

function on() {
	document.getElementById("overlay").style.display = "block";
}

function off() {
	document.getElementById("overlay").style.display = "none";
}