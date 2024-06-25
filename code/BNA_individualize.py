#!/bin/python

import argparse, os
import shutil
import ants


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
    bna = "/n01dat01/xlcheng/brain_template/BN_Atlas/BN_Atlas_246_1mm.nii.gz"
    bna = ants.image_read(bna)
    sc = "/n01dat01/xlcheng/brain_template/BN_Atlas/BNA_SC_3D_246/057.nii.gz"
    sc = ants.image_read(sc)
    fc = "/n01dat01/xlcheng/brain_template/BN_Atlas/BNA_FC_3D_246/057.nii.gz"
    fc = ants.image_read(fc)
    out_dir = args.out_dir or "./"

    # SyN registration
    # mytx = ants.registration(fixed=fi, moving=mi, write_composite_transform=True)

    # move transform files
    os.makedirs(out_dir, exist_ok=True)
    fwd_transform_path = os.path.join(out_dir, "hmhs2t1.h5")
    inv_transform_path = os.path.join(out_dir, "t12hmhs.h5")
    # shutil.move(mytx['fwdtransforms'], fwd_transform_path)
    # shutil.move(mytx['invtransforms'], inv_transform_path)

    # apply transform to warp hMHS file
    native_bna = ants.apply_transforms(fixed=fi, moving=bna, transformlist=fwd_transform_path, interpolator='nearestNeighbor')
    native_sc = ants.apply_transforms(fixed=fi, moving=sc, transformlist=fwd_transform_path,)
    native_fc = ants.apply_transforms(fixed=fi, moving=fc, transformlist=fwd_transform_path,)

    # save file
    ants.image_write(native_bna, os.path.join(out_dir, "native_bna.nii.gz"))
    ants.image_write(native_sc, os.path.join(out_dir, "native_057_sc.nii.gz"))
    ants.image_write(native_fc, os.path.join(out_dir, "native_057_fc.nii.gz"))
