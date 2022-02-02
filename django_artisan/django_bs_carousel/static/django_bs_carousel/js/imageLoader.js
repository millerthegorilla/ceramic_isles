self.addEventListener('message', async event => {
  // const mimetype = Boolean(event.data.webp_support) ? 'image/webp' : type='image/jpeg'
  console.log('hi')
  const cache = event.data.useCache;
  if(cache)
  {
    var arrStr = encodeURIComponent(JSON.stringify(event.data.indexes));
    const request = new Request(
        `${event.data.requestUrl}${event.data.webpSupport}/${event.data.screenSize}/${arrStr}`,
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
    const urls = event.data.urls;
    urls.forEach(async imgurl => {
        const pic = await fetch(imgurl.url);
        const blob = await pic.blob();
        abs.push(await blob.arrayBuffer())
        ids.push(imgurl.id)
        console.log(imgurl.id)
        if(ids.length == urls.length)
        {
          self.postMessage(
            {'ids': ids, 'abs':abs}, abs 
          );
        }
    })
  }
});