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

var input = document.querySelector('input');
var preview = document.querySelector('.preview');

input.style.opacity = 0;input.addEventListener('change', updateImageDisplay);function updateImageDisplay() {
while(preview.firstChild) {
	preview.removeChild(preview.firstChild);
}

var curFiles = input.files;
if(curFiles.length === 0) {
	var para = document.createElement('p');
	para.textContent = 'No files currently selected for upload';
	preview.appendChild(para);
} else {
	var list = document.createElement('ol');
	preview.appendChild(list);
	for(var i = 0; i < curFiles.length; i++) {
	var listItem = document.createElement('li');
	var para = document.createElement('p');
	if(validFileType(curFiles[i])) {
		para.textContent = 'File name ' + curFiles[i].name + ', file size ' + returnFileSize(curFiles[i].size) + '.';
		var file = document.createElement('img');
		image.src = window.URL.createObjectURL(curFiles[i]);

		listItem.appendChild(file);
		listItem.appendChild(para);

	} else {
		para.textContent = 'File name ' + curFiles[i].name + ': Not a valid file type. Update your selection.';
		listItem.appendChild(para);
	}

	list.appendChild(listItem);
	}
}
}var fileTypes = [
'file/xlsx',
'file/csv'
]

function validFileType(file) {
	for(var i = 0; i < fileTypes.length; i++) {
		if(file.type === fileTypes[i]) {
			return true;
		}
	}

return false;
}function returnFileSize(number) {
if(number < 1024) {
	return number + 'bytes';
} else if(number >= 1024 && number < 1048576) {
	return (number/1024).toFixed(1) + 'KB';
} else if(number >= 1048576) {
	return (number/1048576).toFixed(1) + 'MB';
}	
}

function on() {
	document.getElementById("overlay").style.display = "block";
}

function off() {
	document.getElementById("overlay").style.display = "none";
}