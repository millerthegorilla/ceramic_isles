// https://dev.to/trezy/loading-images-with-web-workers-49ap
self.addEventListener('message', async event => {
  const request = new Request(
      event.data.request_url,
      {
          method: 'GET',
          headers: {'X-CSRFToken': event.data.token},
          mode: 'cors' // Do not send CSRF token to another domain.
      }
  );
  fetch(request).then(function(response) {
     // response.json then has the list of the urls
      return response.json();
  })
  .then(imgUrls => {
    imgUrls.forEach(async imgurl => {
      const response = await fetch(imgurl)
      const blob = await response.blob()
      self.postMessage({
        'blob': blob,
      })
    })
  })
});