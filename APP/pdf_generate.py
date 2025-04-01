from fpdf import FPDF
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
# Define the REPORT_FOLDER
# REPORT_FOLDER = os.path.join(os.getcwd(), 'reports')
REPORT_FOLDER = os.path.join(os.getcwd(), 'reports')
os.makedirs(REPORT_FOLDER, exist_ok=True)  # Ensure the folder exists

class AttendanceReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
        # Define paths as instance variables
        self.poornima_logo_path = os.path.join(os.getcwd(), 'pdf_template_img', 'poornima_logo.png')
        self.nexusiq_logo_path = os.path.join(os.getcwd(), 'pdf_template_img', 'nexusiq_logo.png')
        self.education_stock_path = os.path.join(os.getcwd(), 'pdf_template_img', 'education_stock.png')

    def header(self):
        if self.page_no() == 1:
            pass
        else:
            if os.path.exists(self.poornima_logo_path):
                self.image(self.poornima_logo_path, 10, 10, 50)
            if os.path.exists(self.nexusiq_logo_path):
                self.image(self.nexusiq_logo_path, 160, 8, 40)
            self.set_line_width(0.5)
            self.line(10, 25, 200, 25)
            
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'L')
        self.cell(0, 10, 'Powered by NexusIQ', 0, 0, 'R')
            
    def cover_page(self, dept, year):
        self.add_page()
        if os.path.exists(self.poornima_logo_path):
            self.image(self.poornima_logo_path, 10, 10, 50)
        if os.path.exists(self.nexusiq_logo_path):
            self.image(self.nexusiq_logo_path, 160, 10, 40)
            
        self.set_font('Arial', 'B', 24)
        self.set_text_color(43, 57, 144)
        self.set_y(60)
        self.cell(0, 15, 'ATTENDANCE ANALYSIS REPORT', 0, 1, 'C')
        
        if os.path.exists(self.education_stock_path):
            self.image(self.education_stock_path, 55, 80, 100)
            
        self.set_y(-80)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f'Department: {dept}', 0, 1, 'L', False)
        self.cell(0, 10, f'Academic Year: {year}', 0, 1, 'L', False)
        self.cell(0, 10, f'Generated on: {time.strftime("%d-%m-%Y")}', 0, 1, 'L', False)
        
    def add_content_page(self, title, content=None):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(43, 57, 144)
        self.set_y(40)
        self.cell(0, 10, title, 0, 1, 'L')
        if content:
            self.set_font('Arial', '', 11)
            self.set_text_color(51, 51, 51)
            self.multi_cell(0, 10, content)
            
    def add_table_page(self, subject, data):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(43, 57, 144)
        self.cell(0, 10, subject, 0, 1, 'C')  # Title of the page (Subject)
        self.ln(10)  # Add some vertical space

        # Table headers
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 200, 200)
        self.cell(60, 10, 'Intervention', 1, 0, 'C', fill=True)
        self.cell(60, 10, 'Monitoring', 1, 0, 'C', fill=True)
        self.cell(60, 10, 'Reinforcement', 1, 1, 'C', fill=True)

        # Table rows
        self.set_font('Arial', '', 12)
        max_rows = max(len(data['Intervention']), len(data['Monitoring']), len(data['Reinforcement']))
        for i in range(max_rows):
            self.cell(60, 10, data['Intervention'][i] if i < len(data['Intervention']) else '', 1, 0, 'C')
            self.cell(60, 10, data['Monitoring'][i] if i < len(data['Monitoring']) else '', 1, 0, 'C')
            self.cell(60, 10, data['Reinforcement'][i] if i < len(data['Reinforcement']) else '', 1, 1, 'C')


def export_pdf(department, academic_year):
    try:

        from APP.model import read_uploaded_files, generate_heatmap, create_and_save_attendance_table, identify_students_needing_support
        df = read_uploaded_files()

        report = AttendanceReport()
        report.cover_page(department, academic_year)
        
        # Generate heatmap and add it to the PDF
        heatmap_buffer = generate_heatmap
        report.add_content_page("Attendance Heatmap", content="Heatmap added here.")
        
        # Generate attendance table and add it to the PDF
        attendance_table_buffer = create_and_save_attendance_table
        report.add_content_page("Attendance Table", content="Attendance table added here.")
        
        # Generate support-needed JSON data and add it to the PDF
        support_need_json_data = identify_students_needing_support(df)
        for subject_data in support_need_json_data:
            report.add_table_page(subject_data['Subject'], subject_data)
        
        # Save the PDF in the REPORT_FOLDER
        pdf_path = os.path.join(REPORT_FOLDER, 'attendance_analysis_report.pdf')
        report.output(pdf_path)
        print(f"PDF generated successfully at: {pdf_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

export_pdf(
    department="Computer Science",
    academic_year="2023-2024"
)
# Example usage
# export_pdf(
#     department="Computer Science",
#     academic_year="2023-2024"
# )

