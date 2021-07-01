import pandas as pd 
import glob 


def toFile(folder,outputFile):
    allFiles = glob.glob(folder+"/*.gz.parquet")
    dfList = []
    for file in allFiles:
        df = pd.read_parquet(file)
        dfList.append(df)

    frame = pd.concat(dfList, axis=0, ignore_index=True) 
    frame = frame.sort_values(by=['timestamp'])
    frame.to_csv(outputFile,index=False)


if __name__ == '__main__':
    pathProd = './CosyGrid.CosyGrid_Electrical_Meter_Readings_Production' 
    fileProd = 'CosyGrid_Electircal_Meter_Readings_Production.csv'

    pathMain = './CosyGrid.CosyGrid_Electrical_Meter_Readings_Mains'
    fileMain = 'CosyGrid_Electircal_Meter_Readings_Mains.csv'

    toFile(pathProd,fileProd)
    toFile(pathMain,fileMain)