import json

from sorl.thumbnail import get_thumbnail

from django import shortcuts, http, conf
from django.apps import apps
from django.views import generic

#webworker ajax request to here, returns url
class ImgURL(generic.base.View):
    # TODO - create a threaded function inside the get, that pushes its handle to 
    # a 'global' array.  Then, if user leaves page, request is made to here from
    # beforeunload handler with an iteration = -1, and threads in array are closed.
    def get(self, request: http.HttpRequest, 
                  webp_support: str, 
                  screen_size: str, 
                  iteration:int, 
                  pks:str, 
                  indexes: str) -> http.JsonResponse:
        image_idxs = json.loads(indexes)
        image_pks = json.loads(pks)
        fmt = "WEBP" if webp_support else "JPEG"
        ql = []
        image_qs = (apps.get_model(*conf.settings.DJANGO_BS_CAROUSEL_IMAGE_MODEL
                                       .split('.')).objects.filter(pk__in=image_pks)) 
        i = 0;
        for im in image_qs.iterator():
            pic = get_thumbnail(im.image_file, screen_size, 
                                    format=fmt, quality=70).url
            ql.append({'id': str(image_idxs[i]),
                       'pic': pic})
            i = i + 1
        r = { 'list': ql }
        return http.JsonResponse(r)
