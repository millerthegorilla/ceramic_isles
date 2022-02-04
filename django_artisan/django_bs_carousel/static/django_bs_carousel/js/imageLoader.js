function isValid(value) {
  return value != undefined;
}

self.addEventListener('message', async event => {
  const cache = event.data.useCache;

  if(cache)
  {
    const indStr = encodeURIComponent(JSON.stringify(event.data.indexes));
    const pkStr = encodeURIComponent(JSON.stringify(event.data.pks));
    const randomizeImages = event.data.randomizeImages;
    const request = new Request(
        `${event.data.requestUrl}${event.data.webpSupport}/${event.data.screenSize}/${event.data.iteration}/${pkStr}/${indStr}`,
        {
            method: 'GET',
            headers: {'X-CSRFToken': event.data.token,
                      'Content-Type': 'application/json'},
            mode: 'same-origin',
        });
    fetch(request).then(function(response) {
        return response.json();
    })
    .then(imgUrls => {
      var imgUrls = imgUrls.list;
      const abs = [];
      var idxs = (randomizeImages ? [] : event.data.indexes);
      imgUrls.forEach(async imgurl => {
          const id = parseInt(imgurl.id);
          const pic = await fetch(imgurl.pic);
          const blob = await pic.blob();
          const ab = await blob.arrayBuffer();
          if(!randomizeImages)
          {
            abs[id] = ab;
          }
          else
          {
            var bob = event.data.indexes.findIndex((el)=>el==id);
            idxs[bob] = id;
            abs[bob] = ab;
          }
          if(abs.filter(isValid).length == imgUrls.length)
          {
            var abs2 = abs.filter(isValid);
            self.postMessage(
              {'ids': idxs, 'abs':abs2}, abs2
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
    console.log(urls);
    urls.forEach(async imgurl => {
        const pic = await fetch(imgurl.url);
        const blob = await pic.blob();
        abs.push(await blob.arrayBuffer())
        ids.push(imgurl.id)
        if(ids.length == urls.length)
        {
          self.postMessage(
            {'ids': ids, 'abs':abs}, abs 
          );
        }
    })
  }
});