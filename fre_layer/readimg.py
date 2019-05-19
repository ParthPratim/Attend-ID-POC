from scipy import misc
from facenet.facenet import to_rgb , prewhiten, crop, flip

def load_image(path):
    image_size = 160
    img = misc.imread(path)
    if img.ndim == 2:
        img = to_rgb(img)
    img = prewhiten(img)
    img = crop(img, False, image_size)
    img = flip(img, False)
    return img

def load_images(paths):
    return [load_image(path) for path in paths]

def raw_process(img):
    if img.ndim == 2:
        img = to_rgb(img)
    try:
        img = prewhiten(img)
    except:
        pass
    img = crop(img, False, 160)
    img = flip(img, False)
    return img
