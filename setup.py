import os
import sys

from setuptools import setup, find_packages, Command


install_requires = [
    'Django>=1.3',
]


class RunTests(Command):
    """From django-celery"""
    description = "Run the django test suite from the tests dir."
    user_options = []
    extra_env = {}
    extra_args = ['auth_remember']

    def run(self):
        for env_name, env_value in self.extra_env.items():
            os.environ[env_name] = str(env_value)

        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "tests")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get(
                        "DJANGO_SETTINGS_MODULE", "settings")
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [''])
        prev_argv = list(sys.argv)
        try:
            sys.argv = [__file__, "test"] + self.extra_args
            execute_manager(settings_mod, argv=sys.argv)
        finally:
            sys.argv = prev_argv

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()


setup(
    name='django-auth-remember',
    version='0.3',
    url='https://github.com/ailabs/django-auth-remember/',
    license='MIT',
    author='Michael van Tellingen',
    author_email='m.vantellingen@auto-interactive.nl',
    description='Django app for remember-me functionality (using a token)',
    long_description=''.join(readme),
    install_requires=install_requires,
    zip_safe=False,
    cmdclass={"test": RunTests},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
    packages=find_packages(exclude=('example_project')),
)
