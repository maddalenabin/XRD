import numpy as np
import h5py
import fabio
import scipy.fftpack

# file tools
def visit_func(name, node):
    '''
    Return all groups and datasets name and shapes of h5 file called name
    '''
    if isinstance(node, h5py.Group):
        print(node.name)
    elif isinstance(node, h5py.Dataset):
        if (node.dtype == 'object') :
            print (node.name, 'is an object Dataset')
        else:
            print('\t', node.name, node.shape)
    else:
        print(node.name, 'is an unknown type')

def open_sfrm_file(filename, bg_ar):
    '''
    PARAMETERS
    filename = name of the file with the path to it
    bg_ar = 2d array of the background you want to subtract, default no bg
    
    RETURNS
    data_array_with_bg = 2d array with no subtracted bg
    data_ar = 2d array with subtracted bg
    '''
    im = fabio.open(filename)
    data_array_with_bg = np.array(im.data,dtype=float)
    
    # subtract the bg
    data_ar = data_array_with_bg - bg_ar
    return data_array_with_bg, data_ar

# analysis tools from scikit-beam (https://github.com/scikit-beam/scikit-beam/tree/master/skbeam/core)
import skbeam.core.roi as roi
import skbeam.core.utils as utils

def ring_mask(data,center,inner_radius=0,width=1,spacing=0,num_rings=10):
    '''
    Creates a ring mask with cocentric rings of given radius, width and spacing 
    center = (cx, cy)
    '''
    edges = roi.ring_edges(inner_radius, width, spacing, num_rings)
    ring_mask = roi.rings(edges, center, data.shape)

    return ring_mask

def find_local_minima(x,y):
    miny = np.r_[True, y[1:] < y[:-1]] & np.r_[y[:-1] < y[1:],True]
    min_pos = x[miny==True]
    return min_pos

def find_local_maxima(x,y):
    miny = np.r_[True, y[1:] > y[:-1]] & np.r_[y[:-1] > y[1:],True]
    max_pos = x[miny==True]
    return max_pos

def FT_low_pass_filter(x,y, cutoff):
    '''
    FT low pass filter
    '''
    N = len(x)
    w = scipy.fftpack.rfft(y)
    f = scipy.fftpack.rfftfreq(N, x[1]-x[0])
    spectrum = w**2

    cutoff_value = spectrum[1:].max()/cutoff
    cutoff_idx = spectrum < cutoff_value #(spectrum.max()/cutoff)
    w2 = w.copy()
    w2[cutoff_idx] = 0
    spectrum2 = w2**2
    y2 = scipy.fftpack.irfft(w2)

    return y2


def FT_high_pass_filter(x,y, cutoff):
    '''
    FT high pass filter
    '''
    N = len(x)
    w = scipy.fftpack.rfft(y)
    f = scipy.fftpack.rfftfreq(N, x[1]-x[0])
    spectrum = w**2

    cutoff_value = spectrum[1:].max()/cutoff
    cutoff_idx = spectrum > cutoff_value #(spectrum.max()/cutoff)
    w2 = w.copy()
    w2[cutoff_idx] = 0
    spectrum2 = w2**2
    y2 = scipy.fftpack.irfft(w2)

    return y2
    

def beam_blocker_mask(nx=1024, ny=1024, center_x=512, center_y=512, radius=30, radius2=None, slope=0.0007, offset=-5, thickness=15):
    '''
    Masking the beam blocker
    nx,ny =  2d pattern dimensions
    center_x, center_y = center of the beam blocker
    radius = radius of the beam blocker
    radius2 = radius of the externa circle (to avoid dip in the angular average)
    slope = of the beam blocker 'stick'
    offset = with respect to the center
    thickness = of the beam blocker stick
    '''
    mask = np.ones((nx,ny),dtype=bool)

    #disk in the center
    x,y= np.mgrid[0:nx,0:ny]
    x-=center_x
    y-=center_y
    rho = np.sqrt(x**2+y**2)
    mask[rho<radius]=0
    if radius2 != None:
        mask[rho>radius2]=0

    # line
    line1 = (1./slope)*(y+offset)-x
    line2 = line1+(1./slope)*thickness
    line = np.ones((nx,ny),dtype=int)
    line[:center_x,:] = line1[:center_x,:]*line2[:center_x,:]
    mask[line<0]=0
    #print('beam blocker : masked %.2f percent' %(len(mask[mask==0])/float(nx*ny)*100.))

    return mask
    
    
