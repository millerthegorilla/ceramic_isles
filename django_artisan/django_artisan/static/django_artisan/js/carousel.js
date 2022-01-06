$(document).ready(function () {
    // display image captions on rollover
    $(".carousel-item").hover(function(){ $(".carousel-caption").hide();
      $(".carousel-caption").css('visibility', 'visible');
      $(".carousel-caption").stop().fadeIn(1000) },
      function(){$(".carousel-caption").stop().fadeOut(800, function() {
                    $(".carousel-caption").css('visibility', 'hidden'); }) });
    
      const ImageLoaderWorker = new Worker('./static/django_artisan/js/image_loader_min.js')
      const imgElements = document.querySelectorAll('.carousel-load')
      var index = 0
      // Once again, it's possible that messages could be returned before the
      // listener is attached, so we need to attach the listener before we pass
      // image URLs to the web worker
      ImageLoaderWorker.addEventListener('message', event => {
        // Grab the message data from the event
        const imageData = event.data
    
        var imageElement = imgElements[index]
        index++
        // We can use the `Blob` as an image source! We just need to convert it
        // to an object URL first
        
        var objectURL = URL.createObjectURL(imageData.blob)

        // Once the image is loaded, we'll want to do some extra cleanup
        imageElement.onload = () => {
          // We'll also revoke the object URL now that it's been used to prevent the
          // browser from maintaining unnecessary references
          URL.revokeObjectURL(objectURL)
        }
        imageElement.setAttribute('src', objectURL)
      })
      const siteurl = location.protocol + '//' + location.host + location.pathname + 'imgurl/'
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      //imgElements.forEach(imageElement => {
      ImageLoaderWorker.postMessage({
          'request_url': siteurl,
          'token': csrftoken,
        })
      //})
      // var image = $(e.relatedTarget).next('.carousel-item')
      // //         image.attr('src', image.data('src'));
      // //         image.removeAttr('data-src');
      // // const imageURL = e.getAttribute('data-src')
      // ImageLoaderWorker.postMessage(image.attr('data-src'))

});