"""
This is the grafana_backup main
"""
__author__ = 'Mihai IDU'
__version__ = '0.0.1'
import argparse
import time
import datetime
#from custom_classes import saveDashboards, saveDatasources
import os, errnoss
def CreateNestedDirectors(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
# function to trigger a period action.
def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)


if __name__ == '__main__':
    # defining the global variable to be accessible to the upper
    global ISO_8601_time
    global compressed_dashboards_name
    global compressed_datasources_name
    global GRAFANA_TOKEN
    global backup_path
    compressed_dashboards_name = "dashboards.tar.gz"
    compressed_datasources_name = "datasources.tar.gz"
    time = datetime.datetime.now()
    ISO_8601_time = time.isoformat()
    parser = argparse.ArgumentParser(description="Process design for Back-up the Grafana dashboards and datasources - Mihai IDU 2021")
    parser.add_argument("-p", "--path", type=str, help="Mention the path where the grafana_backup would manage the backups")
    parser.add_argument("-k", "--api-key", type=str, help="")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
    backup_path = args.path
    GRAFANA_TOKEN = args.api_key
