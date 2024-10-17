from setuptools import setup, find_packages

setup(
    name='latta-django-recorder',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django package for error reporting to Latta API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://latta.ai',
    author='Latta',
    author_email='info@latta.ai',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=4.2.12',
        'requests>=2.25.1',
        'psutil>=6.0.0'
    ],
)