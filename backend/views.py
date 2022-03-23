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
from backend.models import ReferralUser, ConfirmationCode, MyToken
from backend.serializers import ReferralUserSerializer


def get_code(user):

    time.sleep(3)

    #  Так как отправка смс имитируется, сам код вернется в теле ответа на запрос
    code = ConfirmationCode.objects.filter(user=user)
    key = randint(1000, 9999)
    if code:
        code.update(code=key)
        status = 200
    else:
        ConfirmationCode.objects.create(user=user, code=key)
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


class LogInView(APIView):

    """Log in endpoint returns AuthToken that is used to see user's profile"""

    def get(self, request):
        phone_number = request.data.get('phone_number', '1')
        code = request.data.get('code')
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise ValidationError("Phone number must be entered in the format: '+999999999'."
                                  " Up to 15 digits allowed.")
        user_to_update = ReferralUser.objects.filter(phone_number=phone_number)
        user = user_to_update[0]
        if not user:
            return JsonResponse({'Response': 'No such user'}, status=400)

        confirmation = ConfirmationCode.objects.filter(user=user)
        if not confirmation:
            return JsonResponse({'Response': 'No active code. Ask the code first'}, status=400)

        if confirmation.first().code != int(code):
            return JsonResponse({'Response': 'Wrong code'}, status=400)

        referral_code = user.referral_code
        if not referral_code:
            referral_code = randint(100000, 999999)
            user_to_update.update(referral_code=referral_code)
        token = MyToken.objects.get_or_create(user=user)[0]
        confirmation.delete()
        return JsonResponse({'AuthToken': f'{token.key}', 'referral code': referral_code}, status=200)


class ProfileView(APIView):
    authentication_classes = [authentication.MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ReferralUserSerializer(request.user)
        return JsonResponse(serializer.data, status=200)
