var Autocomplete = function (options) {
  this.form_selector = options.form_selector;
  this.url = options.url || '/search/autocomplete/';
  this.delay = parseInt(options.delay || 200);
  this.minimum_length = parseInt(options.minimum_length || 3);
  this.form_elem = null;
  this.query_box = null;
};

Autocomplete.prototype.setup = function () {
  var self = this;

  this.form_elem = $(this.form_selector);
  this.query_box = this.form_elem.find('input[name=q]');

  // Watch the input box.
  this.query_box.on('keyup', function (event) {
    var query = self.query_box.val().split(' ');
    var query = query[query.length - 1]
    if (query.length < self.minimum_length) {
      return false
    }
    self.fetch(query)
  });

  // On selecting a result, populate the search field.
  this.form_elem.on('click', '.ac-result', function (ev) {
    self.query_box.val($(this).text());
    $('.ac-results').remove();
    return false
  })
};

Autocomplete.prototype.fetch = function (query) {
  var self = this;

  $.ajax({
    url: this.url, 
    data: {
      'q': query
    },
    success: function (data) {
      self.show_results(data)
    }
  })
};

Autocomplete.prototype.show_results = function (data) {
  // Remove any existing results.
  $('#datalistOptions').remove();
  var results = data.results || [];
  var results_wrapper = $('<datalist id="datalistOptions"></datalist>');
  var base_elem = $('<option class="ac-result"></option>');

  if (results.length > 0) {
    for (var res_offset in results) {
      var elem = base_elem.clone();
      elem.text(results[res_offset]);
      results_wrapper.append(elem)
    }
  } else {
    var elem = base_elem.clone();
    results_wrapper.append(elem)
  }

  this.query_box.after(results_wrapper)
};


// <script type="application/javascript">
//   $(function () {
//     window.autocomplete = new Autocomplete({
//       form_selector: '.form-autocomplete',
//       minimum_length: 2,
//       url: '{% url "django_forum_app:autocomplete" %}'
//     });
//     window.autocomplete.setup()
//   });
// </script>