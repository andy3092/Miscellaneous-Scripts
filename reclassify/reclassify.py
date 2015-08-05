#! /usr/bin/python  

#Change the value with your raster filename here  
raster_file = 'aspect15m.tif'  
output_file = 'classified.tiff'  

classification_values = [67.5,292.5,360] #The interval values to classify  
classification_output_values = [1,0,1] #The value assigned to each interval  

from osgeo import gdal  
from osgeo.gdalconst import *  
import numpy
import time

# Set the timer
startTime = time.time()
 
#Opening the raster file  
dataset = gdal.Open(raster_file, GA_ReadOnly )  

#Reading the raster properties  
band = dataset.GetRasterBand(1)  
projectionfrom = dataset.GetProjection()  
geotransform = dataset.GetGeoTransform()  
xsize = band.XSize  
ysize = band.YSize  
datatype = band.DataType  

# Get the block size
rows = dataset.RasterYSize
cols = dataset.RasterXSize
blockSizes = band.GetBlockSize()
xBSize =  blockSizes[0]
yBSize = blockSizes[1]

originX = geotransform[0]
originY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]

# Setup output
driver = gdal.GetDriverByName('GTiff')
outDataset = driver.Create(output_file, xsize, ysize, 1, GDT_Float32)
outBand = outDataset.GetRasterBand(1)

#Reading the raster values using numpy
data = band.ReadAsArray(0, 0, cols, rows)
data = data.astype(numpy.float)

# use numpy select to reclassify the image 
outData = numpy.select([data == -9999, (data >= 0) & (data <= 67.5), (data > 67.5) & (data < 292), data >=272],[-9999,1,-9999,1])
outBand.WriteArray(outData, 0, 0)
outBand.FlushCache()
outBand.SetNoDataValue(-9999)

# # Georefrence the image and set the projection
outDataset.SetGeoTransform(geotransform)
outDataset.SetProjection(projectionfrom)  

outBand = None
output_dataset = None  

endTime = time.time()

print 'The script took ' + str(endTime - startTime) + ' seconds.'
