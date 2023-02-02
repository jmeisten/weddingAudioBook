#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apiKey=$(cat ~/api.txt)
echo 1234 > test.txt

sudo python3 weddingAudioBook.py &

while [ 1 ]; do
    online=$(curl -s -o /dev/null -w "%{http_code}" http://www.google.com)
    echo $online
    if [ $online == 200 ]
    then
        git add -A .
        git commit -m "Auto Commit from shell"
        git push https://$apiKey@github.com/jmeisten/weddingAudioBook.git
        echo "Git pushed successfully"
        sleep 15m
    else
        echo "Not online"
    fi


    
done