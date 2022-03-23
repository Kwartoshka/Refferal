from rest_framework import serializers
from backend.models import ReferralUser


class ReferralUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralUser
        fields = ('__all__')