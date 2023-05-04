import random
import sys
from ngram_score import ngram_score

#参数初始化
ciphertext ='UNGLCKVVPGTLVDKBPNEWNLMGVMTTLTAZXKIMJMBBANTLCMOMVTNAAMILVTMCGTHMKQTLBMVCMXPIAMTLBMVGLTCKAUILEDMGPVLDHGOMIZWNLMGBZLGKSMAZBMKOMKTWNLMGBZKTLCKAMHMIMDMVGBZLXBLCSAZTBMMOMTVPGMOMVKJLTQPXCBPNEJLBBLUILVDKJKZ'
parentkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#只是用来声明key是个字典
key = {'A': 'A'}
#读取quadgram statistics
fitness = ngram_score('english_quadgrams.txt')
parentscore = -99e9
maxscore = -99e9

print('---------------------------start---------------------------')
j=0
while 1:
    j=j+1
    #随机打乱key中的元素
    random.shuffle(parentkey)
    #将密钥做成字典
    #密文:明文
    for i in range(len(parentkey)):
        key[parentkey[i]] = chr(ord('A')+i)
    #用字典一一映射解密
    decipher = ciphertext
    for i in range(len(decipher)):
        decipher = decipher[:i]+key[decipher[i]]+decipher[i+1:]
    parentscore = fitness.score(decipher)#计算适应度
    #在当前密钥下随机交换两个密钥的元素从而寻找是否有更优的解
    count = 0
    while count < 2000:
        a = random.randint(0,25)
        b = random.randint(0,25)
        #随机交换父密钥中的两个元素生成子密钥，并用其进行解密
        parentkey[a],parentkey[b]= parentkey[b],parentkey[a]
        key[parentkey[a]],key[parentkey[b]] = key[parentkey[b]],key[parentkey[a]]
        decipher = ciphertext
        for i in range(len(decipher)):
            decipher = decipher[:i]+key[decipher[i]]+decipher[i+1:]
        score = fitness.score(decipher)
        #此子密钥代替其对应的父密钥，提高明文适应度
        if score > parentscore:
            parentscore = score
            count=0
        else:
            #还原
            parentkey[a],parentkey[b]=parentkey[b],parentkey[a]
            key[parentkey[a]],key[parentkey[b]]=key[parentkey[b]],key[parentkey[a]]
            count +=1
    #输出该key和明文
    if parentscore > maxscore:
        maxscore = parentscore
        print ('Currrent key: '+''.join(parentkey))
        print ('Iteration total:', j)
        decipher = ciphertext
        for i in range(len(decipher)):
            decipher = decipher[:i]+key[decipher[i]]+decipher[i+1:]
        print ('Plaintext: ', decipher.lower(),maxscore)
        sys.stdout.flush()