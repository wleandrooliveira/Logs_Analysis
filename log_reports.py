#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# Script for Database Log Analysis
#

import psycopg2
import os
import sys

# Database name
DB = "news"
# Log Report Output Filename
FILERPORT = "logs-reports.txt"

# List of questions for the log reports
QUESTION_ARRAY = [
    '1. What are the most popular three articles of all time?',
    '2. Who are the most popular article authors of all time?',
    '3. On which days did more than 1% of requests lead to errors?']

# Queries to be executed
QUERY_ARRAY = [
    ('''
    SELECT articles.title, subq.views
    FROM articles
    LEFT JOIN
    (SELECT path, count(ip) as views
    FROM log
    WHERE status='200 OK'
    GROUP BY path) as subq
    ON subq.path=CONCAT('/article/',articles.slug)
    ORDER BY subq.views DESC LIMIT 3;
    '''),
    ('''
    SELECT  subq2.name, count(subq2.path) as views
    FROM
    (SELECT log.path, log.ip, subq1.slug, subq1.title, subq1.name
    FROM log
    RIGHT JOIN
    (SELECT articles.slug, articles.title, authors.name
    FROM articles JOIN authors ON articles.author=authors.id) as subq1
    ON log.path=CONCAT('/article/',subq1.slug)
    WHERE status='200 OK') as subq2
    GROUP BY subq2.name ORDER BY views DESC;
    '''),
    ('''
    SELECT subq.day, ROUND((100.0*subq.err/subq.total),2) as error
    FROM
    (SELECT date_trunc('day', time) as day,
    count(id) as total,
    sum(case when status!='200 OK' then 1 else 0 end) as err
    FROM log
    GROUP BY day) as subq
    WHERE ROUND((100.0*subq.err/subq.total),2) >1;
    ''')]


def execute_query(queries):
    """
    Connects to the database and execute the queries.
    Args:
        queries: Array of queries for execution.
    Returns:
        Query results in array.
    """
    try:
        db = psycopg2.connect(database=DB)
        c = db.cursor()
        ret = []

        for i in queries:
            c.execute(i)
            ret.append(c.fetchall())
        db.close()

        return ret
    except psycopg2.Error as e:
        print e
        sys.exit(1)


def output_to_file(text_format):
    """
    Outputs a body of text to a file
    Args:
        text_format: The body of text for output.
    """
    f = open('./' + FILERPORT, 'w')
    f.write(text_format)
    f.close()


def format_query1(query_result):
    """
    Formats the query result to be more readable (for question 1&2)
    Args:
        query_result: The Query result in array format.
    Returns:
        The formatted result in string.
    """
    ret = ''
    for res in query_result:
        ret += ('• {i[0]} - {i[1]} views\n').format(i=res)
    return ret


def format_query2(query_result):
    """
    Formats the query result to be more readable (for question 3)
    Args:
        query_result: The Query result in array format.
    Returns:
        The formatted result in string.
    """
    ret = ''
    for res in query_result:
        ret += ('• {i[0]:%B %d, %Y} - {i[1]:}% errors\n').format(i=res)

    return ret


def format_report(query_result):
    """
    Formats the report and congregate with the questions
    Args:
        query_result: The Query result in array format.
    Returns:
        The formatted report in string.
    """
    result = ''
    for i in range(len(QUESTION_ARRAY)):
        result += QUESTION_ARRAY[i] + '\n'

        if(i != 2):
            result += format_query1(query_result[i]) + '\n\n'
        else:
            result += format_query2(query_result[i]) + '\n\n'

    return result


# Executes the script
if __name__ == "__main__":
    query_result = execute_query(QUERY_ARRAY)
    text_format = format_report(query_result)
    output_to_file(text_format)
    print '{} successfully generated.'.format(FILERPORT)