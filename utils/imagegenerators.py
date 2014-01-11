import os
import uuid
from django.contrib.contenttypes.models import ContentType
from easy_thumbnails.files import get_thumbnailer
from kindy.celery import app


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)

    ctype = ContentType.objects.get_for_model(instance)
    model = ctype.model

    if model == 'diaryimage':
        return os.path.join('images/diary/', filename)

    if model == 'newsimage':
        return os.path.join('images/news/', filename)

    if model == 'newsfile':
        return os.path.join('files/news/', filename)

    if model == 'pagefile':
        return os.path.join('files/page/', filename)


@app.task
def utils_generate_thumbnail(object):
    thumbnailer = get_thumbnailer(object)
    thumbnailer.generate = True  # so a not generate a thumb if sthg went wrong
    thumbnail_options = {'crop': True, 'size': (100, 100), 'upscale': True}
    thumbnail = thumbnailer.get_thumbnail(thumbnail_options)
    object.thumbnail = thumbnail.url
    object.save()