from setuptools import setup, find_packages

setup(
    name='rvd_ap',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='ARAVIND SREE U',
    author_email='uaravindsree@gmail.com',
    description='My description will help you to pass time and understand my ability of writing codes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AravindSreeU/rvd_ap',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
