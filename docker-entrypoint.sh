#!/bin/sh
echo "Created by Endkind Ender (www.endkind.net)"

if [ ! -f "/endkind/server.jar" ]; then
    /endkind/getPaperMC.sh

    if [ $? -ne 0 ]; then
        exit 1
    fi
fi

while true; do
    java -Xms$MIN_RAM -Xmx$MAX_RAM $JAVA_FLAGS -jar /endkind/server.jar $PAPERMC_FLAGS --nogui
    if [ $? -ne 0 ]; then
        exit 1
    fi
done