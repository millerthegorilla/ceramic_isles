import json

from sorl.thumbnail import get_thumbnail

from django import shortcuts, http, conf
from django.apps import apps
from django.views import generic


#webworker ajax request to here, returns url
class ImgURL(generic.base.View):
    # this is returning images in different order to that on the web page
    def get(self, request: http.HttpRequest, webp_support: str, screen_size: str, iteration: int) -> http.JsonResponse:
        images = json.loads(self.request.session['images'])
        ql = []
        images_per_request = conf.settings.NUM_IMAGES_PER_REQUEST
        lazyload_offset = conf.settings.LAZYLOAD_OFFSET
        if lazyload_offset < 2: 
            lazyload_offset = 2
        # iteration is zero based
        offset = lazyload_offset if iteration == 0 else 0
        start = iteration * images_per_request + offset
        count = len(images)
        finish = (count - 1 if (iteration == 0 and images_per_request > count) 
                    or (iteration * images_per_request + images_per_request > count)
                            else iteration * images_per_request
                                 + images_per_request)
        fmt = "WEBP" if webp_support else "JPEG"
        if start == finish:  # handle case where there are only three images.
            finish += 1
        #breakpoint()
        image_pk_list = []
        for i in range(start,finish):
            if i >= lazyload_offset - 1:
                image_pk_list.append(images[i]['pk'])
        image_qs = (apps.get_model(*conf.settings.DJANGO_BS_CAROUSEL_IMAGE_MODEL
                                       .split('.')).objects.filter(pk__in=image_pk_list)) 
        for im in image_qs.iterator():
            pic = get_thumbnail(im.image_file, screen_size, 
                                    format=fmt, crop='center', quality=70).url
            ql.append({'id': im.pk,
                       'pic': pic}) 
        ql.append({'id': '', 'pic': ''})
        return http.JsonResponse(ql, safe=False)
