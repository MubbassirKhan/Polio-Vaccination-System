# Polio Vaccination System

## Project Description
The Polio Vaccination System is an innovative web-based solution designed to help manage and track polio vaccination campaigns. It allows parents to register their children, schedule vaccinations, and receive reminders for upcoming doses. Additionally, healthcare providers and administrators can monitor vaccination progress, manage appointments, and ensure timely immunization.

## Features
- **User Registration**: Parents can register their children for vaccination.
- **Vaccination Scheduling**: Schedule and manage polio vaccine appointments.
- **Notifications**: Automated reminders for upcoming vaccinations.
- **Admin Panel**: Allows administrators to monitor vaccination data, approve appointments, and manage users.
- **Tracking**: Monitor the status of vaccination doses administered to children.
  
## Tech Stack
- **Frontend**: HTML, CSS, JavaScript (with Bootstrap for styling)
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Version Control**: Git/GitHub

## Installation

### Prerequisites:
Ensure you have the following installed:
- **Python** (preferably Python 3.6+)
- **MySQL** for the database
- **pip** (Python's package installer)

### Steps to Install:

1. Clone the repository:
   ```bash
   git clone https://github.com/MubbassirKhan/Polio-Vaccination-System.git
Navigate to the project folder:

bash
Copy
Edit
cd Polio-Vaccination-System
Set up a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
Activate the virtual environment:

On Windows:
bash
Copy
Edit
venv\Scripts\activate
On macOS/Linux:
bash
Copy
Edit
source venv/bin/activate
Install the required Python packages:

bash
Copy
Edit
pip install -r requirements.txt
Set up the MySQL database:

Ensure MySQL is running on your system.
Create a database and configure your connection settings in config.py (you may need to create this file).
Run the application:

bash
Copy
Edit
python app.py
Open your browser and navigate to http://127.0.0.1:5000 to use the system.
