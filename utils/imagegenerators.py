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