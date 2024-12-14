import pandas as  pd
import sqlite3
import csv

conn = sqlite3.connect('amazon.db')

cur = conn.cursor()

with open('dataset/ec2Instances.csv') as f:
    reader = csv.reader(f)
    data = list(reader)
    


table = ('''CREATE TABLE ec2_Instance(
    Name TEXT NOT NULL,
    API_Name TEXT NOT NULL,
    Instance_Memory TEXT NOT NULL,
    vCPUs TEXT NOT NULL,
    Instance_Storage TEXT NOT NULL,
    Network_Performance TEXT NOT NULL,
    On_Demand TEXT NOT NULL,
    Linux_Reserved_cost TEXT NOT NULL,
    Linux_Spot_Minimum_cost TEXT NOT NULL,
    Windows_Demand_cost TEXT NOT NULL,
    Windows_Reserved_cost TEXT NOT NULL);
    '''
)


for row in data:
    cur.execute("INSERT INTO ec2_Instance (Name,API_Name,Instance_Memory,vCPUs,Instance_Storage,Network_Performance,On_Demand,Linux_Reserved_cost,Linux_Spot_Minimum_cost,Windows_Demand_cost,Windows_Reserved_cost) values (?,?,?,?,?,?,?,?,?,?,?)", row)

fetch_rows = cur.execute("SELECT * FROM ec2_Instance").fetchall()

for r in fetch_rows:
    print(r)
conn.commit()
conn.close()