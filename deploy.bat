@echo off

git push

cd deploy
fab deploy
cd ..