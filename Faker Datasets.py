# Databricks notebook source
!pip install Faker faker-credit-score fpdf reportlab

# COMMAND ----------

# !pip install reportlab

# COMMAND ----------

# !pip install reportlab

# COMMAND ----------

from faker import Faker
import random
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from fpdf import FPDF
import json

# COMMAND ----------

fake = Faker('en_US')
first_name = 'N'
last_name = 'D'
address = '123 Main Street, Anytown, USA, 11111'
city= 'Anytown'
state = 'Anytown'
zip = '11111'
ssn_last_four = random.randint(1000, 9999)
employer_name = 'ABC LLC'
employer_address = '1, A Street, USA'
annual_salary = 120000
seller_name = "Cars of Hollywood"
seller_address = "123 Hollywood Street, Los Angeles, CA"
fake = Faker('en_US')
date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d")

# COMMAND ----------

# DBTITLE 1,W2

fake = Faker('en_US') # Use en_US locale for US-specific data

def generate_fake_w2_data(first_name, last_name, address, ssn_last_four, employer_name, employer_address, annual_salary):
    """Generates a dictionary containing fake data relevant to a W-2 form."""
    
    # Employee Information
    first_name = first_name
    last_name = last_name
    employee_name = f"{first_name} {last_name}"
    employee_address = address.replace('\n', ', ') # Format address for single line
    employee_ssn = ssn_last_four # Generates a realistic-looking SSN

    # Employer Information
    employer_name = employer_name
    employer_address = employer_address.replace('\n', ', ')
    # EIN is typically 9 digits, formatted as XX-XXXXXXX
    employer_ein = f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"

    # Financial Information (example data, adjust as needed for realism)
    wages_tips_other_comp = round(annual_salary)
    federal_income_tax_withheld = round(wages_tips_other_comp * random.uniform(0.10, 0.25), 2)
    social_security_wages = wages_tips_other_comp # Generally the same as Box 1 up to a limit
    social_security_tax_withheld = round(social_security_wages * 0.062, 2) # 6.2%
    medicare_wages_tips = wages_tips_other_comp
    medicare_tax_withheld = round(medicare_wages_tips * 0.0145, 2) # 1.45%
    state_wages = wages_tips_other_comp
    state_tax_withheld = round(state_wages * random.uniform(0.01, 0.06), 2)

    w2_data = {
        "Year": 2025,
        "Box b - Employer identification number (EIN)": employer_ein,
        "Box c - Employer name, address, and ZIP code": f"{employer_name}, {employer_address}",
        "Box d - Control number": fake.bban(), # Use BBAN for a random alphanumeric control number
        "Box e - Employee first name and initial": f"{first_name} {last_name[0]}.",
        "Box e - Employee last name": last_name,
        "Box e/f - Employee address and ZIP code": employee_address,
        "Box a - Employee's social security number (SSN)": f'xxx-xx-{employee_ssn}',
        "Box 1 - Wages, tips, other compensation": wages_tips_other_comp,
        "Box 2 - Federal income tax withheld": federal_income_tax_withheld,
        "Box 3 - Social security wages": social_security_wages,
        "Box 4 - Social security tax withheld": social_security_tax_withheld,
        "Box 5 - Medicare wages and tips": medicare_wages_tips,
        "Box 6 - Medicare tax withheld": medicare_tax_withheld,
        "Box 16 - State wages, tips, etc.": state_wages,
        "Box 17 - State income tax withheld": state_tax_withheld,
        "Box 15 - State and employer's state ID number": f"{fake.state_abbr()} {random.randint(10000, 99999)}",
    }
    return w2_data

def save_w2_as_pdf(w2_data, filename=f"fake_w2_{first_name}_{last_name}.pdf"):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='W2Header', fontSize=16, leading=20, spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='W2Label', fontSize=10, leading=12, spaceAfter=2, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='W2Value', fontSize=10, leading=12, spaceAfter=8))
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    story.append(Paragraph("W-2 Wage and Tax Statement (FAKE)", styles['W2Header']))
    story.append(Spacer(1, 12))

    table_data = []
    for key, value in w2_data.items():
        table_data.append([Paragraph(f"<b>{key}</b>", styles['W2Label']), Paragraph(str(value), styles['W2Value'])])

    table = Table(table_data, colWidths=[250, 250])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightyellow])
    ]))
    story.append(table)
    doc.build(story)
    print(f"W2 PDF saved as {filename}")



# COMMAND ----------



# 1. Generate fake data
fake = Faker('en_US')

def generate_profile_data(first_name, last_name, address,employer_name,annual_salary,date_of_birth):
    """Generates a dictionary of fake personal data."""
    data = {
        "Personal Information": {
            "Name": f'{first_name} {last_name}',
            "Date of Birth": date_of_birth,
            "Address": address.replace('\n', ', '),
            "Phone Number": fake.phone_number(),
            "Email": f'{first_name}.123@gmail.com'
        },
        "Employment Information": {
            "Job Title": fake.job(),
            "Company": employer_name,
            "Sentence": fake.catch_phrase()
        },
        "Job Details": {
            "Job Role": fake.paragraph(nb_sentences=5),
            "Start Date": fake.date_this_decade().strftime("%Y-%m-%d"),
            "Annual Salary": annual_salary
        }
    }
    return data

# 2. Format the data into a readable string
def format_data_for_pdf(data):
    """Formats the data dictionary into a string with line breaks."""
    report_text = "EMPLOYMENT VERIFICATION LETTER\n\n"
    for section, details in data.items():
        report_text += f"--- {section} ---\n"
        for key, value in details.items():
            report_text += f"{key}: {value}\n"
        report_text += "\n"
    return report_text

# 3. Save the formatted data as a PDF
def save_as_pdf(text, filename=f"fake_profile_data_{first_name}_{last_name}.pdf"):
    """Saves the given text to a PDF file using FPDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split text into lines for FPDF
    for line in text.split('\n'):
        # Ensure that lines do not exceed the page width
        pdf.multi_cell(0, 10, txt=line, align="L")

    pdf.output(filename)
    print(f"Successfully generated and saved {filename}")



# COMMAND ----------



def generate_utility_bill_pdf(first_name, last_name, address, filename=f"utility_bill_{first_name}_{last_name}.pdf"):
    fake = Faker('en_US') # Use 'en_US' locale for realistic US data
    styles = getSampleStyleSheet()
    
    # Custom style for bill details
    styles.add(ParagraphStyle(name='BillDetail', parent=styles['Normal'], fontSize=10, leading=12))
    styles.add(ParagraphStyle(name='BillHeader', parent=styles['Heading2'], fontSize=16, spaceAfter=12))

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    # Bill Data Generation
    company_name = f"{fake.company()} {fake.random_element(elements=('Electric', 'Gas & Electric', 'Water & Sewer', 'Utility Services'))}"
    customer_name = f'{first_name} {last_name}'
    billing_address = address.replace('\n', ', ')
    service_address = address.replace('\n', ', ')
    account_number = fake.bothify(text='ACC#####-######')
    bill_date = fake.date_this_month().strftime("%B %d, %Y")
    due_date = fake.date_this_month().strftime("%B %d, %Y")
    current_charges = round(fake.random_int(min=50, max=300) + fake.random.random(), 2)
    previous_balance = round(fake.random_int(min=0, max=100) + fake.random.random(), 2)
    total_due = round(current_charges + previous_balance, 2)
    usage_kwh = fake.random_int(min=500, max=2500)

    # Add content to the story
    story.append(Paragraph(f"**{company_name}**", styles['BillHeader']))
    story.append(Paragraph(f"{fake.address().replace('\n', ', ')}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(f"**BILLING DATE:** {bill_date}", styles['BillDetail']))
    story.append(Paragraph(f"**ACCOUNT NUMBER:** {account_number}", styles['BillDetail']))
    story.append(Paragraph(f"**CUSTOMER NAME:** {customer_name}", styles['BillDetail']))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("**SERVICE ADDRESS:**", styles['Normal']))
    story.append(Paragraph(service_address, styles['BillDetail']))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("**BILLING ADDRESS:**", styles['Normal']))
    story.append(Paragraph(billing_address, styles['BillDetail']))
    story.append(Spacer(1, 0.4 * inch))

    story.append(Paragraph("<u>BILLING SUMMARY</u>", styles['Heading3']))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(f"Previous Balance: ${previous_balance:.2f}", styles['BillDetail']))
    story.append(Paragraph(f"Current Charges: ${current_charges:.2f}", styles['BillDetail']))
    story.append(Paragraph("-" * 30, styles['BillDetail']))
    story.append(Paragraph(f"**TOTAL AMOUNT DUE: ${total_due:.2f}**", styles['BillDetail']))
    story.append(Paragraph(f"**DUE DATE: {due_date}**", styles['BillDetail']))
    story.append(Spacer(1, 0.4 * inch))

    story.append(Paragraph("<u>USAGE DETAILS</u>", styles['Heading3']))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(f"Total kWh Used: {usage_kwh} kWh", styles['BillDetail']))
    from datetime import timedelta

    service_start_date = (fake.date_this_month() - timedelta(days=30)).strftime('%B %d, %Y')
    story.append(Paragraph(f"Service Period: {service_start_date} - {bill_date}", styles['BillDetail']))


    # Build the PDF
    doc.build(story)
    print(f"Fake utility bill '{filename}' generated successfully.")



# COMMAND ----------



def generate_fake_paystub_data(first_name, last_name, address,employer_name, employer_address,annual_salary,last_four_ssn):
    """Generates a dictionary of fake paystub data."""
    fake = Faker('en_US')
    pay_period_start = date(2025, 10, 1)
    pay_period_end = date(2025, 10, 15)
    hours_worked = round(random.uniform(75.0, 85.0), 2)
    pay_rate = round(random.uniform(25.0, 40.0), 2)
    gross_pay = round(annual_salary/24, 2)
    federal_tax = round(gross_pay * 0.15, 2)
    state_tax = round(gross_pay * 0.05, 2)
    social_security = round(gross_pay * 0.062, 2)
    medicare = round(gross_pay * 0.0145, 2)
    net_pay = round(gross_pay - federal_tax - state_tax - social_security - medicare, 2)

    data = {
        "company_name": employer_name,
        "company_address": employer_address,
        "employee_name": f'{first_name} {last_name}',
        "employee_address": address,
        "employee_id":fake.random_number(digits=8),
        "ssn_last_four": random.randint(1000, 9999),
        "pay_period_start": pay_period_start.strftime("%Y-%m-%d"),
        "pay_period_end": pay_period_end.strftime("%Y-%m-%d"),
        "pay_date": date(2025, 10, 15).strftime("%Y-%m-%d"),
        "pay_rate": f"${pay_rate:.2f}",
        "hours_worked": f"{hours_worked:.2f}",
        "gross_pay": f"${gross_pay:.2f}",
        "federal_tax": f"${federal_tax:.2f}",
        "state_tax": f"${state_tax:.2f}",
        "social_security": f"${social_security:.2f}",
        "medicare": f"${medicare:.2f}",
        "net_pay": f"${net_pay:.2f}",
    }
    return data

def create_paystub_pdf(data, filename=f"paystub_{first_name}_{last_name}.pdf"):
    """Creates a PDF paystub using ReportLab."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    # Define a normal style with some leading (line spacing)
    styles.add(ParagraphStyle(name='Normal_Leading', parent=styles['Normal'], leading=14))
    story = []

    # Company Information
    story.append(Paragraph(f"<b>{data['company_name']}</b>", styles['Title']))
    story.append(Paragraph(data['company_address'], styles['Normal_Leading']))
    story.append(Spacer(1, 12))

    # Employee Information
    story.append(Paragraph(f"<b>Employee Name:</b> {data['employee_name']}", styles['Normal_Leading']))
    story.append(Paragraph(f"<b>Employee Address:</b> {data['employee_address']}", styles['Normal_Leading']))
    story.append(Paragraph(f"<b>SSN (last 4):</b> ***-**-{data['ssn_last_four']}", styles['Normal_Leading']))
    story.append(Paragraph(f"<b>Employee ID:</b> {data['employee_id']}", styles['Normal_Leading']))
    story.append(Spacer(1, 24))

    # Pay Period Details
    story.append(Paragraph("<b>Pay Details</b>", styles['h2']))
    details_data = [
        ["Pay Period Start:", data['pay_period_start']],
        ["Pay Period End:", data['pay_period_end']],
        ["Pay Date:", data['pay_date']],
        ["Pay Rate:", data['pay_rate']],
        ["Hours Worked:", data['hours_worked']],
    ]
    details_table = Table(details_data, colWidths=[150, 150])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 24))

    # Earnings and Deductions
    story.append(Paragraph("<b>Earnings and Deductions</b>", styles['h2']))
    financial_data = [
        ["Description", "Amount"],
        ["Gross Pay", data['gross_pay']],
        ["Federal Tax", data['federal_tax']],
        ["State Tax", data['state_tax']],
        ["Social Security", data['social_security']],
        ["Medicare", data['medicare']],
        ["Net Pay", f"{data['net_pay']}"],
    ]
    financial_table = Table(financial_data, colWidths=[150, 150])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(financial_table)

    # Build the PDF
    doc.build(story)
    print(f"Successfully generated paystub: {filename}")




# COMMAND ----------

from datetime import datetime

def generate_credit_application(first_name, last_name, address, employer_name, employer_address, annual_salary, ssn_last_four, date_of_birth, locale='en_US'):
    """
    Generates a single dictionary of fake credit application data.

    Args:
        locale (str): The locale for generating localized data (default: 'en_US').
    """
    fake = Faker(locale)
    
    # Generate personal information
    first_name = first_name
    last_name = last_name
    email = f'{first_name.lower()}.{last_name.lower()}@gmail.com'
    phone_number = fake.phone_number()
    date_of_birth = date_of_birth # Ensure applicant is an adult
    ssn = ssn_last_four # Generates a fake SSN for US locale
    auto_loan_paid_off = random.choice([True, False])
    auto_loan_paid_off_date = (
        fake.date_between_dates(
            date_start=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
            date_end=datetime.strptime('2024-12-31', '%Y-%m-%d').date()
        )
        if auto_loan_paid_off else None
    )


    # Generate address information
    address = address.replace('\n', ', ') # Format address into a single line

    # Generate financial and employment information
    job_title = fake.job()
    company_name = employer_name
    income = annual_salary # Random annual income
    credit_score = random.randint(300, 850) # FICO score range

    application_data = {
        "personal_info": {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": str(date_of_birth),
            "ssn": ssn,
            "email": email,
            "phone_number": phone_number,
        },
        "contact_info": {
            "address": address,
            "time at present address": "1 year"
        },
        "employment_info": {
            "current_employment_title": job_title,
            "employment_status": "Full-Time",
            "employment_type": "Skilled Labor",
            "company": company_name,
            "gross_income": income,
            "income_received": "Yearly",
        },
        "financial_info": {
            "credit_score": credit_score,
            "requested_card_type": "Visa",
            "monthly_rent": random.randint(500, 2000),
            "creditor_reference": random.choice(["Equifax", "TransUnion"]),
            "auto_loan_paid_off": auto_loan_paid_off,
            "auto_loan_paid_off_date": auto_loan_paid_off_date
        }
    }
    return application_data

def save_credit_application_pdf(app_data, filename=f"credit_application_{first_name}_{last_name}.pdf"):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Header', fontSize=16, leading=20, spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='Label', fontSize=10, leading=12, spaceAfter=2, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='Value', fontSize=10, leading=12, spaceAfter=8))
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    story.append(Paragraph("Credit Card Application (FAKE)", styles['Header']))
    story.append(Spacer(1, 12))

    for section, details in app_data.items():
        story.append(Paragraph(f"<b>{section.replace('_', ' ').title()}</b>", styles['Label']))
        table_data = []
        for key, value in details.items():
            table_data.append([Paragraph(f"{key.replace('_', ' ').title()}:", styles['Label']), Paragraph(str(value), styles['Value'])])
        table = Table(table_data, colWidths=[180, 320])
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.whitesmoke, colors.lightyellow])
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

    doc.build(story)
    print(f"Credit application PDF saved as {filename}")
    

# if __name__ == "__main__":
#     app_data = generate_credit_application(first_name, last_name, address, employer_name, employer_address, annual_salary, ssn_last_four)
#     save_credit_application_pdf(app_data)

# COMMAND ----------



fake = Faker()

def create_odometer_disclosure_statement(seller_name, seller_address, first_name, last_name, address):
    seller_name = seller_name
    buyer_name = f'{first_name} {last_name}'
    seller_address = seller_address.replace('\n', ', ')
    buyer_address = address.replace('\n', ', ')
    vin = fake.vin()
    make_model = f"{random.choice(["Black", "Blue", "Red", "White"])} {random.choice(["Honda", "Buick", "Toyota", "Chevrolet", "Jeep"])} {random.choice(["Acadia", "Cuyahoga", "Everglades", "Denali", "Badlands"])}"
    type = random.choice(["Truck", "SUV", "Sedan", "Coupe", "Van"])
    year = random.randint(1990, 2024)
    odometer_reading = random.randint(10000, 250000)
    sale_date = fake.date_this_year()
    return {
        "vin": vin,
        "make_model": make_model,
        "type": type,
        "year": year,
        "seller_name": seller_name,
        "seller_address": seller_address,
        "buyer_name": buyer_name,
        "buyer_address": buyer_address,
        "odometer_reading": odometer_reading,
        "sale_date": sale_date
    }

def save_odometer_disclosure_pdf(data, filename=f"odometer_disclosure_{first_name}_{last_name}.pdf"):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Header', fontSize=16, leading=20, spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='Section', fontSize=12, leading=14, spaceAfter=8, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='NormalBold', fontSize=10, leading=12, spaceAfter=6, fontName='Helvetica-Bold'))
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    story.append(Paragraph("ODOMETER DISCLOSURE STATEMENT", styles['Header']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("VEHICLE DESCRIPTION", styles['Section']))
    story.append(Paragraph(f"VIN: <b>{data['vin']}</b>", styles['Normal']))
    story.append(Paragraph(f"Make/Model: <b>{data['make_model']}</b>", styles['Normal']))
    story.append(Paragraph(f"Type: <b>{data['type']}</b>", styles['Normal']))
    story.append(Paragraph(f"Year: <b>{data['year']}</b>", styles['Normal']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("TRANSFEROR (SELLER) INFORMATION", styles['Section']))
    story.append(Paragraph(f"Name: <b>{data['seller_name']}</b>", styles['Normal']))
    story.append(Paragraph(f"Address: <b>{data['seller_address']}</b>", styles['Normal']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("TRANSFEREE (BUYER) INFORMATION", styles['Section']))
    story.append(Paragraph(f"Name: <b>{data['buyer_name']}</b>", styles['Normal']))
    story.append(Paragraph(f"Address: <b>{data['buyer_address']}</b>", styles['Normal']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("ODOMETER DISCLOSURE", styles['Section']))
    story.append(Paragraph(
        f"I, <b>{data['seller_name']}</b>, the Transferor, hereby state that the odometer reading of the vehicle described above is <b>{data['odometer_reading']:,}</b> miles/kilometers.",
        styles['Normal']
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Check one of the following:", styles['NormalBold']))
    story.append(Paragraph("[X] - The mileage is correct.", styles['Normal']))
    story.append(Paragraph("[ ] - The mileage does not reflect the actual mileage (odometer discrepancy).", styles['Normal']))
    story.append(Paragraph("[ ] - The odometer reading exceeds its mechanical limits.", styles['Normal']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("CERTIFICATION", styles['Section']))
    story.append(Paragraph("I certify under penalty of perjury that the foregoing is true and correct.", styles['Normal']))
    story.append(Spacer(1, 16))

    story.append(Paragraph(f"Transferor Signature: _________________________", styles['Normal']))
    story.append(Paragraph(f"Date: {data['sale_date']}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Transferee Signature: _________________________", styles['Normal']))
    story.append(Paragraph(f"Date: {data['sale_date']}", styles['Normal']))

    doc.build(story)
    print(f"Odometer PDF saved to {filename}")

# odometer_data = create_odometer_disclosure_statement(seller_name, seller_address, first_name, last_name, address)
# save_odometer_disclosure_pdf(odometer_data)

# COMMAND ----------

from datetime import date

def generate_drivers_license_data(first_name, last_name, address,city,state,zip,date_of_birth, locale='en_US'):
    """Generates a dictionary of fake driver's license data."""
    fake = Faker(locale)

    # Generate core personal information
    first_name = first_name
    last_name = last_name
    full_name = f"{first_name} {last_name}"
    address = address.replace('\n', ', ')
    city_state_zip = f"{city} {state} {zip}"
    
    # Generate dates (age >= 18)
    date_of_birth = date_of_birth
    issue_date = fake.date_between(start_date='-1y', end_date='today')
    # Expiry date is usually a few years after the issue date (e.g., 4 years)
    expiry_date = date(issue_date.year + 4, issue_date.month, issue_date.day)

    # Generate license-specific fields
    # Example format: A two-letter state code followed by a unique number/string
    license_number = f"{fake.state_abbr()}-{fake.unique.random_number(digits=9)}"
    sex = random.choice(['M', 'F'])
    height = f"{random.randint(5, 6)} ft, {random.randint(0, 11)} in"
    weight = f"{random.randint(120, 250)} lbs"
    eye_color = random.choice(['Blue', 'Brown', 'Green', 'Hazel', 'Gray'])
    hair_color = random.choice(['Black', 'Brown', 'Blond', 'Red', 'Gray'])
    
    # Vehicle provider can generate a license plate if needed for the data
    license_plate = fake.license_plate()

    return {
        "License Number": license_number,
        "Name": full_name,
        "Address": address,
        "City, State, Zip": city_state_zip,
        "Date of Birth": date_of_birth,
        #  if date_of_birth.year > 1950 else fake.date_of_birth(minimum_age=18, maximum_age=75, tzinfo=None, end_datetime=date(2007, 1, 1)).strftime("%Y-%m-%d"),
        "Issue Date": issue_date.strftime("%Y-%m-%d"),
        "Expiry Date": expiry_date.strftime("%Y-%m-%d"),
        "Sex": sex,
        "Height": height,
        "Weight": weight,
        "Eye Color": eye_color,
        "Hair Color": hair_color,
        "License Plate": license_plate
    }

def save_drivers_license_pdf(data, filename=f"drivers_license_{first_name}_{last_name}.pdf"):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Header', fontSize=16, leading=20, spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='Label', fontSize=10, leading=12, spaceAfter=2, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='Value', fontSize=10, leading=12, spaceAfter=8))
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    story.append(Paragraph("Driver's License", styles['Header']))
    story.append(Spacer(1, 12))

    table_data = []
    for key, value in data.items():
        table_data.append([Paragraph(f"{key}:", styles['Label']), Paragraph(str(value), styles['Value'])])

    table = Table(table_data, colWidths=[180, 320])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.whitesmoke, colors.lightyellow])
    ]))
    story.append(table)
    doc.build(story)
    print(f"DL PDF saved as {filename}")



# COMMAND ----------

from datetime import timedelta

# Initialize Faker
fake = Faker('en_US')

def generate_loan_approval_letter(first_name, last_name, address):
    """Generates a fake auto loan approval letter."""

    # Generate fake personal and loan data
    customer_name = f"{first_name} {last_name}"
    customer_address = address.replace('\n', ', ') # Format address for single line
    loan_amount = random.randint(20000, 60000)
    interest_rate = round(random.uniform(3.5, 9.9), 2)
    loan_term_months = random.choice([36, 48, 60, 72])
    monthly_payment = round(loan_amount * (interest_rate/100/12) / (1 - (1 + interest_rate/100/12)**-loan_term_months), 2)
    approval_date = fake.date_between(start_date='-1y', end_date='today')
    expiration_date = approval_date + timedelta(days=30)
    loan_officer_name = "MJ"
    bank_name = "BBT"
    bank_phone = "111-222-3456"

    # Letter template with placeholders
    letter_template = f"""
{bank_name}
{fake.address().replace('\n', ', ')}
{bank_phone}
{fake.email()}

{approval_date.strftime('%B %d, %Y')}

{customer_name}
{customer_address}

Subject: Auto Loan Approval Notification

Dear {customer_name},

We are pleased to inform you that your application for an auto loan with {bank_name} has been approved!

This approval is subject to the following terms and conditions:

    Loan Amount: ${loan_amount:,.2f}
    Interest Rate: {interest_rate:.2f}% APR
    Loan Term: {loan_term_months} months
    Estimated Monthly Payment: ${monthly_payment:,.2f}

This offer is valid until {expiration_date.strftime('%B %d, %Y')}. To accept these terms and finalize your loan, please contact us at your earliest convenience.

We congratulate you on your new vehicle purchase and look forward to serving your financial needs.

Sincerely,

{loan_officer_name}
Loan Officer
{bank_name}
"""
    return letter_template

def save_loan_approval_letter_pdf(letter_text, filename=f"loan_approval_letter_{first_name}_{last_name}.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in letter_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line, align="L")
    pdf.output(filename)
    print(f"Loan approval letter PDF saved as {filename}")

# # Generate and save the letter as PDF
# if __name__ == "__main__":
#     letter = generate_loan_approval_letter(first_name, last_name, address)
#     save_loan_approval_letter_pdf(letter)

# COMMAND ----------

if __name__ == "__main__":
    #paystub
    paystub_data = generate_fake_paystub_data(first_name, last_name, address,employer_name, employer_address,annual_salary,ssn_last_four)
    create_paystub_pdf(paystub_data)
    #utility bill
    generate_utility_bill_pdf(first_name, last_name, address)
    #employment verification
    profile_data = generate_profile_data(first_name, last_name, address,employer_name,annual_salary,date_of_birth)
    report_string = format_data_for_pdf(profile_data)
    save_as_pdf(report_string)
    #w2 generation
    w2_info = generate_fake_w2_data(first_name, last_name, address, ssn_last_four, employer_name, employer_address, annual_salary)
    save_w2_as_pdf(w2_info)
    #credit application
    app_data = generate_credit_application(first_name, last_name, address, employer_name, employer_address, annual_salary, ssn_last_four,date_of_birth)
    save_credit_application_pdf(app_data)
    #odometer disclosure
    odometer_data = create_odometer_disclosure_statement(seller_name, seller_address, first_name, last_name, address)
    save_odometer_disclosure_pdf(odometer_data)
    #drivers license
    data = generate_drivers_license_data(first_name, last_name, address,city,state,zip,date_of_birth)
    save_drivers_license_pdf(data)
    #preapproval
    letter = generate_loan_approval_letter(first_name, last_name, address)
    save_loan_approval_letter_pdf(letter)

# COMMAND ----------

