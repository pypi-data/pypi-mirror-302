from typing import Optional, Callable

import torch
import numpy as np
from .data_loading import preprocess_image_numpy, resize_image
from .predict_case import predict_case_3D_net
from .utils import postprocess_prediction, SetNetworkToVal, get_params_fname, download_parameter_file
import os
from .padorcut import padorcut

from . import config



def run_hd_bet_function(input_data, input_spacing, mode="accurate", device=0,
               postprocess=False, do_tta=True, progress_callback: Optional[Callable[[int, int], None]] = None):
    """

    :param input_data: numpy array containing the original MRI data
    :param input_spacing: list/tuple of 3 floats, the spacing of the original MRI data
    :param mode: fast or accurate
    :param device: either int (for device id) or 'cpu'
    :param postprocess: whether to do postprocessing or not. Postprocessing here consists of simply discarding all
    but the largest predicted connected component. Default False
    :param do_tta: whether to do test time data augmentation by mirroring along all axes. Default: True. If you use
    CPU you may want to turn that off to speed things up
    :return: bet: the brain extracted image, mask: the brain mask
    """

    MODEL_SPACING = (1.5, 1.5, 1.5)

    list_of_param_files = []

    if mode == 'fast':
        params_file = get_params_fname(0)
        download_parameter_file(0, progress_callback)

        list_of_param_files.append(params_file)
    elif mode == 'accurate':
        for i in range(5):
            params_file = get_params_fname(i)
            download_parameter_file(i, progress_callback)

            list_of_param_files.append(params_file)
    else:
        raise ValueError("Unknown value for mode: %s. Expected: fast or accurate" % mode)

    assert all([os.path.isfile(i) for i in list_of_param_files]), "Could not find parameter files"

    cf = config.config()

    net, _ = cf.get_network(cf.val_use_train_mode, None)
    if device == "cpu":
        net = net.cpu()
    else:
        net.cuda(device)

    params = []
    for p in list_of_param_files:
        params.append(torch.load(p, map_location=lambda storage, loc: storage, weights_only=True))

    data = preprocess_image_numpy(input_data, input_spacing, spacing_target=MODEL_SPACING)

    print(data.shape)

    softmax_preds = []

    print("prediction (CNN id)...")
    for i, p in enumerate(params):
        print("Running fold", i, "of", len(params))
        net.load_state_dict(p)
        net.eval()
        net.apply(SetNetworkToVal(False, False))
        _, _, softmax_pred, _ = predict_case_3D_net(net, np.expand_dims(data, 0), do_tta, cf.val_num_repeats,
                                                    cf.val_batch_size, cf.net_input_must_be_divisible_by,
                                                    cf.val_min_size, device, cf.da_mirror_axes)
        softmax_preds.append(softmax_pred[None])

    seg = np.argmax(np.vstack(softmax_preds).mean(0), 0)
    print("Seg shape", seg.shape)
    print("Data shape", input_data.shape)

    if postprocess:
        seg = postprocess_prediction(seg)

    seg = padorcut(resize_image(seg, MODEL_SPACING, input_spacing, order=0), input_data.shape)

    print("Seg shape after resize", seg.shape)

    bet = np.copy(input_data)
    bet[seg == 0] = 0

    return bet, seg