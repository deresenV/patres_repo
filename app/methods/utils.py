import bcrypt

def hash_password(plain_password: str) -> str:
    """
    Хэширует пароль.
    :param plain_password: Введенный пользователем пароль.
    :return: Хэшированный пароль в виде строки.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Проверка пароля'''
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))