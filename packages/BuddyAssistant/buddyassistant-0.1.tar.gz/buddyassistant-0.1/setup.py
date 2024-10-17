from setuptools import setup, find_packages

setup(
    name='BuddyAssistant',               
    version='0.1',                   
    description='BuddyAssistant is a conversational AI assistant.',  
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Anis Langar',
    author_email='anisd116@gmail.com',
    url='https://github.com/anislangar/buddyassistant',
    packages=find_packages(),
    license='MIT',
    classifiers=[],
    python_requires='>=3.6',
)
