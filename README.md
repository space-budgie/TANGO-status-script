#### Status Monitor Script

This is a small script that allows you to view the status of specified TANGO devices in specified states. For example, you can view all powersupplies, matching a specific pattern, that are in OFF state.

#### Usage
```
usage: status_monitor.py [-h] --states
                         {ON,OFF,CLOSE,OPEN,INSERT,EXTRACT,MOVING,STANDBY,FAULT,INIT,RUNNING,ALARM,DISABLE,UNKNOWN}
                         [{ON,OFF,CLOSE,OPEN,INSERT,EXTRACT,MOVING,STANDBY,FAULT,INIT,RUNNING,ALARM,DISABLE,UNKNOWN} ...]
                         --include INCLUDE [INCLUDE ...]
                         [--exclude [EXCLUDE [EXCLUDE ...]]] [--init]

Status Monitor Application

optional arguments:
  -h, --help            show this help message and exit
  --states {ON,OFF,CLOSE,OPEN,INSERT,EXTRACT,MOVING,STANDBY,FAULT,INIT,RUNNING,ALARM,DISABLE,UNKNOWN} [{ON,OFF,CLOSE,OPEN,INSERT,EXTRACT,MOVING,STANDBY,FAULT,INIT,RUNNING,ALARM,DISABLE,UNKNOWN} ...]
                        Specify the TANGO DevStates to filter by
  --include INCLUDE [INCLUDE ...]
                        Specify the strings to include. Wildcard: '*'
  --exclude [EXCLUDE [EXCLUDE ...]]
                        Specify the strings to exclude. Wildcard: '*'
  --init                Send an init command to all the devices beforehand.
```

#### Example

The following command shows you all the devices that match the string "\*r1\*pspi\*" or "\*r1\*psia\*" in FAULT or ALARM state, but excludes all devices that contain the string "\*ktr1\*" or "\*dserver\*". Here, '\*' is a wildcard.

```
python3 status_monitor.py --include "*r1*pspi*" "*r1*psia*" --exclude "*ktr1*" "*dserver*" --states FAULT ALARM
```

