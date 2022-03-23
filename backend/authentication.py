from rest_framework.authentication import TokenAuthentication
from backend.models import MyToken


class MyTokenAuthentication(TokenAuthentication):
    model = MyToken
