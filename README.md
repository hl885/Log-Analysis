# SQL reporting tool
Source code for reporting results from a database. The code formulates sql statements to query a postgresql database and return appropriate data from the database. The returned data is then output to a text file called 'sql_reporting_result.txt' generated under the same directory where the code is run.

# Usage
To run the program, first create a view in the postgresql datebase in command line tool:
```sh
$ psql news

$ create view popular_article as select articles.title as title, count(log.path) as view_count from articles, log where articles.slug = substring (log.path from 10) group by articles.title order by view_count desc;
```

Then, install python (https://www.python.org/downloads/), run the following command in command line tool:

```sh
$ python sql_reporting_tool.py
```
A text file called 'sql_reporting_result.txt' is generated under the same directory where the code is run.