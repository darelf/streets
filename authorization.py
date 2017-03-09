import jwt, datetime, json

config = None
with open('config.json') as f:
    config = json.load(f)


def create_token(name):
    d = datetime.datetime.utcnow()
    d = d + datetime.timedelta(weeks=1)
    data = {
        'username': name,
        'exp': int(d.timestamp()),
        'iss': 'streetnode.dikaion.us'
    }
    return jwt.encode(data, config['secret_key'], algorithm='HS512')


def authorize(name, pword):
    if pword == config['simple_password']:
        return create_token(name)
    return None


def validate(token):
    v = None
    try:
        v = jwt.decode(token, config['secret_key'])
    finally:
        return v
