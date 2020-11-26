# iex-replicator
A simple python script that downloads data for all available (equity) symbols from IEX.
### Purpose
I got tired of using IEX sandbox data because it is inconsistent and makes it harder for me to identify problems in the web app that I am building using the IEX API. (iexcloud.io)
### Usage
Set apikey in config.ini to your IEX private key and then run the script with no parameters.
It will download company and chart data for all (equity) symbols on the IEX cloud API into the data folder.

###### config.ini example:
`
[iexcloud]
apikey = Tsk_********************************
`