from app.utils.hashing import hash_password, verify_password


def test_password_return_hash():
    result = hash_password('mysecret123')
    assert isinstance(result, str)
    assert len(result) > 12

def test_password_is_different():
    result1 = hash_password('test')
    result2 = hash_password('test')
    assert result1 != result2

def test_verify_password_works():
    password = 'mysecret123'
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True
    assert verify_password('wrong_password', hashed) is False

def test_hash_empty_password():
    result = hash_password('')
    assert isinstance(result, str)
    assert len(result) > 0