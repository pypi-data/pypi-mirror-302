from setuptools import setup, find_packages

"""
Run `python setup.py sdist bdist_wheel` to build the package.
"""


def main() -> None:
    setup(
        name='BuildYourOwnEmbedding',
        version='1.0',
        packages=find_packages(),
        install_requires=[
            'numpy>=1.24.0',
            'matplotlib>=3.9.1',
            'matplotlib-inline>=0.1.6',
            'typing_extensions>=4.4.0',
            'mplcursors>=0.5.3',
            'scikit-learn>=1.3.0 ',
        ]
    )


if __name__ == "__main__":
    main()