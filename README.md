# grafana_backup
Service to ensure that Grafana datasources and dashboards are backed up.

## 

The service is running it can be easly manged by monit or systemd. The service should run all the time, but the backup would be done once a week.


## How to run the solution:
```

$ grafana_backup --host http://localhost:3000 --api-key 'eyJrIjoiaDhuazQ0aXdiZmFjMFFXWHlGOTVLcnlxMDFyVFlmWnoiLCJuIjoidGVzdCIsImlkIjoxfQ==' --path '/appl/backup/grafana-backup-exports'

```

