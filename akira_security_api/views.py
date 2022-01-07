from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

import re
import secrets
import random

class IndexView(APIView):
    def get(self, request, MetaKey, EncryptedMetaKey):
        username = MetaKey
        ASCII_Username = []
        for i in range(len(username)):
            ASCII_Username.append(ord(username[i]))
        ASCII_Username_Sum = sum(ASCII_Username)

        encrypted_username = ""
        for i in range(len(username)):
            encrypted_username += chr(ord(username[i]) + ASCII_Username_Sum)

        ep = EncryptedMetaKey
        afterRAN = re.sub('[0-9a-zA-Z]+', '', ep)

        List1 = list(afterRAN)
        List2 = list(encrypted_username)
        checkKeyEncrypted =  any(item in List1 for item in List2)

        l_rot = 0
        r_rot = len(username)
        temp = (l_rot - r_rot) % len(afterRAN)
        encrypted_password = afterRAN[temp : ] + afterRAN[ : temp]

        password = ""
        de_key_length = len(encrypted_password) - len(username)
        for i in range(de_key_length):
            password += chr(ord(encrypted_password[i]) - ASCII_Username_Sum)

        data = {
            'checkKeyEncrypted': checkKeyEncrypted,
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