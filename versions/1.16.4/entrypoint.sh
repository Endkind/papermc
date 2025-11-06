#!/bin/bash

while [ true ]; do
    java -Xms${MIN_RAM} -Xmx${MAX_RAM} ${JAVA_FLAGS} -jar /endkind/server.jar ${PAPERMC_FLAGS} --nogui

    echo Server restarting...
    echo Press CTRL + C to stop.
done
