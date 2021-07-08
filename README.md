# Nagios-Oneview-Synergy-Python

Monitor synergy through oneview easily in nagios. Integrate alarm easily to nagios 

## Prerequisite
Before starting you need to install the following.
>**Python 3.6**
>->Pip (requirement.txt)
>---->amqplib1.0.2
>---->future 0.18.2
>---->future 0.18.2
>---->hpOneView 5.3.0
>---->requests 2.10.0
>---->six 1.10.0
>**Connection with api or server**
>**Credentials**

### Install python and libraries on RHL7
1) yum install python3
2) pip install requests= =2.10.0
3) pip install setuptools= =39.0.1
4) pip install six= =1.16.0
5) pip install hpOneView
6) pip install amqplib
7) pip install future

> **Note:** The tests were done with that version of each package, however it is possible to use more updated packages. **But this is not fully proven. Please send me your feedback**

## Test check

1) **We will first execute the help command:**
       ./check_onview.py -h

<pre><code>
	 $./check_onview.py -h
		usage: oneView_Synergy_2021.py [-h] [-H HOST] [-S SERVICE] [-o OPCION]
                               [-u USER] [-p PASSWORD] [-t]

	optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  ip adress: -H
  -S SERVICE, --service SERVICE
                        Service general : 0 (it is necessary to use -o
                        attribute ) Service powersupply : 1 Service thermal :
                        2
  -o OPCION, --opcion OPCION
                        Index of the service you want to show
  -u USER, --user USER  Username:
  -p PASSWORD, --password PASSWORD
                        Password:
  -t, --test            captures number of alarms, warning or critical. It
                        serves to test

</code></pre>

2) **Test command execution (example):**
	./check_onview.py -H < ip > -u < user > -p < password > -t
<pre><code>
$./check_onview.py -H < ip > -u < user > -p < password > -t
Number of errors: 3 // Critical:  1 // Warning: 2

</code></pre>

> **Note:** If your password has symbols, it is recommended to put it in single quotes ( ' ) example 'P!AS#woRd'
 
3) **Alert check by index:**
./check_onview.py -H < ip > -u < user > -p < password > -S 0 -o < index 0 - 10>
<pre><code>
$./check_onview.py -H < ip > -u < user > -p < password > -S 0 -o 0
Critical: Alert type server-hardware.opStatus.outofmaintenancemode.withcriticalstatus
Alert status: Critical
Description: At least one critical alert for this server hardware was active when maintenance mode was disabled.


$./check_onview.py -H < ip > -u < user > -p < password > -S 0 -o 1
Warning: Alert type remote-support.unEntitledDevice
Alert status: Warning
Description: Remote support is not monitoring 1 eligible devices: device registration with the HPE data center may have failed or the warranty or contract on some of these devices may have expired.


$./check_onview.py -H < ip > -u < user > -p < password > -S 0 -o 2
The reports do not indicate an alert for the index: 2

</code></pre>

> **Note:** This monitoring is general, and is ranked first in the order of critical alerts.  Since there can be multiple reasons for alarms, it was chosen to index them. This allows you to know the status and description of the alert.  In production I use 3 indexes (Images in the repository). you can use the amount you want

4) **Power supply alert check** 
./check_onview.py -H < ip > -u < user > -p < password > -S 1
<pre><code>
$./check_onview.py -H < ip > -u < user > -p < password > -S 1
Status power supply OK
</code></pre>

5) **Temperature check**
./check_onview.py -H < ip > -u < user > -p < password > -S 2
<pre><code>
$./check_onview.py -H < ip > -u < user > -p < password > -S 2
Status Thermal :Ok the temperature threshold has not been exceeded
</code></pre>
> **Note:** It does not give the temperature of the moment. Detect designated value from oneview to alert
