function isValid(value) {
  return value != undefined;
}

self.addEventListener('message', async event => {
  // const mimetype = Boolean(event.data.webp_support) ? 'image/webp' : type='image/jpeg'
  const cache = event.data.useCache;

  if(cache)
  {
    var indStr = encodeURIComponent(JSON.stringify(event.data.indexes));
    var pkStr = encodeURIComponent(JSON.stringify(event.data.pks));
    const request = new Request(
        `${event.data.requestUrl}${event.data.webpSupport}/${event.data.screenSize}/${event.data.iteration}/${pkStr}/${indStr}`,
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
      var imgUrls = imgUrls.list;
      console.log('imgurls = ',imgUrls);
      const abs = []
      const ids = []
      const idxs = event.data.indexes;
      imgUrls.forEach(async imgurl => {
            const pic = await fetch(imgurl.pic);
            const blob = await pic.blob();
            const ab = await blob.arrayBuffer();
            abs[imgurl.id] = ab
          // ids is the offset of abs into the array 
          //so, ids[3] == 6 then abs[6] is in the 3rd position in the array
          if(abs.filter(isValid).length == imgUrls.length)
          {
             var abs2 = abs.filter(isValid); 
          //   var abs2 = [];
          //   var ids2= [];
               
          //   idxs.forEach((id,idx) =>
          //   {
          //     //find idx inside ids and return its offset
          //     //take the abs at that offset and 
          //     abs2[idx] = abs[ids[idx]]
          //   });
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