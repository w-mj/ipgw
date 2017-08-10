import re


def encrypt(key, psd):
    ans = str()
    k = 0
    c = 0
    for x in key:
        k += ord(x)

    for x in psd:
        cal = str(ord(x) + k + c)
        if len(cal) > 9:
            raise Exception("too long")
        ans += str(len(cal)) + cal
        # print("加密: " + x + str(len(cal)) + "   " + cal + "  " + str(c))
        c += 11
    return ans


def decrypt(key, psd):
    ans = str()
    k = 0
    i = 0
    for x in key:
        k += ord(x)

    c = 0
    i = 0
    while i < len(psd):
        length = int(psd[i])
        a_psd = psd[i + 1: i + length + 1]
        # print("解密: " + psd[i] + "   " + a_psd)
        ans += chr(int(a_psd) - k - c)
        c += 11
        i = i + length + 1
    return ans


if __name__ == '__main__':
    ans = encrypt('20161234', 'abc012ZXC!@#$%^&*()_+')
    print("加密的结果是: " + ans)
    de = decrypt('20161234', ans)
    print("解密的结果是: " + de)
