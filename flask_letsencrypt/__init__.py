"""
Let's Encrypt is a certificate authority that allows you to automatically
generate DV TLS certificates for domains that you control. This Flask extension
provides support for automatically responding to challenges that is sent from
time to time to ensure that you remain in control of the domain.

This extension specifically supports the 'Simple Http' part of the spec as
defined in `https://github.com/letsencrypt/acme-spec/blob/master/
draft-barnes-acme.md#simple-http`.

For the moment - there is no specific JWT signing support. The response is an
opaque blob that means something to the Let's Encrypt client.

Usage example:
    from flask import Flask
    from flask_letsencrypt import LetsEncrypt

    responses = {
        'foo': 'bar',
        'baz': 'gak',
    }

    # this should look up the challenge in a db or somesuch
    def handle_letsencrypt_challenge(challenge):
        return responses.get(challenge, None)

    app = Flask(__name__)
    le = LetsEncrypt(app)

    le.challenge_loader(handle_letsencrypt_challenge)

    app.run()
"""

from .core import LetsEncrypt


__all__ = [
    'LetsEncrypt',
]
