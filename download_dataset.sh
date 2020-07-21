#!/bin/bash

#DATASET="https://storage.googleapis.com/kaggle-data-sets/551982/1125240/bundle/archive.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1589313149&Signature=oBY7xp8zixOTiGizk%2BSSA5VMlYWJ8fepW9Q87GDzW5mnQleh%2BratcgxbR4QRZ5vRAb5%2BsPD66XQv%2BvtEDQHa%2Fp9ICTGcpM4HsJES0qkPwN8wYXNxGjdghRKeQ5pzhkRggSz%2F%2BAy5Ykbycd2xXuCa5p%2Fam3OoGPh03RDtjrPeoBEfotym0r%2BD3AUKU%2FAY0aUTyFwZQQz26v5mL539OsgOqPQKZ3VtBsAkFhF9ZWHti49rdHvU3g4uR%2B0JPndknggPuwh4h50Z9bJIWoACtTY6VGKOCqLtMKnMlhE5f2YqEa4AKSYSfmZ7H8NORY5WM%2BgWWzF03lOMG6mtvL5QP2GPNw%3D%3D&response-content-disposition=attachment%3B+filename%3DCORD-19-research-challenge.zip"
# Version 12 
DATASET=http://labs.coronawhy.org/CORD-19-research-challenge.zip
DATADIR="./data"
echo "Downloading CORD-19 dataset from $DATASET..."
mkdir -p $DATADIR/original/CORD-19-research-challenge
wget -O $DATADIR/original/CORD-19-research-challenge/CORD-19-research-challenge.zip $DATASET
cd $DATADIR/original/CORD-19-research-challenge
echo "Unzipping dataset and preparing CoronaWhy infrastructure..."
unzip CORD-19-research-challenge.zip
cp ./metadata.csv ./metadata_old.csv
# Removing last paper to run test
LAST=$(tail -n 1 ./metadata.csv)
# truncate old metadata file
let TRUNCATE_SIZE="${#LAST} + 1"
truncate -s -"$TRUNCATE_SIZE" ./metadata_old.csv
# Move original zip one level higher
mv $DATADIR/original/CORD-19-research-challenge/CORD-19-research-challenge.zip ../
cd ../../
