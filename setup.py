from setuptools import find_packages, setup

from pip.req import parse_requirements


def get_requirements(filename):
    try:
        from pip.download import PipSession

        session = PipSession()
    except ImportError:
        session = None

    reqs = parse_requirements(filename, session=session)

    return [str(r.req) for r in reqs]


setup_args = dict(
    name='flask-letsencrypt',
    version='0.1',
    maintainer='Nick Joyce',
    maintainer_email='nick@boxdesign.co.uk',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    tests_require=get_requirements('requirements_dev.txt'),
)


if __name__ == '__main__':
    setup(**setup_args)
