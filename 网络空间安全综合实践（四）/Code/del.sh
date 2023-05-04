#!/bin/bash
while :
do
     find /opt/wwwphp/sport/static/images/  -name "new*" | xargs rm -rf
done
