def simple_middleware(get_response):
    
    from base64 import b64encode
    from collections import OrderedDict
    from hashlib import sha256
    from hmac import HMAC
    from urllib.parse import urlparse, parse_qsl, urlencode

    from django.conf import settings

    def middleware(request):

        def is_valid(*, query: dict, secret: str) -> bool:
            """Check VK Apps signature"""
            vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))
            hash_code = b64encode(HMAC(secret.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
            decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
            return query.get("sign") == decoded_hash_code

        url = request.get_full_path()
        client_secret = settings.VK_SECRET_KEY  # Защищённый ключ из настроек вашего приложения

        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        status = is_valid(query=query_params, secret=client_secret)

        print("OK" if status else "FAIL")

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware