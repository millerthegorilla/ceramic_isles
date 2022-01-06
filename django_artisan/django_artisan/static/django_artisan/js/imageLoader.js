// https://dev.to/trezy/loading-images-with-web-workers-49ap
self.addEventListener('message', async event => {
  const request = new Request(
      event.data.url,
      {
          method: 'GET',
          headers: {'X-CSRFToken': event.data.token},
          mode: 'cors' // Do not send CSRF token to another domain.
      }
  );
  fetch(request).then(function(response) {
      return response.json();
  })
  .then(async responseData => {
      const response = await fetch(responseData.imgurl)
      const blob = await response.blob()
      self.postMessage({
        'elid': event.elementid,
        'imageURL': responseData.url,
        'blob': blob,
      })
  })
})