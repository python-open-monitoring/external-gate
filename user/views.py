import hashlib
from datetime import datetime
from datetime import timedelta
from json import JSONDecodeError

import jwt
from passlib.hash import pbkdf2_sha256
from simple_print import sprint
from starlette.authentication import requires
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from user_agents import parse

from .models import User
from mailer.mailer import Mailer
from settings import FRONTEND_URL
from settings import JWT_ALGORITHM
from settings import JWT_PREFIX
from settings import JWT_SECRET_KEY
from settings import PROJECT_MAIL


async def create_token(token_config: dict) -> str:

    expired = datetime.utcnow() + timedelta(minutes=token_config["expiration_minutes"])
    token = {
        "username": token_config["username"],
        "user_id": token_config["user_id"],
        "email": token_config["email"],
        "iat": datetime.utcnow(),
        "exp": expired,
    }

    if "get_expired_token" in token_config:
        token["sub"] = "token"
    else:
        token["sub"] = "refresh_token"

    token = jwt.encode(token, str(JWT_SECRET_KEY), algorithm=JWT_ALGORITHM)
    return str(token.decode())


async def user_register__default_1(request: Request) -> JSONResponse:

    # user/register/default/Monitoring3f2SX5w2nJhMuWtU

    username = "Andrey Sobolev"
    email = "email.asobolev@gmail.com"
    password = pbkdf2_sha256.hash("Monitoring3f2SX5w2nJhMuWtU^%")

    user_exist = await User.filter(email=email).first()
    if user_exist:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="You are already registered")

    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.password = password
    await new_user.save()

    token = await create_token({"email": email, "username": username, "user_id": new_user.id, "get_expired_token": 1, "expiration_minutes": 300000})
    refresh_token = await create_token({"email": email, "username": username, "user_id": new_user.id, "get_refresh_token": 1, "expiration_minutes": 10080})

    return JSONResponse(
        {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "token": f"{JWT_PREFIX} {token}",
            "refresh_token": f"{JWT_PREFIX} {refresh_token}",
        },
        status_code=200,
    )


async def user_register__default_2(request: Request) -> JSONResponse:

    # user/register/default/Monitoring3f2SX5w2nJhMuWtU

    username = "Andrey Sobolev"
    email = "mail.asobolev@yandex.ru"
    password = pbkdf2_sha256.hash("Monitoring3f2SX5w2nJhMuWtU^%")

    user_exist = await User.filter(email=email).first()
    if user_exist:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="You are already registered")

    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.password = password
    await new_user.save()

    token = await create_token({"email": email, "username": username, "user_id": new_user.id, "get_expired_token": 1, "expiration_minutes": 300000})
    refresh_token = await create_token({"email": email, "username": username, "user_id": new_user.id, "get_refresh_token": 1, "expiration_minutes": 10080})

    return JSONResponse(
        {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "token": f"{JWT_PREFIX} {token}",
            "refresh_token": f"{JWT_PREFIX} {refresh_token}",
        },
        status_code=200,
    )


async def user_register(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request")

    username = payload["username"]
    email = payload["email"]
    password = pbkdf2_sha256.hash(payload["password"])

    user_exist = await User.filter(email=email).first()
    if user_exist:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="You are already registered")

    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.password = password
    await new_user.save()

    mailer_message = Mailer(
        sender=PROJECT_MAIL,
        recipient_list=(f"{email}"),
        subject="You have successfully registered",
        letter_body=f"Welcome {username}! <br>Your login: {email} <br>Your password: {payload['password']} <hr>",
    )
    mailer_message.send_email()

    token = await create_token({"email": email, "username": username, "user_id": new_user.id, "get_expired_token": 1, "expiration_minutes": 300000})
    refresh_token = await create_token({"email": email, "username": username, "user_id": new_user.id, "get_refresh_token": 1, "expiration_minutes": 10080})

    return JSONResponse(
        {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "token": f"{JWT_PREFIX} {token}",
            "refresh_token": f"{JWT_PREFIX} {refresh_token}",
        },
        status_code=200,
    )


async def user_login(request: Request) -> JSONResponse:

    try:
        ua_string = request.headers.get("User-Agent", "<unknown>")
    except:
        ua_string = None

    if ua_string:
        user_agent = parse(ua_string)
        user_agent = str(user_agent)

    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request")

    email = payload["email"]
    password = payload["password"]

    user = await User.filter(email=email).first()
    if user:
        if pbkdf2_sha256.verify(password, user.password):
            user.last_login_date = datetime.now()
            await user.save()

            # mailer_message = Mailer(
            #     sender=PROJECT_MAIL, recipient_list=(f"{user.email}"), subject="You are logged to the Project!", letter_body=f"You are welcome {user.username}! Today at {datetime.now()} you entered the site from: <br> {user_agent}.",
            # )
            # mailer_message.send_email()

            token = await create_token({"email": user.email, "username": user.username, "user_id": user.id, "get_expired_token": 1, "expiration_minutes": 300000})
            refresh_token = await create_token({"email": user.email, "username": user.username, "user_id": user.id, "get_refresh_token": 1, "expiration_minutes": 10080})
            sprint(token, s=1, p=1)
            return JSONResponse(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "token": f"{JWT_PREFIX} {token}",
                    "refresh_token": f"{JWT_PREFIX} {refresh_token}",
                },
                status_code=200,
            )
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Invalid password")
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"No such user")


async def reset_password(request: Request) -> JSONResponse:

    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request")

    email = payload["email"]

    user = await User.filter(email=email).first()
    if user:
        time_now = datetime.now()
        user.reset_password_md5 = hashlib.md5((str(user.id) + str(JWT_SECRET_KEY) + str(time_now)).encode("utf-8")).hexdigest()
        await user.save()

        mailer_message = Mailer(
            sender=PROJECT_MAIL,
            recipient_list=(f"{email}"),
            subject="Update your password",
            letter_body=f"Hello dear user. To update the password for accessing your personal account, please follow the link below:<br><br> <a href='{FRONTEND_URL}/user/reset-password-confirm/#{user.reset_password_md5}'>UPDATE PASSWORD</a>",
        )
        mailer_message.send_email()

        return JSONResponse(
            {"user_id": user.id},
            status_code=200,
        )
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Invalid request. This email is not registered.")


async def reset_password_confirm(request: Request) -> JSONResponse:

    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request")

    reset_password_md5 = payload["reset_password_md5"]
    new_password_flag = payload["new_password_flag"]

    if new_password_flag == "no":
        user = await User.filter(reset_password_md5=reset_password_md5).first()
        if user:
            return JSONResponse(
                {"md5 check status": "Checked. It's correct md5", "user_email": user.email},
                status_code=200,
            )
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Invalid md5 hash.")
    elif new_password_flag == "yes":
        user = await User.filter(reset_password_md5=reset_password_md5).first()
        if user:
            new_password = pbkdf2_sha256.hash(payload["new_password"])
            user.password = new_password
            user.reset_password_md5 = None
            await user.save()
            return JSONResponse(
                {"Password change status": "Checked. It's correct md5. Password has been changed", "user_email": user.email},
                status_code=200,
            )
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Invalid md5 hash.")
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Invalid request. This password flag is incorrect.")


@requires("authenticated")
async def change_password(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request")

    email = request.user.email
    new_password = pbkdf2_sha256.hash(payload["new_password"])

    user = await User.filter(email=email).first()

    if user:
        user.password = new_password
        await user.save()

        mailer_message = Mailer(
            sender=PROJECT_MAIL,
            recipient_list=(f"{email}"),
            subject="Your password changed",
            letter_body=f"Hello dear user. Your password has been successfully changed.",
        )
        mailer_message.send_email()

        return JSONResponse(
            {"status": "Password changed.", "user_id": user.id},
            status_code=200,
        )
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Invalid request.")


@requires("authenticated")
async def refresh_token(request: Request) -> JSONResponse:

    # TODO blacklist redis

    username = request.user.username
    user_id = request.user.user_id
    email = request.user.email

    token = await create_token({"email": email, "username": username, "user_id": user_id, "get_expired_token": 1, "expiration_minutes": 300000})
    refresh_token = await create_token({"email": email, "username": username, "user_id": user_id, "get_refresh_token": 1, "expiration_minutes": 10080})

    return JSONResponse(
        {
            "id": user_id,
            "username": username,
            "email": email,
            "token": f"{JWT_PREFIX} {token}",
            "refresh_token": f"{JWT_PREFIX} {refresh_token}",
        },
        status_code=200,
    )
