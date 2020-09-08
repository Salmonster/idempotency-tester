import pytest
import random
import string


def test_main_view(client):
    """
    Test that the main view loads.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Idempotency Tester' in response.data

def test_form_submit_new_key(client):
    """
    Test that a form submission with an idempotency key
    that is most likely not yet used DOES increment
    the account balance.
    """
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(7))
    response = client.post('/transact', data=dict(
        existing_balance='10550',
        idempotency_key=random_str,
        deposit_amount='15',
        idempotency_toggle=''
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Your balance is $10,565' in response.data

def test_form_submit_existing_key(client):
    """
    Test that a form submission with an idempotency key
    that is known to be already used doesn't increment
    the account balance.
    """
    response = client.post('/transact', data=dict(
        existing_balance='10565',
        idempotency_key='x8zfq',
        deposit_amount='100',
        idempotency_toggle=''
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Your balance is $10,565' in response.data
