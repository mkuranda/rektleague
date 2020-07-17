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
	console.log($form.serializeObject());
        e.preventDefault();
        var jqxhr = $.ajax({
          url: url,
          method: "GET",
          dataType: "json",
          data: $form.serializeObject()
        }).success(function(e){
            console.log(e);
            alert("You're all set!")}
          
        );
      })
