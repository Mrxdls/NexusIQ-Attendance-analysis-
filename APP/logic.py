import os
from flask import send_file, flash, redirect, url_for, request
from datetime import datetime
# Define paths for schema files and uploaded datasets
  # Save files in the "uploads" folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
REPORT_FOLDER = os.path.join(os.getcwd(), 'reports')
SCHEMA_FOLDER = 'schema_files'
SCHEMA_FILE = 'Dataset_schema.csv'
# Ensure the folders exist
# os.makedirs(SCHEMA_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_home_data():
    """
    Provides data for the home page.
    """
    # Data for "What We Offer" section
    offers = [
        {"icon": "<i class='fas fa-chart-line'></i>", "title": "Analytics", "description": "Detailed attendance analytics."},
        {"icon": "<i class='fas fa-user-check'></i>", "title": "Tracking", "description": "Real-time attendance tracking."},
        {"icon": "<i class='fas fa-chart-pie'></i>", "title": "Visualization", "description": "Intuitive data visualizations."},
        {"icon": "<i class='fas fa-cogs'></i>", "title": "Automation", "description": "Automated attendance reports."}
    ]

    # Data for "Meet Our Team" section
    team = [
        {"name": "Ms. Appoorva Bansal", "role": "Assistant Professor, PCE<br>Project Guide & Mentor", 
         "linkedin": "#", "image": "images/team1.jpg"},
        {"name": "Mridul Soni", "role": "B.Tech Undergraduate, PCE", 
         "linkedin": "https://linkedin.com/in/mridulsoni", "image": "images/team2.jpg"},
        {"name": "Mohammed Sameen", "role": "B.Tech Undergraduate, PCE", 
         "linkedin": "#", "image": "images/team3.jpg"},
        {"name": "Shaily Sharma", "role": "B.Tech Undergraduate, PCE", 
         "linkedin": "#", "image": "images/team4.jpg"},
        {"name": "Divyam Upadhyay", "role": "B.Tech Undergraduate, PCE", 
         "linkedin": "#", "image": "images/team5.jpg"}
    ]

    # Data for social links
    socials = [
        {"icon": "fab fa-facebook", "link": "https://facebook.com"},
        {"icon": "fab fa-twitter", "link": "https://twitter.com"},
        {"icon": "fab fa-linkedin", "link": "https://linkedin.com"},
        {"icon": "fab fa-instagram", "link": "https://instagram.com"}
    ]

    # Contact email and current year
    contact_email = "2022pcecamridul037@poornima.org"
    current_year = datetime.now().year

    return {
        "offers": offers,
        "team": team,
        "socials": socials,
        "contact_email": contact_email,
        "current_year": current_year
    }
    
def handle_download(SCHEMA_FOLDER, SCHEMA_FILE):
    
    file_path = os.path.join(SCHEMA_FOLDER, SCHEMA_FILE)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(f"Error during file download: {e}")
        flash("File not found or an error occurred.", "error")
        return redirect(url_for('app_routes.services'))


def radio_buttons(button):
    analysis_type = request.form.get('dataset')
    if analysis_type == 'day-wise':
        flash('Day-Wise Analysis is currently unavailable. Please select another option.', 'error')
        return redirect(url_for('app_routes.services'))
    else:
        return button



def handle_upload(request):
    """
    Handles uploading a dataset.
    """
    if 'dataset' not in request.files:
        flash('No file part')
        return redirect(url_for('app_routes.services'))

    file = request.files['dataset']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('app_routes.services'))

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    flash('File uploaded successfully!')
    return redirect(url_for('app_routes.services'))