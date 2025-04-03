from setuptools import setup, find_packages

setup(
    name="mind-wellness-backend",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-cors',
        'flask-jwt-extended',
        'flask-sqlalchemy',
        'python-dotenv',
        'stripe',
    ]
)
