import numpy as np
from scipy.special import erfinv
from sar_apps.filters import Cross_DePolRAD, Co_DePolRAD, stats_guard, pnf, pwf, pmf


def cfar(image, target_window_shape=(1,1), guard_window_shape=(30,30), background_window_shape=(100,100), pfa=0.65, probabilityMethod='gaussian', padding='reflect'):
    ''' 
    Constant False Alarm Rate Algorythm
    
    Refrence
    --------
    [1] D. J. Crisp, "The State-of-the-Art in Ship Detection in Synthetic Aperture Radar Imagery." DSTO–RR–0272, 2004-05.

    Parameters:
    -----------
    image: numpy array
        The image to perform CFAR on
    target_window_shape: (int,int)
        Size in pixel of the cell under test
    guard_window_shape: (int,int) 
        Size in pixel of the guard Window around the Cell under Test
    background_window_shape: (int,int)
        Size in pixel of the background used to calculate statistic of the scene
    pfa: float
        Falsealarm threshold value
    probabilityMethod: str
        Method used to estimate statistic of scence
    padding: str
        padding method apllied to image
    '''

    t=erfinv(1-(2*pfa))*1.414213562
    
    stats=stats_guard(image,target_window_shape, guard_window_shape, background_window_shape, padding)
    
    result=stats>t

    return result


def iDePolRAD_comb1(cross, co, T, background_window_shape, guard_window_shape, target_window_shape):
    ''' 
    combined Depolarization Ratio Anomaly Detector according to [1]

    Refrences:
    ----------
    [1] Lanz, P.; Marino, A.;Brinkhoff, T.; Köster, F.; Möller, M.
    The InflateSAR Campaign: Testing SAR Vessel Detection Systems for
    Refugee Rubber Inflatables. Remote Sens. 2021, 13, 1487. 
    https://doi.org/10.3390/rs13081487   

    Parameters:
    -----------
    cross : array
        Intensity of Cross-Polarization channel
    co : array
        Intensity of Co-Polarization channel
    T : float
        Threshold
    background_window_shape : (int, int)
        Size in pixel of the background used to calculate statistic of the scene
    guard_window_shape : (int, int) 
        Size in pixel of the guard Window around the Cell under Test
    target_window_shape : (int, int)
        Size in pixel of the cell under test

    Returns:
    --------
    lam : array
        Depolarisation Ratio multiplyed with Co-Polarization Intensity
    '''
    CrossDePolRAD=Cross_DePolRAD(cross, co, background_window_shape, guard_window_shape, target_window_shape)
    CoDePolRAD=Co_DePolRAD(cross, co, background_window_shape, guard_window_shape, target_window_shape)

    bitMask=(CrossDePolRAD+CoDePolRAD)>T

    return bitMask

def iDePolRAD_comb2(cross, co, T:float, background_window_shape:tuple, guard_window_shape:tuple, target_window_shape:tuple):
    ''' 
    combined Depolarization Ratio Anomaly Detector according to [1]

    Refrences:
    ----------
    [1] Lanz, P.; Marino, A.;Brinkhoff, T.; Köster, F.; Möller, M.
    The InflateSAR Campaign: Testing SAR Vessel Detection Systems for
    Refugee Rubber Inflatables. Remote Sens. 2021, 13, 1487. 
    https://doi.org/10.3390/rs13081487   

    Parameters:
    -----------
    cross : array
        Intensity of Cross-Polarization channel
    co : array
        Intensity of Co-Polarization channel
    T : float
        Threshold
    background_window_shape : (int, int)
        Size in pixel of the background used to calculate statistic of the scene
    guard_window_shape : (int, int) 
        Size in pixel of the guard Window around the Cell under Test
    target_window_shape : (int, int)
        Size in pixel of the cell under test

    Returns:
    --------
    lam : array
        Depolarisation Ratio multiplyed with Co-Polarization Intensity
    '''
    CrossDePolRAD=Cross_DePolRAD(cross, co, background_window_shape, guard_window_shape, target_window_shape)>T
    CoDePolRAD=Co_DePolRAD(cross, co, background_window_shape, guard_window_shape, target_window_shape)>T

    print(np.max(CrossDePolRAD))
    print(np.max(CoDePolRAD))

    bitMask=np.bitwise_or(CrossDePolRAD,CoDePolRAD)

    return bitMask

def ensemble_detection(i_vh, i_vv,sig_vh, sig_vv, c2, n=5):
    """ 
    This ensemble detector runs different filters on the input and performs 
    a CFAR-based score. Instead of thresholding the image right away the factor
    by which the pixel value is above the mean and standard deviation
    (See stats guard filter) is calculated.
    The top n highest scores are saved to top_score_idx as flat indices and to 
    top_score_image as binary mask.

    Parameters:
    -----------
    i_vh : ndarray
        2D array with Intensity of Cross-polarisation. 
    i_vv : ndarray
        2D array with Intensity of Co-polarisation. 
    C2 : ndarray
        C2 array of image 
    n : int
        number of top top_score_idx to go into the score image
        Default 5

    Returns:
    --------
    detectors : dict
        dict with top_score_idx result for each detection method
    top_score_idx : dict
        dict with top 5 indices of flattened input for each detection method
    top_score_image : ndarray
        Bit Mask with the top 5 top_score_idx and a band for each detector.
    """
    n+=1 #correct for indexing lag

    width, height=i_vh.shape
    detectors={}
    detectors['VH_CFAR']=stats_guard(i_vh)
    detectors['VV_CFAR']=stats_guard(i_vv)
    detectors['Cross_DePolRAD']=stats_guard(Cross_DePolRAD(i_vh,i_vv))
    detectors['Co_DePolRAD']=stats_guard(Co_DePolRAD(i_vh,i_vv))
    detectors['Sig_VH_CFAR']=stats_guard(sig_vh)
    detectors['Sig_VV_CFAR']=stats_guard(sig_vv)
    detectors['Sig_Cross_DePolRAD']=stats_guard(Cross_DePolRAD(sig_vh,sig_vv))
    detectors['Sig_Co_DePolRAD']=stats_guard(Co_DePolRAD(sig_vh,sig_vv))
    detectors['PWF']=stats_guard(pwf(c2))
    detectors['PNF']=stats_guard(pnf(c2))
    detectors['PMF']=stats_guard(pmf(c2))
    keys=detectors.keys()
    top_score_idx={}
    top_score_image=np.zeros((width*height, len(keys)))
    for idx, key in enumerate(keys):
        top_score_idx[key]=np.argsort(detectors[key].flatten())[:-n:-1]
        top_score_image[top_score_idx[key],idx]=1
    top_score_image=top_score_image.reshape((width,height,len(keys)))

    return detectors, top_score_idx, top_score_image