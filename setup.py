from setuptools import setup, find_packages

setup(
    name="mind-wellness",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-marshmallow',
        'flask-jwt-extended',
        'flask-cors',
        'python-dotenv',
        'psycopg2-binary',
    ]
)
