from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(props: str):
    return pwd_context.hash(props)

def verify(plain_text, hash_text):
    return pwd_context.verify(plain_text, hash_text)