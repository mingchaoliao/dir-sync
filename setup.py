from setuptools import setup

setup(
    name='google-drive-sync',
    version='0.1',
    description='Sync files in the local folder with files in the Google Drive folder',
    author='Mingchao Liao',
    author_email='mingchaoliao95@gmail.com',
    url='https://github.com/mingchaoliao/google-drive-sync',
    license='MIT',
    packages=['sync'],
    zip_safe=False,
    install_requires=['google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'google-drive-sync = sync.main:main'
        ]
    }
)
