from os import system, getcwd, makedirs, walk, rename, remove
from os.path import exists, isfile, join, sep
import shutil

DIRSYNTHSEG = join(sep, "Synthseg", "scripts",
                   "launch_scripts_from_terminal", "SynthSeg_predict.py")


def run_SynthSeg(infile, outfolder):
    import subprocess
    import time
    # turn on trial env
    subprocess.call(["python", DIRSYNTHSEG, infile, outfolder + sep,
                     "--out_posteriors", outfolder + sep + "posteriors.nii.gz"])

    name = infile.split(sep)[-1]

    if isfile(join(outfolder, name.split(".")[0]+'_seg.nii.gz')):
        seg_vol = nib.load(join(outfolder, name.split(".")
                                [0]+'_seg.nii.gz')).get_data()
    else:
        namefile = name.split(".")[0]+'_seg.nii.gz'
        #raise ValueError("%s was not created", namefile)

    # filling gaps of lesions
    posteriors = nib.load(join(outfolder, "posteriors.nii.gz"))
    data = posteriors.get_fdata()
    mask = nib.load(infile).get_fdata() != 0
    # here the gaps are fill
    Acor = np.multiply(np.argmax(data[:, :, :, 1:], axis=3), mask)
    # delete innecesary files
    remove(join(outfolder, "posteriors.nii.gz"))
    remove(join(outfolder, name.split(".")[0]+'_seg.nii.gz'))
    # save output
    nib.save(nib.Nifti1Image(Acor, posteriors.affine), join(
        outfolder, name.split(".")[0]+'_seg.nii.gz'))


def run_intensity_delis(infile, outfolder):

    from scipy.ndimage import binary_erosion, generate_binary_structure
    from intensity_normalization.utilities import hist
    # 0. get the segmentation mask with synthseg tool

    run_SynthSeg(infile, outfolder)

    # 1. load the image and segmentation mask

    name = infile.split(sep)[-1]

    in_vol = nib.load(infile)

    if isfile(join(outfolder, name.split(".")[0]+'_seg.nii.gz')):
        seg_vol = nib.load(join(outfolder, name.split(".")
                                [0]+'_seg.nii.gz')).get_data()
    else:
        namefile = name.split(".")[0]+'_seg.nii.gz'
        #raise ValueError("%s was not created" % namefile)

    # 2.get the white matter from the mask
    mask = np.logical_or(seg_vol == 18, seg_vol == 3)

    header = in_vol.header
    affine = in_vol.affine
    in_vol = in_vol.get_data()

    # 3. erode the mask
    mask = binary_erosion(mask, generate_binary_structure(3, 1))

    # 4. get the points on the data of the tails at 5% and 95%
    # min_p = np.percentile(in_vol[mask], 5)
    # max_p = np.percentile(in_vol[mask], 95)

    # 5. get the data between with no tails(outliers)
    values = in_vol[mask].flatten()
    # values = values[values > min_p]
    # values = values[values < max_p]

    # 6. get the mean and standard deviation
    # from scipy.stats import mode
    # wm_peak = mode(values)[0]
    wm_peak = hist.get_last_mode(values)
    # std = values.std()
    # 7. perform the zscore formula and save the data in a image format
    normalised = nib.Nifti1Image(in_vol/wm_peak, affine, header)
    # 8. save the normalized image
    nib.save(normalised, join(
        outfolder, name.split(".")[0]+"_delis.nii.gz"))