// https://dev.to/trezy/loading-images-with-web-workers-49ap
self.addEventListener('message', async event => {
  // for (i=0; i <(event.data.len_im_els/event.data.images_per_request); i++)
  // {
    // if (typeof event.data.id !== 'undefined')
    // {
    //    self.postMessage({
    //       'id': event.data.id,
    //       'blob': event.data.blob,
    //    })
    // }
    // else
    // {
      const request = new Request(
          `${event.data.request_url}${event.data.webp_support}/${event.data.screen_size}/${event.data.iteration}`,
          {
              method: 'GET',
              headers: {'X-CSRFToken': event.data.token,
                        'Content-Type': 'application/json'},
              mode: 'same-origin',
              // body: JSON.stringify({'webp_support': event.data.webp_support,
              //        'screen_size': event.data.screen_size, 'iteration': i }),
          }
      );
      fetch(request).then(function(response) {
         // response.json then has the list of the urls
          return response.json();
      })
      .then(imgUrls => {
        imgUrls.forEach(async imgurl => {
          const pic = await fetch(imgurl.pic);
          const blob = await pic.blob();
          const ab = await blob.arrayBuffer()
          self.postMessage({
            'id': new Int32Array([imgurl.id]).buffer,
            'blob': [ab],
          });
          // if (event.data.iteration < (event.data.len_im_els/event.data.images_per_request))
          // {
          //   const ImageLoaderWorker = new Worker('./image_loader_min.js')
          //   iteration = int(event.data.iteration) + 1
          //   ImageLoaderWorker.postMessage({
          //       'iteration': iteration,
          //       'images_per_request': event.data.images_per_request,
          //       'len_im_els': event.data.len_im_els,
          //       'webp_support': event.data.webp_support,
          //       'screen_size': event.data.screen_size,
          //       'request_url': event.data.request_url,
          //       'token': event.data.csrftoken,
          //   })
          // }
        })
      })
});