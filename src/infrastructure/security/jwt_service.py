import datetime
from datetime import timedelta

import jwt

jwt_options = {
    "SECRET_KEY": "uY&$^'+1N9UGwwfMY.~`qht^HbzWo_@jp{Dqw%i*WTSSlY&BqOFJJ]VQraEl7]@",
    "ALGORITHM": "HS256",
    "EXPIRE_TIME_MINUTES": 15,
}


async def encode_jwt(
    payload: dict,
    expire_time_minutes: int = jwt_options.get("EXPIRE_TIME_MINUTES"),
    expire_time_days: int | None = None,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    elif expire_time_days:
        expire = now + datetime.timedelta(minutes=expire_time_days)
    else:
        expire = now + datetime.timedelta(minutes=expire_time_minutes)
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(
        to_encode,
        jwt_options.get("SECRET_KEY"),
        jwt_options.get("ALGORITHM"),
    )


async def decode_jwt(token: str) -> dict:
    payload = jwt.decode(token, jwt_options.get("SECRET_KEY"), algorithms=[jwt_options.get("ALGORITHM")])
    return payload
