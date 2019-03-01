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
	$("#pic2").attr('src',profile.getImageUrl());
	$.post("/getemail", {"myData": profile.getEmail()})
	$("#email").text(profile.getEmail());
	$('#name').text(profile.getName());
	$('#name2').text(profile.getName());
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

function query_data(group_name){
	$.post("/grab_group" + group_name)
}

// Overlay function to turn on
function on() {
	document.getElementById("overlay").style.display = "block";
}

// Overlay function to turn on
function uploadOn() {
	document.getElementById("upload").style.display = "block";
}

// Overlay function to turn on
function adminOn() {
	document.getElementById("admin").style.display = "block";
}

// Overlay function to turn off
function off() {
	document.getElementById("overlay").style.display = "none";
}

// Overlay function to turn off
function uploadOff() {
	document.getElementById("upload").style.display = "none";
}

// Overlay function to turn off
function adminOff() {
	document.getElementById("admin").style.display = "none";
}

// Changes the theme color
function dark_mode() {
	document.body.style.background = "#4d4d4d";
    document.getElementsByTagName("p").style.color = "white";
    document.getElementsByTagName("a").style.color = "white";
}