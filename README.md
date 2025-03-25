# QR Code-Based Student Verification and Gate Access System

A secure and efficient system for student verification and gate access management using QR codes. This system is designed for university environments, providing a modern and secure way to manage student access to campus facilities.

## Features

- 🔒 Secure QR code generation with encryption and expiration
- 📱 Mobile-friendly interface
- ⚡ Real-time verification
- 📊 Admin dashboard for user management
- 🔐 Role-based access control
- 📝 Activity logging and monitoring
- 🎨 Modern, responsive UI
- 🔄 Automatic QR code refresh

## Prerequisites

- Python 3.8 or higher
- Django 4.2 or higher
- PostgreSQL database
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd qr-verification-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

## Configuration

1. Update settings in `settings.py`:
   - Database configuration
   - Email settings
   - Security settings
   - QR code settings

2. Configure your email settings for QR code delivery:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

## Usage

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the admin interface:
   - URL: http://localhost:8000/admin
   - Login with your superuser credentials

3. Generate QR codes for students:
   - Navigate to the admin interface
   - Select a student
   - Generate and send QR code

4. Use the scanner interface:
   - URL: http://localhost:8000/
   - Scan student QR codes for verification

## Security Features

- JWT-based QR code encryption
- Rate limiting for API endpoints
- CSRF protection
- XSS protection
- SQL injection prevention
- Secure session management
- Input validation and sanitization

## Deployment

### Self-Hosted Server (Recommended)

1. Server Requirements:
   - CPU: Intel Core i5 or equivalent
   - RAM: 8GB minimum
   - Storage: 256GB SSD
   - Network: Gigabit Ethernet

2. Software Requirements:
   - Ubuntu Server LTS
   - Nginx
   - PostgreSQL
   - Python 3.8+
   - SSL certificate

3. Deployment Steps:
   ```bash
   # Install system dependencies
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql

   # Set up PostgreSQL
   sudo -u postgres psql
   CREATE DATABASE qr_system;
   CREATE USER qr_user WITH PASSWORD 'your_password';
   ALTER ROLE qr_user SET client_encoding TO 'utf8';
   ALTER ROLE qr_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE qr_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE qr_system TO qr_user;
   \q

   # Configure Nginx
   sudo nano /etc/nginx/sites-available/qr_system
   ```

   Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /path/to/your/project;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/run/gunicorn.sock;
       }
   }
   ```

   ```bash
   # Enable the site
   sudo ln -s /etc/nginx/sites-available/qr_system /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx

   # Set up Gunicorn
   sudo nano /etc/systemd/system/gunicorn.service
   ```

   Add the following configuration:
   ```ini
   [Unit]
   Description=gunicorn daemon
   Requires=gunicorn.socket
   After=network.target

   [Service]
   User=your_user
   Group=www-data
   WorkingDirectory=/path/to/your/project
   ExecStart=/path/to/venv/bin/gunicorn \
       --access-logfile - \
       --workers 3 \
       --bind unix:/run/gunicorn.sock \
       qr_system.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   # Start Gunicorn
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

## Maintenance

1. Regular Tasks:
   - Database backups
   - Log rotation
   - Security updates
   - Performance monitoring

2. Backup Commands:
   ```bash
   # Database backup
   pg_dump -U qr_user qr_system > backup.sql

   # Media files backup
   tar -czf media_backup.tar.gz media/
   ```

## Troubleshooting

Common issues and solutions:

1. Database Connection:
   - Check PostgreSQL service status
   - Verify database credentials
   - Ensure database exists

2. QR Code Generation:
   - Check email settings
   - Verify file permissions
   - Check storage space

3. Scanner Issues:
   - Verify camera permissions
   - Check browser compatibility
   - Clear browser cache

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgments

- Django Framework
- QR Code Library
- All contributors and maintainers 
