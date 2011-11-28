from setuptools import setup, find_packages

install_requires = [
    'Django>=1.3',
]

setup(
    name='auth_remember',
    version='0.1',
    url='',
    license='MIT',
    author='Michael van Tellingen',
    author_email='m.vantellingen@auto-interactive.nl',
    description='Django rememberme app',
    long_description=__doc__,
    install_requires=install_requires,
    zip_safe=False,
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
