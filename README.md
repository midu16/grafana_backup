# grafana_backup
Service to ensure that Grafana datasources and dashboards are backed up.

## The purpose 

The scope of the project is to export, manage and administrate in a more automatic way the Grafana Dashboards and Datasources of a specific Grafana instance. This purpose is achieved into a dynamic and robust software solution that provides zero dependencies to the system. 

The service is running it can be easly manged by monit or systemd. The service should run all the time, but the backup would be done once a week based on the ``` --days``` parameter value.

## How to run the solution:
```
$ grafana_backup --host http://localhost:3000 --api-key 'eyJrIjoiaDhuazQ0aXdiZmFjMFFXWHlGOTVLcnlxMDFyVFlmWnoiLCJuIjoidGVzdCIsImlkIjoxfQ==' --path '/appl/backup/grafana-backup-exports' --ssl-verify <optional> --auto-cleanup <optional> --days <optional>

```
## Command Line help structure
```
$ grafana_backup --help
usage: grafana_backup.py [-h] [-p PATH] [-k API_KEY] [-v] [-hs HOST] [-ssl SSL_VERIFY] [-ac AUTO_CLEANUP] [-days BACKUP_DAYS]

Process design for Back-up the Grafana dashboards and datasources - Mihai IDU 2021

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Mention the path where the grafana_backup would manage the backups
  -k API_KEY, --api-key API_KEY
  -v, --version         show program's version number and exit
  -hs HOST, --host HOST
                        Adding the Grafana host url.
  -ssl SSL_VERIFY, --ssl-verify SSL_VERIFY
                        SSL verification or not of the Grafana service endpoint.
  -ac AUTO_CLEANUP, --auto-cleanup AUTO_CLEANUP
                        Enable or Disable the automatic cleanup of the previous and mention the data backup rendundancy.
  -days BACKUP_DAYS, --backup-days BACKUP_DAYS
                        Number of days between consecutive the backups.
```

### Further developments 

