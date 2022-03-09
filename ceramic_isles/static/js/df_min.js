(function(){var Autocomplete=function(options){this.form_selector=options.form_selector;this.url=options.url||'/search/autocomplete/';this.delay=parseInt(options.delay||200);this.minimum_length=parseInt(options.minimum_length||3);this.form_elem=null;this.query_box=null;};Autocomplete.prototype.setup=function(){var self=this;this.form_elem=$(this.form_selector);this.query_box=this.form_elem.find('input[name=q]');this.query_box.on('keyup',function(event){var query=self.query_box.val().split(' ');var query=query[query.length-1]
if(query.length<self.minimum_length){return false}
self.fetch(query)});this.form_elem.on('click','.ac-result',function(ev){self.query_box.val($(this).text());$('.ac-results').remove();return false})};Autocomplete.prototype.fetch=function(query){var self=this;$.ajax({url:this.url,data:{'q':query},success:function(data){self.show_results(data)}})};Autocomplete.prototype.show_results=function(data){$('#datalistOptions').remove();var results=data.results||[];var results_wrapper=$('<datalist id="datalistOptions"></datalist>');var base_elem=$('<option class="ac-result"></option>');if(results.length>0){for(var res_offset in results){var elem=base_elem.clone();elem.text(results[res_offset]);results_wrapper.append(elem)}}else{var elem=base_elem.clone();results_wrapper.append(elem)}
this.query_box.after(results_wrapper)};;var Autocomplete=function(options){this.form_selector=options.form_selector;this.url=options.url||'/search/autocomplete/';this.delay=parseInt(options.delay||200);this.minimum_length=parseInt(options.minimum_length||3);this.form_elem=null;this.query_box=null;};Autocomplete.prototype.setup=function(){var self=this;this.form_elem=$(this.form_selector);this.query_box=this.form_elem.find('input[name=q]');this.query_box.on('keyup',function(event){var query=self.query_box.val().split(' ');var query=query[query.length-1]
if(query.length<self.minimum_length){return false}
self.fetch(query)});this.form_elem.on('click','.ac-result',function(ev){self.query_box.val($(this).text());$('.ac-results').remove();return false})};Autocomplete.prototype.fetch=function(query){var self=this;$.ajax({url:this.url,data:{'q':query},success:function(data){self.show_results(data)}})};Autocomplete.prototype.show_results=function(data){$('#datalistOptions').remove();var results=data.results||[];var results_wrapper=$('<datalist id="datalistOptions"></datalist>');var base_elem=$('<option class="ac-result"></option>');if(results.length>0){for(var res_offset in results){var elem=base_elem.clone();elem.text(results[res_offset]);results_wrapper.append(elem)}}else{var elem=base_elem.clone();results_wrapper.append(elem)}
this.query_box.after(results_wrapper)};;function showEditor(){$('.update-form-text').val($('#textarea').html())
$('#post-edit-div').show();tinymce.editors[0].show();$('#textarea').hide()
$('#modify-post-btns').hide();$('#editor-cancel-btn').click(function(){tinymce.editors[0].hide();$('.update-form-text').hide()
$('#post-edit-div').hide()
$('#textarea').html($('.update-form-text').val())
$('#textarea').show()
$('#modify-post-btns').show();});}
function getCookie(name){var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}
function showUpdateComment(id){console.log(id)
$("#comment-textarea-"+id).val($('#comment-text-'+id).text().trim())
$('#comment-textarea-'+id).show()
$('#comment-text-'+id).hide()
$('#comment-form-buttons-'+id).show()
$('#comment-modify-btns-'+id).hide()}
function hideUpdateComment(id){$('#comment-form-buttons-'+id).hide()
$('#comment-modify-btns-'+id).show()
$('#comment-textarea-'+id).val('')
$('#comment-textarea-'+id).hide()
$('#comment-text-'+id).show()}
function onInstanceInit(editor){editor.hide()
$(editor.getContainer()).find('button.tox-statusbar__wordcount').click();$('#textarea').show()}
$(document).ready(function(){$("#id_text").keyup(function(){$("#count").text("...characters left: "+String(500-$(this).val().length));});$('#post-edit-div').hide();$('.update-form-text').hide();$('#comment-textarea').hide();$('.comment-form-buttons').hide();$('#editor-btn').click(function(){showEditor()});$('.comment-save').on("click",function(event){event.preventDefault();event.currentTarget.closest("#comment-update-form").submit();});$('.report-post').on("click",function(event){event.preventDefault();event.currentTarget.closest("#form-report-post").submit();});$('.report-comment').on("click",function(event){event.preventDefault();event.currentTarget.closest("#form-report-comment").submit();});$('.comment-edit').on("click",function(event){event.preventDefault();showUpdateComment(event.currentTarget.id)});$('.comment-cancel').on("click",function(event){event.preventDefault();hideUpdateComment(event.currentTarget.id)});tinymce.init({'selector':'.update-form-text','init_instance_callback':onInstanceInit,'menubar':"False",'min-height':"500px",'browser_spellcheck':"True",'contextmenu':"False",'plugins':"advlist autolink lists link image charmap print preview anchor searchreplace fullscreen insertdatetime media table paste code help wordcount spellchecker",'toolbar':"undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor | a11ycheck ltr rtl | showcomments addcomment table",'custom_undo_redo_levels':"10",});var commentModal=document.getElementById('commentModal')
if(commentModal!=null)
{commentModal.addEventListener('show.bs.modal',function(event){var button=event.relatedTarget
var comment_slug_value=button.getAttribute('data-bs-comment-slug')
var comment_id_value=button.getAttribute('data-bs-comment-id')
$('#rem-comment-slug').attr('value',comment_slug_value)
$('#rem-comment-id').attr('value',comment_id_value)})}
$('#subscribed_cb').change(function(){parts=$(location).attr('pathname').split('/');var slugSegment=parts[3];$.ajax({type:'POST',url:"/forum/subscribe/",data:{'slug':slugSegment,'data':this.checked,'csrfmiddlewaretoken':getCookie('csrftoken')},success:function(response){text=$("label[for='subscribed_cb']").text();if(text=='Subscribe to this thread'){text='Subscribed to this thread';}else{text='Subscribe to this thread';}
$("label[for='subscribed_cb']").text(text);}})})
if($('#subscribed_cb').prop("checked")==true){text='Subscribed to this thread';}else{text='Subscribe to this thread';}
$("label[for='subscribed_cb']").text(text);});;function showEditor(){$('.update-form-text').val($('#textarea').html())
$('#post-edit-div').show();tinymce.editors[0].show();$('#textarea').hide()
$('#modify-post-btns').hide();$('#editor-cancel-btn').click(function(){tinymce.editors[0].hide();$('.update-form-text').hide()
$('#post-edit-div').hide()
$('#textarea').html($('.update-form-text').val())
$('#textarea').show()
$('#modify-post-btns').show();});}
function getCookie(name){var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}
function showUpdateComment(id){console.log(id)
$("#comment-textarea-"+id).val($('#comment-text-'+id).text().trim())
$('#comment-textarea-'+id).show()
$('#comment-text-'+id).hide()
$('#comment-form-buttons-'+id).show()
$('#comment-modify-btns-'+id).hide()}
function hideUpdateComment(id){$('#comment-form-buttons-'+id).hide()
$('#comment-modify-btns-'+id).show()
$('#comment-textarea-'+id).val('')
$('#comment-textarea-'+id).hide()
$('#comment-text-'+id).show()}
function onInstanceInit(editor){editor.hide()
$(editor.getContainer()).find('button.tox-statusbar__wordcount').click();$('#textarea').show()}
$(document).ready(function(){$("#id_text").keyup(function(){$("#count").text("...characters left: "+String(500-$(this).val().length));});$('#post-edit-div').hide();$('.update-form-text').hide();$('#comment-textarea').hide();$('.comment-form-buttons').hide();$('#editor-btn').click(function(){showEditor()});$('.comment-save').on("click",function(event){event.preventDefault();event.currentTarget.closest("#comment-update-form").submit();});$('.report-post').on("click",function(event){event.preventDefault();event.currentTarget.closest("#form-report-post").submit();});$('.report-comment').on("click",function(event){event.preventDefault();event.currentTarget.closest("#form-report-comment").submit();});$('.comment-edit').on("click",function(event){event.preventDefault();showUpdateComment(event.currentTarget.id)});$('.comment-cancel').on("click",function(event){event.preventDefault();hideUpdateComment(event.currentTarget.id)});tinymce.init({'selector':'.update-form-text','init_instance_callback':onInstanceInit,'menubar':"False",'min-height':"500px",'browser_spellcheck':"True",'contextmenu':"False",'plugins':"advlist autolink lists link image charmap print preview anchor searchreplace fullscreen insertdatetime media table paste code help wordcount spellchecker",'toolbar':"undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor | a11ycheck ltr rtl | showcomments addcomment table",'custom_undo_redo_levels':"10",});var commentModal=document.getElementById('commentModal')
if(commentModal!=null)
{commentModal.addEventListener('show.bs.modal',function(event){var button=event.relatedTarget
var comment_slug_value=button.getAttribute('data-bs-comment-slug')
var comment_id_value=button.getAttribute('data-bs-comment-id')
$('#rem-comment-slug').attr('value',comment_slug_value)
$('#rem-comment-id').attr('value',comment_id_value)})}
$('#subscribed_cb').change(function(){parts=$(location).attr('pathname').split('/');var slugSegment=parts[3];$.ajax({type:'POST',url:"/forum/subscribe/",data:{'slug':slugSegment,'data':this.checked,'csrfmiddlewaretoken':getCookie('csrftoken')},success:function(response){text=$("label[for='subscribed_cb']").text();if(text=='Subscribe to this thread'){text='Subscribed to this thread';}else{text='Subscribe to this thread';}
$("label[for='subscribed_cb']").text(text);}})})
if($('#subscribed_cb').prop("checked")==true){text='Subscribed to this thread';}else{text='Subscribe to this thread';}
$("label[for='subscribed_cb']").text(text);});;$(document).ready(function(){function sleep(ms){return new Promise(resolve=>setTimeout(resolve,ms));}
async function onInstanceInit(){await sleep(3500);$('.tox-statusbar__wordcount').click();}
tinymce.init({'selector':'.update-form-text','init_instance_callback':onInstanceInit(),'menubar':"False",'min-height':"500px",'browser_spellcheck':"True",'contextmenu':"False",'plugins':"advlist autolink lists link image charmap print preview anchor searchreplace fullscreen insertdatetime media table paste code help wordcount spellchecker",'toolbar':"undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor | a11ycheck ltr rtl | showcomments addcomment table",'custom_undo_redo_levels':"10",});});;$(document).ready(function(){function sleep(ms){return new Promise(resolve=>setTimeout(resolve,ms));}
async function onInstanceInit(){await sleep(3500);$('.tox-statusbar__wordcount').click();}
tinymce.init({'selector':'.update-form-text','init_instance_callback':onInstanceInit(),'menubar':"False",'min-height':"500px",'browser_spellcheck':"True",'contextmenu':"False",'plugins':"advlist autolink lists link image charmap print preview anchor searchreplace fullscreen insertdatetime media table paste code help wordcount spellchecker",'toolbar':"undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor | a11ycheck ltr rtl | showcomments addcomment table",'custom_undo_redo_levels':"10",});});;$(document).ready(function(){$("#avatarImage").click(function(e){$("#avatarUpload").click();});$('#avatarUpload').on("change",function(event){$("#avatarform").submit();});});;$(document).ready(function(){$("#avatarImage").click(function(e){$("#avatarUpload").click();});$('#avatarUpload').on("change",function(event){$("#avatarform").submit();});});}).call(this);