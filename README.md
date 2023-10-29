# Population-based probability map and connectional profiles of the hand motor hotspot in transcranial magnetic stimulation 
Here you may find the result of hand motor hotspot (hMHS) for our article on [Population-based probability map and connectional profiles of the hand motor hotspot in transcranial magnetic stimulation](). All resources are provided as complementary to the following article:

## hMHS probability map
The hMHS probability is one of our main result and can be applied in practice clinical setting. We place the hMHS probability files in `./hs_prob.func.gii`

![hMHS Probability Map](fig/hs_prob.png)

## hMHS deterministic map range in probability threshold
For clinical application, we provide a series of deterministic hMHS maps in different probability threshold. Our article describes the cover rate, areas, volumes, Euclidean distance and surface distance of different probability threshold. So a deterministic hMHS map can be selected by fully comparsion in clinical setting. The following figure shows the deterministic hMHS in different probability threshold. 
![hMHS desc maps](fig/hs_desc_map.png)
And the deterministic hMHS maps in fsaverage32k and MNI152 template space are saved in [./hs_desc_maps/fsaverage32k](./hs_desc_maps/fsaverage32k/) and [./hs_desc_maps/MNI152](./hs_desc_maps/MNI152/), respectively. These population-based hMHS map can be warpped into native to acquire the individualized hMHS for TMS treatment.

## A simple tools for hMHS individualize
There is a simple [python scripts](./code/hMHS_individualize.py) for hMHS individualize. This scripts uses the ANTs tool to map the population-based hMHS toward native hMHS. 

Here is an example:
```shell
# Only providing the t1 image. The t1 MRI firstly acts as the reference image for registration from MNI152 to Native space. The default hMHS map is set by 'hs_desc_maps/MNI152/hs_map_prob-0.70.nii.gz'. The default output directory is the work directory.
cd code
python hMHS_individualize.py \
    --subj_t1 $t1w_path
```
