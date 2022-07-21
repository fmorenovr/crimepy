#!/usr/bin/bash

echo "Moving to $PWD/data/sql/ ..."
cd "$PWD/data/sql/"

echo "Creating 2019/ directory ..."
mkdir "2019/"

echo "Copying _2019/ to 2019/ ..."
cp -R _2019/*.sql 20219/

echo "Moving to $PWD/2019/ ..."
cd "$PWD/2019/"

echo "Processing $PWD/2019/*.sql files ..."
sed -i 's/"Site"/site/g' crimeBB_2019-10-31_*
sed -i 's/"Forum"/forum/g' crimeBB_2019-10-31_*
sed -i 's/"Post"/post/g' crimeBB_2019-10-31_*
sed -i 's/"Member"/member/g' crimeBB_2019-10-31_*
sed -i 's/"Thread"/thread/g' crimeBB_2019-10-31_*
sed -i 's/"ReputationVotes"/reputationvotes/g' crimeBB_2019-10-31_*
