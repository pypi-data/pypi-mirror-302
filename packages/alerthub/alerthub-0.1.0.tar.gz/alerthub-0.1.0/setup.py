from setuptools import setup, find_packages

setup(
    name='alerthub',  
    version='0.1.0',  
    description='A Python package for managing email services across multiple platforms',
    author='Harnath Atmakuri',
    author_email='akvdkharnath@gmail.com',
    url='https://github.com/akvdkharnath/alerthub',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'requests',
        'python-dotenv',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
