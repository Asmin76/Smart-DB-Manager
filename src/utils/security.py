import bcrypt


def hash_password(password):
    """
    Convert a plain password into a secure bcrypt hash.
    """

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed.decode("utf-8")


def verify_password(password, password_hash):
    """
    Check whether the entered password matches
    the stored bcrypt hash.
    """

    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hash_bytes
    )