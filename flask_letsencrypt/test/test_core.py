from . import BaseTestCase

from flask_letsencrypt import LetsEncrypt


class SanityCheckTestCase(BaseTestCase):
    """
    This high level integration test makes sure that the basic set up and flow
    of sending a challenge/response works as expected.
    """

    def test_index(self):
        app = self.make_app()

        LetsEncrypt(app)

        with app.test_client() as c:
            response = c.get('/.well-known/acme-challenge')

            self.assertEqual(response.status_code, 404)

        # with a trailing slash
        with app.test_client() as c:
            response = c.get('/.well-known/acme-challenge/')

            self.assertEqual(response.status_code, 404)

    def test_challenge_missing(self):
        app = self.make_app()

        LetsEncrypt(app)

        with app.test_client() as c:
            response = c.get('/.well-known/acme-challenge/foobar')

            self.assertEqual(response.status_code, 404)

    def test_challenge_good(self):
        def check_challenge(challenge):
            self.assertEqual(challenge, 'dat-challenge')

            return 'foobar'

        app = self.make_app()

        le = LetsEncrypt(app)

        le.challenge_loader(check_challenge)

        with app.test_client() as c:
            response = c.get('/.well-known/acme-challenge/dat-challenge')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'text/plain')
            self.assertEqual(response.get_data(), b'foobar')

    def test_challenge_bad_return_type(self):
        """
        Return a non string when handling the challenge
        """
        def check_challenge(challenge):
            return object()

        app = self.make_app()

        le = LetsEncrypt(app)

        le.challenge_loader(check_challenge)

        with app.test_client() as c:
            with self.assertRaises(ValueError):
                c.get('/.well-known/acme-challenge/foobar')

    def test_challenge_exception(self):
        """
        Ensure that the correct exception is raised if an error occurs within
        the challenge
        """
        class TestException(Exception):
            pass

        def check_challenge(challenge):
            raise TestException

        app = self.make_app()

        app.testing = False
        app.debug = False

        le = LetsEncrypt(app)

        le.challenge_loader(check_challenge)

        with app.test_client() as c:
            response = c.get('/.well-known/acme-challenge/foobar')

            self.assertEqual(response.status_code, 500)


class ChallengeLoaderTestCase(BaseTestCase):
    """
    Tests for the challenge loader.
    """

    def test_function(self):
        le = LetsEncrypt()

        sentinel = object()

        le.challenge_loader(sentinel)

        self.assertIs(le._challenge_loader, sentinel)

    def test_decorator(self):
        le = LetsEncrypt()

        @le.challenge_loader
        def le_challenge():
            pass

        self.assertIs(le._challenge_loader, le_challenge)
