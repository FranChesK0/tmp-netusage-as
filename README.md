# NetworkUsage Service

A web application for monitoring and managing network usage with separate interfaces for administrators and users.

## Features

### Admin Interface
- Global network usage statistics with interactive graphics
- User management capabilities
- System monitoring and configuration

### User Interface
- Personal network usage statistics
- VPN connection details
- Usage reports and analytics

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```
5. Run the application:
```bash
flask run
```

## Configuration

Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///network_usage.db
```

## Usage

Visit the application at http://localhost:5000/

Here are the test credentials for the admin interface:
- Username: admin
- Password: admin123

And the test credentials for the user interface:
- Username: testuser
- Password: test123
