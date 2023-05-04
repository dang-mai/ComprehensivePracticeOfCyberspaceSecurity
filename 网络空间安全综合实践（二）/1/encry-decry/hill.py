#3*3hill密码加解密示例
import random
from ngram_score import ngram_score
ciphertext0 ='RYLLAFFSOJJEYVSBYWGDEEKCKUISULIEFVXVZKHBXMVPHMIBQJZSEIXTMNUUIOHPGVFFVYTSUNUWSGLJTVPMXSGWMDJJEZRZIEEBHLTJFDFFXVJOCOJGNQJZVOUGMXHEQBCTVWZBHLGGSTRCSKUGDEIJMWYGJWCFSVVWZJALXZRSVYHAFTDDYJUXNCNBUBZXFFVYTSTGATRPTMWHQCCAMTIZPEMPDZDWRZRZIEEBHLKPINJRSLUTBTSYINEKOJAFOERKILRENTCTFZWHIBDJWSRDOPFYVHFREQYOJAVUCXGLHAIXMIAQZVEOCBTDSAJRWYQIBPZFDQKZGTAOQGXAJCLLIVUZOHMJMYNOHBWGIEFJHIPEMPBGNTCBZXFFVYTSCOWYPPPEMLYYLJKMOMIEFQSNKSHVOHKNRXVJNBUBZXWQEBATQBTVXQCBYPGYHHTTKEXYKJGOSYIKPIPDHZRZIEETMTOAOQQXBSTXCJLUETMTOAOQQXWSRMSRJFWEQWZKHWZFNPVFPFWSSECRDFLETYSWXFIWVUZAGZGBYTTSHIAHFREQYXCJLUEBHLLLYBSWNXFMKUEQLZZUQIWSIHNDOPPEBRYMBGIEFCTKIGBBTOXNFWWBPDHXUAQYPHNVWSSRWWBHZJCGSUYHWMLZJPGYLCJMMBBZDVPHKDCLIQUPXWRWNXIHIAHUCNYMBSHIEFDTZTAOZJLJLZRHHXKOXGLHAIGOTNBHVXQMDWBPZUTGZMMXKWJGSHTWRGRBYARYLBXMJLZZQWHFXDITLRVWDGJTWMHWBVTWSGVSBZJLJLZVPHMPSBYEJLZXKOXGLHAIAUDIEFRKINTCCUEFGPCXSTAOVVLFSOMPSBZXQANLVIEGMTFBFSOSWXFIWPSKKAMTVZWGOHHEZESJGNYERWSRLCJGWYVPHJGSHTWRGRCRAXNCNISJVMJFKWESQDOGRABTXLAAXTMBZXCJYHIADWPWSXXYXJDIXNCNTCZOJXKOTWIDBVGOPWSRLJTYJGZTICXSWSRUPXMLOTMWNWWQGLFIHVBZNLIHFRURQWPEHFKVHZMWRBOKIZWSZLNGCTKKEOTZJYVJUDFFKVWHTLTHENMCTRIVKIKNPNMCTRIAPQNLIPDHXTFUTGQANLVIIWMKNP'
# ciphertext0=ciphertext0[:240]
R = Zmod(26)
MR = MatrixSpace(R,3,3)
key = MR()
vcode=[0]*(len(ciphertext0)//3)
dic={}
fitness = ngram_score('english_quadgrams.txt')
parentscore = -99e9
maxscore = -99e9

#hill加密/解密
def hill(ciphertext):
    cipher=''
    for i in range(len(ciphertext)//3):
        v = vcode[i]*key
        cipher = cipher+dic[v[0]]+dic[v[1]]+dic[v[2]]
    return cipher

#密文转化成数字
for i in range(len(ciphertext0)//3):
    vcode[i]=vector([R(ord(ciphertext0[3*i])-ord('A')),R(ord(ciphertext0[3*i+1])-ord('A')),R(ord(ciphertext0[3*i+2])-ord('A'))])

#数字转化成密文
for i in range(26):
    dic[R(i)] = chr(ord('A')+i)

# 给密钥赋值

for i in range(3):
        for j in range(3):
            key[i,j]=R(randint(0,26))

# while (parentscore < -1520):
#     for i in range(3):
#         for j in range(3):
#             key[i,j]=R(randint(0,25))
#     decipher = hill(ciphertext0)
#     parentscore = fitness.score(decipher)
#     if parentscore > maxscore:
#         maxscore = parentscore
#         temp = [key[0,0], key[1,0], key[2,0]]
#         print('Currrent key:\n', key)
#         print('Plaintext: ', decipher.lower(), maxscore)

# key[0,0]=R(6)
# key[1,0]=R(18)
# key[2,0]=R(11)
# key[0,1]=R(23)
# key[1,1]=R(8)
# key[2,1]=R(5)
# key[0,2]=R(22)
# key[1,2]=R(17)
# key[2,2]=R(4)

# decipher = hill(ciphertext0)
# parentscore = fitness.score(decipher)
# if parentscore > maxscore:
#     maxscore = parentscore
#     print('Currrent key:\n', key)
#     print('Plaintext: ', decipher.lower(), maxscore)

print('----start------')
for j in range(3):
    for j1 in range(26):
        for j2 in range(26):
            for j3 in range(26):
                key[0,j]=R(j1)
                key[1,j]=R(j2)
                key[2,j]=R(j3)
                if (gcd([key[0,j],key[1,j],key[2,j]]) == 1):
                    decipher = hill(ciphertext0)
                    parentscore = fitness.score(decipher)
                    if parentscore > maxscore:
                        maxscore = parentscore
                        temp = [key[0,j], key[1,j], key[2,j]]
                        print('Currrent key:\n',key)
                        print('Iteration total:', j)
                        print('Plaintext: ', decipher.lower(), maxscore)
                        sys.stdout.flush()
    key[0,j] = R(temp[0])
    key[1,j] = R(temp[1])
    key[2,j] = R(temp[2])
#     maxscore = -99e9
#     temp = [0,0,0]

print('-----adjust------')
temp = key
for i in range(2):
    key[0,0],key[1,0],key[2,0],key[0,1],key[1,1],key[2,1],key[0,2],key[1,2],key[2,2] = key[0,1],key[1,1],key[2,1],key[0,2],key[1,2],key[2,2],key[0,0],key[1,0],key[2,0]
    decipher = hill(ciphertext0)
    parentscore = fitness.score(decipher)
    if parentscore > maxscore:
        maxscore = parentscore
        temp = key
        print('Currrent key:\n',key)
        print('Iteration total:', i)
        print('Plaintext: ', decipher.lower(), maxscore)
        sys.stdout.flush()
key = temp

print('----end----')
print(key)
decipher = hill(ciphertext0)
print('Plaintext: ', decipher.lower(), maxscore)







# #3*3hill密码加解密示例
# ciphertext0 ='RYLLAFFSOJJEYVSBYWGDEEKCKUISULIEFVXVZKHBXMVPHMIBQJZSEIXTMNUUIOHPGVFFVYTSUNUWSGLJTVPMXSGWMDJJEZRZIEEBHLTJFDFFXVJOCOJGNQJZVOUGMXHEQBCTVWZBHLGGSTRCSKUGDEIJMWYGJWCFSVVWZJALXZRSVYHAFTDDYJUXNCNBUBZXFFVYTSTGATRPTMWHQCCAMTIZPEMPDZDWRZRZIEEBHLKPINJRSLUTBTSYINEKOJAFOERKILRENTCTFZWHIBDJWSRDOPFYVHFREQYOJAVUCXGLHAIXMIAQZVEOCBTDSAJRWYQIBPZFDQKZGTAOQGXAJCLLIVUZOHMJMYNOHBWGIEFJHIPEMPBGNTCBZXFFVYTSCOWYPPPEMLYYLJKMOMIEFQSNKSHVOHKNRXVJNBUBZXWQEBATQBTVXQCBYPGYHHTTKEXYKJGOSYIKPIPDHZRZIEETMTOAOQQXBSTXCJLUETMTOAOQQXWSRMSRJFWEQWZKHWZFNPVFPFWSSECRDFLETYSWXFIWVUZAGZGBYTTSHIAHFREQYXCJLUEBHLLLYBSWNXFMKUEQLZZUQIWSIHNDOPPEBRYMBGIEFCTKIGBBTOXNFWWBPDHXUAQYPHNVWSSRWWBHZJCGSUYHWMLZJPGYLCJMMBBZDVPHKDCLIQUPXWRWNXIHIAHUCNYMBSHIEFDTZTAOZJLJLZRHHXKOXGLHAIGOTNBHVXQMDWBPZUTGZMMXKWJGSHTWRGRBYARYLBXMJLZZQWHFXDITLRVWDGJTWMHWBVTWSGVSBZJLJLZVPHMPSBYEJLZXKOXGLHAIAUDIEFRKINTCCUEFGPCXSTAOVVLFSOMPSBZXQANLVIEGMTFBFSOSWXFIWPSKKAMTVZWGOHHEZESJGNYERWSRLCJGWYVPHJGSHTWRGRCRAXNCNISJVMJFKWESQDOGRABTXLAAXTMBZXCJYHIADWPWSXXYXJDIXNCNTCZOJXKOTWIDBVGOPWSRLJTYJGZTICXSWSRUPXMLOTMWNWWQGLFIHVBZNLIHFRURQWPEHFKVHZMWRBOKIZWSZLNGCTKKEOTZJYVJUDFFKVWHTLTHENMCTRIVKIKNPNMCTRIAPQNLIPDHXTFUTGQANLVIIWMKNP'
# R = Zmod(26)
# MR = MatrixSpace(R,3,3)
# key = MR()
# vcode=[0]*(len(ciphertext0)//3)
# dic={}
# #密文转化成数字
# for i in range(len(ciphertext0)//3):
#     vcode[i]=vector([R(ord(ciphertext0[3*i])-ord('A')),R(ord(ciphertext0[3*i+1])-ord('A')),R(ord(ciphertext0[3*i+2])-ord('A'))])
#
# #数字转化成密文
# for i in range(26):
#     dic[R(i)]=chr(ord('A')+i)
#
# #给密钥赋值
# for i in range(3):
#     for j in range(3):
#         key[i,j]=R(randint(0,25))
# #hill加密/解密
# def hill(ciphertext):
#     cipher=''
#     for i in range(len(ciphertext)//3):
#         v = vcode[i]*key
#         cipher = cipher+dic[v[0]]+dic[v[1]]+dic[v[2]]
#     return cipher