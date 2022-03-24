from rest_framework import serializers
from backend.models import ReferralUser


class ShortReferralUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralUser
        fields = ('referral_code',)

class ReferralUserSerializer(serializers.ModelSerializer):
    inviter = ShortReferralUserSerializer()
    class Meta:
        model = ReferralUser
        fields = ('__all__')
