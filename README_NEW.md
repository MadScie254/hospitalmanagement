# 🏥 Hospital Management System - Enhanced Version

A comprehensive Django-based hospital management system with modern UI/UX, enhanced security, and improved database architecture.

## ✨ Features

### For Patients
- 📅 **Online Appointment Booking** - Schedule appointments with doctors
- 👤 **Patient Dashboard** - View appointments, medical history, and bills
- 💊 **Prescription Viewer** - Access your prescriptions digitally
- 📧 **Email Notifications** - Get updates on appointment status
- 📱 **Responsive Design** - Access from any device

### For Doctors
- 📊 **Doctor Dashboard** - Manage appointments and patient records
- 👥 **Patient Management** - View and update patient information
- 📅 **Appointment Calendar** - Track your daily schedule
- 💼 **Discharge Management** - Process patient discharges and billing

### For Administrators
- 👨‍⚕️ **Doctor Management** - Add, approve, and manage doctors
- 🏥 **Patient Management** - Oversee all patient records
- 📈 **Analytics Dashboard** - View statistics and metrics
- ⚙️ **System Configuration** - Manage hospital settings
- 💰 **Billing System** - Generate and track patient bills

## 🚀 Recent Improvements

### Security Enhancements
- ✅ Environment variable configuration
- ✅ Secure secret key management
- ✅ Enhanced password validation
- ✅ Security headers implementation
- ✅ Session security improvements
- ✅ Comprehensive logging system

### Database Improvements
- ✅ Proper foreign key relationships
- ✅ Database indexes for performance
- ✅ Timestamp tracking on all models
- ✅ Enhanced data validation
- ✅ Backward compatibility maintained
- ✅ New fields: blood_group, date_of_birth, emergency_contact

### UI/UX Improvements
- ✅ Modern, responsive design
- ✅ Gradient color schemes
- ✅ Smooth animations and transitions
- ✅ Improved navigation
- ✅ Enhanced forms with better validation
- ✅ Professional dashboard cards
- ✅ Better mobile experience

### Backend Improvements
- ✅ Enhanced admin panel with filters and search
- ✅ Better error handling
- ✅ Logging system for debugging
- ✅ Improved code organization
- ✅ Static file optimization

## 📋 Requirements

- Python 3.6+
- Django 3.0.5
- See `requirement.txt` for full list

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MadScie254/hospitalmanagement.git
cd hospitalmanagement
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirement.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` and configure:
```env
DJANGO_SECRET_KEY=your-unique-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
EMAIL_RECEIVING_USER=admin@hospital.com
```

**To generate a new SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Database Setup
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 📧 Email Configuration

For Gmail:
1. Enable 2-Step Verification in your Google Account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `.env` file

## 🎨 Default Accounts

After running migrations, you can create test accounts:

### Admin
- Go to `/adminsignup`
- Create admin account
- Login at `/adminlogin`

### Doctor
- Go to `/doctorsignup`
- Fill in details (requires admin approval)
- Login at `/doctorlogin`

### Patient
- Go to `/patientsignup`
- Fill in details (requires admin approval)
- Login at `/patientlogin`

## 📱 Usage

### Admin Workflow
1. Login to admin panel
2. Approve pending doctors and patients
3. Add/manage doctors and patients
4. Create appointments
5. Process patient discharges
6. Generate bills

### Doctor Workflow
1. Wait for admin approval
2. Login to doctor dashboard
3. View assigned patients
4. Manage appointments
5. View discharged patients

### Patient Workflow
1. Register and wait for approval
2. Login to patient dashboard
3. Book appointments with doctors
4. View appointment status
5. Access medical records and bills

## 🗂️ Project Structure

```
hospitalmanagement/
├── hospital/               # Main app
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin panel config
│   └── migrations/        # Database migrations
├── hospitalmanagement/    # Project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── templates/             # HTML templates
│   └── hospital/          # App templates
├── static/                # Static files
│   ├── style.css          # Old styles
│   ├── modern-style.css   # New modern styles
│   └── images/            # Images
├── .env                   # Environment variables (create this)
├── .env.example           # Environment template
├── manage.py              # Django management
└── requirement.txt        # Dependencies
```

## 🔐 Security Notes

### Production Deployment
Before deploying to production:

1. **Set DEBUG to False** in `.env`:
   ```env
   DJANGO_DEBUG=False
   ```

2. **Use strong SECRET_KEY**:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Configure ALLOWED_HOSTS**:
   ```env
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

4. **Enable HTTPS security**:
   ```env
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

5. **Use PostgreSQL** instead of SQLite for production

6. **Set up proper static file serving** (use Nginx or CDN)

7. **Regular backups** of database

## 📊 Database Schema

### Core Models
- **User** - Django's built-in user model
- **Doctor** - Doctor profiles with specialization
- **Patient** - Patient records with medical info
- **Appointment** - Appointment scheduling
- **PatientDischargeDetails** - Billing and discharge records

### Key Relationships
- Doctor → User (OneToOne)
- Patient → User (OneToOne)
- Patient → Doctor (ForeignKey - assigned_doctor)
- Appointment → Patient (ForeignKey)
- Appointment → Doctor (ForeignKey)
- PatientDischargeDetails → Patient (ForeignKey)

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check
```

## 📝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'dotenv'`**
```bash
pip install python-dotenv
```

**Issue: Static files not loading**
```bash
python manage.py collectstatic
```

**Issue: Migration errors**
```bash
python manage.py makemigrations --empty hospital
python manage.py migrate --fake hospital
```

**Issue: Email not sending**
- Check Gmail security settings
- Use App Password instead of regular password
- Enable "Less secure app access" (not recommended)

## 📄 License

This project is open source. Original code by Sumit Kumar, enhanced by MadScie254.

## 🤝 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## 🎯 Roadmap

### Planned Features
- [ ] RESTful API with Django REST Framework
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Medical records upload
- [ ] Telemedicine integration
- [ ] Payment gateway integration
- [ ] SMS notifications
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Export reports (PDF, CSV, Excel)
- [ ] Automated testing suite
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 📸 Screenshots

*Screenshots coming soon*

## 🙏 Acknowledgments

- Original Developer: Sumit Kumar
- Enhanced by: MadScie254
- Built with Django
- Bootstrap for UI components
- Font Awesome for icons

---

**⭐ If you find this project helpful, please consider giving it a star!**
