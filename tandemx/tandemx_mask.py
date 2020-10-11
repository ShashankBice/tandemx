#! /usr/bin/env python

"""
This library is just a functionized copy of David's tandemx_mask.py script
All credits to https://github.com/dshean/tandemx/blob/master/tandemx_mask.py
"""
import sys
import os
import glob
from pygeotools.lib import iolib
import numpy as np
import scipy.ndimage as ndimage


def mask_tandemx(tiledir,return_fn=True):
    """
    Function to mask and clean up TanDEM-X DEMs based on the theoretical ancillary files
    Documentation of AUX products is here: https://tandemx-science.dlr.de/pdfs/TD-GS-PS-0021_DEM-Product-Specification_v3.1.pdf
    Parameters
    -----------
    tiledir: str
          path to unzipped TanDEM-X file dir
    return_fn: bool
          whether to return masked DEM filename or not (default: True)
    """
    print(tiledir)
    dem_fn = glob.glob(os.path.join(tiledir, 'DEM/*DEM.tif'))[0]
    print(dem_fn)
    dem_ds = iolib.fn_getds(dem_fn)
    dem = iolib.ds_getma(dem_ds)
    print(dem.count())
    
    #Get original mask, True where masked
    mask = np.ma.getmaskarray(dem)
    
    #Theoretical height error
    err_fn = glob.glob(os.path.join(tiledir, 'AUXFILES/*HEM.tif'))[0]
    err = iolib.fn_getma(err_fn)
    max_err_multi = 1.5
    mask = np.logical_or(mask, (err.data > max_err_multi))
    
    #Water mask
    wam_fn = glob.glob(os.path.join(tiledir, 'AUXFILES/*WAM.tif'))[0]
    wam = iolib.fn_getma(wam_fn)
    wam_clim = (33,127)
    #wam_clim = (3,127)
    mask = np.logical_or(mask, (wam >= wam_clim[0]) & (wam <= wam_clim[1]))
    
    #Consistency mask
    com_fn = glob.glob(os.path.join(tiledir, 'AUXFILES/*COM.tif'))[0]
    com = iolib.fn_getma(com_fn)
    com_valid = (8,9,10)
    #4 is only one obs
    #com_invalid = (0,1,2,4)
    com_invalid = (0,1,2)
    mask = np.logical_or(mask, np.isin(com.data, com_invalid))
    
    #Apply
    dem_masked = np.ma.array(dem, mask=mask)
    print(dem_masked.count())
    out_fn = os.path.splitext(dem_fn)[0]+'_masked.tif'
    iolib.writeGTiff(dem_masked, out_fn, dem_ds)
    return_fname = out_fn
    
    # Include this in function docstring
    #if erode isolated pixels
    if erode_isolated:
        #Dilate mask by n_iter px to remove isolated pixels and values around nodata 
        n_iter = 1
        mask = ndimage.morphology.binary_dilation(mask, iterations=n_iter)
        #To keep valid edges, do subsequent erosion 
        mask = ndimage.morphology.binary_erosion(mask, iterations=n_iter)
        #(dilation of inverted mask, to avoid maasking outer edge)
        #mask = ~(ndimage.morphology.binary_dilation(~mask, iterations=n_iter))
        #Apply
        dem_masked = np.ma.array(dem, mask=mask)
        print(dem_masked.count())
        out_fn = os.path.splitext(dem_fn)[0]+'_masked_erode.tif'
        iolib.writeGTiff(dem_masked, out_fn, dem_ds)
        return_fname = out_fn
   
    if return_fn:
        return return_fname


