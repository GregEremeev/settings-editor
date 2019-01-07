from setuptools import setup, find_packages


REQUIREMENTS = ('Flask==0.12.3', 'Flask-Admin==1.5.3', 'Flask-BasicAuth==0.2.0')


setup(
    name='settings-editor',
    author='Greg Eremeev',
    author_email='budulianin@gmail.com',
    version='0.1.0',
    license='BSD',
    url='https://github.com/Budulianin/settings-editor',
    py_modules=('settings_editor',),
    install_requires=REQUIREMENTS,
    description='Application with web GUI to change settings file',
    packages=find_packages(),
    extras_require={'dev': ['pdbpp==0.9.1']},
    classifiers=['Programming Language :: Python :: 3.6'],
    zip_safe=False,
    include_package_data=True
)
