from setuptools import setup, find_packages

setup(
    name='sentiment_words',
    version='0.1',
    author='fouad attig algeria-2024',
    author_email="fouad.dbz@gmail.com",
    description='مكتبة الكلمات الإيجابية والسلبية.',
    packages=find_packages(),
    py_modules=['sentiment_words_arabic'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
