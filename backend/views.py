import re
import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint
from backend import authentication
from backend.models import ReferralUser, ConfirmationCode

def get_code(user):

    time.sleep(3)

    #  Так как отправка смс имитируется, сам код вернется в теле ответа на запрос
    code = ConfirmationCode.objects.filter(user=user)
    key = randint(1000, 9999)
    if code:
        code.update(code=key)
        status = 200
    else:
        ConfirmationCode.objects.create(user=user, code=randint(1000, 9999))
        status = 200
    return (key, status)



class GetMessageView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number', '1')
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise ValidationError("Phone number must be entered in the format: '+999999999'."
                                  " Up to 15 digits allowed.")
        user = ReferralUser.objects.get_or_create(phone_number=phone_number)[0]
        code, status = get_code(user)
        return JsonResponse({'code': code}, status=status)



        # authentication_classes = [authentication.MyTokenAuthentication]
        # permission_classes = [IsAuthenticated]
