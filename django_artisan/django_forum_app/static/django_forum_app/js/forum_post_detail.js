
$(document).ready(function () {

$("#id_text").keyup(function(){
  $("#count").text("...characters left: " + (500 - $(this).val().length));
});
function showEditor() {
	$('.update-form-text').val($('#textarea').html())
	$('#post-edit-div').show();
	tinymce.editors[0].show();
	$('#textarea').hide()
	$('#modify-post-btns').hide();
	
	$('#editor-cancel-btn').click(function(){
		tinymce.editors[0].hide();
		$('.update-form-text').hide()
		$('#post-edit-div').hide()
		$('#textarea').html($('.update-form-text').val())
		$('#textarea').show()
	    $('#modify-post-btns').show();
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

function onInstanceInit(editor) {
    editor.hide()
    $(editor.getContainer()).find('button.tox-statusbar__wordcount').click();
    $('#textarea').show()
}

	$('.update-form-text').hide();
	$('#post-edit-div').hide();
	$('#comment-textarea').hide();
	$('.comment-form-buttons').hide();
	$('#editor-btn').click(function(){
        showEditor()
	});
	$('.comment-save').on("click", function( event ) {
  		event.preventDefault();
  		event.currentTarget.closest("#comment-update-form").submit();
  	});	
  	$('.report-post').on("click", function( event ) {
  		event.preventDefault();
  		event.currentTarget.closest("#form-report-post").submit();
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
	tinymce.init({
	'selector': '.update-form-text',
	'init_instance_callback': onInstanceInit,
    'menubar': "False",
    'min-height': "500px",
    'browser_spellcheck': "True",
    'contextmenu': "False",
    'plugins': "advlist autolink lists link image charmap print preview anchor searchreplace fullscreen insertdatetime media table paste code help wordcount spellchecker",
    'toolbar': "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor | a11ycheck ltr rtl | showcomments addcomment table",
    'custom_undo_redo_levels': "10",
	});
	//tinymce.editors[0].hide()
  var commentModal = document.getElementById('commentModal')
  commentModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget
    var value_val = button.getAttribute('data-bs-whatever')
    $('#rem-comment').attr('value', value_val)
  })
  $('#subscribed_cb').change(function() {
    parts = $(location).attr('href').split('/');
    var lastSegment = parts.pop() || parts.pop();
    $.ajax({
      type: 'POST',
      url: "/forum/subscribe/",
      data: { 'post_slug': lastSegment, 'data': this.checked, 'csrfmiddlewaretoken': getCookie('csrftoken') },
      success: function (response) {
        text=$("label[for='subscribed_cb']").text();
        if(text=='Subscribe to this thread') {
            text='Subscribed to this thread';
        } else {
            text='Subscribe to this thread';
        }
        $("label[for='subscribed_cb']").text(text);
      }
    })
  })
  if ($('#subscribed_cb').prop("checked") == true) {
    text='Subscribed to this thread';
  } else {
    text='Subscribe to this thread';
  }
  $("label[for='subscribed_cb']").text(text);
});