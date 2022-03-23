from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
import binascii
import os
from django.db import models
from django.utils.translation import gettext_lazy as _


class ReferralUser(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'."
                                         "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    referral_code = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(100000),
                                                                                   MaxValueValidator(999999)])

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class ConfirmationCode(models.Model):
    user = models.OneToOneField(ReferralUser, on_delete=models.CASCADE)
    code = models.PositiveSmallIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])


class MyToken(models.Model):

    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        ReferralUser, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name="referral_user"
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(MyToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key



