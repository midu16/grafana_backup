"""
This is the grafana_backup main
"""
__author__ = 'Mihai IDU'
__version__ = '0.0.7'

import argparse
import datetime
import time
#import datetime
import errno
import json
import requests
import os
import shutil
from git import Repo
import socket

# Defining global static variables
"""
DIR = /tmp/grafana-exports-desktop-localdomain/ directory this would be transparent for the localhost backup. Valueble for the remote git backup.
PATH_OF_GIT_REPO = /tmp/grafana-exports-desktop-localdomain/.git
COMMIT_MESSAGE = desktop-localdomain the commit message it would be only the hostname, therefore it would be easy to track on the github repo
in the scenario that there are multiple GrafanaWEBUI to be commited, Each site/environmnet would be tracked based on the commit message.

"""
DIR = '/tmp/grafana-exports-' + str(socket.gethostname()) + '/'
DIR_DASH = DIR + 'grafana-dashboards/'
DIR_DATA = DIR + 'grafana-datasources/'
PATH_OF_GIT_REPO = DIR + '.git'
COMMIT_MESSAGE = socket.gethostname()




# function to trigger a period action.
def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)

"""
Function that performs dynamic cleanup of the pervious backup.
"""
def DynamicCleanupOfBackup(path_to_file, data_redundancy):
    t = os.path.getmtime(path_to_file)
    # return the last modification time of the file : datetime.datetime.fromtimestamp(t)
    if datetime.datetime.fromtimestamp(t) > data_redundancy:

        return 0

"""
Function that backups the data to the specific git repository.
"""
def GitPush():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(str(COMMIT_MESSAGE))
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')

"""
Function that performs the archive file of the directory, adds the date and time.
"""
def make_archive(source, destination, format='zip'):
    base, name = os.path.split(destination)
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(destination)
    print(f'\nTimeStamp: {time.strftime("%b  %d %H:%M:%S")}\nSource: {source}\nDestination: {destination + time.strftime("-%Y%m%d-%H:%M:%S")}\nArchive From: {archive_from}\nArchive To: {archive_to}\n')
    shutil.make_archive(name, format, archive_from)
    shutil.move('%s.%s' % (name, format), destination + '/grafana-backup-exports'+ time.strftime("-%Y%m%d-%H:%M:%S"))

"""
This function is creating the backup directory, creates the full path no mather if the full nested exists or not.
"""
def CreateNestedDirectors(path):
    path = path
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
"""
This function is exporting the Grafana dashboard json files.
"""
def dashboard():
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    response = requests.get('%s/api/search?query=&' % (HOST,), headers=headers, verify=bool(ssl))
    response.raise_for_status()
    dashboards = response.json()

    CreateNestedDirectors(DIR_DASH)

    print("============= Dashboards =============")
    for d in dashboards:
        print ("Saving: " + d['title'])
        response = requests.get('%s/api/dashboards/%s' % (HOST, d['uri']), headers=headers, verify=bool(ssl))
        data = response.json()['dashboard']
        dash = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        name = data['title'].replace(' ', '_').replace('/', '_').replace(':', '').replace('[', '').replace(']', '').replace('-', '')
        tmp = open(DIR_DASH + name + '.json', 'w')
        tmp.write(dash)
        tmp.write('\n')
        tmp.close()

"""
This function is exporting the Grafana datasources json files.
"""
def datasources():
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    response = requests.get('%s/api/datasources' % (HOST,), headers=headers, verify=bool(ssl))
    response.raise_for_status()
    datasources = response.json()
    #print(datasources)

    CreateNestedDirectors(DIR_DATA)

    print("============= Datasources =============")
    for ds in datasources:
        print("Saving: "+ ds['name'] + " " + ds['type'])
        response = requests.get('%s/api/datasources/%s' % (HOST, ds['id']), headers=headers, verify=bool(ssl))
        data = response.json()
        dash = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        name = data['name'].replace(' ', '_').replace('/', '_').replace(':', '').replace('[', '').replace(']', '')
        tmp = open(DIR_DATA + name + '.json', 'w')
        tmp.write(dash)
        tmp.write('\n')
        tmp.close()

if __name__ == '__main__':
    # defining the global variable to be accessible to the upper
    global API_KEY
    global backup_path
    global HOST
    global BACKUP_DIR
    global ssl

    #BACKUP_DIR = '/home/midu/PycharmProjects/grafana_backup/custom_classes/grafana-backup-exports'
    #time = datetime.datetime.now()
    #ISO_8601_time = time.isoformat()
    parser = argparse.ArgumentParser(description="Process design for Back-up the Grafana dashboards and datasources - Mihai IDU 2021")
    parser.add_argument("-p", "--path", type=str, help="Mention the path where the grafana_backup would manage the backups")
    parser.add_argument("-k", "--api-key", type=str, help="")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s ' + __version__)
    parser.add_argument("-hs", "--host", type=str, help="Adding the Grafana host url.")
    parser.add_argument("-ssl", "--ssl-verify", type=bool, help="SSL verification or not of the Grafana service endpoint.", default=False)
    parser.add_argument("-ac", "--auto-cleanup", type=int, help="Enable or Disable the automatic cleanup of the previous and mention the data backup rendundancy.", default=20)
    parser.add_argument("-days", "--backup-days", type=int, help="Number of days between consecutive the backups.", default=7.0)
    args = parser.parse_args()
    BACKUP_DIR = args.path
    API_KEY = args.api_key
    HOST = args.host
    ssl = args.ssl_verify
    cleanup = args.auto_cleanup
    backup_days = args.backup_days
    # defining a full loop
    while True:
    # checking each argument exists
        if args.path is not None and args.api_key is not None:
            dashboard()
            datasources()
            CreateNestedDirectors(str(BACKUP_DIR))
            make_archive(DIR, str(BACKUP_DIR))
            time.sleep(int(backup_days) * 24.0 * 60.0 * 60.0) # 7 x 24h converted to seconds.
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
