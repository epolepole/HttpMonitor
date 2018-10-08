# HttpLogMonitor
## Description
HTTP log monitoring console program

This monitoring tool will monitor file (defaulted to /var/log/access.log).

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
python -m pytest
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


