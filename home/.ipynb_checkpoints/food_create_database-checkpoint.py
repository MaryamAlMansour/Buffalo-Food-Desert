import configparser
import psycopg2
from food_desert_sqlqueries import create_table_queries, drop_table_queries


"""The drop_tables function will call the queries to drop the fact and dimension tables if they ever exist in database"""
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

"""create fact and dimension database in database"""
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

"""Summens all require functions in here. By parsing the AWS configuration and connecting to redshift so it creats the table using its database"""
def main():
    config = configparser.ConfigParser()
    config.read('food_warehouse.cfg')
                                                                                       
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DWH'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()
    
if __name__ == "__main__":
    main()