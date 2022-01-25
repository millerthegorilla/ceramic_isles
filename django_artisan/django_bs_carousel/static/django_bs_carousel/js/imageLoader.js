self.addEventListener('message', async event => {
      // const mimetype = Boolean(event.data.webp_support) ? 'image/webp' : type='image/jpeg'
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
          if(imgurl.id)
          {
            const pic = await fetch(imgurl.pic);
            const blob = await pic.blob();
            const ab = await blob.arrayBuffer()
            obj = { id: imgurl.id, pic:ab }
            self.postMessage(
              obj, [obj.pic]
             );
          }
          else
          {
            self.postMessage({
              'id': -1,
              'pic': "",
            });
            self.close()
          }
        })
      })
});