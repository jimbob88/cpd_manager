# Continuous Personal Development Manager (CLI)
This is a command line pice of software that connects with a [MySQL](https://dev.mysql.com/downloads/) Server in order to keep a record of your personal development!

## Features
- Ability to export to a csv for distribution
- Efficient storage system using SQL
- Fast
- Autocompletion of commands
- Automatic colouring of commands when you need to type something in SQL
- Fancy (TABULATE) table formatting

## Creating the database

```sql
CREATE DATABASE cpd;
use cpd;

CREATE TABLE report (id int primary key auto_increment, date DATE, activity VARCHAR(150),
       brief_description text, values_obtained text, hours_spent FLOAT, category VARCHAR(150));
```
