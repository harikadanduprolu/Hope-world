import json
from flask import Flask, render_template, request
import sqlite3
import pandas as pd


import matplotlib.pyplot as plt


app = Flask(__name__)


@app.route('/')
def index():
  return render_template('lalal.html')


@app.route('/lalal.html', methods=['GET'])
def lalal():
    selected_section = request.args.get('section')

    # Replace with your logic to populate cards data for About section
    about_cards = [  # Replace with actual data from database or other sources
        {'title': 'Card Title 1 (About)', 'content': 'Content for card 1 (About)'},
        {'title': 'Card Title 2 (About)', 'content': 'Content for card 2 (About)'},
    ]

    # Replace with your logic to populate cards data for Home section (optional)
    home_cards = [  # Replace with actual data (optional)
        {'title': 'Card Title 1 (Home)', 'content': 'Content for card 1 (Home)'},
        {'title': 'Card Title 2 (Home)', 'content': 'Content for card 2 (Home)'},
    ]

    if selected_section == 'about':
        cards = about_cards  # Use cards specific to About section
    elif selected_section=='home':
        cards = home_cards  # Use cards specific to Home section (or None if not needed)

    return render_template('lalal.html', cards=cards, selected_section=selected_section)

@app.route('/lalal.html/home',methods=['GET'])
def lol():
   about_cards = [  # Replace with actual data from database or other sources
        {'title': 'Card Title 1 (About)', 'content': 'Content for card 1 (About)'},
        {'title': 'Card Title 2 (About)', 'content': 'Content for card 2 (About)'},
    ]

    # Replace with your logic to populate cards data for Home section (optional)
   home_cards = [  # Replace with actual data (optional)
        {'title': 'Card Title 1 (Home)', 'content': 'Content for card 1 (Home)'},
        {'title': 'Card Title 2 (Home)', 'content': 'Content for card 2 (Home)'},
    ]
   cards=home_cards
   return render_template('lalal.html', cards=cards)

   
   


if __name__ == '__main__':
  app.run(debug=True)