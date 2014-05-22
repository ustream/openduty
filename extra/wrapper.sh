#! /bin/bash
usage()
{
cat << EOF
usage: $0 options

This script is a wrapper for pagerduty_nagios.pl

OPTIONS:
   -h      Show this message
   -t      Notification type can be ‘PROBLEM′ or ‘RECOVERY′
   -k      Service key
   -i      Incident key
   -d      Description
   -e      Details
EOF
}




declare TYPE=
declare API_BASE="your.dutyfree.host"
declare SERV_KEY=
declare INCIDENT_KEY=
declare DESCRIPTION=
declare DETAILS=
while getopts “ht:k:i:d:e:” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         t)
             TYPE=$OPTARG
             ;;
         k)
             SERV_KEY=$OPTARG
             ;;
         i)
             INCIDENT_KEY=$OPTARG
             ;;
         d)
             DESCRIPTION=$OPTARG
             ;;
         e)
			 DETAILS=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [[ -z $TYPE ]] || [[ -z $SERV_KEY ]] || [[ -z $INCIDENT_KEY ]] || [[ -z $DESCRIPTION ]] || [[ -z $DETAILS ]]
then
	 echo "mandatory parameter missing :("
     usage
     exit 1
fi

if [ $TYPE == "PROBLEM" ] || [ $TYPE == "CUSTOM" ]
then
	ACTION=trigger
elif [ $TYPE == "ACKNOWLEDGEMENT" ]
then
    ACTION=acknowledge
else
	ACTION=resolve
fi

perl /opt/dutyfree-nagios-pl/pagerduty_nagios.pl enqueue --api-base=$API_BASE  -f service_key=$SERV_KEY  -f incident_key=$INCIDENT_KEY -f description=$DESCRIPTION -f event_type=$ACTION -f details="$DETAILS"