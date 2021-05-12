### 데이터 가져오기
CSV, JSON, SQL, NoSQL

#### Reading CSV Files
CSV는 ','로 분류된 데이터 행으로 구성되어있다.  
Pandas에서, CSV파일은 몇줄의 코드만으로 읽어들일 수 있다.  
```python
import pandas as pd
filepath = 'data/iris_data.csv'
# Import the data
data = pd.read_csv(filepath)
#print a few rows
print(data.iloc[:5])
```

```python
# 다른 구분자 - 탭-separated file (.tsv):
data = pd.read_csv(filepath, sep='\t')
# 다른 구분자 - 공백-separated file:
data = pd.read_csv(filepath, delim_whitespace=True)
# 최상단 행의 정보를 헤더로 사용하지 않음
data = pd.read_csv(filepath, header=None)
# 특정 column 이름을 정의한다.
data = pd.read_csv(filepath, names=['Name1', 'Name2'])
# 특정 값을 가지는 경우 Nan로 처리한다.
data = pd.read_csv(filepath, na_values=['Na', 99])
```
**pd.read_csv의 argument list : sep, delim_whitespace, header, names, na_values**

```python
# 다른 구분자 - 탭-separated file (.tsv):
data = pd.read_csv(filepath, sep='\t')
```

#### Reading JSON Files
JSON파일은 여러 플랫폼에 거쳐 데이터를 저장하는 표준 방법이다.  
파이썬의 dictionary 구조와 유사하다.  

```python
# Read JSON file as dataframe
data = pd.read_json(filepath)
data.to_json('outputfile.json')
```
**json을 읽거나 쓰기, pd.read_json, dt.to_json (dt 인스턴스는 pd를 상속받았기 때문에 to_json method를 가지고 있다.)** 
**split, records, index, columns, values**
**json 데이터 참조방식 argument인 orient 참고**  
'split' : {index -> [index], columns -> [columns], data -> [values]}/dictionary 참조방식  
'records' : [{column -> value}, ... , {column -> value}]   /list 참조방식  
'index' : {index -> {column -> value}}/dictionary 참조방식  
'columns' :  {column -> {index -> value}}/dictionary 참조방식  
'values' : just the values array  


#### SQL Databases
고정 스키마를 가진 고도로 구조화된 관계형 데이터베이스  
파이썬의 dictionary 구조와 유사하다.  
SQL DB는 다양한 형태로 존재하는데, Microsoft SQL server, Postgres, MySQL, AWS Redshift, Oracle DB, IBM용 Db2 제품군 등이 있다.  
표시된 예처럼 적절한 파이썬 라이브러리를 사용하여 미묘하게 다른 포맷을 불러올 수 있다.  


```python
# SQL Data Imports
import sqlite3 as sq3 #가용한 sql 라이브러리가 많음
import pandas as pd
con = sq3.Connection(path) # 이것으로 DB와 연결을 생성함
query = ''' SELECT * FROM rock_songs; '''
data = pd.read_sql(query, con)
```


#### NoSQL Databases
비관계형이며 구조상 더 다르다. application에 따라 더빠르거나 기술적 오버헤드를 줄인다. 대부분 JSON 형태로 저장된다.  
문서DB : mongoDB, couchDB  
key-value stores : Riak, Voldemort, Redis  
Graph DB : Neo4j, HyperGraph  
Wide-column stores : Cassandra, HBase


```python
# SQL Data Imports
import pymongo import MongoClient
# Create a Mongo connection
con = MongClient()
# Choose DB (con.list_database_names()를 통해 가용 리스트를 볼 수 있다.)
db = con.database_name
# Create a cursor object using a query
cursor = db.collection_name.find(query) # 여기서 query는 MongoDB query형태나 {}를 이용해야 한다.
# Expand cursor and construct DataFrame
df = pd.DataFrame(list(cursor))
```
**NoSQL은 별로 해보질 않아서 확실하게 와닿지 않으므로 해봐야할것 같다.**
