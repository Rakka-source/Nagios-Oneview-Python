#!/usr/bin/python3
from hpOneView.oneview_client import OneViewClient
from pprint import pprint
import argparse
import hpOneView

###############################################################################
# Nagios plugin  OneView monitoring
#
# Notes
# - The RHEL 7
# - This monitoring it's not completly exactli, becouse we use the api. I try to monitoring Synergy
# - Python 3.6 and requiermient.txt
# - It's not necessary docker or other services. Only run the command per query
#
# Author: Delta-Rakkautta [F.G.]
# Date: 08 July 2021
###############################################################################

###Arguments input ###
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host" ,help="ip adress: -H ")
parser.add_argument("-S", "--service", help="Service general : 0 (it is necessary to use -o attribute  ) \n Service powersupply : 1 \n Service thermal : 2 ")
parser.add_argument("-o", "--opcion", help="Index of the service you want to show ")
parser.add_argument("-u", "--user", help="Username: ")
parser.add_argument("-p", "--password", help="Password: ")
parser.add_argument("-t", "--test", help="captures number of alarms, warning or critical. It serves to test ",action="store_true")


args=parser.parse_args()



### Request Api ####

config = {
"ip" : args.host,
"credentials":{
"userName": args.user,
"password": args.password
}
}
oneview_client = OneViewClient(config)
alertas=oneview_client.alerts
requestOneview= alertas.get_by("alertState","Active")
oneview_client.connection.logout()


## Power supply check
if args.service == "1":
        status=0  # 0: Ok 1: Warning 2:Critical
        descript=""
        alertTyp=""
        severity=""
        cont=0

        for i in range(0,len(requestOneview)):
                if 'PowerSupply'in requestOneview[i]["alertTypeID"]:
                        if requestOneview[i]["severity"]== "Critical" or requestOneview[i]["severity"]=="Unknown":
                                status = 2
                                alertTyp = requestOneview[i]["alertTypeID"]
                                descript = requestOneview[i]["description"]
                                severity = requestOneview[i]["severity"]

                        elif requestOneview[i]["severity"]=="Warning" and status==0:
                                status = 1
                                alertTyp = requestOneview[i]["alertTypeID"]
                                descript = requestOneview[i]["description"]
                                severity = requestOneview[i]["severity"]

        if status== 0:
                ## Status: OK Default message
                print("Status power supply OK")
                exit(0)
        if status==1:
                ##Status: Warning
                print ("Warning: Alert type " +alertTyp + "\n"+"Alert Status: "+ severity + "\n" + "Description: "+descript)
                exit(1)
        if status ==2:
                #Status: Critical
                print ("Critical: Alert type " +alertTyp + "\n"+"Alert Status: "+ severity + "\n" + "Description: "+descript)
                exit(2)

## Thermal check
if args.service == "2":
        status=0  # 0: Ok 1: Warning 2:Critical
        descript=""
        alertTyp=""
        severity=""
        cont=0

        for i in range(0,len(requestOneview)):
                if (not 'PowerSupply'in requestOneview[i]["alertTypeID"]) and ('Thermal'in requestOneview[i]["healthCategory"]):
                        if requestOneview[i]["severity"]== "Critical" or requestOneview[i]["severity"]=="Unknown":
                                status = 2
                                alertTyp = requestOneview[i]["alertTypeID"]
                                descript = requestOneview[i]["description"]
                                severity = requestOneview[i]["severity"]

                        elif requestOneview[i]["severity"]=="Warning" and status==0:
                                status = 1
                                alertTyp = requestOneview[i]["alertTypeID"]
                                descript = requestOneview[i]["description"]
                                severity = requestOneview[i]["severity"]

        if status== 0:
                ## Status: OK Default message
                print("Status Thermal :Ok the temperature threshold has not been exceeded")
                exit(0)
        if status==1:
                ##Status: Warning
                print ("Warning: Alart type " +alertTyp + "\n"+"Alert status: "+ severity + "\n" + "Description: "+descript)
                exit(1)
        if status ==2:
                #Status: Critical
                print ("Critical: Alert type " +alertTyp + "\n"+"Alert status: "+ severity + "\n" + "Description: "+descript)
                exit(2)

## Capture alert
elif args.service == "0" :
    ### Validation that all the parameters of the index come. 0 to 10 .
        if args.opcion:
            numeroServicio= int(args.opcion)
        else:
            print("Error: it is necessary that it comes accompanied with an option. -o . The index (0 - 10)")
            exit(2)

        indice = 0
        mach = 0
        status=0
        sw=0
        while indice < len(requestOneview) and mach <= numeroServicio:
            if (not 'PowerSupply'in requestOneview[indice]["alertTypeID"]) and (not 'Thermal'in requestOneview[indice]["healthCategory"]):
                if requestOneview[indice]["severity"]== "Critical" or requestOneview[indice]["severity"]=="Unknown" and mach==numeroServicio:
                    status = 2
                    alertTyp = requestOneview[indice]["alertTypeID"]
                    descript = requestOneview[indice]["description"]
                    severity = requestOneview[indice]["severity"]

                elif requestOneview[indice]["severity"]=="Warning" and mach == numeroServicio:
                    status = 1
                    alertTyp = requestOneview[indice]["alertTypeID"]
                    descript = requestOneview[indice]["description"]
                    severity = requestOneview[indice]["severity"]
                mach += 1
                indice +=1
        if status== 0:
                ## Status: OK Default message
                print("The reports do not indicate an alert for the index: " + str(numeroServicio))
                exit(0)
        if status==1:
                ##Status: Warning
                print ("Warning: Alert type " +alertTyp + "\n"+"Alert status: "+ severity + "\n" + "Description: "+descript)
                exit(1)
        if status ==2:
                #Status: Critical
                print ("Critical: Alert type " +alertTyp + "\n"+"Alert status: "+ severity + "\n" + "Description: "+descript)
                exit(2)

## Test ( Total errors)
elif args.test :

        contWarning=0
        contCritical=0
        exitcode=0
        for i in range(0,len(requestOneview)):

            if requestOneview[i]["severity"]== "Critical" or requestOneview[i]["severity"]=="Unknown":
                    contCritical += 1
                    alertTyp = requestOneview[i]["alertTypeID"]
                    descript = requestOneview[i]["description"]
                    severity = requestOneview[i]["severity"]

            elif requestOneview[i]["severity"]=="Warning":
                    contWarning += 1
                    alertTyp = requestOneview[i]["alertTypeID"]
                    descript = requestOneview[i]["description"]
                    severity = requestOneview[i]["severity"]
        if contCritical>0:
            exitcode=2
        elif contWarning>0:
            exitcode=1
        else:
            exitcode=0

        print ("Number of errors: " + str( len(requestOneview)) + " // Critical:  " + str(contCritical) + " // Warning: "+ str(contWarning))
        exit(exitcode)
