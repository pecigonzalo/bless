import os

import pytest

from bless.aws_lambda.bless_lambda import lambda_handler_host
from tests.ssh.vectors import EXAMPLE_RSA_PUBLIC_KEY, RSA_CA_PRIVATE_KEY_PASSWORD, \
    EXAMPLE_ED25519_PUBLIC_KEY, EXAMPLE_ECDSA_PUBLIC_KEY


class Context(object):
    aws_request_id = 'bogus aws_request_id'
    invoked_function_arn = 'bogus invoked_function_arn'


VALID_TEST_REQUEST = {
    "public_key_to_sign": EXAMPLE_RSA_PUBLIC_KEY,
    "hostnames": "thisthat.com",
}

INVALID_TEST_REQUEST = {
    "public_key_to_sign": EXAMPLE_RSA_PUBLIC_KEY,
    "hostname": "wrongfieldname",
}

os.environ['AWS_REGION'] = 'us-west-2'


def test_basic_local_request():
    output = lambda_handler_host(VALID_TEST_REQUEST, context=Context,
                            ca_private_key_password=RSA_CA_PRIVATE_KEY_PASSWORD,
                            entropy_check=False,
                            config_file=os.path.join(os.path.dirname(__file__), 'bless-test.cfg'))
    print(output)
    assert output['certificate'].startswith('ssh-rsa-cert-v01@openssh.com ')


def test_invalid_request():
    output = lambda_handler_host(INVALID_TEST_REQUEST, context=Context,
                            ca_private_key_password=RSA_CA_PRIVATE_KEY_PASSWORD,
                            entropy_check=False,
                            config_file=os.path.join(os.path.dirname(__file__), 'bless-test.cfg'))
    assert output['errorType'] == 'InputValidationError'
