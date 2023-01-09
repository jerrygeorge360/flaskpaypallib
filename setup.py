from setuptools import find_packages, setup
setup(
    name= 'flask-paypal-sdk',
    packages=find_packages(include=['flask-paypal-sdk']),
    version='0.0.1',
    description='Easy to use library for making your payments',
    long_description='This easy to use library ensures seamless integration of the paypal sdk into the flask framework.(More functionalities coming..)',
    author='Jerry George(Jbotrex)',
    author_email='jbotrex@gmail.com',
    url='https://github.com/jerrygeorge360',
    install_requires=['flask','requests','json'],
    tests_require=['uuid','pyjwt'],
    keywords=['python', 'paypal', 'sdk', 'flask', 'library', 'payment'],
    classifiers=[
        "Framework :: Flask",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    license='MIT',
)

