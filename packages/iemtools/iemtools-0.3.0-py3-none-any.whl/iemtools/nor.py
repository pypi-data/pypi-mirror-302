from skimage import exposure
from skimage import feature
import skimage as ski
import numpy as np
import os, sys
import time
import glob

def NOR( subfolder , subject , time_limit , fps , rescale_low , rescale_hi , sigma ):
    #load images and masks
    image_list = []
    mask_list = []
    for frame in glob.glob( subfolder+"/*.jpg" ):
        im = np.sum(ski.io.imread(frame) , axis=2)
        image_list.append(im)
    for file in glob.glob( subfolder+"/masks/*.png" ):
        #load masks and threshold them
        mask_list.append( np.where( np.sum(ski.io.imread( file ) , axis=2) < 1 , 0 , 1 ) )
    #IMAGE PROCESSING
    sequence = []
    overlaps = []
    timestamps = []
    timestamp = 0
    #load one frame from image list
    for frame in image_list:
        #increment timestamp by fps of the video
        timestamp += fps
        #rescale intensity
        s_low, s_hi = np.percentile( frame , ( rescale_low , rescale_hi ) )
        rescaled = exposure.rescale_intensity( frame, in_range=( s_low , s_hi) )
        #find edges in current rescaled img
        edges = feature.canny( rescaled , sigma )
        #overlap (1*1) between image and arms' masks, outside mask = 0 ie 1*0 or 0*0
        arms = []        
        for mask in mask_list:
            arms.append( np.sum( edges * mask ) )
        #find greatest overlap
        max_overlap = sorted( arms )[1]
        if max_overlap == 0:
            position = "O"
        elif arms[0] == max_overlap:
            position = "L"
        elif arms[1] == max_overlap:
            position = "R"
        else: pass
        sequence.append(position)
        timestamps.append(timestamp)
    #find duration spent in either area
    ls = sequence.count("L")
    rs = sequence.count("R")
    duration_L = ls / fps
    duration_R = rs / fps
    #count instances of staying in either area
    i = 1
    N_ls = 0
    N_rs = 0
    while i < len( sequence ) - 1:
        if sequence[ i ] == "L" and sequence[ i+1 ] != sequence[ i ]:
            N_ls += 1
        elif sequence[ i ] == "R" and sequence[ i+1 ] != sequence[ i ]:
            N_rs += 1
        else: pass
        i += 1
    try: index = (duration_L-duration_R)/(duration_L+duration_R)
    except: index = 0
    return subject , duration_L , N_ls , duration_R , N_rs , index

def unblind( to_sort , template ):
    """
    Compares lists of L/R-indices with the position of the novel object.
    Returns a list of correctly identified recognition indices and a list of mistakes
    """
    try:
        iter = 0
        recognition_indices = []
        for subject in to_sort:
            if ( to_sort[ iter ][ 1 ] > 0 ) and ( template[ iter ][ 1 ] == "left" ):
                recognition_indices.append( subject )
            elif ( to_sort[ iter ][ 1 ] < 0 ) and ( template[ iter ][ 1 ] == "right" ):
                recognition_indices.append( [ to_sort[ iter ][ 0 ] , -to_sort[ iter ][ 1 ] ] )
            else: recognition_indices.append( [ to_sort[ iter ][ 0 ] , -to_sort[ iter ][ 1 ] ] )
            iter += 1
    except: print( "List lengths do not match or are of a wrong format." )
    return recognition_indices