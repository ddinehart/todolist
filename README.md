# Todo List

## Attributes

+ id
+ item

## User Attributes

+ fname
+ lname
+ email
+ password


## Database Schema

```
CREATE TABLE users (
uid INTEGER PRIMARY KEY,
fname TEXT,
lname TEXT,
email TEXT,
password TEXT);

```

```
CREATE TABLE todoitems (id INTEGER PRIMARY KEY,
item TEXT);

```
Name | HTTP Method | path
---- | ----------- | ----
List | Get| /todoitems/
Retrieve | Get | /todoitems/id
Create   | POST | /todoitems/id
UPDATE | PUT | /todoitems/id
Delete | DELETE | /todoitems/id
Create | POST | /sessions
Create | POST | /users

## Encryption

encrpass = bcrypt.hash(password)
