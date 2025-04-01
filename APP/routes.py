from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from APP.logic import handle_download, get_home_data, SCHEMA_FOLDER, SCHEMA_FILE, UPLOAD_FOLDER
from APP.model import get_dataset_info
from APP.model import generate_zip_report
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def home():
    """
    Renders the home page.
    """
    data = get_home_data()
    print("Rendering template: index.html")  # Debugging
    return render_template(
        'index.html',
        offers=data['offers'],
        team=data['team'],
        socials=data['socials'],
        contact_email=data['contact_email'],
        current_year=data['current_year']
    )

@app_routes.route('/radio_button', methods=['GET'])
def radio_button():
    analysis_type = request.args.get('dataset')
    if not analysis_type:
        flash('Please select an analysis type.')
        return redirect(url_for('app_routes.services'))
    if analysis_type == 'day-wise':
        flash('Day-Wise Analysis is currently unavailable. Please select another option.', 'error')
        return redirect(url_for('app_routes.services'))

    return render_template('app_routes.services')



@app_routes.route('/services')
def services():

    data = get_home_data()
    print("Rendering template: services.html")  # Debugging
    return render_template(
        'services.html',
        socials=data['socials'],
        contact_email=data['contact_email'],
        current_year=data['current_year']
    )

@app_routes.route('/services/download-schema', methods=['GET'])
def download_schema():
    """
    Route to download the schema file based on the selected analysis type.
    """
    analysis_type = request.args.get('dataset')  # Get the selected type directly

    if analysis_type == 'day-wise':
        flash("Day-Wise Analysis is currently unavailable. Please select another option.", "error")
        return redirect(url_for('app_routes.services'))

    if analysis_type == 'cumulative':
            return handle_download(SCHEMA_FOLDER, SCHEMA_FILE)

    # Default case (should not happen if buttons are properly hidden)
    flash("Invalid analysis type.", "error")
    return redirect(url_for('app_routes.services'))



@app_routes.route('/services/upload-dataset', methods=['POST'])
def upload_dataset():
    """
    Handles uploading a dataset.
    """
    # Get the selected analysis type
    analysis_type = request.form.get('dataset')

    # Check if "Day-Wise" is selected
    if analysis_type == 'day-wise':
        flash("Day-Wise Analysis is currently unavailable. Please select another option.", "error")
        return redirect(url_for('app_routes.services'))

    # Check if the file is included in the request
    if 'dataset_file' not in request.files:
        flash("No file part in the request.", "error")
        return redirect(url_for('app_routes.services'))

    file = request.files['dataset_file']

    # Check if a file is selected
    if file.filename == '':
        flash("No file selected for upload.", "error")
        return redirect(url_for('app_routes.services'))

    # Save the file to the upload folder
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        file.save(file_path)
        flash("File uploaded successfully!", "success")
    except Exception as e:
        print(f"Error during file upload: {e}")
        flash("An error occurred while uploading the file.", "error")

    return redirect(url_for('app_routes.report'))


# ===============================================================================


# app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/report', methods=['GET'])
def report():
    """
    Renders the report page with dataset information.
    """

    data = get_home_data()
    print("Rendering template: report.html")  # Debugging
    dataset_info = get_dataset_info()
    return render_template(
        'report.html',
        dataset_info=dataset_info,
        socials=data['socials'],
        contact_email=data['contact_email'],
        current_year=data['current_year']
    )


    # return render_template('report.html', dataset_info=dataset_info)


@app_routes.route('/report/download', methods=['GET'])
def download_zip_report():
    try:
        zip_buffer = generate_zip_report()
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name='analysis_reports.zip',
            mimetype='application/zip'
        )
    except Exception as e:
        print(f"Error during ZIP file generation: {e}")
        flash("An error occurred while generating the ZIP file.", "error")
        return redirect(url_for('app_routes.report'))
    



@app_routes.route('/report/upload-dataset', methods=['GET', 'POST'])
def re_upload():
    """
    Placeholder route for uploading another dataset.
    """
    # Logic for uploading another dataset will be added here
    return render_template('services.html')


@app_routes.route('/report/email', methods=['GET', 'POST'])
def email_report():
    """
    Placeholder route for emailing the report.
    """
    # Logic for emailing the report will be added here
    return "Email Report route is under construction."