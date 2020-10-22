import mysql.connector


def get_connection(db_config):
    connection = mysql.connector.connect(user=db_config['username'],
                                         password=db_config['password'],
                                         host=db_config['host'],
                                         database=db_config['database'])
    return connection
