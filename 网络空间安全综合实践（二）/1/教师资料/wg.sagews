︠167e6005-41a8-46b9-9a7c-8d0f5c0b59d6s︠
import random
from ngram_score import ngram_score
#参数初始化
ciphertext ='YRAAHYHBIUWGRWBYCHCMHKXKUVRQNFSPWULNRMPQYHBMQDWKLNMBJCKUOEJENVLDYLPWCLDAYOUFQOXFAFVLCRMPVZQQQMNSDLCIPWPCHDLYJWKLPKMZQRQQMTAAVDMLYJQVWYVCOHRUDMUEZCWOPJPVVJSVJEZFYOCMQWWLRETAHFDNHYZSRGVMLAHFWRIJKJVLRSNAWKZSPJXSKHXXFKIJDXHWAOIV'
#读取quadgram statistics
fitness = ngram_score('english_quadgrams.txt')
def sub(c,m):
    return chr((ord(c)-ord('A')-m)%26+ord('A'))
maxscore = -99e9
for k in range (1,8):
    print('---------------------------start---------------------------')
    print('assume key length=%d'%k);sys.stdout.flush()
    parentscore = -99e9
    key=list(range(k))
    j=0
    while j<10*k:
        pos=randint(0,k-1)
        j+=1
        for item in range(26):
            temp=key[pos]
            key[pos]=item
            decipher = ciphertext
            for i in range(len(decipher)):
                decipher = decipher[:i]+sub(decipher[i],key[i%k])+decipher[i+1:]
            score = fitness.score(decipher)
            #此子密钥代替其对应的父密钥，提高明文适应度
            if score > parentscore:
                parentscore = score
            else:
                #还原
                key[pos]=temp
    #输出该key和明文
    if parentscore > maxscore:
        maxscore = parentscore
        print ('Currrent key: ',key)
        print ('Iteration total:', j)
        decipher = ciphertext
        for i in range(len(decipher)):
            decipher = decipher[:i]+sub(decipher[i],key[i%k])+decipher[i+1:]
        print ('Plaintext: ', decipher.lower(),maxscore)
        sys.stdout.flush()
︡18f9f547-9b4b-4dfc-9658-3699664c566c︡









