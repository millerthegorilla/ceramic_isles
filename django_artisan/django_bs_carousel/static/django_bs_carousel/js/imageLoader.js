self.addEventListener('message', async event => {
      const request = new Request(
          `${event.data.request_url}${event.data.webp_support}/${event.data.screen_size}/${event.data.iteration}`,
          {
              method: 'GET',
              headers: {'X-CSRFToken': event.data.token,
                        'Content-Type': 'application/json'},
              mode: 'same-origin',
          }
      );
      fetch(request).then(function(response) {
         // response.json then has the list of the urls
          return response.json();
      })
      .then(imgUrls => {
        imgUrls.forEach(async imgurl => {
          const pic = await fetch(imgurl.pic);
          if(pic)
          {
            const blob = await pic.blob();
            const ab = await blob.arrayBuffer()
            self.postMessage({
              'id': new Int32Array([imgurl.id]).buffer,
              'blob': ab,
            });
          }
          else
          {
            self.postMessage({
              'id': "",
              'blob': "",
            });
          }
        })
      })
});