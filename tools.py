# import hashlib
# import hmac
# from datetime import datetime
# from json import dumps
# from math import floor
# import random
# import string
#
#
# def get_timestamp():
#     return str(floor(datetime.now().timestamp() * 1000))
#
#
# def create_nonce():
#     letters = string.ascii_lowercase
#     length = 36
#     rand_string = ''.join(random.choice(letters) for i in range(length))
#     return rand_string
#
#
# def get_auth_header(nicehash, xtime, xnonce, method, path, query, body=None):
#     message = bytearray(nicehash.key, 'utf-8')
#     message += bytearray('\x00', 'utf-8')
#     message += bytearray(str(xtime), 'utf-8')
#     message += bytearray('\x00', 'utf-8')
#     message += bytearray(xnonce, 'utf-8')
#     message += bytearray('\x00', 'utf-8')
#     message += bytearray('\x00', 'utf-8')
#     message += bytearray(nicehash.organization_id, 'utf-8')
#     message += bytearray('\x00', 'utf-8')
#     message += bytearray('\x00', 'utf-8')
#     message += bytearray(method, 'utf-8')
#     message += bytearray('\x00', 'utf-8')
#     message += bytearray(path, 'utf-8')
#     message += bytearray('\x00', 'utf-8')
#     message += bytearray(query, 'utf-8')
#
#     if body:
#         body_json = dumps(body)
#         message += bytearray('\x00', 'utf-8')
#         message += bytearray(body_json, 'utf-8')
#
#     digest = hmac.new(bytearray(nicehash.key, 'utf-8'), message, hashlib.sha256).hexdigest()
#     xauth = nicehash.api + ":" + digest
#
#     return xauth
#
#
#
