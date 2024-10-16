# -*- coding: future_fstrings -*-
# This file containt the actual functions. It is these that are imported into pyFAT
from astropy.io import fits
from astropy.wcs import WCS
from scipy import ndimage

import copy
import os
import numpy as np
import warnings

class InputError(Exception):
    pass



def print_log(log_statement,log=False):
    if log:
        return log_statement
    else:
        print(log_statement)
        return ''

# Extract a PV-Diagrams
def extract_pv(filename = None,cube= None, overwrite = False,cube_velocity_unit= None,log = False,\
        map_velocity_unit = None,\
        PA=0.,center= [None, None, None],finalsize=None,convert=-1,restfreq = None,silent=False,velocity_type= None,\
        output_directory = None,output_name =None,debug =False, spectral_frame= None, carta=False):
    log_statement = ''
   
    if finalsize is None:
        finalsize=[-1,-1]
   
    if not output_directory:
        output_directory= f'{os.getcwd()}'
   
    close = False
    if filename == None and cube == None:
        raise InputError("EXTRACT_PV: You need to give us something to work with.")
    elif not filename is None and not cube is None:
        raise InputError("EXTRACT_PV: Give us a cube or a file but not both.")
    
    if not filename is None:
        cube = fits.open(filename)
        close = True
    if cube_velocity_unit:
        if 'CUNIT3' in cube[0].header:
            if cube[0].header['CUNIT3'].lower().strip() in ['m/s','km/s'] and \
                cube_velocity_unit.lower().strip() in ['m/s','km/s']:
                pass
            elif cube[0].header['CUNIT3'].lower().strip() != cube_velocity_unit.lower().strip():
                raise InputError(f"The cube velocity units {cube[0].header['CUNIT3'].lower().strip()} do not match your input {cube_velocity_unit}.")
        else:
           cube[0].header['CUNIT3'] = cube_velocity_unit 
    else:
        if 'CUNIT3' in cube[0].header:
            cube_velocity_unit = cube[0].header['CUNIT3']
        else:
            log_statement += print_log(f"We have no velocity units for your cube. \n",log)  
    if map_velocity_unit is None:
        map_velocity_unit = cube[0].header['CUNIT3']     
    if not velocity_type is None:
        cube[0].header['CTYPE3'] = velocity_type
    

    log_statement += print_log(f'''EXTRACT_PV: We are starting the extraction of a PV-Diagram
{'':8s} PA = {PA}
{'':8s} center = {center}
{'':8s} finalsize = {finalsize}
{'':8s} convert = {convert}
''', log)

    hdr = copy.deepcopy(cube[0].header)
    TwoD_hdr= copy.deepcopy(cube[0].header)
    data = copy.deepcopy(cube[0].data)
    #Because astro py is even dumber than Python
  
    if hdr['CUNIT3'].lower() == 'km/s' and cube_velocity_unit.lower().strip() == 'm/s':
        hdr['CUNIT3'] = 'm/s'
        hdr['CDELT3'] = hdr['CDELT3']*1000.
        hdr['CRVAL3'] = hdr['CRVAL3']*1000.
    elif hdr['CUNIT3'].lower() == 'm/s' and cube_velocity_unit.lower().strip() == 'km/s': 
        hdr['CUNIT3'] = 'km/s'
        hdr['CDELT3'] = hdr['CDELT3']/1000.
        hdr['CRVAL3'] = hdr['CRVAL3']/1000.
       

   
    if all(x is None for x in center):
        center = [hdr['CRVAL1'],hdr['CRVAL2'],hdr['CRVAL3']]
        xcenter,ycenter,zcenter = hdr['CRPIX1'],hdr['CRPIX2'],hdr['CRPIX3']
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            coordinate_frame = WCS(hdr)        
        xcenter,ycenter,zcenter = coordinate_frame.wcs_world2pix(center[0], center[1], center[2], 1.)
    log_statement +=  print_log(f'''EXTRACT_PV: We get these pixels for the center,
xcenter={xcenter}, ycenter={ycenter}, zcenter={zcenter}              
''', log)
    nz, ny, nx = data.shape
    if finalsize[0] != -1:
        if finalsize[1] >nz:
            finalsize[1] = nz
        if finalsize[0] > nx:
            finalsize[0] = nx
    # if the center is not set assume the crval values

    log_statement += print_log(f'''EXTRACT_PV: The shape of the output
{'':8s} nz = {nz}
{'':8s} ny = {ny}
{'':8s} nx = {nx}
''', log)
   
    x1,x2,y1,y2 = obtain_border_pix(PA,[xcenter,ycenter],[hdr['NAXIS1'],hdr['NAXIS2']])
    
    linex,liney,linez = np.linspace(x1,x2,nx), np.linspace(y1,y2,nx), np.linspace(0,nz-1,nz)

    #We need to find our center in these coordinates
    if x1 > x2 and y1 > y2:
        offset = [(xcenter-x+ycenter-y) for x,y in zip (linex,liney)]
    elif x1 < x2 and y1 > y2:
        offset = [(x-xcenter+ycenter-y) for x,y in zip (linex,liney)]
    elif x1 > x2 and y1 < y2:
        offset = [(xcenter-x+y-ycenter) for x,y in zip (linex,liney)]
    else:
        offset = [(x-xcenter+y-ycenter) for x,y in zip (linex,liney)]
    #for i in range(len(linex)):
    #    print(f'{linex[i]} {i} {xcenter}  {liney[i]} {ycenter} {offset[i]}')
    offset_abs = [abs(x) for x in offset]
    if not np.isnan(np.nanmin(offset_abs)):
        centralpix = offset_abs.index(np.nanmin(offset_abs))
    else:
        log_statement += print_log(f'''EXTRACT_PV: all our offset values are NaN
''', log)
        raise InputError(f'EXTRACT_PV: all our offset values are NaN')

    if offset[centralpix] > 0:
        xc1 =  centralpix-1
        yc1 = offset[centralpix-1]
        xc2 = centralpix
        yc2 = offset[centralpix]
    else:
        xc1 = centralpix
        yc1 = offset[centralpix]
        xc2 = centralpix+1
        yc2 = offset[centralpix+1]
  
    xcen = xc1+(xc2-xc1)*(-yc1/(yc2-yc1))
    #if PA < 180.:
    if y1 > y2:
        xcen= nx-xcen
  


    #This only works when ny == nx hence nx is used in liney
    new_coordinates = np.array([(z,y,x)
                        for z in linez
                        for y,x in zip(liney,linex)
                        ],dtype=float).transpose().reshape((-1,nz,nx))
    #spatial_resolution = abs((abs(x2-x1)/nx)*np.sin(np.radians(angle)))+abs(abs(y2-y1)/ny*np.cos(np.radians(angle)))
    PV = ndimage.map_coordinates(data, new_coordinates,order=1)
    if hdr['CDELT1'] < 0:
        PV = PV[:,::-1]

    if finalsize[0] == -1:
        # then lets update the header
        # As python is stupid making a simple copy will mean that these changes are still applied to hudulist
        TwoD_hdr['NAXIS2'] = nz
        TwoD_hdr['NAXIS1'] = nx

        TwoD_hdr['CRPIX2'] = hdr['CRPIX3']
        TwoD_hdr['CRPIX1'] = xcen
    else:
        zstart = set_limits(int(zcenter-finalsize[1]/2.),0,int(nz))
        zend = set_limits(int(zcenter+finalsize[1]/2.),0,int(nz))
        xstart = set_limits(int(xcen-finalsize[0]/2.),0,int(nx))
        xend = set_limits(int(xcen+finalsize[0]/2.),0,int(nx))

        PV =  PV[zstart:zend, xstart:xend]
        TwoD_hdr['NAXIS2'] = int(finalsize[1])
        TwoD_hdr['NAXIS1'] = int(finalsize[0])
        TwoD_hdr['CRPIX2'] = hdr['CRPIX3']-int(nz/2.-finalsize[1]/2.)
        TwoD_hdr['CRPIX1'] = xcen-xstart


    TwoD_hdr['CRVAL2'] = hdr['CRVAL3']
    TwoD_hdr['CDELT2'] = hdr['CDELT3']
    TwoD_hdr['CTYPE2'] = hdr['CTYPE3']
    TwoD_hdr['CUNIT2'] = hdr['CUNIT3']
    
    if hdr['CUNIT3'].lower() == 'm/s' and map_velocity_unit.lower() == 'km/s':
        TwoD_hdr['CDELT2'] = hdr['CDELT3']/1000.
        TwoD_hdr['CRVAL2'] = hdr['CRVAL3']/1000.
        TwoD_hdr['CUNIT2'] = 'km/s'
    elif hdr['CUNIT3'].lower() == 'km/s' and map_velocity_unit.lower() == 'm/s':
        TwoD_hdr['CDELT2'] = hdr['CDELT3']*1000.
        TwoD_hdr['CRVAL2'] = hdr['CRVAL3']*1000.
        TwoD_hdr['CUNIT2'] = 'm/s'


    if convert != -1:
        TwoD_hdr['CDELT2'] = hdr['CDELT3']*convert
        TwoD_hdr['CRVAL2'] = hdr['CRVAL3']*convert
        TwoD_hdr['CUNIT2'] = map_velocity_unit
    
    del (TwoD_hdr['CUNIT3'])
    del (TwoD_hdr['CRPIX3'])
    del (TwoD_hdr['CRVAL3'])
    del (TwoD_hdr['CDELT3'])
    del (TwoD_hdr['CTYPE3'])
    del (TwoD_hdr['NAXIS3'])
    #del (TwoD_hdr['EPOCH'])

    TwoD_hdr['NAXIS'] = 2
    TwoD_hdr['CRVAL1'] = 0.
    #Because we used nx in the linspace for liney we also use it here
    TwoD_hdr['CDELT1'] = np.sqrt(((x2-x1)*abs(hdr['CDELT1'])/nx)**2+((y2-y1)*abs(hdr['CDELT2'])/nx)**2)*3600.
    TwoD_hdr['CTYPE1'] = 'OFFSET'
    TwoD_hdr['CUNIT1'] = 'arcsec'
    TwoD_hdr['HISTORY'] = f'EXTRACT_PV: PV diagram extracted with angle {PA} and center {center}'
    # Ensure the header is Carta compliant
    if 'RESTFRQ' not in TwoD_hdr and 'RESTFREQ' not in TwoD_hdr : 
        if restfreq == None and not silent:
            restfreq = input(f'Please specify the rest frequency of the observation in hz (default = 1.42e9 hz):')
            if restfreq == '':
                restfreq = 1.420405751767E+09
        TwoD_hdr['RESTFRQ'] = restfreq
    elif 'RESTFREQ' in TwoD_hdr:
         TwoD_hdr['RESTFRQ'] = TwoD_hdr['RESTFREQ'] 
         del (TwoD_hdr['RESTFREQ']) 
        
        
    if 'SPECSYS3' in TwoD_hdr:
        TwoD_hdr['SPECSYS2'] =  TwoD_hdr['SPECSYS3']
        #TwoD_hdr['SPECSYS'] =  TwoD_hdr['SPECSYS3']
        del (TwoD_hdr['SPECSYS3'])
    elif 'SPECSYS' in TwoD_hdr:
        TwoD_hdr['SPECSYS2'] =  TwoD_hdr['SPECSYS'] 
        del (TwoD_hdr['SPECSYS'])
    else:
        if spectral_frame == None and not silent:
            spectral_frame  = input(f'Please specify the spectral_frame of the observation (default = BARYCENT):')
            if spectral_frame  == '':
                spectral_frame  = 'BARYCENT'
        TwoD_hdr['SPECSYS2'] = spectral_frame
    spectral_frame = TwoD_hdr['SPECSYS2']
    
    if carta and TwoD_hdr['CTYPE2'] != 'FREQ' :    
        #As carta is not fits standard compliant  and generally ridiculous there are a set of ridicul;ous demands on viewing the coordinate system
        # it wants a specsys even though fits standard says this is a axis specific keyword
        TwoD_hdr['SPECSYS'] = TwoD_hdr['SPECSYS2']

        # Needs the the spectral axis in frequency even when the original axis is in velocity which is simply ridiculous
        if restfreq == None:
            restfreq = 1.420405751767E+09
        c=299792458 # In meter/s
        if  TwoD_hdr['CUNIT2'].lower() == 'km/s':
            c = c/1000.
        if  TwoD_hdr['CTYPE2'] == 'VRAD':
            TwoD_hdr['CDELT2'] = -restfreq * float(TwoD_hdr['CDELT2']) / c 
            TwoD_hdr['CRVAL2'] = restfreq * \
                (1 - float(TwoD_hdr['CRVAL2']) / c)
       
        else:
            log_statement += print(f'As only the radio definition leads to equal increments in frequency we dont know how to make your PV-Diagram compliant. \n')
        TwoD_hdr['CUNIT2'] = 'hz'
        #TwoD_hdr['SPECSYS'] = 'FREQ'
        TwoD_hdr['CTYPE2'] = 'FREQ'
       
    if close:
        cube.close()

    if not output_name is None:
        fits.writeto(f"{output_directory}/{output_name}_PV.fits",PV,TwoD_hdr,overwrite = overwrite)
    else:
        PV_diagram = copy.deepcopy(cube)
        PV_diagram[0].data = PV
        PV_diagram[0].header = TwoD_hdr
        if log:
            return PV_diagram,log_statement
        else:
            return PV_diagram
   
    if log:
        return log_statement

extract_pv.__doc__ = '''
 NAME:
    extract_pv

 PURPOSE:
    extract a PV diagram from a cube object. Angle is the PA and center the central location. The profile is extracted over the full length of the cube and afterwards cut back to the finalsize.

 CATEGORY:
     fits_functions

 INPUTS:
    Configuration = Standard FAT Configuration
    cube_in = is a fits cube object
    angle = Pa of the slice

 OPTIONAL INPUTS:
    center = [-1,-1,-1]
    the central location of the slice in WCS map_coordinates [RA,DEC,VSYS], default is the CRVAL values in the header

    finalsize = [-1,-1,-1]
    final size of the PV-diagram in pixels, default is no cutting

    convert=-1
    conversion factor for velocity axis, default no conversion

 KEYWORD PARAMETERS:

 OUTPUTS:

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''



def moments(filename = None, cube = None, mask = None, moments = None,overwrite = False,\
            level=None,cube_velocity_unit= None, map_velocity_unit= None,\
            threshold = 3.,debug = False, log=False,output_directory = None,output_name =None):
    log_statement = ''
    log_statement += print_log(f'''MOMENTS: We are starting to create the moment maps.
''',log)
    if moments is None:
        moments = [0,1,2]  
    if not mask and not level and not threshold:
        InputError("MOMENTS: Moments requires a threshold (sigma), level (units of input cube) or a mask. ")
    close = False
    if filename == None and cube == None :
        InputError("MOMENTS: There is no default for filename, it needs be sets to the input cube fits file or cube to an astropy construct.")
    elif filename != None and cube != None :
        InputError("MOMENTS: Give us a cube or a file but not both.")
    elif filename != None:
        cube = fits.open(filename)
        close = True

    if output_directory is None:
        output_directory= f'{os.getcwd()}'
   
    if cube_velocity_unit is None:
        if 'CUNIT3' not in cube[0].header:
            raise InputError(f"MOMENTS: Your CUNIT3 is missing, that is bad practice. You can use moments by setting cube_velocity_unit")
        else:
            cube_velocity_unit = cube[0].header['CUNIT3']
    else: 
        if 'CUNIT3' not in cube[0].header:
            cube[0].header['CUNIT3'] = cube_velocity_unit
        elif cube[0].header['CUNIT3'] != cube_velocity_unit:
            raise InputError(f"You're input  cube velocity unit and the unit of the cube do not match.")  
    if mask:
        if isinstance(mask,str): 
            mask_cube = fits.open(mask)
        else:
            mask_cube = mask 
        if len(np.where(mask_cube[0].data > 0.5)[0]) < 1:
           raise InputError(f'We expect mask values to start at 1 your mask has no values above 0.5')

        if mask_cube[0].header['NAXIS1'] != cube[0].header['NAXIS1'] or \
           mask_cube[0].header['NAXIS2'] != cube[0].header['NAXIS2'] or \
           mask_cube[0].header['NAXIS3'] != cube[0].header['NAXIS3']:
           raise InputError(f'Your mask {mask_cube} and cube {filename} do not have the same dimensions')
        with np.errstate(invalid='ignore', divide='ignore'):
            cube[0].data[mask_cube[0].data < 0.5] = float('NaN')
        mask_cube.close()
    else:
        if level is None:
            level = threshold*np.mean([np.nanstd(cube[0].data[0:2,:,:]),np.nanstd(cube[0].data[-3:-1,:,:])])
        with np.errstate(invalid='ignore', divide='ignore'):
            cube[0].data[cube[0].data <= level] = float('NaN')
    try:
        if map_velocity_unit is not None:
            if cube[0].header['CUNIT3'].lower().strip() == 'm/s' and map_velocity_unit.lower().strip() == 'km/s':
                log_statement += print_log(f"MOMENTS: We convert your m/s to km/s. \n",log)
                cube[0].header['CUNIT3'] = 'km/s'
                cube[0].header['CDELT3'] = cube[0].header['CDELT3']/1000.
                cube[0].header['CRVAL3'] = cube[0].header['CRVAL3']/1000.
            elif cube[0].header['CUNIT3'].lower().strip() == 'km/s' and map_velocity_unit.lower().strip() == 'm/s' :
                log_statement += print_log(f"MOMENTS: We convert your km/s to m/s. \n",log)
                cube[0].header['CUNIT3'] = 'm/s'
                cube[0].header['CDELT3'] = cube[0].header['CDELT3']*1000.
                cube[0].header['CRVAL3'] = cube[0].header['CRVAL3']*1000.
            else:
                if cube_velocity_unit.lower().strip() != map_velocity_unit.lower().strip():
                    raise InputError(f'We do not know how to convert from {cube_velocity_unit} to {map_velocity_unit}')
    except KeyError:
        log_statement += print_log(f"MOMENTS: Your CUNIT3 is missing, that is bad practice. You can run make moments by setting cube_velocty_unit.", log)
        cube[0].header['CUNIT3'] = 'Unknown'
    #Make a 2D header to use
    hdr2D = copy.deepcopy(cube[0].header)
    hdr2D.remove('NAXIS3')
    hdr2D['NAXIS'] = 2
    # removing the third axis means we cannot correct for varying platescale, Sofia does so this is and issue so let's not do this
    hdr2D.remove('CDELT3')
    hdr2D.remove('CTYPE3')
    hdr2D.remove('CUNIT3')
    hdr2D.remove('CRPIX3')
    hdr2D.remove('CRVAL3')
    moment_maps = []
    # we need a moment 1  for the moment 2 as well
    if 0 in moments:
        log_statement += print_log(f"MOMENTS: Creating a moment 0. \n", log)
        hdr2D['BUNIT'] = f"{cube[0].header['BUNIT']}*{cube[0].header['CUNIT3']}"
        moment0 = np.nansum(cube[0].data, axis=0) * abs(cube[0].header['CDELT3'])
        moment0[np.invert(np.isfinite(moment0))] = float('NaN')
        try:
            hdr2D['DATAMAX'] = np.nanmax(moment0)
            hdr2D['DATAMIN'] = np.nanmin(moment0)
            if not output_name is None:
                fits.writeto(f"{output_directory}/{output_name}_mom0.fits",moment0,hdr2D,overwrite = overwrite)
            else:
                mom0 = copy.deepcopy(cube)
                mom0[0].header=hdr2D
                mom0[0].data=moment0
                moment_maps.append(mom0)
        except ValueError:
            log_statement += print_log(f"MOMENTS: Your Moment 0 has bad data and we could not write the moment 0 fits file. \n", log)
            raise  InputError(f'Something went wrong in the moments module')

   
    
    if 1 in moments or 2 in moments:
        log_statement += print_log(f"MOMENTS: Creating a moment 1. \n", log)
        zaxis = cube[0].header['CRVAL3'] + (np.arange(cube[0].header['NAXIS3'])+1 \
              - cube[0].header['CRPIX3']) * cube[0].header['CDELT3']
        c=np.transpose(np.resize(zaxis,[cube[0].header['NAXIS1'],cube[0].header['NAXIS2'],len(zaxis)]),(2,1,0))
        hdr2D['BUNIT'] = f"{cube[0].header['CUNIT3']}"
        # Remember Python is stupid so z,y,x
        with np.errstate(invalid='ignore', divide='ignore'):
            moment1 = np.nansum(cube[0].data*c, axis=0)/ np.nansum(cube[0].data, axis=0)
        moment1[np.invert(np.isfinite(moment1))] = float('NaN')
        try:
            hdr2D['DATAMAX'] = np.nanmax(moment1)
            hdr2D['DATAMIN'] = np.nanmin(moment1)
            if 1 in moments:
                if not output_name is None:
                    fits.writeto(f"{output_directory}/{output_name}_mom1.fits",moment1,hdr2D,overwrite = overwrite)
                else:
                    mom1 = copy.deepcopy(cube)
                    mom1[0].header=hdr2D
                    mom1[0].data=moment1
                    moment_maps.append(mom1)
  
        except ValueError:
            log_statement += print_log(f"MOMENTS: Your Moment 1 has bad data and we could not write the moment 1 fits file. \n", log)
            raise  InputError(f'Something went wrong in the moments module')

        if 2 in moments:
            log_statement += print_log(f"MOMENTS: Creating a moment 2. \n", log)
            d = c - np.resize(moment1,[len(zaxis),cube[0].header['NAXIS2'],cube[0].header['NAXIS1']])
            with np.errstate(invalid='ignore', divide='ignore'):
                moment2 = np.sqrt(np.nansum(cube[0].data*d**2, axis=0)/ np.nansum(cube[0].data, axis=0))
            moment2[np.invert(np.isfinite(moment1))] = float('NaN')
            try: 
                hdr2D['DATAMAX'] = np.nanmax(moment2)
                hdr2D['DATAMIN'] = np.nanmin(moment2)
                if not output_name is None:
                    fits.writeto(f"{output_directory}/{output_name}_mom2.fits",moment2,hdr2D,overwrite = overwrite)
                else:
                    mom2 = copy.deepcopy(cube)
                    mom2[0].header=hdr2D
                    mom2[0].data=moment2
                    moment_maps.append(mom2)
            except ValueError:
                log_statement += print_log(f"MOMENTS: Your Moment 2 has bad data and we could not write the moment 2 fits file. \n", log)
                raise  InputError(f'Something went wrong in the moments module')

    log_statement += print_log(f"MOMENTS: Finished moments.\n", log)
    if close:
        cube.close()
  
    if output_name is None:
        if log:
            return moment_maps,log_statement
        else:
            return moment_maps
    if log:
        return log_statement

moments.__doc__ =f'''
 NAME:
    make_moments

 PURPOSE:
    Make the moment maps

 CATEGORY:
    Spectral line cube manipulations.

 INPUTS:
    filename = input file name


 OPTIONAL INPUTS:
    mask = name of the cube to be used as a mask

    debug = False

    moments = [0,1,2]
    moment maps to create

    overwrite = False
    overwrite existing maps

    level=None
    cutoff level to use, if set the mask will not be used

    cube_velocity_unit= none
    velocity unit of the input cube

    map_velocity_unit= none
    velocity unit of the output maps

    threshold = 3.
    Cutoff level in terms of sigma, if used the std in in the first two and last channels in the cube is measured and multiplied.

    log = None
    Name for a logging file

    output_directory = None
    Name of the directory where to put the created maps. If none the current working directory is used.

    output_name = None
    Base name for output maps i.e. maps are output_name_mom#.fits with # number of the moments
    default is filename -.fits

 OUTPUTS:

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''

def obtain_border_pix(angle,center, naxes):
    rotate = False
    # only setup for 0-180 but 180.-360 is the same but -180
    if angle > 180.:
        angle -= 180.
        rotate = True

    if angle < 90.:
        x1 = center[0]-(naxes[1]-center[1])*np.tan(np.radians(angle))
        x2 = center[0]+(center[1])*np.tan(np.radians(angle))
        if x1 < 0:
            x1 = 0
            y1 = center[1]+(center[0])*np.tan(np.radians(90-angle))
        else:
            y1 = naxes[1]
        if x2 > naxes[0]:
            x2 = naxes[0]
            y2 = center[1]-(center[0])*np.tan(np.radians(90-angle))
        else:
            y2 = 0
    elif angle == 90:
        x1 = 0 ; y1 = center[1] ; x2 = naxes[0]; y2 = center[1]
    else:
        x1 = center[0]-(center[1])*np.tan(np.radians(180.-angle))
        x2 = center[0]+(naxes[1]-center[1])*np.tan(np.radians(180-angle))
        if x1 < 0:
            x1 = 0
            y1 = center[1]-(center[0])*np.tan(np.radians(angle-90))
        else:
            y1 = 0
        if x2 > naxes[0]:
            x2 = naxes[0]
            y2 = center[1]+(center[0])*np.tan(np.radians(angle-90))
        else:
            y2 = naxes[1]
    # if the orginal angle was > 180 we need to give the line 180 deg rotation
    x = [x1,x2]
    y = [y1,y2]
    if rotate:
        x.reverse()
        y.reverse()
    return (*x,*y)

obtain_border_pix.__doc__ =f'''
 NAME:
    obtain_border_pix
 PURPOSE:
    Get the pixel locations of where a line across a map exits the map

 CATEGORY:
    support_functions

 INPUTS:
    Configuration = standard FAT Configuration
    hdr = header of the map
    angle = the angle of the line running through the map
    center = center of the line running through the map

 OPTIONAL INPUTS:


 OUTPUTS:
    x,y
    pixel locations of how the line runs through the map

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    np.tan,np.radians,.reverse()

 NOTE:
'''

def set_limits(value,minv,maxv):
    if value < minv:
        return minv
    elif value > maxv:
        return maxv
    else:
        return value

set_limits.__doc__ =f'''
 NAME:
    set_limits
 PURPOSE:
    Make sure Value is between min and max else set to min when smaller or max when larger.
 CATEGORY:
    support_functions

 INPUTS:
    value = value to evaluate
    minv = minimum acceptable value
    maxv = maximum allowed value

 OPTIONAL INPUTS:


 OUTPUTS:
    the limited Value

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''
