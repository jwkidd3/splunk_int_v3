@echo off
echo Removing Splunk container...
docker rm -f splunk

echo Removing Splunk image...
docker rmi splunk/splunk:latest

echo Cleanup complete!
