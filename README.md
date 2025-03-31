# Mind_Wellness
# Mental Health Donation and Support Platform

This repository contains the backend code for a mental health donation and support platform. It's built with Flask and uses various extensions for database management, API development, and authentication.

## Features

* **User Authentication:** Secure user registration and login with JWT (JSON Web Tokens).
* **Provider Management:** 
    * Mental health providers can apply, manage their profiles, and track donations.
    * Admins can approve/reject provider applications and feature providers.
* **Donation Processing:** Handles donations, including recurring donations, with a focus on M-Pesa integration.
* **Impact Stories:** Providers can share success stories about their work and impact.
* **Testimonial Management:** Providers can manage patient testimonials.
* **Inventory Tracking:** Basic inventory management for providers to track donated goods.
* **Admin Dashboard:** Provides an overview of platform data and tools for managing users and providers.
* **API Documentation:** (To be added) Clear documentation for all API endpoints.

## Technologies Used

* **Flask:** Python web framework.
* **SQLAlchemy:** ORM for database interaction.
* **Flask-Migrate:** Database migrations.
* **Marshmallow:** Object serialization/deserialization.
* **Flask-JWT-Extended:** JWT authentication.
* **Flask-CORS:** Cross-Origin Resource Sharing.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* **Node.js and npm:** Make sure you have Node.js and npm installed on your system.
* **Python and pip:** Ensure you have Python and pip installed.
* **Virtual environment:** Use a virtual environment for the backend.
* **Database:** Set up a database (e.g., PostgreSQL, MySQL).

### Installing

1. **Clone the repository:**
   ```bash
   git clone <repository_url>

2. **Backend setup:**
cd /home/raymond/Mind_Wellness/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade

3. **Frontend setup**
npm install

4. **Running the application**
flask run
npm run dev

5. **Deployment server**

## Built with:
* **Flask** - The web framework used

* **React** - Frontend library

* **Redux** - State management library