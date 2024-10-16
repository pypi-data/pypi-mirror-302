import os

ROOTDIR = os.path.split(__file__)[0]


def get_ckpt_folder(metric, type):
    return os.path.join(ROOTDIR, "weights", f"{metric}-{type}")
