import re
import time
from django.core.exceptions import ObjectDoesNotExist
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

        try:
            user = ReferralUser.objects.get(phone_number=phone_number)
        except ObjectDoesNotExist:
            return JsonResponse({'Response': 'No such user'}, status=400)

        confirmation = ConfirmationCode.objects.filter(user=user)

        if not confirmation:
            return JsonResponse({'Response': 'No active code. Ask the code first'}, status=400)

        if confirmation.first().code != int(code):
            return JsonResponse({'Response': 'Wrong code'}, status=400)

        referral_code = user.referral_code

        if not referral_code:
            referral_code = randint(100000, 999999)
            user.referral_code = referral_code
            user.save()

        token = MyToken.objects.get_or_create(user=user)[0]
        confirmation.delete()
        return JsonResponse({'AuthToken': f'{token.key}', 'referral code': referral_code}, status=200)


class ProfileView(APIView):
    authentication_classes = [authentication.MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        related_users = ReferralUser.objects.filter(inviter=user)
        phones = [user.phone_number for user in related_users]
        serializer = ReferralUserSerializer(request.user)
        data = serializer.data
        data['invited users'] = phones
        return JsonResponse(data, status=200)

    def post(self, request):
        user = request.user
        inviter_code = request.data.get("inviter")
        if not inviter_code:
            return JsonResponse({'No inviter error': "Please, enter the inviter"}, status=400)
        try:
            inviter_code = int(inviter_code)
        except Exception:
            return JsonResponse({'Wrong referal code': "Please, enter the referal code as an example format '111111'"},
                         status=400)
        if not 100000 <= inviter_code <= 999999:
            return JsonResponse({'Wrong referal code': "Please, enter the referal code as an example format '111111'"},
                         status=400)
        if user.inviter:
            return JsonResponse({'Inviter already exists': "Sorry, but you've already added an inviter."},
                                status=400)
        try:
            inviter = ReferralUser.objects.get(referral_code=inviter_code)
        except ObjectDoesNotExist:
            return JsonResponse({'Wrong referral code': "User with this referral code does not exist"},
                                status=400)
        if inviter.inviter == user:
            return JsonResponse({'Wrong referral code': "You've already invited this user."
                                                        "He can not be invited by you"}, status=400)
        if user.referral_code == inviter_code:
            return JsonResponse({'Wrong referral code': "You can not invite yourself"}, status=400)
        user.inviter = inviter
        user.save()
        serializer = ReferralUserSerializer(request.user)
        data = serializer.data
        return JsonResponse(data, status=200)
