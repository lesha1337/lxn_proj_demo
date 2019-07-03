#!/bin/bash

Path="/home/bogdan/data/lxn_proj/tmp"

while true; 
do
    String=$(df | grep "/dev/sd[b-z]")
    Cameras=($String)

    for ((i = 0; i < ${#Cameras[@]}; i += 1))
    do
        #if [ -d "${Cameras[$i]}/CARDV" ]; then
        echo 0
        if [[ ${Cameras[$i]} =~ /media/* && -d "${Cameras[$i]}/CARDV" ]]; then
            RawData=$(rsync -rvti "${Cameras[$i]}/CARDV" $Path | grep ">f")
            echo "before"
            if ! [ -z "$RawData" ]; then
                echo "after"
                python3 curl.py "$Path/" "$RawData"
            fi

            chown -R bogdan:bogdan "$Path/CARDV" 
            
            echo ${Data[@]}
        fi  
    done

    sleep 2s;
done
