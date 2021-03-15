#!/bin/bash
echo "#################Building the image for backend-op #################"
BUILD_NAME="op-backend-blob"
sudo docker build -t $BUILD_NAME .
CHK="$?"
if [ "$CHK" -ne 0 ];then
    echo "##################Build failed####################"
    exit 3
fi
