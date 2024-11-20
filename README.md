# Real-Time Blog Application with Notifications REST API

This is a Django-based blog application REST API with support for real-time notifications using Django Channels. It includes features like user authentication, blog posts, comments, likes, views tracking, and notification preferences. Notifications are delivered via WebSocket to provide real-time updates.

## Features

1. **User Management**
   - Register, Login, Logout
   - Authentication using JWT
   - Two-factor authentication with TOTP

2. **Blog Management**
   - Create, read, update, delete (CRUD) blog posts
   - Pagination for blog posts

3. **Comments**
   - Add comments to posts
   - Support for nested comments (replies)

4. **Likes**
   - Like/unlike blog posts
   - Prevent duplicate likes

5. **Views**
   - Track views for each post

6. **Notifications**
   - Real-time notifications via WebSocket
   - Notification preferences (email, push notifications)
   - Mark notifications as read

7. **Analytics**
   - Admin-only view for application analytics (e.g., total users, posts, comments, likes, views)

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Real-Time**: Django Channels
- **Database**: SQLite (default, can be replaced with PostgreSQL or other DBs)
- **Authentication**: SimpleJWT, Django-OTP
- **Frontend**: Basic HTML templates (can be integrated with modern JS frameworks like React)

## Installation

### Prerequisites

- Python 3.8+
- Node.js (optional for frontend build tools)
- Redis (required for Django Channels)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/thapelomagqazana/blog_platform_api.git
   cd blog_platform_api
   ```
2. **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure Redis**
    - Install Redis:

    ```bash
    sudo apt install redis  # On Linux
    brew install redis      # On macOS
    ```
    - Start Redis:

    ```bash
    redis-server
    ```
5. **Apply migrations**

    ```bash
    python manage.py migrate
    ```
6. **Run the server**

    ```bash
    python manage.py runserver
    ```

7. **Start the WebSocket server** WebSocket functionality is integrated into the Django development server when using Channels.

## API Endpoints

### Authentication
- **Register:** POST /api/register/
- **Login:** POST /api/login/
- **Logout:** POST /api/logout/

### Blog Posts
- **List/Create:** GET/POST /api/posts/
- **Retrieve/Update/Delete:** GET/PUT/DELETE /api/posts/<id>/

### Comments
- **List/Create:** GET/POST /api/comments/
- **Retrieve/Update/Delete:** GET/PUT/DELETE /api/comments/<id>/

### Likes
- **Like Post:** POST /api/posts/<id>/like/
- **Unlike Post:** DELETE /api/posts/<id>/unlike/

### Notifications
- **List Notifications:** GET /api/notifications/
- **Mark as Read:** PUT /api/notifications/<id>/read/

### Analytics
- **Admin Analytics:** GET /api/analytics/

## WebSocket Endpoints
- **Notifications:** ws://<your-domain>/ws/notifications/

## Testing
Run tests with:
```bash
pytest
```

## Deployment
- Use a production-grade web server like Gunicorn or uWSGI.
- Use Daphne for ASGI support.
- Configure Redis in production for WebSocket handling.

## Contributing
- Fork the repository.
- Create a feature branch.
- Commit your changes.
- Push to your fork.
- Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Developed by Thapelo Magqazana. Contributions are welcome!
