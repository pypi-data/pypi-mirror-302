from setuptools import setup, find_packages

setup(
    name='wak',  
    version='1.0',
    description= "Bibliothèque Python pour extraire les données financières de la Bourse de Casablanca, y compris les cours historiques des actions, les dividendes, et d'autres informations.",
    author='Ayoub KAMEL',
    author_email='ayoub@kamel.ma', 
    url='https://kamel.ma',  
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'lxml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    project_urls={  
        'Documentation': 'https://github.com/votre-utilisateur/ayoub',  
        'Source': 'https://github.com/votre-utilisateur/ayoub',  
        'Github': 'https://github.com/Ayoub-Kamel',
        'Linkedin': 'https://www.linkedin.com/in/ayoub-kamel/' 
    }
)
