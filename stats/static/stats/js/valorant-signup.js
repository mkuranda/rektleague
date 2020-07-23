var sending = false;

var $form = $('form#form'),
    url = 'https://script.google.com/macros/s/AKfycbxX-XpKyITGeMDLKYBhZyImmWT4DfxHFsLlzGhl5hKfCgIRdfE/exec'

    $.fn.serializeObject = function() {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
    $('#submit-form').on('click', function(e) {
        e.preventDefault();
	if (!validateForm())
	{
		return false;
	}
	if (!sending)
	{
		sending = true;
        	var jqxhr = $.ajax({
        	  url: url,
        	  method: "GET",
        	  dataType: "json",
        	  data: $form.serializeObject()
        	}).success(function(e){
        	    console.log(e);
        	    window.location = "/valorant-thanks";
		    sending = false;
		}
        	);
	}
      })

function resetErrors(){
	document.getElementById('email-error').innerHTML = "";
	document.getElementById('account-error').innerHTML = "";
	document.getElementById('playWho-error').innerHTML = "";
	document.getElementById('teamForming-error').innerHTML = "";
	document.getElementById('valFormat-error').innerHTML = "";
	document.getElementById('rank-error').innerHTML = "";
	document.getElementById('accept-error').innerHTML = "";
}


function validateForm(){
	resetErrors();
	var email = document.forms["submitForm"]["email"].value;
	var account = document.forms["submitForm"]["account"].value;
	var playWho = document.forms["submitForm"]["playWho"];
	var teamFormingPremade = document.forms["submitForm"]["teamFormingPremade"];
	var teamFormingCaptains = document.forms["submitForm"]["teamFormingCaptains"];
	var teamFormingRandomWithFriends = document.forms["submitForm"]["teamFormingRandomWithFriends"];
	var teamFormingRandom = document.forms["submitForm"]["teamFormingRandom"];
	var valFormat = document.forms["submitForm"]["valFormat"];
	var rank = document.forms["submitForm"]["rank"];
	var accept = document.forms["submitForm"]["TC"];
	
	if (email.length<1) {
		document.getElementById('email-error').innerHTML = "Email is required";
		return false;
	}
	if (!email.includes("@")) {
		document.getElementById('email-error').innerHTML = "Email must contain an @";
		return false;
	}
	if (account.length<1) {
		document.getElementById('account-error').innerHTML = "Account name is required";
		return false;
	}
	if (!playWho.value) {
		document.getElementById('playWho-error').innerHTML = "Please select an option";
		return false;
	}
	if (!teamFormingPremade.checked && !teamFormingCaptains.checked && !teamFormingRandomWithFriends.checked && !teamFormingRandom.checked)
	{
		document.getElementById('teamForming-error').innerHTML = "Please choose at least one";
		return false;
	}
	if (!valFormat.value) {
		document.getElementById('valFormat-error').innerHTML = "Please select an option";
		return false;
	}          
	if (!rank.value) {
		document.getElementById('rank-error').innerHTML = "Please select an option";
		return false;
	}          
	if (!accept.checked) {
		document.getElementById('accept-error').innerHTML = "YOU MUST ACCEPT";
		return false;
	}          
	return true;
}
