// When the user clicks on div, open the popup
function myFunction() {
	var popup = document.getElementById("myPopup");
	popup.classList.toggle("show");
}

// Used to sign in to Google Profile
function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	//$(".g-signin2").css("display","none");
	$(".data").css("display","block");
	$(".goaway").css("display","none");
	$("#pic").attr('src',profile.getImageUrl());
	$("#pic2").attr('src',profile.getImageUrl());
	window.location.replace("http://localhost:5000/loggedin/" + profile.getEmail().slice(0,-10));
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
	$.post("/grab_group/" + group_name);
	// setTimeout(function(){location.reload(true)}, 1000);
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

// When the user clicks the button, open the modal
function showModel() {
  document.getElementById("myModal").style.display = "block";
}

// When the user clicks on <span> (x), close the modal
function spanClick() {
  document.getElementById("myModal").style.display = "none";
}

function showUploader() {
	document.getElementById("myUploader").style.display = "block";
}

// When the user clicks on <span> (x), close the modal
function spanClickUploader() {
	document.getElementById("myUploader").style.display = "none";
}

// When the user clicks the button, open the modal
function showTaskIn() {
	document.getElementById("myTaskIn").style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  function spanTaskIn() {
	document.getElementById("myTaskIn").style.display = "none";
  }

  // When the user clicks the button, open the modal
function showAdmin() {
	document.getElementById("myAdmin").style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
function spanAdmin() {
	document.getElementById("myAdmin").style.display = "none";
  }
