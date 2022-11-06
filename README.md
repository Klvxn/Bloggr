## Bloggr

![Test workflow](https://github.com/klvxn/Bloggr/actions/workflows/bloggr_workflow.yml/badge.svg)
![Coverage ](/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a blog application built with Flask Framework.
It comes with basic CRUD functionalities.
Users can register, login into their accounts, add, edit and delete blogs they posted and more.

### Set Up
#### Requirements
1. Python 3.10
2. Flask 2.2.

#### Clone the repository
```
git clone https://github.com/Klvxn/Bloggr
```

#### Enter project root folder
```
cd Bloggr
```
#### Install and activate virtual environment
```
python venv .venv
```
Activate the virtual environment
```
.venv\Scripts\activate
```

#### Install dependencies
With the virtual env activated, update python package manager, 'pip' and install dependencies
```
pip install --upgrade pip
```
```
pip install -r requirements.txt
```

#### Start the local server
```
flask --app main --debug run
```

Open your browser and go to http://127.0.0.1:5000
There is currently no blogs or users in the database. You'd have to create an account to add or update blogs etc.

#### To run tests
```
coverage run -m pytest --disable-warnings
```