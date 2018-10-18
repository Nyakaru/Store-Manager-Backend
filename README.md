# Store-Manager-Backend
A backend for a web application that helps store owners manage sales and product inventory records.

### Branches
* master - main branch: all source after review and feedback.
* develop - all the features developed.
* features - contains all the features created with all the necessary pages to allow the application function .


### Prerequisites
What you need to get started:
    
    Python 3: https://www.python.org/downloads/
    Flask: http://flask.pocoo.org/docs/1.0/installation/
    Flask_restful: https://flask-restful.readthedocs.io/en/latest/installation.html
    Pytest: https://docs.pytest.org/en/latest/getting-started.html
    


# Running and testing app
# Running:
```
$ virtualenv venv
$ cd venv
$ git clone https://github.com/Nyakaru/Store-Manager-Backend.git
$ source venv/bin/activate
$ cd fast_food_fast_backend
$ export APP_SETTINGS=development
$ export APP_SECRET_KEY="verysecret"
$ python run.py
```

# Testing

Follow the steps above then:

$ python -m pytest

## Endpoints

| URL                  | METHODS   | DESCRIPTION              |
| :---                 |     :---: |          ---:            |
| `/api/v1/products`   | POST      | Create a product         |
| `/api/v1/products`   | GET       | Fetch all products       |
| `/api/v1/products/1` | GET       | Fetch a single product   | 
| `/api/v1/sales`      | POST      | Create a sale order      |
| `/api/v1/sales`      | GET       | Fetch all sale orders    |
| `/api/v1/sales/1`    | GET       | Fetch a single sale order|


# Hosting 
https://store-manager-v1.herokuapp.com/

# Documentation
https://documenter.getpostman.com/view/5294981/RWgtTHYF

# Author

Kinara Nyakaru

# Contributions

This repo can be forked and contributed to.

[![Build Status](https://travis-ci.org/Nyakaru/Store-Manager-Backend.svg?branch=develop)](https://travis-ci.org/Nyakaru/Store-Manager-Backend)[![Coverage Status](https://coveralls.io/repos/github/Nyakaru/Store-Manager-Backend/badge.svg)](https://coveralls.io/github/Nyakaru/Store-Manager-Backend)

