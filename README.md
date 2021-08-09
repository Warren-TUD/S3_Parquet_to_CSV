# S3 Parquet to CSV 
The purpose of this repository is to convert extracted data from the CosyGrid database from the parquet format to csv. The parquet format is used by AWS as the storage costs are less, 1 TB in CSV format is equal to 130 Gb in parquet format. 

This readme goes through how to get the data from RDS to S3, if you have already done this and have the data on your local machine skip to the section [Converting Parquet to CSV](https://github.com/Warren-TUD/S3_Parquet_to_CSV#converting-parquet-to-csv).

## Exporting the data from the database 
To first get the data from the database a snapshot of the database must be created using the AWS console. A snapshot is like freezing the database at particular point in time.   
To create a snapshot naviagte to the AWS console and then the RDS console https://eu-west-1.console.aws.amazon.com/rds/home. Select the "CosyGrid" database, then the "Actions" dropdown menu and finally select "Take Snapshot". Name the snapshot and it should then appear in the "Snapshots" section of the RDS console. 

Once you have the snapshot you need to export this data to an S3 bucket. There is a guide on how to do this [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ExportSnapshot.html#USER_ExportSnapshot.Overview) and the main steps are listed below. 

Select the snapshot you want to export from the AWS RDS console, select the "Actions" dropdown menu and then the option "Export to Amazon S3". 

Fill in the form requested with an identifier that is unique. The exported data can be the entire database or a "Partial" export. If only meter data is required, select "Partial" and in the text box paste the following. 

**Note the single space between the two elements below sperating them, it is not a line break**
```
CosyGrid.CosyGrid_Electrical_Meter_Readings_Mains CosyGrid.CosyGrid_Electrical_Meter_Readings_Production
```

For the "S3 Destinantion" select ```cosy-grid-database``` if this does not appear in the dropdown you need to request access for it. 

For the IAM Role select ```CosyGridDatabaseExport```. For the "Encryption" select ```CosyGrid-Database-Export``` for the "AWS KMS Key". 

Finally select "Export to Amazon S3". This will take some time depending upon how arge the data exported is, the status of which can be checked in the S3 console [here](https://s3.console.aws.amazon.com/s3/home?region=eu-west-1).

## Exporting the data from AWS S3
Navigate to the S3 console and select the bucket ```cosy-grid-database```. Find the folder with the name of the unique identifier you gave this extraction and select it. 

There should be a folder with the name of the database that you extracted from, in this instace ```CosyGrid```, select this folder. 

At this level each table that has been extracted has its own folder, for example if the meter data was only extracted there would be two folders named ```CosyGrid.CosyGrid_Electrical_Meter_Readings_Mains/``` and ```CosyGrid.CosyGrid_Electrical_Meter_Readings_Production/```. Select the folder with the data you want to extract. 

In this folder are the parquet files with the data in them. There may be multiple parquet files if the table contained a large amount of data or a single parquet file. Select the parquet file which you want to download, and then select "Download" from the actions menu. 

## Exporting the data from AWS S3 using AWS CLI 
This wasy is a lot quicker and involves less steps to get the data in S3 to your local machine. It does involve you setting up the aws cli however, a guide can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Once the AWS Cli is configured, the [S3](https://docs.aws.amazon.com/cli/latest/reference/s3/) commands can be used to interact with the S3 service from your local machine. 

Naviagte to a command line interface and type the following command to list the buckets in s3. 

***DO NOT TYPE $ ONLY WHAT COMES AFTER $***
```
$ aws s3 ls
2021-02-16 10:08:17 Example Bucket A
2021-05-19 13:19:43 cosy-grid-database
2021-02-16 17:16:48 Example Bucket B
2021-06-01 10:27:46 Example Bucket C
```
The ```cosy-grid-database``` bucket should be present as in the output above for the second bucket. The ls option works the same as the [linux ls](https://man7.org/linux/man-pages/man1/ls.1.html) command.  

To see inside the ```cosy-grid-database``` bucket ```ls``` can be used again. 
```
$ aws s3 ls cosy-grid-database
PRE Export_1/
PRE data-only/
PRE Export_2/
PRE Export_3/
```
Keep using the ```ls``` command until you find the file or folder you want to extract. In my case I want to download all the contents from the location ```s3://cosy-grid-database/data-only/CosyGrid/``` whcih contains two folders. The first being  ```CosyGrid.CosyGrid_Electrical_Meter_Readings_Mains``` containing the mains meter readings and the second folder being ```CosyGrid.CosyGrid_Electrical_Meter_Readings_Production``` containing the production readings. 

This can be done using the command below. 
```
$ aws s3 sync s3://cosy-grid-database/data-only/CosyGrid/ .
```
Both folders should now be in my local directory where my terminal is open and contain the parquet files. 

## Converting Parquet to Csv
To use this reporsitory clone it to your local machine. Python3 must be installed on your local machine as well as the pip package manager.  
Install the dependencies from the requirements.txt file using the command below. 
```
pip3 install -r requirements.txt
```
Place all the parquet files associated with the production readings in the folder ```CosyGrid.CosyGrid_Electrical_Meter_Readings_Production``` and place all the files associated with the mains meter readings in the folder ```CosyGrid.CosyGrid_Electrical_Meter_Readings_Mains```. Create these folders if you have not already in the directory where this repository is cloned to. 

The script combines, sorts and merges all the production and consumption parquet files to output two csv files being ```CosyGrid_Electircal_Meter_Readings_Mains.csv``` and ```CosyGrid_Electircal_Meter_Readings_Production.csv```. 

To run the script use the following command 
```
python3 main.py
```

The ouptut should be two csv files ```CosyGrid_Electircal_Meter_Readings_Production.csv``` and ```CosyGrid_Electircal_Meter_Readings_Mains.csv``` which contain the mains and solar data. 
The script can be edited if different files need to be converted from parquet to csv.





