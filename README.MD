## Creating the database

```sql
CREATE DATABASE cpd;
use cpd;

CREATE TABLE report (id int primary key auto_increment, date DATE, activity VARCHAR(150),
       brief_description text, values_obtained text, hours_spent FLOAT, category VARCHAR(150));
```