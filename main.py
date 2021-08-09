import pandas as pd 
import glob 

### toFile ###
# This function converts the multiple parquet files into 
# a single csv file 
# Inputs:
#   folder     - The location of the folder containing the parquet files to be combined 
#   outputFile - The location of the csv output file which contains the combined parquet data 
#   sort       - If set to true and a timestamp column exists it will sort the readings, should be used with meter readings 
def toFile(folder,outputFile,sort=False):
    allFiles = glob.glob(folder+"/*.gz.parquet")
    dfList = []
    for file in allFiles:
        df = pd.read_parquet(file)
        dfList.append(df)

    frame = pd.concat(dfList, axis=0, ignore_index=True) 
    if sort ==True:
        frame = frame.sort_values(by=['timestamp'])
    frame.to_csv(outputFile,index=False)


# Script starts here 
if __name__ == '__main__':
    # ****YOU MAY NOT HAVE THESE FILES, COMMENT THEM OUT IF NOT AND SELECT WHICH FILES YOU WANT TO CONVERT TO CSV****#
    pathProd  = './CosyGrid.CosyGrid_Electrical_Meter_Readings_Production' 
    fileProd  = 'CosyGrid_Electircal_Meter_Readings_Production.csv'

    pathMain  = './CosyGrid.CosyGrid_Electrical_Meter_Readings_Mains'
    fileMain  = 'CosyGrid_Electircal_Meter_Readings_Mains.csv'

    # Call the functions for different inputs,
    # again edit this for your files 
    toFile(pathProd,fileProd,True)
    toFile(pathMain,fileMain,True)