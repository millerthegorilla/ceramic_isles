function showEditor() {
  $('.update-form-text').val($('#textarea').html());
  $('.update-form-text').show();
  $('#msg-edit-div').show();
  $('#textarea').hide();
  $('#modify-msg-btns').hide();  
  $('#editor-cancel-btn').click(function(){
    $('.update-form-text').hide();
    $('#msg-edit-div').hide();
    $('#textarea').html($('.update-form-text').val());
    $('#textarea').show();
      $('#modify-msg-btns').show();
  });
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function showUpdateComment(id) {
  //$("textarea[id='#comment-textarea-" + id + "']").val($('#comment-text-' + id).html().trim())
  $("#comment-textarea-" + id).val($('#comment-text-' + id).text().trim())
  $('#comment-textarea-' + id).show()
  $('#comment-text-' + id).hide()
  $('#comment-form-buttons-' + id).show()
  $('#comment-modify-btns-' + id).hide()
}

function hideUpdateComment(id) {
    $('#comment-form-buttons-' + id).hide()
    $('#comment-modify-btns-' + id).show()
    $('#comment-textarea-' + id).val('')
    $('#comment-textarea-' + id).hide()
    $('#comment-text-' + id).show()
}

$(document).ready(function () {

	$('#msg-edit-div').hide();
	$('.update-form-text').hide();
	$('#comment-textarea').hide();
	$('.comment-form-buttons').hide();
	$('#editor-btn').click(function(){
        showEditor()
	});
	$('.comment-save').on("click", function( event ) {
  		event.preventDefault();
  		event.currentTarget.closest("#comment-update-form").submit();
  	});	
  	$('.report-msg').on("click", function( event ) {
  		event.preventDefault();
  		event.currentTarget.closest("#form-report-msg").submit();
  	});
  	$('.report-comment').on("click", function( event ) {
  		event.preventDefault();
  		event.currentTarget.closest("#form-report-comment").submit();
  	});
	$('.comment-edit').on("click", function( event ) {
  		event.preventDefault();
  		showUpdateComment(event.currentTarget.id)
	});
	$('.comment-cancel').on("click", function( event ) {
  		event.preventDefault();
  		hideUpdateComment(event.currentTarget.id)
	});

  var commentModal = document.getElementById('commentModal')
  if (commentModal != null)
  {
    commentModal.addEventListener('show.bs.modal', function (event) {
      var button = event.relatedTarget
      var comment_slug_value = button.getAttribute('data-bs-comment-slug')
      var comment_id_value = button.getAttribute('data-bs-comment-id')
      $('#rem-comment-slug').attr('value', comment_slug_value)
      $('#rem-comment-id').attr('value', comment_id_value)
    })
  }

});