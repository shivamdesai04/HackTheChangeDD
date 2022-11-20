DROP DATABASE IF EXISTS COMMUNIFY;
CREATE DATABASE COMMUNIFY; 
USE COMMUNIFY;

CREATE TABLE CLIENT_USER_PASS (
User_n		varchar(30)		not NULL,
Pass_w		varchar(30)		not Null,
PRIMARY KEY(User_n)
);

CREATE TABLE UNIQUE_USER_DATA (
User_name	varchar(30)		not NULL,
Language 	varchar(15)		not NULL,
FOREIGN KEY (User_name) REFERENCES CLIENT_USER_PASS (User_n)
);
