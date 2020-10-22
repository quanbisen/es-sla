from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from src.dao.es_sla_dao import ES_SLA_DAO
from src.util.logger import print_message
import time


class ES_Job:

    def __init__(self, elasticsearch_config, index_config, database_config):
        self.elasticsearch_config = elasticsearch_config
        self.index_config = index_config
        self.database_config = database_config

    # function which query elasticsearch job
    def query_es_job(self):
        # set up query time ranger
        str_from_time = (datetime.utcnow() + timedelta(seconds=-300)).strftime('%Y-%m-%dT%H:%M:%S')
        str_to_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        self.elasticsearch_config["query_object"]["query"]["bool"]["filter"]["range"]["@timestamp"]['gte'] \
            = str_from_time
        self.elasticsearch_config["query_object"]["query"]["bool"]["filter"]["range"]["@timestamp"]['lt'] = str_to_time

        # query ElasticSearch
        es = Elasticsearch([{'host': self.elasticsearch_config["host"], 'port': self.elasticsearch_config["port"]}],
                           http_auth=(self.elasticsearch_config['username'], self.elasticsearch_config['password']))
        response = es.search(index=self.elasticsearch_config['index'], body=self.elasticsearch_config["query_object"])
        # get our needed buckets
        buckets = response['aggregations']['group_by_status']['buckets']

        # set up time format for database attributes
        from_time = (datetime.strptime(str_from_time, '%Y-%m-%dT%H:%M:%S') + timedelta(hours=8))\
            .strftime('%Y-%m-%d %H:%M:%S')
        to_time = (datetime.strptime(str_to_time, '%Y-%m-%dT%H:%M:%S') + timedelta(hours=8))\
            .strftime('%Y-%m-%d %H:%M:%S')

        if len(buckets) > 0 and buckets is not None:
            # construct record object list
            es_sla_list = []
            for bucket in buckets:
                es_sla = {
                    'from_time': from_time,
                    'from_timestamp': int(time.mktime(time.strptime(from_time, '%Y-%m-%d %H:%M:%S'))),
                    'to_time': to_time,
                    'to_timestamp': int(time.mktime(time.strptime(to_time, '%Y-%m-%d %H:%M:%S'))),
                    'status_code': int(bucket['key']),
                    'count': bucket['doc_count'],
                    'es_index': self.elasticsearch_config['index']
                }
                es_sla_list.append(es_sla)

            # create ES_SLA_DAO object and insert
            es_sla_dao = ES_SLA_DAO(self.database_config)
            row = es_sla_dao.insert_list(es_sla_list)
            if row == len(es_sla_list):
                print_message('execute sql success.')
            else:
                print_message('execute sql fail.')
        else:
            print_message('Buckets length is 0. Noting to do.')





