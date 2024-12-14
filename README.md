# Employee Management System

A Django-based Employee Management System using MongoDB as the database backend.

## Prerequisites

- Python 3.x
- MongoDB 6.0+
- Git

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gayathri8282/Employee_Management.git
   cd Employee_Management
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # For Windows
   venv\Scripts\activate
   # For Unix or MacOS
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install specific compatible versions**
   ```bash
   pip install djongo==1.3.6
   pip install pymongo==3.12.3
   pip install django-mongodb-engine==0.6.0
   ```

5. **Make migrations and migrate**
   ```bash
   python manage.py makemigrations
   python manage.py migrate --run-syncdb
   ```

6. **Create a superuser (Required for Login)**
   ```bash
   python manage.py createsuperuser
   # Follow the prompts to create username and password
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Important Notes

- You must create a superuser to access the system
- Use the superuser credentials to log in at: `http://127.0.0.1:8000/login/`
- Make sure MongoDB is running on your system before starting the application

## Features

- User Authentication
- Employee Management (CRUD operations)
- Department Management
- Image Upload for Employees
- Search Functionality
- Responsive Design

## Project Structure

Employee_Management/
├── employees/ # Main app directory
├── employee_management/ # Project settings directory
├── templates/ # HTML templates
├── static/ # Static files (CSS, JS, Images)
├── media/ # Uploaded media files
├── requirements.txt # Project dependencies
└── manage.py # Django management script



## Access Routes

- Login: `http://127.0.0.1:8000/login/`
- Dashboard: `http://127.0.0.1:8000/dashboard/`
- Employee List: `http://127.0.0.1:8000/dashboard/employee/list/`
- Create Employee: `http://127.0.0.1:8000/dashboard/employee/create/`

## Troubleshooting

1. If you encounter database connection issues:
   - Ensure MongoDB is running
   - Check MongoDB connection settings in settings.py

2. If login fails:
   - Verify superuser was created successfully
   - Check if migrations were applied properly

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
