from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for donations
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100), nullable=False)
    food_details = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    ngo = db.Column(db.String(100), nullable=False)
    donation_time = db.Column(db.String(100), nullable=False)  # Date and time as string

# Create the database tables and clear any previous records
with app.app_context():
    db.create_all()
    # db.session.query(Donation).delete()   # Optional: Uncomment if you want to clear old records on startup
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_donation', methods=['POST'])
def submit_donation():
    try:
        # Get the data from the request
        data = request.json
        donor_name = data['donorName']
        food_details = data['foodDetails']
        quantity = float(data['quantity'])
        location = data['location']
        ngo = data['ngo']
        donation_time = data['donationTime']

        # Create a new Donation entry
        new_donation = Donation(
            donor_name=donor_name,
            food_details=food_details,
            quantity=quantity,
            location=location,
            ngo=ngo,
            donation_time=donation_time
        )

        # Add and commit the donation to the database
        db.session.add(new_donation)
        db.session.commit()

        return jsonify({'success': True})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False}), 500

@app.route('/donations')
def donations():
    # Fetch all donation records from the database
    all_donations = Donation.query.all()
    return render_template('donations.html', donations=all_donations)

# New route to handle deletion
@app.route('/delete_donation', methods=['POST'])
def delete_donation():
    donation_id = request.form.get('donation_id')
    if donation_id:
        # Find the donation by ID and delete it
        donation_to_delete = Donation.query.get(donation_id)
        if donation_to_delete:
            db.session.delete(donation_to_delete)
            db.session.commit()
    return redirect(url_for('donations'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
