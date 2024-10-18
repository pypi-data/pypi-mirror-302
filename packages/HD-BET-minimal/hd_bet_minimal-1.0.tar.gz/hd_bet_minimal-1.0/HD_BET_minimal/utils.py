from typing import Optional, Callable
from urllib.request import urlopen

import requests
import torch
from appdirs import AppDirs
from torch import nn
import numpy as np
from skimage.morphology import label
import os
import hashlib

APP_NAME = "HD-BET-minimal"
APP_DEVELOPER = "Dafne-imaging"

app_dirs = AppDirs(APP_NAME, APP_DEVELOPER)
MODEL_PATH = os.path.join(app_dirs.user_data_dir, 'models')
os.makedirs(MODEL_PATH, exist_ok=True)

folder_with_parameter_files = MODEL_PATH

def get_params_fname(fold):
    return os.path.join(folder_with_parameter_files, "%d.model" % fold)

SHA_SUMS = {
    get_params_fname(0): '6f75233753c4750672815e2b7a86db754995ae44b8f1cd77bccfc37becd2d83c',
    get_params_fname(1): '5fcd430c271bb5e13ea8d44f3d303b2dfafa4d0845c1aec6c5a7375f6d727189',
    get_params_fname(2): '558ede4acb35537585219ece9c6b4b627dd3c019c6865daed0dfc80781dd94e9',
    get_params_fname(3): '57bf67a58c9e925b13d5b9ae6d6bb648deaf759f6d0af2ccad67651d7a2a93db',
    get_params_fname(4): '567689e4dff87debe357b30e4414c412485207657d1e99c33bf0bf587d28bf32'
}

SIZES = {
    get_params_fname(0): 65443735,
    get_params_fname(1): 65443803,
    get_params_fname(2): 65443755,
    get_params_fname(3): 65443847,
    get_params_fname(4): 65443955
}

def check_sha256(fname, sha256):
    sha = hashlib.sha256()
    with open(fname, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha.update(byte_block)
    return sha.hexdigest() == sha256

def download_parameter_file(fold, progress_callback: Optional[Callable[[int, int], None]] = None):

    path = get_params_fname(fold)

    try:
        size = os.path.getsize(path)
    except FileNotFoundError:
        size = 0

    if size != SIZES[path]:
        print('Downloading checkpoint...')
        # model needs to be downloaded
        url = "https://zenodo.org/record/2540695/files/%d.model?download=1" % fold
        r = requests.get( url , stream=True)
        if r.ok:
            success = True
            total_size_in_bytes = int(r.headers.get('content-length', 0))
            print("Size to download:", total_size_in_bytes)
            block_size = 1024 * 1024  # 1 MB
            current_size = 0
            with open(path, 'wb') as file:
                for data in r.iter_content(block_size):
                    current_size += len(data)
                    if progress_callback is not None:
                        progress_callback(current_size, total_size_in_bytes)
                    file.write(data)

            print("Downloaded size", current_size)
            if current_size != total_size_in_bytes or not check_sha256(path, SHA_SUMS[path]):
                print("Download failed!")
                raise requests.ConnectionError("Error downloading model checkpoint")


def init_weights(module):
    if isinstance(module, nn.Conv3d):
        module.weight = nn.init.kaiming_normal(module.weight, a=1e-2)
        if module.bias is not None:
            module.bias = nn.init.constant(module.bias, 0)


def softmax_helper(x):
    rpt = [1 for _ in range(len(x.size()))]
    rpt[1] = x.size(1)
    x_max = x.max(1, keepdim=True)[0].repeat(*rpt)
    e_x = torch.exp(x - x_max)
    return e_x / e_x.sum(1, keepdim=True).repeat(*rpt)


class SetNetworkToVal(object):
    def __init__(self, use_dropout_sampling=False, norm_use_average=True):
        self.norm_use_average = norm_use_average
        self.use_dropout_sampling = use_dropout_sampling

    def __call__(self, module):
        if isinstance(module, nn.Dropout3d) or isinstance(module, nn.Dropout2d) or isinstance(module, nn.Dropout):
            module.train(self.use_dropout_sampling)
        elif isinstance(module, nn.InstanceNorm3d) or isinstance(module, nn.InstanceNorm2d) or \
                isinstance(module, nn.InstanceNorm1d) \
                or isinstance(module, nn.BatchNorm2d) or isinstance(module, nn.BatchNorm3d) or \
                isinstance(module, nn.BatchNorm1d):
            module.train(not self.norm_use_average)


def postprocess_prediction(seg):
    # basically look for connected components and choose the largest one, delete everything else
    print("running postprocessing... ")
    mask = seg != 0
    lbls = label(mask, connectivity=mask.ndim)
    lbls_sizes = [np.sum(lbls == i) for i in np.unique(lbls)]
    largest_region = np.argmax(lbls_sizes[1:]) + 1
    seg[lbls != largest_region] = 0
    return seg


def subdirs(folder, join=True, prefix=None, suffix=None, sort=True):
    if join:
        l = os.path.join
    else:
        l = lambda x, y: y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isdir(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res


def subfiles(folder, join=True, prefix=None, suffix=None, sort=True):
    if join:
        l = os.path.join
    else:
        l = lambda x, y: y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isfile(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res


subfolders = subdirs  # I am tired of confusing those