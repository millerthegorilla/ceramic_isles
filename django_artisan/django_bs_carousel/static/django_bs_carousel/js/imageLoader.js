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
            const ab = await blob.arrayBuffer(Boolean(event.data.webp_support) ? type='image/webp' : type='image/jpeg')
            obj = { id: imgurl.id, pic:ab }
            self.postMessage(
              obj, [obj.pic]
             );
            if(ab)
            {
              self.postMessage({id:999, pic:blob})
            }
          }
          else
          {
            self.postMessage({
              'id': 666,
              'pic': "",
            });
            self.close()
          }
        })
      })
});