#!/bin/bash

apiKey=$(cat ~/api.txt)
while [ 1 ]; do
    echo $apiKey 
    git add -A .
    git commit -m "Auto Commit from shell"
    git push master

    sleep 15
    

done