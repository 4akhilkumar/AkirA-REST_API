from rest_framework.views import APIView
from rest_framework.response import Response

import re
import secrets
import random

class IndexView(APIView):
    def get(self, request, MetaKey, EncryptedMetaKey):
        username = MetaKey
        encryptedText = EncryptedMetaKey

        encryptedTextLength = len(encryptedText)

        ASCII_Username = []
        for i in username:
            ASCII_Username.append(ord(i))

        ASCII_Username_Sum = list(map(int, str(sum(ASCII_Username))))

        # Print the second largest number from ASCII_Username_Sum
        second_largest = sorted(ASCII_Username_Sum)[-2]

        # Finding the Password length
        lengthUsername10 = len(username) * 10
        password_length = encryptedTextLength / lengthUsername10

        # Divide the encrypted text into password_length value parts and store it in a list
        encryptedText_list = []
        for i in range(int(password_length)):
            encryptedText_list.append(encryptedText[i*int(lengthUsername10):(i+1)*int(lengthUsername10)])

        # Find the random digits in the encryptedText_list
        randomDigits = []
        # Store the last 5th character of each element in the encryptedText_list in randomDigits list
        for i in range(len(encryptedText_list)):
            randomDigits.append(encryptedText_list[i][-second_largest])

        # get the elements of the encryptedText_list at specific index using randomDigits elements as index values and store it in a list name final_list
        final_list = []
        for i in range(len(encryptedText_list)):
            final_list.append(encryptedText_list[i][int(randomDigits[i])])

        Plain_password = []
        for i in final_list:
            value = max(ASCII_Username_Sum) + int(max(randomDigits))
            Plain_password.append(chr(ord(i) - value))

        password = "".join(Plain_password)

        data = {
            'MetaKey': password,
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