from flask import request
from flask import render_template
from flask import Blueprint

import providers
tracker = Blueprint('tracker', __name__)

# Main view rendering the index page
@tracker.route('/')
def index():
    return render_template('index.html')

# Search view to get parcel informations and display the results
@tracker.route('/search', methods=['GET','POST'])
def search():
    parcel_code = request.form.get('parcel_code', None)
    provider = request.form.get('provider', 'EMS')
    parcels = []
    if(parcel_code):
        parcels = [getattr(providers, provider)(parcel=code).request() for code in parcel_code.replace(r'\s\s+', '').strip().split(',')]
    return render_template('result.html', data=parcels)
