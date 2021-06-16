"""
This is the grafana_backup main
"""
__author__ = 'Mihai IDU'
__version__ = '0.0.1'
import argparse
import time, datetime
#from custom_classes import saveDashboards, saveDatasources
import os, errno
def CreateNestedDirectors(path):
    path = path + time.strftime("-%Y%m%d-%H:%M:%S")
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
    # defining a full loop
    while True:
    # checking each argument exists
        if args.path is not None and args.api_key is not None:
            CreateNestedDirectors(str(backup_path))
        elif args.path is None and args.api_key is None:
            print("--path and --api-key has not been added!")
            print("----------------------------------------")
            print("Please check the cli! $ grafana_backup -h")
            break
        elif args.path is None:
            print("--path has not been added!")
            break
        elif args.api_key is None:
            print("--api-key has not been added!")
            print("-----------------------------------------")
            print("{0:^5}".format("This parameter its required to be previously"
                  "defined from the GrafanaWEBUI.\nLogin as "
                  "administrative user and go to "
                  "Configuration->API Keys and generate a key!"
                  "The key generated should be parsed to "
                  "grafana_backup in order to retrieve the "
                  "Dashboards and Datasources for backup purpose."
                  "\nNO INTRUSIVE ACTIONS would be performed on the "
                  "current status of Grafana!"))
            print("-----------------------------------------")
            print("Please check the cli! $ grafana_backup -h")
            break
