import numpy as np

def create_guard_filter(background_window_shape, guard_window_shape, normalize=True):
    """ 
    Creates rectangle stencil filter:

    |<----background_window_shape---->|
    |111111111111111111111111111111111|
    |111111111111111111111111111111111|
    |111111111111111111111111111111111|
    |11111111111|<-guard->|11111111111|
    |11111111111|000000000|11111111111|
    |11111111111|000000000|11111111111|
    |11111111111|000000000|11111111111|
    |11111111111|---------|11111111111|
    |111111111111111111111111111111111|
    |111111111111111111111111111111111|
    |111111111111111111111111111111111|
    |---------------------------------|

    Prameters:
    ----------
    background_window_shape : (int, int)
        Size in pixel of the background used to calculate statistic of the scene
    guard_window_shape : (int, int) 
        Size in pixel of the guard Window around the Cell under Test

    Returns:
    --------
    filter : numpy array
        filter stencil
    """

    output=np.zeros(guard_window_shape)
    padWidth = pad_width(guard_window_shape,background_window_shape)
    output=np.pad(output,pad_width=padWidth,mode='constant', constant_values=1)
    if normalize:
        output=output/np.sum(output)
    return output

def convolve2D(image, filter,pad_mode='reflect', pad_kwargs=None, kernel_is_fft=False, complex=False):
    ''' 
    Efficiently compute the convolution of an image with a filter using FFT.
    Here the filter in Fourierspace is called kernel.

    Parameters:
    image : array
        Image to be convoluted
    filter : array
        filter for convolution. mu_bst be of smaller size than image.
    pad_mode : str
        pad mode for padding the image with numpy.pad()
    pad_kwargs : dict
        Keywordarguments for padding the image with numpy.pad()
    kernel_is_fft : Bool
        Flag if the 'filter' is already in Fourierspace e.g. is a kernel
        Default: False
    complex : Bool
        Flag if the return should be in complex value or not.
        Default: False        
            
    Returns:
    ---------
    image: array
        filtered image
    '''
    drop=False
    if len(image.shape) != 3:
        image=image[...,np.newaxis]
        drop=True

    if kernel_is_fft:
        padWidthImage=pad_width(image.shape,filter.shape)
        paddedImageShape=(filter.shape[0],filter.shape[1],image.shape[2])
        kernelFFT=filter
    else:
        paddedImageShape=(image.shape[0]+filter.shape[0],image.shape[1]+filter.shape[1],image.shape[2])
        padWidthImage=pad_width(image.shape,paddedImageShape)
        kernelFFT=create_kernel(filter,paddedImageShape)
    
    paddedImage=np.zeros(paddedImageShape,dtype=image.dtype)
    if pad_kwargs:
        for i in range(image.shape[2]):
            paddedImage[...,i] = np.pad(image[...,i],pad_width=padWidthImage,mode=pad_mode, **pad_kwargs)
    else:
        for i in range(image.shape[2]): 
            paddedImage[...,i] = np.pad(image[...,i],pad_width=padWidthImage,mode=pad_mode)
    convolved=np.zeros(paddedImageShape, dtype=np.cdouble)

    for i in range(convolved.shape[2]):
        convolved[...,i]=np.fft.ifft2(np.fft.fft2(paddedImage[...,i])*kernelFFT)
    convolved=convolved[padWidthImage[0][0]:-padWidthImage[0][1],padWidthImage[1][0]:-padWidthImage[1][1]]
    if drop:
        convolved=convolved[...,0]
    if complex:
        return convolved
    else:
        return convolved.real

def create_kernel(filter, image_shape):
    padWidthfilter=pad_width(filter.shape,image_shape)
    paddedfilter=np.pad(filter, pad_width=padWidthfilter)
    return np.fft.fft2(np.fft.fftshift(paddedfilter))

def pad_width(image_shape, target_shape):
    padX, remainder = divmod(target_shape[0]-image_shape[0],2)
    padX=(padX+remainder,padX)
    padY, remainder = divmod(target_shape[1]-image_shape[1],2)
    padY=(padY+remainder,padY)
    return (padX,padY)