// https://dev.to/trezy/loading-images-with-web-workers-49ap
self.addEventListener('message', async event => {
  for (i=0; i <(event.data.len_im_els/event.data.images_per_request); i++)
  {
    const request = new Request(
        event.data.request_url,
        {
            method: 'POST',
            headers: {'X-CSRFToken': event.data.token,
                      'Content-Type': 'application/json'},
            mode: 'same-origin',
            body: JSON.stringify({'webp_support': event.data.webp_support,
                   'screen_size': event.data.screen_size, 'iteration': i }),
        }
    );
    fetch(request).then(function(response) {
       // response.json then has the list of the urls
        return response.json();
    })
    .then(imgUrls => {
      imgUrls.forEach(async imgurl => {
        const pic = await fetch(imgurl.pic)
        const blob = await pic.blob()
        self.postMessage({
          'id': imgurl.id,
          'blob': blob,
        })
      })
    })
  }
});