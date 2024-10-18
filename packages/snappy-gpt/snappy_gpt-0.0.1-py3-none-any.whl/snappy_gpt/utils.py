from esa_snappy import WKTReader, jpy, ProductIO, Rectangle,  PixelPos, GeoPos
import numpy as np
from shapely.geometry import Point, box
from shapely.ops import transform
from pyproj import Transformer

def read(filename):
    return ProductIO.readProduct(filename)

def write(product, filename, format='BEAM-DIMAP'):
    ProductIO.writeProduct(product, filename, format)

def read_subset(filename, wellKnownText):
    p=ProductIO.readProduct(filename)
    return subset(p,wellKnownText)

def distance(lon1, lat1, lon2, lat2):
    point1=Point(lon1,lat1)
    point2=Point(lon2,lat2)
    epsg=find_epsg((lon1+lon2)/2,(lat1+lat2)/2)
    transformer=Transformer.from_crs('EPSG:4326',epsg).transform
    point1=transform(transformer,point1)
    point2=transform(transformer,point2)
    return point1.distance(point2)

def point2polygon(wellKnownText, border=0.05):
    g=WKTReader().read(wellKnownText)
    crd=g.getCoordinate()
    x=crd.x
    y=crd.y
    lon_max=x+border
    lon_min=x-border
    lat_max=y+border
    lat_min=y-border
    return f"POLYGON(({lon_max} {lat_max}, {lon_min} {lat_max}, {lon_min} {lat_min}, {lon_max} {lat_min}, {lon_max} {lat_max}))"

def bounding_box(lon, lat, size):
    half_size=size/2
    point=Point(lon,lat)
    epsg=find_epsg(lon,lat)
    transformer=Transformer.from_crs('EPSG:4326',epsg).transform
    point=transform(transformer,point)
    x=point.x
    y=point.y
    bb=box(x-half_size,y-half_size,x+half_size,y+half_size)
    transformer=Transformer.from_crs(epsg, 'EPSG:4326')
    bb=transform(transformer,bb)
    return bb.wkt

def find_epsg(lon, lat):
        """
        Find suitable 2D cartesian coordinate system in transversal mercator projection

        Parameter:
        ----------
        lon : float
            longitude (x-axes)
        lat : float
            latitude (y-axes)
        """
        epsg = ""
        if lat >= 0:
            epsg = "EPSG:326"
        else:
            epsg = "EPSG:327"

        if lon >= 0:
            epsg = epsg+f'{31+int(lon/6)}'
        else:
            zone = 30 + int(lon/6)
            if zone < 10:
                epsg = epsg+'0'
            epsg = epsg+f'{zone}'
        return epsg


def point2rectangle(wellKnownText):
    g=WKTReader().read(wellKnownText)
    crd=g.getCoordinate()
    x=crd.x+0.1
    y=crd.y+0.1
    return Rectangle(x,y,0.1,0.1)

def subset(product, region):
    subsetOP=jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
    op=subsetOP()
    if type(region)==str:
        g=WKTReader().read(region)
        op.setGeoRegion(g)
    else:
        region=[int(r) for r in region]
        x,y,w,h=region
        r=Rectangle(x,y,w,h)
        op.setRegion(r)

    op.setSourceProduct(product)
    op.setCopyMetadata(True)

    return op.getTargetProduct()


def read_to_array(product, band_names=None, x=0, y=0, width=None, height=None):
    ''' 
    Read all bands of a product into a numpy array
    
    Parameters:
    -----------
    product : org.esa.snap.core.datamodel.Product
        Esa snap product that needs to be read into a numpy array
    band_names : [str]
        band names to be read
        Default: all bands
    x : int
        x-Position of the upper left corner
        Default 0
    y : int
        y-Position of the upper left corner
        Default 0
    width : int
        width of the extracted image. If None the remaining width is used.
        Default None
    height : int
        height of the extracted image. If None the remeining height is used. 

    Returns:
    --------
    image : array
        product as numpy array of shape (width, height, bands)
    '''
    if band_names == None:
        band_names = list(product.getBandNames())
    elif type(band_names) == str:
        band_names=[band_names]

    if width==None or width+x>product.getSceneRasterWidth():
        width = product.getSceneRasterWidth()-x

    if height==None or height+y>product.getSceneRasterHeight():
        height = product.getSceneRasterHeight()-y
    
    if len(band_names)==1:
        image=np.zeros((height,width),np.float32)
        try:
            image=product.getBand(band_names[0]).readPixels(x,y,width,height,image)
        except:
            return None
    else:
        image=np.zeros((height,width,len(band_names)),np.float32)
        band=np.zeros((height,width),np.float32)
        for idx, bandName in enumerate(band_names):
            try:
                band=product.getBand(bandName).readPixels(x,y,width,height,band)
            except:
                return None
            image[...,idx]=band

    return image

def read_grid_tie_point_to_array(product,grid_name,x=0,y=0,width=None,height=None):
    if width==None or width+x>product.getSceneRasterWidth():
        width = product.getSceneRasterWidth()-x

    if height==None or height+y>product.getSceneRasterHeight():
        height = product.getSceneRasterHeight()-y
    grid=np.zeros((width,height))
    grid=product.getTiePointGrid(grid_name).readPixels(x,y,width,height,grid)
    return np.reshape(grid,(width,height))
    

def read_C2_to_array(C2_product, x=0, y=0, width=None, height=None):

    if width==None or width+x>C2_product.getSceneRasterWidth():
        width = C2_product.getSceneRasterWidth()-x
    if height==None or height+y>C2_product.getSceneRasterHeight():
        height = C2_product.getSceneRasterHeight()-y
    c2=np.zeros((height,width,3),dtype=np.complex)
    temp=np.zeros((height,width))
    temp=C2_product.getBand('C11').readPixels(x,y,width,height,temp)
    c2[...,0]=temp
    temp=C2_product.getBand('C22').readPixels(x,y,width,height,temp)
    c2[...,1]=temp
    temp=C2_product.getBand('C12_real').readPixels(x,y,width,height,temp)
    c2[...,2].real=temp
    temp=C2_product.getBand('C12_imag').readPixels(x,y,width,height,temp)
    c2[...,2].imag=temp
    return c2

def getGeoPos(source,x,y):
    if str(type(source))=="<class 'org.esa.snap.core.datamodel.GeoCoding'>":
        gc=source
    if str(type(source))=="<class 'org.esa.snap.core.datamodel.Product'>":
        gc=source.getSceneGeoCoding()
    pp=PixelPos(x,y)
    gp=GeoPos()
    gc.getGeoPos(pp,gp)
    return (gp.lon, gp.lat)

def getPixelPos(source,lon,lat):
    if str(type(source))=="<class 'org.esa.snap.core.datamodel.GeoCoding'>":
        gc=source
    if str(type(source))=="<class 'org.esa.snap.core.datamodel.Product'>":
        gc=source.getSceneGeoCoding()
    pp=PixelPos()
    gp=GeoPos(lat,lon)
    gc.getPixelPos(gp,pp)
    return (pp.x, pp.y)
