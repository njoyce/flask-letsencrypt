from flask import abort
from flask_letsencrypt import compat


class LetsEncrypt(object):
    """
    :ivar _challenge_loader: The user supplied callable that provides responses
        to the challenges that this extension supplies. See
        :ref:`challenge_loader` for more information.
    :ivar app: The linked :ref:`flask.Flask` application instance.
    """

    def __init__(self, app=None):
        """
        Initialise this instance.

        :param app: The :ref:`flask.Flask` application instance. Can be `None`.
            If supplied, the app will be automatically configured. This allows
            support for delayed Flask app setup.
        """
        self._challenge_loader = None
        self.app = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        Link this extension to the Flask application. This sets up the views
        so that we can respond appropriately to the ACME challenges.

        It also registers itself as the `letsencrypt` extension on the app.

        :param app: The :ref:`flask.Flask` application instance.
        """
        self.app = app

        if not hasattr(app, 'extensions'):
            # support for Flask that does not create the extensions attribute
            app.extensions = {}

        app.extensions['letsencrypt'] = self

        self.register_views(app)

    def register_views(self, app):
        """
        Register all the view endpoints for this extension

        :param app: The :ref:`flask.Flask` application instance.
        """
        app.add_url_rule(
            '/.well-known/acme-challenge/<challenge>',
            'letsencrypt.challenge',
            self.handle_challenge
        )

    def challenge_loader(self, loader):
        """
        A user supplied callable must be registered on the instance before any
        Let's Encrypt request can be serviced.

        The callable takes one param that is the challenge token supplied by
        the request.

        When called, the challenge_loader must respond in one of these ways:
            - string -> Returned as part of the response body.
            - None (or other falsey boolean expressions) -> 404 response.
            - Exceptions will be propagated.
            - Anything else will generate an exception.

        This method can be used inline or as a decorator:
            from flask_letsencrypt import LetsEncrypt

            le = LetsEncrypt()

            @le.challenge_loader
            def my_loader(challenge):
                pass

        OR inline:
            from flask_letsencrypt import LetsEncrypt

            le = LetsEncrypt()

            def my_loader(challenge):
                pass

            le.challenge_loader(my_loader)

        :param loader: The user defined callable.
        :returns: The loader so that the decorator contract is upheld.
        """
        self._challenge_loader = loader

        return loader

    def handle_challenge(self, challenge):
        """
        This is the view function that handles all ACME Simple Http challenge
        requests. It wraps the user defined callable (see
        :ref:`challenge_loader` for more info on this) and ensures that the
        correct response/content type metadata is set.

        :param challenge: The challenge token that is supplied as part of the
            url of the request.
        """
        if not self._challenge_loader:
            self.app.logger.debug(
                'No `challenge_loader` has been set, ignoring request'
            )

            return abort(404)

        challenge_response = self._challenge_loader(challenge)

        if not challenge_response:
            return abort(404)

        if not isinstance(challenge_response, compat.basestring):
            raise ValueError(
                'Unexpected challenge response type (require a string)'
            )

        flask_response = self.app.make_response(challenge_response)

        # let's encrypt demands that the response type is set to text/plain
        flask_response.content_type = 'text/plain'

        return flask_response
