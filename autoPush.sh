#!/bin/bash

apiKey=$(cat ~/api.txt)
while [ 1 ]; do
    echo $apiKey 
    git add -A .
    git commit -m "Auto Commit from shell"
    git push https://github.com/jmeisten/weddingAudioBook.git

    sleep 15
    

done