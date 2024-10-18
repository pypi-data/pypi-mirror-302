from setuptools import setup, find_packages

def main():
    print("The Feeling Kindness is installed to this computer successfully")

setup(
    name='kindness',
    version='0.1',
    description='A package that promotes kindness',
    author='Codeboy28',
    author_email='surya.mail.personal@example.com',
    url='https://github.com/codeboyspace/kindness',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kindness=kindness.core:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
