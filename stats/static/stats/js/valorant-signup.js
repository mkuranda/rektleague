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
	document.getElementById('rank-error').innerHTML = "";
	document.getElementById('accept-error').innerHTML = "";
}


function validateForm(){
	resetErrors();
	var email = document.forms["submitForm"]["email"].value;
	var account = document.forms["submitForm"]["account"].value;
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
