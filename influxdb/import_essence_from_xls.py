import xlrd
import pandas as pd
import sys
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from enum import Enum
import re

def importToInfluxdb():
    org = "carignan"
    token = "2zhGO0LoXJYG9ngjaGyHmGzU9EOgfPFb2MZaGtlGcwKcNRZC7aKnx0PNY69sFLrPn0kRzT5YRdsGFeksquq6sQ=="
    # Store the URL of your InfluxDB instance
    url = "https://influxdb.mypersonalstats.duckdns.org/"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return write_api


def deleteBucket():
    org = "carignan"
    token = "2zhGO0LoXJYG9ngjaGyHmGzU9EOgfPFb2MZaGtlGcwKcNRZC7aKnx0PNY69sFLrPn0kRzT5YRdsGFeksquq6sQ=="
    # Store the URL of your InfluxDB instance
    url = "https://influxdb.mypersonalstats.duckdns.org/"
    bucket = "db_essence"
    
    print("- deleting bucket <",bucket,">...")

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    delete_api = client.delete_api()
    delete_api.delete(start="2000-01-01T00:00:00Z",stop="2030-01-01T00:00:00Z", predicate="",bucket=bucket)

    
    print("- delete bucket finished ! ")

def readXlsFile(file: str, write_api) -> None:
    org = "carignan"
    bucket = "db_essence"

    myBook = xlrd.open_workbook(file)
    mySheet = myBook.sheet_by_index(0)
    print("- importing datas... ")

    for i in range(mySheet.nrows):
        firstCol = mySheet.cell_value(i, 0)
        if i > 0:
            try:
                if mySheet.cell_type(i, 0) == 3:
                    # first column is a datetime type
                    
                    d = datetime(* xlrd.xldate.xldate_as_tuple(firstCol, myBook.datemode)) 
                    #print("date : ",d)
                    
                    if mySheet.cell_type(i, 9) == 2:
                        plein_vit_moy = mySheet.cell_value(i, 9)
                    else:
                        plein_vit_moy = 0.0
             
                    #print("plein_vit_moy", plein_vit_moy, " : ", type(plein_vit_moy))
                    p = influxdb_client\
                        .Point("essence") \
                        .tag("voiture", str(mySheet.cell_value(i, 1 )))\
                        .field("plein_prix", mySheet.cell_value(i, 2)) \
                        .field("prix_litre", mySheet.cell_value(i, 3)) \
                        .field("plein_litre", mySheet.cell_value(i, 4)) \
                        .field("plein_distance", mySheet.cell_value(i, 5)) \
                        .field("conso_indique", mySheet.cell_value(i, 6)) \
                        .field("conso_calcule", mySheet.cell_value(i, 7)) \
                        .field("plein_lieu", mySheet.cell_value(i, 8)) \
                        .field("plein_vit_moy", plein_vit_moy) \
                        .field("kilometrage_par_voiture", mySheet.cell_value(i, 10)) \
                        .field("kilometrage_total", mySheet.cell_value(i, 11)) \
                        .time(d.isoformat()) \
            
                    write_api.write(bucket=bucket, org=org, record=p)

                    
            except ValueError as err:                
                print("error : ")

    # print("type : ", type(d))
    # print("date :", d)


    # df = pd.read_excel
    # print("dataframe :")
    # print(df.columns.values.tolist())

    # print(df.head(10))
    print("- importing datas finished !")

def main() -> int:    
    print("xlrd version :",xlrd.__version__)
    print("panda version :",pd.__version__)
    
    deleteBucket()

    write_api = importToInfluxdb()
    readXlsFile("/home/pi/server/influxdb_2/import/essence/essence.xls", write_api)
    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
