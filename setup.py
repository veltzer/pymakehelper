import setuptools

setuptools.setup(
    name='pymakehelper',
    version='0.0.1',
    description='pymakehelper is set of useful command line tools to help with writing make files',
    long_description='pymakehelper is set of useful command line tools to help with writing make files',
    url='https://veltzer.github.io/pymakehelper',
    download_url='https://github.com/veltzer/pymakehelper',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='python command line shell utilities',
    packages=setuptools.find_packages(),
    install_requires=[
        'pytconf',  # for command line parsing
        'pylogconf',  # for logging
    ],
    entry_points={
        # order of console_scripts is the same order of files in the 'scripts' folder
        'console_scripts': [
            'pymakehelper_install=pymakehelper.scripts.install',
        ],
    },
)
