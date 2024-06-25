#!/bin/python

import argparse, os
import shutil
import pandas as pd
import ants

DMPFC_coords = []   # todo 设置DMPFC的在MNI空间下的坐标

def get_args():
    args = argparse.ArgumentParser("hMHS individualize")
    args.add_argument("--subj_t1", required=True, help="The T1w path")
    args.add_argument("--out_dir", help="The out directory")
    opts = args.parse_args()
    return opts

if __name__ == '__main__':
    # load args parameters
    args = get_args()
    fi = ants.image_read(args.subj_t1)
    mi = ants.image_read(os.path.join(os.path.dirname(__file__), 'template', 'MNI152_T1_1mm.nii.gz'))
    out_dir = args.out_dir or "./"

    # SyN registration
    mytx = ants.registration(fixed=fi, moving=mi, write_composite_transform=True)

    # move transform files
    os.makedirs(out_dir, exist_ok=True)
    fwd_transform_path = os.path.join(out_dir, "mni2t1.h5")
    inv_transform_path = os.path.join(out_dir, "t12mni.h5")
    shutil.move(mytx['fwdtransforms'], fwd_transform_path)
    shutil.move(mytx['invtransforms'], inv_transform_path)

    # save reg nifti files
    warpedfixout = os.path.join(out_dir, "warped_t1.nii.gz")
    warpedmovout = os.path.join(out_dir, "warped_mni.nii.gz")
    shutil.move(mytx['warpedfixout'], warpedfixout)
    shutil.move(mytx['warpedmovout'], warpedmovout)

    df_vmpfc = pd.DataFrame([DMPFC_coords, DMPFC_coords], columns=['x', 'y', 'z'])
    df_vmpfc[['x', 'y']] = -df_vmpfc[['x', 'y']]
    df_native_vmpfc = ants.apply_transforms_to_points(3, df_vmpfc, transformlist=inv_transform_path)
    df_native_vmpfc[['x', 'y']] = -df_native_vmpfc[['x', 'y']]
    df_native_vmpfc.to_csv(os.path.join(out_dir, 'native_dmpfc.csv'))
