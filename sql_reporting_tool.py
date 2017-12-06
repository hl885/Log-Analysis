 #!/usr/bin/env python 3
import psycopg2


def main():
    # Open file for writing output, and connect to database
    report_file = open('sql_reporting_result.txt', 'w')
    sql_connect = psycopg2.connect("dbname=news")
    sql_cursor = sql_connect.cursor()

    # Create view to find popular articles
    try:
        sql_cursor.execute(
            """create view popular_article as
            select articles.title as title, count(log.path) as view_count
            from articles, log
            where articles.slug = substring(log.path from 10)
            group by articles.title
            order by view_count desc;""")
    except psycopg2.ProgrammingError:
        sql_connect.rollback()

    # Select top 3 popular articles and write output to the file
    sql_cursor.execute("select * from popular_article limit 3;")
    section_title = "\r\nTop 3 popular articles: \r\n"
    print(section_title)
    report_file.write(section_title)
    for row in sql_cursor.fetchall():
        out_string = "\t\""+row[0].title()+"\" - "+str(row[1])+" views\r\n"
        print(out_string)
        report_file.write(out_string)

    # Select poular article authors and write output to the file
    sql_cursor.execute(
        """select authors.name, sum(popular_article.view_count) as total_view
        from articles, popular_article, authors
        where articles.author = authors.id
            and articles.title = popular_article.title
        group by authors.name
        order by total_view desc;""")
    section_title = "\r\nPoular article authors: \r\n"
    print(section_title)
    report_file.write(section_title)
    for row in sql_cursor.fetchall():
        out_string = "\t"+row[0]+" - "+str(row[1])+" views\r\n"
        print(out_string)
        report_file.write(out_string)

    # Select days when more than 1% of requests lead to errors
    # and write output to the file
    sql_cursor.execute(
        """select
            tbl_200.trunc_time,
            not_found_404::decimal/(not_found_404+ok_200) as error_rate
        from
            (select
               date_trunc('day', time) as trunc_time,
                count(status) as ok_200
            from log where status = '200 OK'
            group by trunc_time) as tbl_200,
            (select
                date_trunc('day', time) as trunc_time,
                count(status) as not_found_404
            from log where status = '404 NOT FOUND'
            group by trunc_time) as tbl_404
        where tbl_200.trunc_time = tbl_404.trunc_time
            and not_found_404::decimal/(not_found_404+ok_200) >= 0.01;""")
    section_title = """
        \r\nDays when more than 1% of requests lead to errors: \r\n"""
    print(section_title)
    report_file.write(section_title)
    for row in sql_cursor.fetchall():
        out_string = "\t" + row[0].strftime("%B %d, %Y")
        out_string += " - " + format(row[1], '.1%') + " errors\r\n"
        print(out_string)
        report_file.write(out_string)

    # Close file, cursor and database transaction
    report_file.close()
    sql_cursor.close()
    sql_connect.close()


if __name__ == '__main__':
    main()
