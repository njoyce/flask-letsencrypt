import unittest

from flask import Flask


class BaseTestCase(unittest.TestCase):
    """
    Base test case to set up an app and be able to run it
    """

    def make_app(self, name=__name__, config=None, response_class=None,
                 test_client_class=None):
        """
        Returns a Flask application ready for use in testing.

        :param config: The config dict supplied to the app creation.
        :param test_client_class: See `http://flask.pocoo.org/docs/0.10/api/
            #flask.Flask.test_client_class`.
        :param response_class: See `http://flask.pocoo.org/docs/0.10/api/
            #flask.Flask.response_class`.
        """
        config = config or {}

        config.setdefault('SECRET_KEY', 'unittest')
        config.setdefault('TESTING', True)

        app = Flask(name)

        app.config.update(config)

        if test_client_class:
            app.test_client_class = test_client_class

        if response_class:
            app.response_class = response_class

        return app
