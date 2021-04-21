def template(key, type, required, default=[], items=[]):
    if isinstance(type, str):
        default = ''
    elif isinstance(type, int):
        default = 0
    elif isinstance(type, bool):
        default = False

    obj = {
        'key': key,
        'type': type,
        'required': required,
        'default': default
    }

    if isinstance(type, list):
        obj['items'] = items

    return obj

user_schema = [
    template('id', int, True),
    template('username', str, False),
    template('password', str, False),
    template('current_password', str, False),
    template('new_password', str, False)
]