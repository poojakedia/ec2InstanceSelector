import pandas as  pd
import sqlite3
import csv


'''
## Ideation:
Input features:
Compute Power
Memory Optimization
Storage Optimization
>>Clustor networking?

"Name","API Name","Instance Memory","vCPUs","Instance Storage","Network Performance","On Demand","Linux Reserved cost","Linux Spot Minimum cost","Windows On Demand cost","Windows Reserved cost"


Implement with an SQL database in the backend, use python logic to develop code analysis
Pycone for frontend UI to streamline the process

filter by (computational requirements-> )

exclude checkbox []
checkboxes for CPU vs GPU usage
slider for lightweight to compute-intensive applications
(low, medium, high)
exclude checkbox []
slider for memory usage requirements
(1-16GB, 16-64GB, )
exclude checkbox []
storage panel
-> clustor networking
storage 
exclude checkbox []
network performance
up to 1Gbp....5-10Gbp range... 12


advanced option section with definitive memory requirements, Linux/ Windows, etc

displays a card with recommended ec2 instance [take top (cheapest) instance from filtration results]

'''
conn = sqlite3.connect('amazon.db')

cur = conn.cursor()

#clean data
#remove unit measurements

df = pd.read_csv('dataset/ec2Instances.csv')

df["Instance Memory"]=df["Instance Memory"].str.replace(" GiB","").astype(float)
df["Instance Storage"] = df["Instance Storage"].replace("EBS only", "-1")


df["Instance Storage"] = df["Instance Storage"].str.split(" ").str[0].astype(float)

df["vCPUs"] = df["vCPUs"].str.split(" ").str[0].astype(int)


#filter cost data so output can be sorted by cost
df = df[(df["Linux Reserved cost"]!="unavailable") & (df["Windows Reserved cost"]!= "unavailable")]

df["Linux Reserved cost"] = df["Linux Reserved cost"].str.split(" ").str[0].str[1:].astype(float)
df["Windows Reserved cost"] = df["Windows Reserved cost"].str.split(" ").str[0].str[1:].astype(float)

print(df[df["Name"]=="M1 General Purpose Large"])
print(df.iloc[138])

with open('dataset/ec2Instances.csv') as f:
    reader = csv.reader(f)
    data = list(reader)
    


table = (
'''CREATE TABLE ec2_Instance(
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

cur.execute(table)

for index,row in df.iterrows():
    cur.execute("INSERT INTO ec2_Instance (Name,API_Name,Instance_Memory,vCPUs,Instance_Storage,Network_Performance,On_Demand,Linux_Reserved_cost,Linux_Spot_Minimum_cost,Windows_Demand_cost,Windows_Reserved_cost) values (?,?,?,?,?,?,?,?,?,?,?)", row)

fetch_rows = cur.execute("SELECT * FROM ec2_Instance").fetchall()

for r in fetch_rows:
    print(r)
conn.commit()
conn.close()
