from ngram_score import ngram_score
ciphertext ='YRAAHYHBIUWGRWBYCHCMHKXKUVRQNFSPWULNRMPQYHBMQDWKLNMBJCKUOEJENVLDYLPWCLDAYOUFQOXFAFVLCRMPVZQQQMNSDLCIPWPCHDLYJWKLPKMZQRQQMTAAVDMLYJQVWYVCOHRUDMUEZCWOPJPVVJSVJEZFYOCMQWWLRETAHFDNHYZSRGVMLAHFWRIJKJVLRSNAWKZSPJXSKHXXFKIJDXHWAOIV'
def sub(c,m):
    return chr((ord(c)-ord('A')-m) % 26+ord('A'))
fitness = ngram_score('english_quadgrams.txt')
parentscore = -99e9
maxscore = -99e9
k = 7

print('---------------------------start---------------------------')

key = [0, 0, 0, 0, 0, 0, 0]
temp = 0
for x in range(7):
    count = 0
    while count < 26:
        key[x] = count
        decipher = ciphertext
        for i in range(len(decipher)):
            decipher = decipher[:i] + sub(decipher[i], key[i % k]) + decipher[i + 1:]
        parentscore = fitness.score(decipher)
        if parentscore > maxscore:
            maxscore = parentscore
            temp = key[x]
        count += 1
    key[x] = temp

print(key)
decipher = ciphertext
for i in range(len(decipher)):
    decipher = decipher[:i] + sub(decipher[i], key[i % k]) + decipher[i + 1:]
print('Plaintext: ', decipher.lower(), maxscore)











# #维吉尼亚密码加密示例
# ciphertext ='YRAAHYHBIUWGRWBYCHCMHKXKUVRQNFSPWULNRMPQYHBMQDWKLNMBJCKUOEJENVLDYLPWCLDAYOUFQOXFAFVLCRMPVZQQQMNSDLCIPWPCHDLYJWKLPKMZQRQQMTAAVDMLYJQVWYVCOHRUDMUEZCWOPJPVVJSVJEZFYOCMQWWLRETAHFDNHYZSRGVMLAHFWRIJKJVLRSNAWKZSPJXSKHXXFKIJDXHWAOIV'
#
# #将字母c减密钥m，变成明文
# def sub(c,m):
#     return chr((ord(c)-ord('A')-m) % 26+ord('A'))
#
# #假设维吉尼亚密码密钥长度为k
# k = 7
#
# #解密密钥初始为[0,1,2,3,4,5,6]
# key = list(range(k))
#
# #更改初试密钥为[1,1,2,3,4,5,6]
# key[0] = 1
# #解密
# decipher = ciphertext
# for i in range(len(decipher)):
#     decipher = decipher[:i]+sub(decipher[i], key[i % k])+decipher[i+1:]
#
# print(decipher)