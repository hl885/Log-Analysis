#!/usr/bin/env python3
import psycopg2


def main():
    # Open file for writing output, and connect to database
    report_file = open('sql_reporting_result.txt', 'w')
    sql_connect = psycopg2.connect("dbname=news")
    sql_cursor = sql_connect.cursor()

    # Select top 3 popular articles and write output to the file
    sql_cursor.execute("select * from popular_article limit 3;")
    section_title = "\r\nTop 3 popular articles: \r\n"
    print(section_title)
    report_file.write(section_title)
    for title, views in sql_cursor.fetchall():
        out_string = ('\t{0:<30}{1:>12} views\r\n'.format(title, views))
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
    for title, views in sql_cursor.fetchall():
        out_string = ('\t{0:<30}{1:>12} views\r\n'.format(title, views))
        print(out_string)
        report_file.write(out_string)

    # Select days when more than 1% of requests lead to errors
    # and write output to the file
    sql_cursor.execute(
        """select
            tbl_all.trunc_time,
            not_found_404::decimal/total as error_rate
        from
            (select
                date_trunc('day', time) as trunc_time,
                count(status) as total
            from log
            group by trunc_time) as tbl_all,
            (select
                date_trunc('day', time) as trunc_time,
                count(status) as not_found_404
            from log where status = '404 NOT FOUND'
            group by trunc_time) as tbl_404
        where tbl_all.trunc_time = tbl_404.trunc_time
            and not_found_404::decimal/total >= 0.01;""")
    section_title = (
        "\r\nDays when more than 1% of requests lead to errors: \r\n")
    print(section_title)
    report_file.write(section_title)
    for title, views in sql_cursor.fetchall():
        out_string = (
            '\t{0:%B %d, %Y}{1:>12.1%} errors\r\n'.format(title, views))
        print(out_string)
        report_file.write(out_string)

    # Close file, cursor and database transaction
    report_file.close()
    sql_cursor.close()
    sql_connect.close()


if __name__ == '__main__':
    main()
