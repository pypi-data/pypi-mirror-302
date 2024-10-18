from setuptools import setup

setup(
    name='mimic_hand_api',
    version='04.1.0',
    description='API for the low-level control the motors in our hands (P4)',
    url='https://github.com/mimicrobotics/mimic_hand_api',
    author='Ben Forrai',
    author_email='ben.forrai@mimicrobotics.com',
    license='Closed source',
    packages=['mimic_hand_api'],
    install_requires=['google',
                      'protobuf',
                      'pyserial',
                      'setuptools',
                      'soupsieve',
                      'pyyaml'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
    ],
)
