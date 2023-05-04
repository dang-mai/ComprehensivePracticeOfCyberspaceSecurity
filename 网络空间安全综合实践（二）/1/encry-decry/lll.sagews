︠8ba1fdb0-e52a-4d4a-80ac-71454b0b0858s︠
def check(guess):
    pubKey = [615436700291,415460700271,15508700231,846430100773,677471501215,139578302079,179168604148,789306608798,563224517265,364498233536,229056467022,670323428329,115934481316,44989786476,518624653302,149955258190,728568829281,796899516776,546782575075,178164449829,356328899658,712657799316,569303048254,223205396187,446410792374,892821584748,524144817108,132888933895,611875519857,877653387647,839906074973,35774353074]
    nbit = len(pubKey)
    encoded = 6020587936087
    print('start %d'%(guess))
    # create a large matrix of 0's (dimensions are public key length +2)
    A = Matrix(ZZ, nbit + 2, nbit + 2)
    # fill in the identity matrix1
    for i in range(nbit):
        A[i, i] = 1
    
    # replace the bottom 2 rows
    for i in range(nbit):
        A[i, nbit] = pubKey[i]
    for i in range(nbit):
        A[i, nbit+1] = 1
    
    # last 2 elements
    A[nbit, nbit] = -encoded
    A[nbit+1, nbit+1] = -guess
    #print(A)
    res = A.LLL()
    #print(res)
    for i in range(0, nbit + 2):
        M = res.row(i).list()
        flag = True
        for m in M:
            if m != 0 and m != 1:
                flag = False
                break
        if flag:
            print('***************')
            print (i, M)
            M = ''.join(str(j) for j in M)
            # remove the last 2 bits
            M = M[:-2]
            print('res='+M)
for i in range(1,33):
    check(i)
print('end')
︡2d4c3d89-85b8-461f-80da-7d28d358ff5b︡{"stdout":"start 1\nstart 2"}︡{"stdout":"\nstart 3"}︡{"stdout":"\nstart 4"}︡{"stdout":"\nstart 5"}︡{"stdout":"\n***************"}︡{"stdout":"\n30 [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]\nres=10111010011001110101001100001000\nstart 6\nstart 7"}︡{"stdout":"\nstart 8"}︡{"stdout":"\nstart 9"}︡{"stdout":"\nstart 10"}︡{"stdout":"\nstart 11"}︡{"stdout":"\nstart 12"}︡{"stdout":"\nstart 13"}︡{"stdout":"\nstart 14"}︡{"stdout":"\nstart 15"}︡{"stdout":"\n***************"}︡{"stdout":"\n29 [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]\nres=10111010011001110101001100001000\nstart 16\nstart 17"}︡{"stdout":"\nstart 18"}︡{"stdout":"\nstart 19"}︡{"stdout":"\nstart 20"}︡{"stdout":"\nstart 21"}︡{"stdout":"\nstart 22"}︡{"stdout":"\nstart 23"}︡{"stdout":"\nstart 24"}︡{"stdout":"\nstart 25"}︡{"stdout":"\n"}︡{"stderr":"Error in lines 29-30\n"}︡{"stderr":"Traceback (most recent call last):\n  File \"/usr/local/sage/local/lib/python3.8/site-packages/smc_sagews/sage_server.py\", line 1230, in execute\n    exec(\n  File \"\", line 2, in <module>\n  File \"\", line 15, in check\n  File \"sage/matrix/matrix_integer_dense.pyx\", line 3206, in sage.matrix.matrix_integer_dense.Matrix_integer_dense.LLL (build/cythonized/sage/matrix/matrix_integer_dense.c:27327)\n    R = A.to_matrix(self.new_matrix())\n  File \"src/fpylll/fplll/integer_matrix.pyx\", line 726, in fpylll.fplll.integer_matrix.IntegerMatrix.to_matrix\n  File \"src/fpylll/fplll/integer_matrix.pyx\", line 869, in fpylll.fplll.integer_matrix.IntegerMatrix._get\n  File \"src/fpylll/io.pyx\", line 50, in fpylll.io.mpz_get_python\n  File \"<frozen importlib._bootstrap>\", line 988, in _find_and_load\n  File \"<frozen importlib._bootstrap>\", line 149, in __enter__\n  File \"<frozen importlib._bootstrap>\", line 101, in acquire\n  File \"src/cysignals/signals.pyx\", line 320, in cysignals.signals.python_check_interrupt\nKeyboardInterrupt\n"}︡{"done":true}









