import numpy as np
from skimage.transform import resize


def resize_image(image, old_spacing, new_spacing, order=3):
    if np.any([[i != j] for i, j in zip(old_spacing, new_spacing)]):
        new_shape = (int(np.round(old_spacing[0]/new_spacing[0]*float(image.shape[0]))),
                     int(np.round(old_spacing[1]/new_spacing[1]*float(image.shape[1]))),
                     int(np.round(old_spacing[2]/new_spacing[2]*float(image.shape[2]))))
        return resize(image, new_shape, order=order, mode='edge', cval=0, anti_aliasing=False)
    return image

def preprocess_image_numpy(image, spacing, spacing_target=(1, 0.5, 0.5)):
    assert len(image.shape) == 3, "The image has unsupported number of dimensions. Only 3D images are allowed"

    image = resize_image(image.astype(np.float32), spacing, spacing_target)

    image -= image.mean()
    image /= image.std()
    return image

def preprocess_image(itk_image, is_seg=False, spacing_target=(1, 0.5, 0.5)):
    spacing = np.array(itk_image.GetSpacing())[[2, 1, 0]]
    image = sitk.GetArrayFromImage(itk_image).astype(float)

    assert len(image.shape) == 3, "The image has unsupported number of dimensions. Only 3D images are allowed"

    if not is_seg:
        image = resize_image(image.astype(np.float32), spacing, spacing_target)

        image -= image.mean()
        image /= image.std()
    else:
        new_shape = (int(np.round(spacing[0] / spacing_target[0] * float(image.shape[0]))),
                     int(np.round(spacing[1] / spacing_target[1] * float(image.shape[1]))),
                     int(np.round(spacing[2] / spacing_target[2] * float(image.shape[2]))))
        image = resize_segmentation(image, new_shape, 1)
    return image



def resize_segmentation(segmentation, new_shape, order=3, cval=0):
    '''
    Taken from batchgenerators (https://github.com/MIC-DKFZ/batchgenerators) to prevent dependency

    Resizes a segmentation map. Supports all orders (see skimage documentation). Will transform segmentation map to one
    hot encoding which is resized and transformed back to a segmentation map.
    This prevents interpolation artifacts ([0, 0, 2] -> [0, 1, 2])
    :param segmentation:
    :param new_shape:
    :param order:
    :return:
    '''
    tpe = segmentation.dtype
    unique_labels = np.unique(segmentation)
    assert len(segmentation.shape) == len(new_shape), "new shape must have same dimensionality as segmentation"
    if order == 0:
        return resize(segmentation, new_shape, order, mode="constant", cval=cval, clip=True, anti_aliasing=False).astype(tpe)
    else:
        reshaped = np.zeros(new_shape, dtype=segmentation.dtype)

        for i, c in enumerate(unique_labels):
            reshaped_multihot = resize((segmentation == c).astype(float), new_shape, order, mode="edge", clip=True, anti_aliasing=False)
            reshaped[reshaped_multihot >= 0.5] = c
        return reshaped
