from setuptools import find_packages, setup

setup(
    name = 'Medical Chatbot',
    version= '0.0.0',
    author= 'Areeb Ahmed',
    author_email= 'areebahmed575@gmail.com',
    packages= find_packages(),
    install_requires = []

)

#find_packages() is a function that helps to find the packages in the project and will look for Constructor files in each and every folder and where it will get this particular file and folder that would be considered as my local package.So this is idea to create our local package
# -e . will look for setup.py and it will install the package