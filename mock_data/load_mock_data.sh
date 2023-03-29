sqlite3 data.sqlite < create-tables.sql
sqlite3 data.sqlite < mock-data-load.sql
cp data.sqlite ../Scheduler/instance/data.sqlite
rm -f data.sqlite