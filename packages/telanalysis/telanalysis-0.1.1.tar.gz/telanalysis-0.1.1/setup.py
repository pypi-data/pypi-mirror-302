from setuptools import setup, find_packages

setup(
    name='telanalysis',  # Имя вашего пакета
    version='0.1.1',  # Версия вашего пакета
    description='A tool for analyzing Telegram channels, chats, and groups.',  # Краткое описание
    long_description=open('README.md').read(),  # Длинное описание из README
    long_description_content_type='text/markdown',  # Указываем тип содержимого для Markdown
    author='krakodjaba',  # Ваше имя
    author_email='op@santgbots.ru',  # Ваша почта
    url='https://github.com/krakodjaba/telanalysis',  # URL к вашему репозиторию
    packages=find_packages(),  # Автоматическое обнаружение пакетов
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Минимальная версия Python
    install_requires=[
         'pywebio',
         'jmespath',
         'emoji',
         'wordcloud',
         'phonenumbers',
         'validate_email',
         'pandas',
         'vaderSentiment',
        'nltk',
        'matplotlib',
        'networkx',
        'twine',
    ],
    entry_points={
        'console_scripts': [
            'telanalysis = telanalysis:starting',  # Убедитесь, что 'main' - это функция, которая запускает ваш код
        ],
    },
)
