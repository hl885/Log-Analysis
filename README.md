# SQL reporting tool
Source code for reporting results from a database containing website log data. The code formulates sql statements to query the database and return result from the database that answers the following questions:

1. What are the most popular three articles of all time ?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements
- Python 3 (https://www.python.org/downloads/)
- PostgreSQL (https://www.postgresql.org/download/)
- psycopg2

## Usage
To run the program, do the following steps:
1. setup the initial database:
    ```sh
    $ createdb news
    ```
2. import the data (download from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip and unzip to the program directory)
    ```sh
    $ psql -d news -f newsdata.sql
    ```
3. create a view in the datebase:
    ```sh
    $ psql news
    ```
    ```sql
    create view popular_article as
    select articles.title as title, count(log.path) as view_count
    from articles, log
    where '/article/' || articles.slug = log.path
    group by articles.title
    order by view_count desc;
    ```
4. run the program
    ```sh
    $ ./sql_reporting_tool.py
    ```
After the program completes, a text file called 'sql_reporting_result.txt' containing the results is generated under the same directory where the code is run.