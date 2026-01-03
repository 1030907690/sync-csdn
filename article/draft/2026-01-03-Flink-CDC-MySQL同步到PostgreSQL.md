






- flink-1.20.3
# Jar 包

- flink-connector-jdbc-3.3.0-1.20.jar
- flink-sql-connector-mysql-cdc-3.5.0.jar
- mysql-connector-java-8.0.29.jar
- postgresql-42.7.8.jar

# SQL

```sql
CREATE TABLE mysql_user (
  id INT,
  name STRING,
  email STRING,
  create_time TIMESTAMP(3),
  PRIMARY KEY (id) NOT ENFORCED   
) WITH (
  'connector' = 'mysql-cdc',
  'hostname' = '192.168.43.166',
  'port' = '3306',
  'username' = 'root',
  'password' = 'root',
  'database-name' = 'test',  
  'table-name' = 't_user',     
  'scan.startup.mode' = 'initial'  
);


CREATE TABLE pg_user (
  id INT ,
  name STRING NOT NULL,
  email STRING NOT NULL,
  create_time TIMESTAMP(3),
   PRIMARY KEY (id) NOT ENFORCED   
) WITH (
     'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://192.168.43.166:5432/test',
    'table-name' = 't_user',  
    'username' = 'postgres',
    'password' = 'root'
);


INSERT INTO pg_user SELECT id, name, email, create_time FROM mysql_user;

```

