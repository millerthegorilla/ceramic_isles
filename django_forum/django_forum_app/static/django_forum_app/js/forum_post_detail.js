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
$(document).ready(function () {
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
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var value_val = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    $('#rem-comment').attr('value', value_val)
  })
});