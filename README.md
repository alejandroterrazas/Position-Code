These are the steps and programs reguried to clean tracking video on Cheetah.


e.g., ./view_video 10607/2019-6-26_7-26-40_10607

1) Run the bash script view_video  (e.g., ./view_video 10601/2018-10-2_7-8-34_10601)  Note: DATASETNAME is a dataset on the AWS S3 bucket.  The data are stored in ./RawData after the download.  If the data have been already processed then the POSITION directory will be downloaded and you will not have to run the below.  If you wish to overwrite the POSITION data, you must remove the POSITION directory in AWS.

2) The script will run VideoSliderPlot.py Note: This program will help you segment the data into sleep1, maze and sleep 2 epochs


