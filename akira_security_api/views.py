from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

import re

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