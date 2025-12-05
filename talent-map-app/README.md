# Talent Map Application

## Overview
The Talent Map Application is a Django web application designed to generate and visualize interactive user talent maps. It allows users to create profiles, search for talents, and display verified badges for users with confirmed skills.

## Features
- User profile creation and management
- Advanced search functionality for user profiles
- Interactive talent map visualization
- "Talent Verified" badge feature for confirmed skills

## Project Structure
```
talent-map-app
├── manage.py
├── requirements.txt
├── talent_map_project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── talent_map_app
│   ├── migrations
│   │   └── __init__.py
│   ├── templates
│   │   ├── base.html
│   │   ├── profile
│   │   │   ├── create.html
│   │   │   ├── detail.html
│   │   │   └── edit.html
│   │   ├── search
│   │   │   └── results.html
│   │   ├── talent_map
│   │   │   └── visualization.html
│   │   └── home.html
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── talent-map.js
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── tests.py
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd talent-map-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage
- Navigate to `http://127.0.0.1:8000/` to access the application.
- Create a user profile to start generating your talent map.
- Use the search functionality to find other users and their talents.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.