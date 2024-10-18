import numpy as np
from sar_apps.convolution import convolve2D, create_guard_filter, create_kernel

def mean_guard(image, guard_window_shape=(30,30), background_window_shape=(100,100), padding='reflect'):
    ''' 
    This function calculates the mean pixel value using a guard filter. 

    Parameters:
    -----------
    image: numpy array
        The image to perform CFAR
    guard_window_shape: (int,int) 
        Size in pixel of the guard Window around the Cell under Test
    background_window_shape: (int,int)
        Size in pixel of the background used to calculate statistic of the scene
    padding: str
        padding method apllied to image
    
    Returns:
    --------
    mean : numpy array
        The mean value of all pixels in the stencil
    '''
    ImageFilter=create_guard_filter(background_window_shape,guard_window_shape)
    mean=convolve2D(image, ImageFilter,kernel_is_fft=False)
    return mean

def C2_train(C2, target_window_shape=(1,1), guard_window_shape=(30,30), background_window_shape=(100,100), padding='reflect'):
    filter_train=create_guard_filter(background_window_shape,guard_window_shape)
    paddedImageShape=(C2.shape[0]+filter_train.shape[0],C2.shape[1]+filter_train.shape[1])
    kernel_train=create_kernel(filter_train,paddedImageShape)

    C11=C2[:,:,0]
    C22=C2[:,:,1]
    C12=C2[:,:,2]
    
    C11_train=convolve2D(C11,kernel_train,kernel_is_fft=True)
    C22_train=convolve2D(C22,kernel_train,kernel_is_fft=True)
    C12_train=convolve2D(C12,kernel_train,kernel_is_fft=True, complex=True)

    if target_window_shape[0]>1 and target_window_shape[1]>1:
        filter_target=np.ones(target_window_shape)
        filter_target=filter_target/np.sum(filter_target)
        kernel_target=create_kernel(filter_target,paddedImageShape)

        C11=convolve2D(C11,kernel_target,kernel_is_fft=True)
        C22=convolve2D(C22,kernel_target,kernel_is_fft=True)
        C12=convolve2D(C12,kernel_target,kernel_is_fft=True, complex=True)

    return (C11, C22, C12, C11_train, C22_train, C12_train)



def stats_guard(image, target_window_shape=(1,1), guard_window_shape=(30,30), background_window_shape=(100,100), padding='reflect'):
    ''' 
    This function calculates the factor by which the pixel value deviates stronger from the mean than the standard deviation does.
    The statistics are estimated using a guard filter.

     pixel = mean + factor * sigma
     factor = (pixel-mean)/sigma
    
    if the target window is bigger than (1,1) instead of the pixel value the mean pixel value of the target window is used.

    Parameters:
    -----------
    image: numpy array
        The image to perform CFAR
    target_window_shape: (int,int)
        Size in pixel of the cell under test
    guard_window_shape: (int,int) 
        Size in pixel of the guard Window around the Cell under Test
    background_window_shape: (int,int)
        Size in pixel of the background used to calculate statistic of the scene
    padding: str
        padding method apllied to image
    
    Returns:
    --------
    stats : numpy array
        The mean value of all pixels in the stencil
    '''

    filter_b=create_guard_filter(background_window_shape,guard_window_shape)

    paddedImageShape=(image.shape[0]+filter_b.shape[0],image.shape[1]+filter_b.shape[1])
    kernel=create_kernel(filter_b,paddedImageShape)

    mu_b=convolve2D(image, kernel,kernel_is_fft=True)
    sig_b=(image-mu_b)**2
    sig_b=np.sqrt(convolve2D(sig_b,kernel,kernel_is_fft=True))
    if target_window_shape[0]>1 and target_window_shape[1]>1:
        filter_t=np.ones(target_window_shape)
        filter_t=filter_t/filter_t.sum()
        image=convolve2D(image,filter_t)
    
    stats=(image-mu_b)/sig_b
    return stats

def pwf(C2, guard_window_shape=(30,30), background_window_shape=(100,100),target_window_shape=(1,1)):
    """ 
    Polarimetric Whitening Filter according to [1,2]. Instead of a normal boxcar filter a guard filter is apllied.
    Algorythm has been adapted for dual pol Data.
   
    The inverse of the C2 matrix is calculated analytically with 
                _       _
    inv= 1/det |C22  -C12|
               |-C12* C11|
               -         -
    The matrix multiplication of the test cell and the training cell 
    is calculated analytically and denoted as A.
    The Eigenvalue of A is calculated analytically with and denoted as lam.

    Refrences:
    ----------
    [1] L.M. Novak, M.C. Burl, R.D. Chaney, and G.J. Owirka (1990). Optimal Processing of Polarimetric
    Synthetic-Aperture Radar Imagery. The Lincoln Laboratory Journal, Volume 3, Number 2
    [2] L.M. Novak and S.R. Hesse. Optimal Polarizations for Radar Detection
    and Recognition of Targets in Clutter. MIT Lincoln Laboratory

    Parameters:
    -----------
    C2 : complex array
        C2 Coherence Matrix
    background_window_shape : (int,int)
        Size in pixel of the background used to calculate statistic of the scene
    guard_window_shape : (int,int) 
        Size in pixel of the guard Window around the Cell under Test
    target_window_shape : (int,int)
        Size in pixel of the cell under test

    Returns:
    --------
    lam : ndarray
        filtered image
    """

    C11, C22, C12, C11_train, C22_train, C12_train=C2_train(C2, target_window_shape, guard_window_shape,background_window_shape)
    C12c=C12.conj()

    det=(C11*C22)-(C12*C12c)
    det[det==0]=np.nan
    C11_train=C11_train/det
    C22_train=C22_train/det
    C12_train=C12_train/det
    C12c_train=C12_train.conj()

    return np.abs((C11*C11_train)+(C12*C12c_train)+(C12c*C12_train)+(C22*C22_train))

def mmse_pwf(C2, guard_window_shape=(30,30), background_window_shape=(100,100), target_window_shape=(1,1)):
    ''' 
    Minimum Mean Square Error Polarimetric Whitening Filter according to [1].

    Refrences:
    ----------
    [1] MODIFIED POLARIMETRIC WHITENING FILTER FOR POLARIMETRIC SAR DATA
    Wentao An, Mingsen Lin, Chunhua Xie, Guangyi Zhou, Xinzhe Yuan
    National Satellite Ocean Application Service, Beijing 100081, China.

    Parameters:
    image : complex array
        complex image
    background_window_shape : (int,int)
        Size in pixel of the background used to calculate statistic of the scene
    guard_window_shape : (int,int) 
        Size in pixel of the guard Window around the Cell under Test
    target_window_shape : (int,int)
        Size in pixel of the cell under test

    Returns:
    --------
    PWF image
    '''
    filter_b=create_guard_filter(background_window_shape,guard_window_shape)
    paddedImageShape=(C2.shape[0]+filter_b.shape[0],C2.shape[1]+filter_b.shape[1])
    kernel_b=create_kernel(filter_b,paddedImageShape)

    C11=C2[:,:,0]
    C22=C2[:,:,1]
    C12=C2[:,:,2]
    
    EC11=convolve2D(C11,kernel_b,kernel_is_fft=True)
    EC22=convolve2D(C22,kernel_b,kernel_is_fft=True)
    EC12=convolve2D(C12,kernel_b,kernel_is_fft=True, complex=True)
    factor=(EC11*EC22)-(EC12**2)
    factor[factor==0]=10**-16
    EC11=EC11/factor
    EC22=EC22/factor
    EC12=EC12/factor

    if target_window_shape[0]>1 and target_window_shape[1]>1:
        filter_t=np.ones(target_window_shape)
        filter_t=filter_t/np.sum(filter_t)
        kernel_t=create_kernel(filter_t,paddedImageShape)

        C11=convolve2D(C11,kernel_t,kernel_is_fft=True)
        C22=convolve2D(C22,kernel_t,kernel_is_fft=True)
        C12=convolve2D(C12,kernel_t,kernel_is_fft=True, complex=True)

    yPWF=(C11*EC22+C22*EC11-2*C12*EC12)
    m=(EC11+EC22+2*EC12)*4
    p=np.sqrt((m**2)-(EC11*EC22-EC12**2))
    lam1=m+p
    lam2=m-p
    w=0.25*(lam1+2*np.sqrt(lam1*lam2)+lam2)
    return w*yPWF


def pnf(C2, red_r=0.002, guard_window_shape=(30,30), background_window_shape=(100,100),target_window_shape=(1,1)):
    ''' 
    Polarimetric Notch Filter according to [1]. Instead of a normal boxcar filter a guard filter is apllied.

    Refrences:
    ----------
    [1] Marino, Armando (2013). A notch filter for ship detection with polarimetric SAR data.
    IEEE Journal of Selected Topics in Applied Earth Observation and Remote Sensing, 6(3) pp. 1219–1232.
    
    Parameters:
    C2 : complex array
        C2 Coherence Matrix
    T : float
        Threshold
    red_r : float
        Reduction Ratio
    background_window_shape : (int,int)
        Size in pixel of the background used to calculate statistic of the scene
    guard_window_shape : (int,int) 
        Size in pixel of the guard Window around the Cell under Test
    target_window_shape : (int,int)
        Size in pixel of the cell under test

    Returns:
    --------
    gam : ndarray
        filtered image
    '''
    C11, C22, C12, C11_train, C22_train, C12_train=C2_train(C2, target_window_shape, guard_window_shape,background_window_shape)
    
    Ptot = C11**2 + C22**2 + np.abs(C12)**2
    norma = np.sqrt(C11_train**2 + C22_train**2 + np.abs(C12_train)**2)
    norma[norma==0]=np.nan
    C11_train=C11_train/norma 
    C22_train=C22_train/norma 
    C12_train=C12_train/norma    

    Psea = np.abs( C11*np.conj(C11_train) + C22*np.conj(C22_train) + C12*np.conj(C12_train))**2

    Pt = Ptot - Psea
    Pt[Pt==0]=np.nan
    
    return np.abs(1./np.sqrt(1 + red_r/Pt))
   

def pmf(Cross, Co, guard_window_shape=(30,30), background_window_shape=(100,100),target_window_shape=(1,1)):
    """ 
    Polarimetric match filter according to Armando Marino. 
    The inverse of the C2 matrix is calculated analytically with 
                _       _
    inv= 1/det |C22  -C12|
               |-C12* C11|
               -         -
    The matrix multiplication of the test cell and the training cell 
    is calculated analytically and denoted as A.
    The Eigenvalue of A is calculated analytically with and denoted as lam.

    Parameters:
    C2 : complex array
        C2 Coherence Matrix
    background_window_shape : (int,int)
        Size in pixel of the background used to calculate statistic of the scene
    guard_window_shape : (int,int) 
        Size in pixel of the guard Window around the Cell under Test
    target_window_shape : (int,int)
        Size in pixel of the cell under test

    Returns:
    --------
    lam : ndarray
        filtered image
    """
    C=np.zeros((Cross.shape[0],Cross.shape[1],3),dtype=complex)
    C[...,0]=Co*Co.conj()
    C[...,1]=Cross*Cross.conj()
    C[...,2]=Co*Cross.conj()
    C11, C22, C12, C11_clutter, C22_clutter, C12_clutter=C2_train(C, target_window_shape, guard_window_shape,background_window_shape)

    C21=C12.conj()
    C21_clutter=C12_clutter.conj()

    det=(C11_clutter*C22_clutter)-(C12_clutter*C21_clutter)
    det[det==0]=np.nan
    C11_clutter=C11_clutter/det
    C22_clutter=C22_clutter/det
    C12_clutter=C12_clutter/det
    C21_clutter=C21_clutter/det

    a=(C11_clutter*C11)+(C12_clutter*C21)
    b=(C11_clutter*C12)+(C12_clutter*C22)
    c=(C21_clutter*C11)+(C22_clutter*C21)
    d=(C21_clutter*C12)+(C22_clutter*C22)

    p=a*d/2
    q=np.sqrt(p**2-((a*d)-(b*c)))
    lam1=-p+q
    lam2=-p-q

    lam=lam1
    dlam=np.abs(lam2)-np.abs(lam1)
    lam[dlam>0]=lam2[dlam>0]

    w1=np.ones(lam.shape,dtype=complex)
    w1[b==0]=0
    w2=(lam-a)/b
    w2[b==0]=1

    return np.abs((w1*Co)+(w2*Cross))**2

def Cross_DePolRAD(cross, co,  guard_window_shape=(30,30), background_window_shape=(100,100),target_window_shape=(1,1)):
    ''' 
    Depolarization Ratio Anomaly Detector according to [1]

    Refrences:
    ----------
    [1] Marino, Armando (2013). A Depolarization Ratio Anomaly Detector
    to identify icebergs in sea ice using dual-polarization SAR images.
    IEEE TRANSACTIONS ON GEOSCIENCE AND REMOTE SENSING, EARLY ACCESS, 2016   

    Parameters:
    -----------
    cross : array
        Intensity of Cross-Polarization channel
    co : array
        Intensity of Co-Polarization channel
    background_window_shape : (int, int)
        Size in pixel of the background used to calculate statistic of the scene
    guard_window_shape : (int, int) 
        Size in pixel of the guard Window around the Cell under Test
    target_window_shape : (int, int)
        Size in pixel of the cell under test

    Returns:
    --------
    lam : array
        Depolarisation Ratio multiplyed with Cross-Polarization Intensity
    '''
    if target_window_shape[0]==1 and target_window_shape[1]==1:
        crossTest=cross
    else:
        filterTest=np.ones(target_window_shape)
        filterTest=filterTest/np.sum(filterTest)
        crossTest=convolve2D(cross,filterTest)
    
    filterTrain=create_guard_filter(background_window_shape,guard_window_shape)
    paddedImageShape=(cross.shape[0]+background_window_shape[0],cross.shape[1]+background_window_shape[1])
    kernel=create_kernel(filterTrain,paddedImageShape)
    crossTrain=convolve2D(cross,kernel,kernel_is_fft=True)
    coTrain=convolve2D(co,kernel,kernel_is_fft=True)
    lam=((crossTest-crossTrain)/coTrain)*cross
    return lam

def Co_DePolRAD(cross, co,  guard_window_shape=(30,30), background_window_shape=(100,100),target_window_shape=(1,1)):
    ''' 
    Depolarization Ratio Anomaly Detector according to [1]

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
    if target_window_shape[0]==1 and target_window_shape[1]==1:
        coTest=co
    else:
        filterTest=np.ones(target_window_shape)
        filterTest=filterTest/np.sum(filterTest)
        coTest=convolve2D(co,filterTest)
    
    filterTrain=create_guard_filter(background_window_shape,guard_window_shape)
    paddedImageShape=(cross.shape[0]+background_window_shape[0],cross.shape[1]+background_window_shape[1])
    kernel=create_kernel(filterTrain,paddedImageShape)
    crossTrain=convolve2D(cross,kernel,kernel_is_fft=True)
    coTrain=convolve2D(co,kernel,kernel_is_fft=True)
    lam=((coTest-coTrain)/crossTrain)*co
    return lam

def NIS (image, target_window_shape=(1,1), guard_window_shape=(30,30), background_window_shape=(100,100), padding='refelct'):
    """ 
    This functions applys the Normalised Intensity Sum to the image.

    Parameters:
    -----------
    image : numpy array
        Image array of intensities with opencv ordering (width, height, band)
    target_window_shape: (int,int)
        Size in pixel of the cell under test
    guard_window_shape: (int,int) 
        Size in pixel of the guard Window around the Cell under Test
    background_window_shape: (int,int)
        Size in pixel of the background used to calculate statistic of the scene
    padding: str
        padding method apllied to image

    Returns:
    --------
    filtered : array
        filtered one channel image (width, height)
    """
    bands = image.shape[2]
    filtered=np.zeros((image.shape[0],image.shape[1]))
    for band in range(bands):
        mean=stats_guard(image[...,band],target_window_shape,guard_window_shape,background_window_shape, padding)
        mean=np.where(mean==0, np.nan, mean)
        filtered=filtered+(image[...,band]/mean)
    return filtered