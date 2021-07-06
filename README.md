# grafana_backup
Service to ensure that Grafana datasources and dashboards are backed up.

## 

The service is running it can be easly manged by monit or systemd. The service should run all the time, but the backup would be done once a week.


## How to run the solution:
```

$ grafana_backup --host http://localhost:3000 --api-key 'eyJrIjoiaDhuazQ0aXdiZmFjMFFXWHlGOTVLcnlxMDFyVFlmWnoiLCJuIjoidGVzdCIsImlkIjoxfQ==' --path '/appl/backup/grafana-backup-exports'

```
## cli-help
```
$ grafana_backup --help
usage: main.py [-h] [-p PATH] [-k API_KEY] [-v] [-hs HOST]

Process design for Back-up the Grafana dashboards and datasources - Mihai IDU 2021

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Mention the path where the grafana_backup would manage the backups
  -k API_KEY, --api-key API_KEY
  -v, --version         show program's version number and exit
  -hs HOST, --host HOST
                        Adding the Grafana host url
```

