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


## Example Usage
(Ignore the rows in this database, these are pretty much just random words all put together, for the sake of an example)

```
> python main.py
User: <USERNAME>
Password:
Would you like to View or Add to your CPD? View
Do you want to do a Query or view a Table or Export? (Query/Table/Export) Table
  id  date        activity     brief_description      values_obtained        hours_spent  category
----  ----------  -----------  ---------------------  -------------------  -------------  -----------
   1  2022-02-10  Programming  Wowie this is awesome  Wow, that's amazing             23  Programming
                               this is so useful
   2  2014-02-01  Python       Poggers development    Gained good info                12  Minecraft

Total Hours Taken:  35.0

> python main.py
User: <USERNAME>
Password:
Would you like to View or Add to your CPD? View
Do you want to do a Query or view a Table or Export? (Query/Table/Export) Table
  id  date        activity     brief_description      values_obtained        hours_spent  category
----  ----------  -----------  ---------------------  -------------------  -------------  -----------
   1  2022-02-10  Programming  Wowie this is awesome  Wow, that's amazing             23  Programming
                               this is so useful
   2  2014-02-01  Python       Poggers development    Gained good info                12  Minecraft

Total Hours Taken:  35.0

> python main.py
User: <USERNAME>
Password:
Would you like to View or Add to your CPD? View
Do you want to do a Query or view a Table or Export? (Query/Table/Export) Query
Do you want to do an SQL Query or Category Query? (SQL/Category) Category
Category Name
---------------
Programming
Minecraft

Which category do you want to view? Programming
  id  date        activity     brief_description      values_obtained        hours_spent  category
----  ----------  -----------  ---------------------  -------------------  -------------  -----------
   1  2022-02-10  Programming  Wowie this is awesome  Wow, that's amazing             23  Programming
                               this is so useful
```
