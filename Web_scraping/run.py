import unittest
from flask import Flask
from layout import app

if __name__ == '__main__':
    app.run(debug=True)