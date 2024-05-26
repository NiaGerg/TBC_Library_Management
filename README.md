# Library Management System

## Introduction
This is a Django-based library management system that allows library employees to control the book database and manage the process of issuing and returning books to users. Additionally, users can register on the website and utilize library services such as browsing available books and making reservations.

## Features
- User Registration and Authentication
- Book Management (Add, Delete, Edit)
- Book Issuing and Returning
- User Profile Management
- Reservation System
- Statistical Analysis (Most Popular Books, Late Returns, etc.)
- Automated Email Notifications for Overdue Books

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NiaGerg/library-management.git
   cd library-management
   
2. Install dependencies:
pip install -r requirements.txt

3. Apply migrations:
python manage.py migrate

# Usage

Visit the registration page to create a new account.
Log in using your credentials.
Browse the list of available books, search, and make reservations.
Librarians can manage books through the Django admin panel or API.

# API Endpoints
/api/users/register/: User registration endpoint.
/api/users/profile/: User profile endpoint.
/api/library/books/{book_id}/reserve/: Book reservation endpoint.
/api/library/statistics/: Statistical data endpoint.