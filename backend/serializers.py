from rest_framework import serializers
from backend.models import ReferralUser


class ShortReferralUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralUser
        fields = ('id', 'phone_number')

class ReferralUserSerializer(serializers.ModelSerializer):
    inviter = ShortReferralUserSerializer()
    class Meta:
        model = ReferralUser
        fields = ('__all__')
