import os

from setuptools import setup

if os.environ.get('CONVERT_README'):
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
else:
    long_description = ''

setup(
    name='dir-sync',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Sync files in the local folder with files in the remote location, e.g. Google Drive.',
    long_description=long_description,
    author='Mingchao Liao',
    author_email='mingchaoliao95@gmail.com',
    url='https://github.com/mingchaoliao/dir-sync',
    license='MIT',
    packages=['sync'],
    zip_safe=False,
    install_requires=['google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib', 'setuptools_scm'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dir-sync = sync.main:main'
        ]
    }
)
