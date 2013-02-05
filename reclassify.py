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
print xBSize,yBSize

originX = geotransform[0]
originY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]

# Setup output
driver = gdal.GetDriverByName('GTiff')
outDataset = driver.Create(output_file, xsize, ysize, 1, GDT_Float32)
outBand = outDataset.GetRasterBand(1)

#outBand.GetStatistics(0,1)

# loop through the rows
# for i in range(0, rows, yBSize):
#     if i + yBSize < rows:
#         numRows = yBSize
#     else:
#         numRows = rows - i
    # loop throough the columns
    # for j in (0, cols, xBSize):
    #     if j + xBSize < cols:
    #         numCols = xBSize
    #     else:
    #         numCols = cols - j
    #     # Read the data and do the work
    #     data = band.ReadAsArray(j, i, numCols, numRows)
    #     data = data.astype(numpy.float)
    #     outData = numpy.where(numpy.greater(data, 0) & numpy.less_equal(data,67.5),1 ,0)

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

#Reading the raster values using numpy

      
# #Now that the raster is into an array, let's classify it 
# out_str = ''  
# for value in values:  
#     index = 0
#     previous_cl_value = 0
#     for cl_value in classification_values:  
#         if value <= cl_value and value >= previous_cl_value:  
#             out_str = out_str + struct.pack('B',classification_output_values[index])  
#             break  
#         index = index + 1  
# #Once classified, write the output raster  
# #In the example, it's not possible to use the same output format than the input file, because GDAL is not able to write this file format. Geotiff will be used instead  
# gtiff = gdal.GetDriverByName('GTiff')   
# output_dataset = gtiff.Create(output_file, xsize, ysize, 4)  

      
# output_dataset.GetRasterBand(1).WriteRaster( 0, 0, xsize, ysize, out_str )   
# output_dataset = None  
endTime = time.time()
print 'The script tool ' + str(endTime - startTime) + ' seconds.'
