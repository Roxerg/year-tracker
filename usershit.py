from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from goaldb import get_password_hash


def login_accepted(password):

    # just one user atm
    hash = get_password_hash("roxerg")

    return check_password_hash(hash, password)
