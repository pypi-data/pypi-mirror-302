from setuptools import setup, find_packages

setup(
    name='task1_semichkaa-uWu',
    version='1.0.0',
    description='Калькулятор',
    author='Victor',
    author_email='logday2017@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'task_1=task1_package.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
