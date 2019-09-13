import os
import random
import string
from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

from django.conf import settings
from django.contrib.auth.models import User



class VkBackend:
    def authenticate(self, request, *args, **kwargs):
        query_params = self.parse_vk_signature(request.get_full_path())
        signature_valid = self.validate_vk_signature(query=query_params, secret=settings.VK_SECRET_KEY)
        username = query_params.get("vk_user_id")

        if signature_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                password = self.create_password(settings.DEFAULT_USER_PASSWORD_LENGTH)
                # maybe send password to user later
                user = User(username=username)
                user.set_password(password)
                user.save()
            return user
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    @staticmethod
    def parse_vk_signature(url):
        return dict(parse_qsl(urlparse(url).query, keep_blank_values=True))


    @staticmethod
    def validate_vk_signature(query, secret):
        vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))
        hash_code = b64encode(
            HMAC(secret.encode(), 
            urlencode(vk_subset, doseq=True).encode(), sha256).digest()
        )
        decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
        return query.get("sign") == decoded_hash_code


    @staticmethod
    def create_password(length=16):
        chars = string.ascii_letters + string.digits + '!@#$%^&*'
        random.seed = (os.urandom(1024))
        return ''.join(random.choice(chars) for i in range(length))



class VkBackendREST(VkBackend):
    def authenticate(self, request, *args, **kwargs):
        user = super().authenticate(request, *args, **kwargs)
        return user, None if user else None


    def authenticate_header(self, *args, **kwargs):
        return None