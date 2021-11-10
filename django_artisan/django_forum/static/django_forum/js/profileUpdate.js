$(document).ready(function () {
    $("#avatarImage").click(function(e) {
        $("#avatarUpload").click();
    });
    $('#avatarUpload').on("change", function( event ) {
        $("#avatarform").submit();
    });
});