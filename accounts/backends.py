from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

from django.conf import settings
from django.contrib.auth.models import User



class VkBackend:
    def authenticate(self, request, username=None, password=None, *args, **kwargs):

        url = request.get_full_path()
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        signature_valid = self.validate_vk_signature(query=query_params, secret=settings.VK_SECRET_KEY)
        username = query_params.get("vk_user_id")

        if signature_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    @staticmethod
    def validate_vk_signature(query, secret):
        vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))
        hash_code = b64encode(
            HMAC(secret.encode(), 
            urlencode(vk_subset, doseq=True).encode(), sha256).digest()
        )
        decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
        return query.get("sign") == decoded_hash_code



class VkBackendREST(VkBackend):
    def authenticate(self, request, username=None, password=None, *args, **kwargs):

        url = request.get_full_path()
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        signature_valid = self.validate_vk_signature(query=query_params, secret=settings.VK_SECRET_KEY)
        username = query_params.get("vk_user_id")

        if signature_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user, None
        return None


    def authenticate_header(self, *args, **kwargs):
        return None