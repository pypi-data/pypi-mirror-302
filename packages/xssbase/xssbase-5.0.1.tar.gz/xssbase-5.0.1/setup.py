from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='xssbase',
    version='5.0.1',
    description='XSSBase: A tool for testing XSS vulnerabilities on websites.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://mrfidal.in/cyber-security/xssbase',
    author='MrFidal',
    author_email='mrfidal@proton.me',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security',
    ],
    keywords='xss, cross-site scripting, vulnerability, scanning, security, mrfidal',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'xssbase': ['payload.txt'],  
    },
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'xssbase=xssbase.cli:main',  
        ],
    },
)
