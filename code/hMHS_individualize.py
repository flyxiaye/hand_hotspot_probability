#!/bin/python

import argparse, os
import shutil
import ants


def get_args():
    args = argparse.ArgumentParser("hMHS individualize")
    args.add_argument("--hs_map", help="The hMHS path")
    args.add_argument("--subj_t1", required=True, help="The T1w path")
    args.add_argument("--out_dir", help="The out directory")
    opts = args.parse_args()
    return opts

if __name__ == '__main__':
    # load args parameters
    args = get_args()
    fi = ants.image_read(args.subj_t1)
    mi = ants.image_read(os.path.join(os.path.dirname(__file__), 'template', 'MNI152_T1_1mm.nii.gz'))
    hmhs = ants.image_read(args.hs_map or os.path.dirname(os.path.dirname(__file__)), 'hs_desc_maps', 'MNI152', 'hs_map_prob-0.70.nii.gz')
    out_dir = args.out_dir or "./"

    # SyN registration
    mytx = ants.registration(fixed=fi, moving=mi, write_composite_transform=True)

    # move transform files
    os.makedirs(out_dir, exist_ok=True)
    fwd_transform_path = os.path.join(out_dir, "hmhs2t1.h5")
    inv_transform_path = os.path.join(out_dir, "t12hmhs.h5")
    shutil.move(mytx['fwdtransforms'], fwd_transform_path)
    shutil.move(mytx['invtransforms'], inv_transform_path)

    # apply transform to warp hMHS file
    native_hmhs = ants.apply_transforms(fixed=fi, moving=hmhs, transformlist=fwd_transform_path, interpolator='nearestNeighbor')

    # save file
    ants.image_write(native_hmhs, os.path.join(out_dir, "native_hMHS.nii.gz"))
