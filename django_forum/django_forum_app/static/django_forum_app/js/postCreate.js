$(document).ready(function () {
    function onInstanceInit(editor) {
        editor.hide()
        $(editor.getContainer()).find('button.tox-statusbar__wordcount').click();
        $('#textarea').show()
    }
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
});
