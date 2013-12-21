'''
from imagekit import ImageSpec, register
from pilkit.processors import ResizeToFill


class ChildThumbnail(ImageSpec):
    processors = [ResizeToFill(100, 100)]
    format = 'JPEG'
    options = {'quality': 80}


class GalleryThumbnail(ImageSpec):
    processors = [ResizeToFill(80, 80)]
    format = 'JPEG'
    options = {'quality': 80}

register.generator('child:thumbnail', ChildThumbnail)
register.generator('gallery:thumbnail', GalleryThumbnail)
'''
import os
import uuid
from django.contrib.contenttypes.models import ContentType


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