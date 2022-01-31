self.addEventListener('message', async event => {
  // const mimetype = Boolean(event.data.webp_support) ? 'image/webp' : type='image/jpeg'
  if(event.data.useCache)
  {
    var arrStr = encodeURIComponent(JSON.stringify(event.data.indexes));
    const request = new Request(
        `${event.data.request_url}${event.data.webp_support}/${event.data.screen_size}/${arrStr}`,
        {
            method: 'GET',
            headers: {'X-CSRFToken': event.data.token,
                      'Content-Type': 'application/json'},
            mode: 'same-origin',
        });
    fetch(request).then(function(response) {
       // response.json then has the list of the urls
        return response.json();
    })
    .then(imgUrls => {
      const abs = []
      const ids = []
      imgUrls.forEach(async imgurl => {
          const pic = await fetch(imgurl.pic);
          const blob = await pic.blob();
          abs.push(await blob.arrayBuffer())
          ids.push(imgurl.id)
          if(ids.length == imgUrls.length)
          {
            self.postMessage(
              {'ids': ids, 'abs':abs}, abs 
            );
          }
      })
    })
  }
  else
  {
    const abs = []
    const ids = []
    urls = event.data.urls;
    urls.forEach(async imgurl => {
        const pic ;= await fetch(imgurl.url);
        const blob = await pic.blob();
        abs.push(await blob.arrayBuffer())
        ids.push(imgurl.id)
        if(ids.length == imgUrls.length)
        {
          self.postMessage(
            {'ids': ids, 'abs':abs}, abs 
          );
        }
    })
  }
});