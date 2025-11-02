# Inkwell Stories - Django Blog Application

A modern, elegant blog platform built with Django, featuring user authentication, post categorization, and a responsive design.

## Features

- **User Authentication**: Registration, login, logout, and profile management
- **Blog Posts**: Create, read, update, and delete blog posts
- **Categories**: Organize posts into predefined categories (Politics, Religion, History, Technology, Science, Culture, Sports, Entertainment)
- **User Profiles**: Custom user profiles with image upload capability
- **Responsive Design**: Modern, mobile-friendly interface with gradient themes
- **Pagination**: Efficient navigation through multiple posts
- **Category Filtering**: Filter posts by category from the sidebar

## Technologies Used

- **Backend**: Django 5.1.2, Python 3.11+
- **Database**: SQLite (development), PostgreSQL ready
- **Frontend**: Bootstrap 4, HTML5, CSS3, JavaScript
- **Media Handling**: Pillow for image processing
- **Forms**: django-crispy-forms with Bootstrap 4 styling

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/inkwell-stories.git
   cd inkwell-stories
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Usage

1. **Access the application** at `http://127.0.0.1:8000/`
2. **Register** a new account or **login** with existing credentials
3. **Create posts** by clicking the "Write New Post" button
4. **Browse posts** by category using the sidebar filters
5. **Manage your profile** through the Profile page

## Project Structure

```
django_project/
├── blog/                   # Main blog application
├── users/                  # User authentication and profiles
├── media/                  # User uploaded files
├── django_project/         # Project settings
└── templates/              # HTML templates
```

