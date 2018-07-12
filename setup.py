from setuptools import setup, find_packages

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='django-role',
    url='https://github.com/sekomy/django-role',
    author='Sekom Yazilim',
    author_email='info@sekomyazilim.com.tr',
    license='MIT',
    description='Django Role',
    long_description=long_description,
    packages=find_packages(exclude=['docs', 'tests*']),
    platforms=['any'],
    include_package_data=True,
    install_requires=[
        'django-guardian>=1.4.8,<2.0',
        'django-mptt>=0.8.1',
        'django-tls-middleware>=1.0<2.0',
    ],
)
