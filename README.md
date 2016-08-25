Flask-LetsEncrypt
=================

This Flask extension provides support for Let's Encrypt's ACME Simple Http
challenge/response. It provides the Http server that will respond to requests
from Let's Encrypt when it checks to ensure that you own the domain that you
are requesting a certificate for.

Usage example:

```python
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
```

You should replace foo/bar etc. with values that certbot provides you with.

Running the tests:

```python 
pip install tox

tox -e py27
```
