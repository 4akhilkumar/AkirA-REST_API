from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

import re
import secrets
import random
import math
import requests

@api_view(['POST'])
def fetchKey(request):
    if request.method == 'POST':
        username = request.POST.get('MetaKey')
        encryptedText = request.POST.get('EncryptedMetaKey')

        encryptedTextLength = len(encryptedText)

        ASCII_Username = []
        for i in username:
            ASCII_Username.append(ord(i))

        ASCII_Username_Sum = list(map(int, str(sum(ASCII_Username))))

        for i in range(len(ASCII_Username_Sum)):
            if ASCII_Username_Sum[i] == 0:
                ASCII_Username_Sum[i] = 1

        max_ASCII_Username_Sum = max(ASCII_Username_Sum)

        def findLargest(arr):
            a=arr
            a=list(set(a))
            a.sort()
            if(len(a)==1 ):
                return (a[0]+1)
            else:
                return (a[-2])

        second_largest = findLargest(ASCII_Username_Sum)

        if second_largest == 0 or math.isinf(second_largest) or second_largest == -math.inf or second_largest == max_ASCII_Username_Sum:
            second_largest = max_ASCII_Username_Sum + 1

        lengthUsername10 = len(username) * 10
        password_length = encryptedTextLength / lengthUsername10

        encryptedText_list = []
        for i in range(int(password_length)):
            encryptedText_list.append(encryptedText[i*int(lengthUsername10):(i+1)*int(lengthUsername10)])

        randomDigits = []
        for i in range(len(encryptedText_list)):
            randomDigits.append(encryptedText_list[i][-second_largest])

        HexList = []
        for i in range(len(encryptedText_list)):
            HexList.append(encryptedText_list[i][int(randomDigits[i])]+encryptedText_list[i][int(randomDigits[i])+1])

        final_list = []
        for i in range(len(HexList)):
            final_list.append(chr(int(HexList[i], 16)))

        Plain_password = []
        for i in final_list:
            value = max_ASCII_Username_Sum + int(max(randomDigits))
            Plain_password.append(chr(ord(i) - value))
        decipherText = "".join(Plain_password)

        data = {
            'MetaKey': decipherText,
        }
        return Response(data)

class CustomEncryption(APIView):
    def get(self, request, MetaKey):
        RanSalt = secrets.token_urlsafe(90)
        SpecialChracter = ["@", "#", "(", ")"] * len(MetaKey)
        EncryptedUsername = ""
        for i in range(len(MetaKey)):
            EncryptedUsername += chr(ord(MetaKey[i]) + 468)
            
        for i in range(len(SpecialChracter)):
            ran = random.randint(0, len(RanSalt) - 1)
            RanSalt = RanSalt[:ran] + SpecialChracter[i] + RanSalt[ran:]

        SpecialChracterPos = []
        for i in range(len(RanSalt)):
            if RanSalt[i] in SpecialChracter:
                SpecialChracterPos.append(i+1)
        
        randomPositions = random.sample(SpecialChracterPos, (len(MetaKey)))
        randomPositions.sort()

        to_modify = list(RanSalt)
        replacements = list(EncryptedUsername)

        for (index, replacement) in zip(randomPositions, replacements):
            to_modify[index] = replacement
        
        FinalEncryptedUsername = "".join(to_modify)
        FinalEncryptedUsername = re.sub('[@#()]+', '', FinalEncryptedUsername)

        data = {
            'EncryptedUsername': FinalEncryptedUsername,
        }
        return Response(data)

class CustomDecryption(APIView):
    def get(self, request, EncryptedMetaData):
        ep = EncryptedMetaData
        afterRAN = re.sub('[0-9a-zA-Z]+', '', ep)
        afterRAN = re.sub('[-_]+', '', afterRAN)

        DecryptedUsername = ""
        for i in range(len(afterRAN)):
            DecryptedUsername += chr(ord(afterRAN[i]) - 468)

        data = {
            'DecryptedUsername': DecryptedUsername,
        }
        return Response(data)

class isSensibleEmail(APIView):
    def get(self, request, email):
        validEmail, disposable = False, True
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            validEmail = True
            domain = re.search("@[\w.]+", email)
            domain = domain.group()[1:]
            try:
                url = 'https://'+domain
                response = requests.get(url)
                if response.status_code == 200:
                    disposable = False
                else:
                    disposable = True
            except Exception as e:
                disposable = True
        else:
            validEmail = False
        data = {
            'ValidEmail': validEmail,
            'Disposable': disposable,
        }
        return Response(data)