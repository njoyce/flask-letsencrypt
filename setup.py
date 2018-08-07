from setuptools import find_packages, setup

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


def get_requirements(filename):
    try:
        from pip._internal.download import PipSession
        session = PipSession()
    except ImportError:
        from pip.download import PipSession
        session = PipSession()
    except Exception:
        session = None

    reqs = parse_requirements(filename, session=session)

    return [str(r.req) for r in reqs]


setup_args = dict(
    name='flask-letsencrypt',
    version='0.2',
    maintainer='Nick Joyce',
    maintainer_email='nick.joyce@realkinetic.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    tests_require=get_requirements('requirements_dev.txt'),
)


if __name__ == '__main__':
    setup(**setup_args)
