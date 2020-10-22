from src.util.mysql_connector import get_connection


class ES_SLA_DAO:

    def __init__(self, database_config):
        # get database connection
        self.connection = get_connection(database_config)

    def insert_list(self, es_sla_list):

        cursor = self.connection.cursor()
        insert_sql = ("insert into es_sla (from_time,from_timestamp,to_time,"
                      "to_timestamp,status_code,count,es_index)"
                      "values (%(from_time)s,%(from_timestamp)s,"
                      "%(to_time)s,%(to_timestamp)s,%(status_code)s,%(count)s,%(es_index)s)")
        row = 0
        for es_sla in es_sla_list:
            print(es_sla['status_code'])
            cursor.execute(insert_sql, es_sla)
            row = row + 1
        if row == len(es_sla_list):
            self.connection.commit()
        else:
            row = 0
        cursor.close()
        return row
