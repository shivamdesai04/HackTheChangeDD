
DROP DATABASE IF EXISTS USERBASE;
CREATE DATABASE USERBASE; 
USE USERBASE;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	user_name 	varchar(30)	not null,
	password	varchar(30) not null,
    primary key(user_name)
);

DROP TABLE IF EXISTS dflt_lang;
CREATE TABLE dflt_lang (
	user_name	varchar(30)	not null,
    language	varchar(30) not null,
    foreign key(user_name) references users(user_name)
);

INSERT INTO users (user_name, password)
VALUES 
('John','hello')
;

INSERT INTO dflt_lang (user_name, language)
VALUES
('John','English')
;
select * from users;
select * from dflt_lang;
