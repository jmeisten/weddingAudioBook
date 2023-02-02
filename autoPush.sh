#!/bin/bash

apiKey=$(cat ~/api.txt)
echo 1234 > test.txt
while [ 1 ]; do
    echo $apiKey 
    curl -H "Authorization: token $apiKey" https://github.com/jmeisten/weddingAudioBook.git
    git add -A .
    git commit -m "Auto Commit from shell"
    git push https://github.com/jmeisten/weddingAudioBook.git
    sleep 15
    

done