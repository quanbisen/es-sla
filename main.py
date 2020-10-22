from apscheduler.schedulers.blocking import BlockingScheduler
from src.job.es_job import ES_Job
from src.util import config_loader
import os


if __name__ == '__main__':
    # index config
    index_config_file_path = os.getcwd() + '\\config\\index.conf'
    index_config = config_loader.load_config_as_json(index_config_file_path)
    # elasticsearch config
    elasticsearch_config_file_path = os.getcwd() + '\\config\\elasticsearch.conf'
    elasticsearch_config = config_loader.load_config_as_json(elasticsearch_config_file_path)
    # database config
    database_config_file_path = os.getcwd() + '\\config\\db.conf'
    database_config = config_loader.load_config_as_json(database_config_file_path)

    es_job = ES_Job(elasticsearch_config=elasticsearch_config, index_config=index_config,
                    database_config=database_config)
    # BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(es_job.query_es_job, 'interval', seconds=5 * 60)
    scheduler.start()
