import os
import pandas as pd  # For Excel file generation
from fpdf import FPDF  # For PDF file generation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import zipfile
from io import BytesIO
import time

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
REPORT_FOLDER = os.path.join(os.getcwd(), 'reports')

os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# func no 1

def get_latest_uploaded_file(folder):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        raise FileNotFoundError("No files found in the upload folder.")
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(folder, x)))
    return os.path.join(folder, latest_file)


def read_uploaded_files():
    """
    Reads the latest uploaded file from the UPLOAD_FOLDER.
    Returns a DataFrame.
    """
    try:
        latest_file_path = get_latest_uploaded_file(UPLOAD_FOLDER)
        if latest_file_path.endswith('.csv'):
            df = pd.read_csv(latest_file_path, header=[0,1])
        elif latest_file_path.endswith('.xlsx'):
            df = pd.read_excel(latest_file_path, header=[0,1])
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
        df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

        return df
    except Exception as e:
        print(f"Error reading uploaded files: {e}")
        return None
df = read_uploaded_files()



def get_dataset_info():
    dataset_info = {
        'columns': df.columns.tolist(),
        'shape': df.shape,
        'sample_data': df.head().to_dict(orient='records')
    }
    return dataset_info



# func no 2
def subject_wise_attendance(df):
  attendance = {}
  for Subject in df.columns:
    if Subject.endswith('Attendance Percent'):
      attendance[Subject] = df[Subject].mean()
  return pd.Series(attendance)


# func no 3
# heatmap
def generate_heatmap(df):
    # Get relevant columns
    attendance_columns = subject_wise_attendance(df).index
    filtered_df = df[attendance_columns]
    # Create the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(filtered_df.corr(), cmap='coolwarm', annot=True)
    plt.title('Correlation Heatmap for Attendance Percentages')
    # Save to BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()  # Close the figure to release resources

    return img_buffer



# func no 5
def create_and_save_attendance_table(df, filename="attendance_table.png"):
    average_attendances = subject_wise_attendance(df)
    attendance_table = pd.DataFrame({'Subject': average_attendances.index, 'Average Attendance (%)': average_attendances.values})
    print(attendance_table)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('off')
    table = ax.table(
        cellText=attendance_table.values,
        colLabels=attendance_table.columns,
        loc='center',
        colLoc='left',  # or 'right' or 'center' to apply to all columns
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    img_buffer = io.BytesIO()
    plt.savefig(filename, bbox_inches='tight', dpi=600)
    plt.savefig(img_buffer, format='png', bbox = 'tight', dpi = 600)
    img_buffer.seek(0)
    plt.close()  # Close the figure to release resources
    return img_buffer

# add function wiht get_students_by_subject_and_category
def attendance_categories(df):
    attendance_categories_df = pd.DataFrame()
    attendance_categories_df['Student Name'] = df['Subject_Student Name']
    attendance_categories_df['Student Reg. No'] = df['Subject_Student Reg No']
    categories = [75, 65, 50]
    subject_columns = [col for col in df.columns if col.endswith('Attendance Percent')]

    for subject_col in subject_columns:
        subject = subject_col.split('_')[0]
        attendance_categories_df[f'{subject}_Attendance Category'] = pd.cut(
            df[subject_col],
            bins=[0, 50, 65, 75, 100],
            labels=['50Below', '50to65', '65to75', '75Above'],
            include_lowest=True
        )

    return attendance_categories_df
attendance_categories_df = attendance_categories(df)


# func no 6
'''
def get_students_by_subject_and_category(attendance_categories_df):
    subject_columns = [col for col in attendance_categories_df.columns if col.endswith('Attendance Category')]
    if not subject_columns:
        raise ValueError("No columns ending with 'Attendance Category' found in attendance_categories_df.")
    
    categories = attendance_categories_df[subject_columns[0]].dropna().unique().tolist()
    result_df = pd.DataFrame(columns=['Subject'] + [f'{cat}_Students' for cat in categories] + [f'{cat}_Count' for cat in categories])

    for subject_col in subject_columns:
        subject_name = subject_col.split('_')[0]
        row_data = {'Subject': subject_name}
        for category in categories:
            filtered_df = attendance_categories_df[attendance_categories_df[subject_col] == category]
            student_names = filtered_df['Student Name'].tolist()

            # Store student names as comma-separated string or "NONE"
            row_data[f'{category}_Students'] = ", ".join(student_names) if student_names else "NONE"
            row_data[f'{category}_Count'] = len(student_names)

        result_df = pd.concat([result_df, pd.DataFrame([row_data])], ignore_index=True)

    return result_df
'''

def get_students_by_subject_and_category(attendance_categories_df):
    subject_columns = [col for col in attendance_categories_df.columns if col.endswith('Attendance Category')]
    categories = attendance_categories_df[subject_columns[0]].unique().tolist()
    result_df = pd.DataFrame(columns=['Subject'] + [f'{cat}_Students' for cat in categories] + [f'{cat}_Count' for cat in categories])

    for subject_col in subject_columns:
        subject_name = subject_col.split('_')[0]
        row_data = {'Subject': subject_name}
        for category in categories:
            filtered_df = attendance_categories_df[attendance_categories_df[subject_col] == category]
            student_names = filtered_df['Student Name'].tolist()

            # Store student names as a list
            row_data[f'{category}_Students'] = student_names 
            row_data[f'{category}_Count'] = len(student_names)

        result_df = pd.concat([result_df, pd.DataFrame([row_data])], ignore_index=True)

    return result_df

# Example usage:
# get_students_by_subject_and_category_df = get_students_by_subject_and_category(attendance_categories_df)


# Example usage:
get_students_by_subject_and_category_df = get_students_by_subject_and_category(attendance_categories_df)



# func no 7
def visualize_count_columns(df):
    count_cols = [col for col in df.columns if col.endswith('Count')]
    count_df = df[['Subject'] + count_cols]  

    melted_df = pd.melt(count_df, id_vars=['Subject'], value_vars=count_cols, 
                        var_name='Attendance Category', value_name='Count')

    plt.figure(figsize=(12, 8)) 
    ax = sns.barplot(data=melted_df, x='Subject', y='Count', hue='Attendance Category')
    
    # Add count labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%d')
    
    plt.title('Student Count in Each Attendance Category by Subject')
    plt.xlabel('Subject')
    plt.ylabel('Number of Students')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.tight_layout()
    plt.legend(title='Attendance Category')  # Add a legend

    # Save to BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=600)
    img_buffer.seek(0)
    plt.close()  # Close the figure to release resources

    return img_buffer

# Assuming 'get_students_by_subject_and_category_df' is your DataFrame
visualize_count_columns(get_students_by_subject_and_category_df)



# funciton no 8
def download_dataframe_as_excel(df, file_name='report.xlsx', sheet_name='Sheet1'):
    try:
        # Construct the full file path in the REPORT_FOLDER
        file_path = os.path.join(REPORT_FOLDER, file_name)

        # Save DataFrame to Excel
        df.to_excel(file_path, index=False, sheet_name=sheet_name)
        print(f"Excel file saved as {file_path}")
        return file_path
    except Exception as e:
        print(f"An error occurred while saving the Excel file: {e}")
        return None


# function no 9
def identify_students_needing_support(attendance_categories_df, intervention_threshold=50, monitoring_threshold=65):
    subject_columns = [col for col in attendance_categories_df.columns if col.endswith('Attendance Category')]
    support_needs_df = pd.DataFrame(columns=['Subject', 'Intervention', 'Monitoring', 'Reinforcement'])

    for subject_col in subject_columns:
        subject_name = subject_col.split('_')[0]
        
        # Intervention: Attendance below intervention_threshold
        intervention_students = attendance_categories_df[attendance_categories_df[subject_col] == '50Below']['Student Name'].tolist()
        
        # Monitoring: Attendance between intervention_threshold and monitoring_threshold
        monitoring_students = attendance_categories_df[attendance_categories_df[subject_col] == '50to65']['Student Name'].tolist()
        
        # Reinforcement: Attendance above monitoring_threshold but below 75 (can be adjusted)
        reinforcement_students = attendance_categories_df[attendance_categories_df[subject_col] == '65to75']['Student Name'].tolist()

        # Convert any non-string elements to strings before joining
        intervention_students = [str(student) for student in intervention_students]
        monitoring_students = [str(student) for student in monitoring_students]
        reinforcement_students = [str(student) for student in reinforcement_students]

        support_needs_df = pd.concat([support_needs_df, pd.DataFrame([{
            'Subject': subject_name,
            'Intervention': ', '.join(intervention_students) if intervention_students else "NONE",
            'Monitoring': ', '.join(monitoring_students) if monitoring_students else "NONE",
            'Reinforcement': ', '.join(reinforcement_students) if reinforcement_students else "NONE"
        }])], ignore_index=True)

    return support_needs_df

support_needs_df = identify_students_needing_support(attendance_categories_df)

# Convert to JSON and store in a variable
support_needs_json_data = support_needs_df.to_json(orient='records')





def generate_zip_report():
    """
    Generates a ZIP file containing the Excel and PDF reports.
    """
    try:
        # Create a BytesIO object to store the ZIP file in memory
        zip_buffer = BytesIO()

        # Create a ZIP archive
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Generate the Excel report
            excel_file_path = download_dataframe_as_excel(get_students_by_subject_and_category_df, file_name='attendance_report.xlsx')
            if excel_file_path:
                zip_file.write(excel_file_path, arcname='attendance_report.xlsx')

            # Generate the PDF report
            from APP.pdf_generate import export_pdf
            pdf_file_path = export_pdf('AI', '2022-2026')  # Replace with actual parameters
            if pdf_file_path and os.path.exists(pdf_file_path):
                zip_file.write(pdf_file_path, arcname='attendance_analysis_report.pdf')


        # Reset the buffer's position to the beginning
        zip_buffer.seek(0)

        return zip_buffer

    except Exception as e:
        print(f"An error occurred while generating the ZIP file: {e}")
        return None