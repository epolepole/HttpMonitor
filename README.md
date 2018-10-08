# HttpLogMonitor
HTTP log monitoring console program. This monitoring tool will monitor a log file with common log format.
It will print some statistics related to the logs in json format. It will print the timestamp, the transactions per second, the most hit resources, the most active users and the number of status returned per category:
```json
{"time": "2018-10-08T23:36:08.331543", "tps": 15773.0, "most_hits": ["/users", "/statistics", "/api"], "most_active_users": ["Alan", "Thom", "Clara"], "status_codes": {"2xx": 5599, "3xx": 4465, "4xx": 13668
, "5xx": 6160}}
```


And traffic alerts can be configured to show when the traffic goes over a certain threshold for a certain period of time. Displayed as:
```
High traffic generated an alert - hits = 3193, triggered at 2018-10-08T23:28:49
High traffic alert recovered at 2018-10-08T23:28:53
```
Several alarms can be configured at the same time


### Display options
The output of the script can be send to 3 different streams:
1. Simple console output
2. The log output
3. A file

### Available Features
1. Stats printer
2. Traffic Alerts

## Application setup
```bash
# Building image
docker build -t http_monitor .

# Deploying 
docker run -it --rm -v /path/to/log/folder:/var/log:ro http_monitor
```
## Testing
### Env setup
```bash
cd /path/to/app
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Unit tests
The folder regression contains a test for the alert mechanism
```bash
python -m pytest
```
### Application tests
Run the log generator in one window (Or as background process)
```bash
python log_generator.py
```
Deploy application in another window and check that logs are printed and alert is triggered and recovered
```bash
python main.py -f logs/access.log
```

## Application Design

