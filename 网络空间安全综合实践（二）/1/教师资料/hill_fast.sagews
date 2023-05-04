︠167e6005-41a8-46b9-9a7c-8d0f5c0b59d6s︠
import random
from ngram_score import ngram_score
#参数初始化
ciphertext0 ='RYLLAFFSOJJEYVSBYWGDEEKCKUISULIEFVXVZKHBXMVPHMIBQJZSEIXTMNUUIOHPGVFFVYTSUNUWSGLJTVPMXSGWMDJJEZRZIEEBHLTJFDFFXVJOCOJGNQJZVOUGMXHEQBCTVWZBHLGGSTRCSKUGDEIJMWYGJWCFSVVWZJALXZRSVYHAFTDDYJUXNCNBUBZXFFVYTSTGATRPTMWHQCCAMTIZPEMPDZDWRZRZIEEBHLKPINJRSLUTBTSYINEKOJAFOERKILRENTCTFZWHIBDJWSRDOPFYVHFREQYOJAVUCXGLHAIXMIAQZVEOCBTDSAJRWYQIBPZFDQKZGTAOQGXAJCLLIVUZOHMJMYNOHBWGIEFJHIPEMPBGNTCBZXFFVYTSCOWYPPPEMLYYLJKMOMIEFQSNKSHVOHKNRXVJNBUBZXWQEBATQBTVXQCBYPGYHHTTKEXYKJGOSYIKPIPDHZRZIEETMTOAOQQXBSTXCJLUETMTOAOQQXWSRMSRJFWEQWZKHWZFNPVFPFWSSECRDFLETYSWXFIWVUZAGZGBYTTSHIAHFREQYXCJLUEBHLLLYBSWNXFMKUEQLZZUQIWSIHNDOPPEBRYMBGIEFCTKIGBBTOXNFWWBPDHXUAQYPHNVWSSRWWBHZJCGSUYHWMLZJPGYLCJMMBBZDVPHKDCLIQUPXWRWNXIHIAHUCNYMBSHIEFDTZTAOZJLJLZRHHXKOXGLHAIGOTNBHVXQMDWBPZUTGZMMXKWJGSHTWRGRBYARYLBXMJLZZQWHFXDITLRVWDGJTWMHWBVTWSGVSBZJLJLZVPHMPSBYEJLZXKOXGLHAIAUDIEFRKINTCCUEFGPCXSTAOVVLFSOMPSBZXQANLVIEGMTFBFSOSWXFIWPSKKAMTVZWGOHHEZESJGNYERWSRLCJGWYVPHJGSHTWRGRCRAXNCNISJVMJFKWESQDOGRABTXLAAXTMBZXCJYHIADWPWSXXYXJDIXNCNTCZOJXKOTWIDBVGOPWSRLJTYJGZTICXSWSRUPXMLOTMWNWWQGLFIHVBZNLIHFRURQWPEHFKVHZMWRBOKIZWSZLNGCTKKEOTZJYVJUDFFKVWHTLTHENMCTRIVKIKNPNMCTRIAPQNLIPDHXTFUTGQANLVIIWMKNP'
R = Zmod(26)
MR = MatrixSpace(R,3,3)
ciphertext=ciphertext0[:240]
#读取quadgram statistics
fitness = ngram_score('english_quadgrams.txt')
vcode=[0]*(len(ciphertext0)//3)
dic={}
for i in range(len(ciphertext0)//3):
    vcode[i]=vector([R(ord(ciphertext0[3*i])-ord('A')),R(ord(ciphertext0[3*i+1])-ord('A')),R(ord(ciphertext0[3*i+2])-ord('A'))])

for i in range(26):
    dic[R(i)]=chr(ord('A')+i)

def hill(ciphertext):
    cipher=''
    for i in range(len(ciphertext)//3):
        v = vcode[i]*key
        cipher = cipher+dic[v[0]]+dic[v[1]]+dic[v[2]]
    return cipher

maxscore = -99e9
key=MR()

for k in range (15):
    print('---------------------------new start %d---------------------------'%k)
    sys.stdout.flush()
    parentscore = -99e9
    pos=k%3
    if pos==0:
        for i in range(3):
            for j in range(3):
                key[i,j]=R(randint(0,25))
    for item1 in range(26):
        for item2 in range(26):
            for item3 in range(26):
                if gcd([item1,item2,item3,26])!=1:
                    continue
                temp1,temp2,temp3=key[0,pos],key[1,pos],key[2,pos]
                key[0,pos],key[1,pos],key[2,pos]=R(item1),R(item2),R(item3)
                #key=MR([[6,23,22],[18,8,17],[11,5,4]])
                decipher = hill(ciphertext)
                score = fitness.score(decipher)
                #此子密钥代替其对应的父密钥，提高明文适应度
                if score > parentscore:
                    parentscore = score
                else:
                    #还原
                    key[0,pos],key[1,pos],key[2,pos]=temp1,temp2,temp3
    #调整可能列的顺序
    st=[[(0,1)],[(1,2)],[(0,2)],[(0,1),(0,2)],[(0,2),(0,1)]]
    if pos==2:
        for s in st:
            for t in s:
                key.swap_columns(t[0],t[1])
            decipher=hill(ciphertext)
            score = fitness.score(decipher)
            if score > parentscore:
                parentscore = score
            else:
                for t in s[::-1]:
                    key.swap_columns(t[0],t[1])
    if parentscore > maxscore:
        maxscore = parentscore
        print ('Currrent key^-1: ') # K=MR([[6,23,22],[18,8,17],[11,5,4]])
        print(key)
        decipher = hill(ciphertext0)
        print ('Plaintext: ', decipher.lower(),maxscore)
        sys.stdout.flush()
︡c24cb8c5-554d-4da4-814a-967267eb7f2f︡
︠8eec5397-644f-40cf-b476-375c4a90beb4︠
︠3f5cbf0a-8a1d-4ab4-b4bf-c2beabb3fa93︠









