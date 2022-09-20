import os
import logging
import jwt

from flask import g, request, abort, make_response

def decode_cookie():
    print(jwt.__file__)
    cookie = request.cookies.get("user")
    print('Abrasado')
    print(cookie)

    if not cookie:
        g.cookie = {}
        return ('No cookie')

    try:
        g.cookie = jwt.decode(cookie,"\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR\xa1\xa8", algorithms=["HS256"])
    except jwt.InvalidTokenError as err:
        logging.warning(str(err))
        response = make_response("")
        response.set_cookie("user", expires=0, samesite='None', secure=True)
        return response