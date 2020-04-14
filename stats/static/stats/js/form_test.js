var $form = $('form#test-form'),
    url = 'https://script.google.com/macros/s/AKfycbyDuQgAfw5LYi8MlFKE6eBnphZbd3f7cKxunROlSbjj02BhYcja/exec'

$('#submit-form').on('click', function(e) {
  e.preventDefault();
  var jqxhr = $.ajax({
    url: url,
    method: "GET",
    dataType: "json",
    data: $form.serializeObject()
  }).success(
    // do something
  );
})