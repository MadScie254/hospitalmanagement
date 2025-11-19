from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils import timezone


# Phone validator
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

# Department choices
departments = [
    ('Cardiologist', 'Cardiologist'),
    ('Dermatologists', 'Dermatologists'),
    ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
    ('Allergists/Immunologists', 'Allergists/Immunologists'),
    ('Anesthesiologists', 'Anesthesiologists'),
    ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons'),
    ('Endocrinologists', 'Endocrinologists'),
    ('Gastroenterologists', 'Gastroenterologists'),
    ('Neurologists', 'Neurologists'),
    ('Oncologists', 'Oncologists'),
    ('Ophthalmologists', 'Ophthalmologists'),
    ('Orthopedic Surgeons', 'Orthopedic Surgeons'),
    ('Pediatricians', 'Pediatricians'),
    ('Psychiatrists', 'Psychiatrists'),
    ('Radiologists', 'Radiologists'),
    ('Urologists', 'Urologists'),
]


class BaseModel(models.Model):
    """Abstract base model with common fields"""
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, db_index=True)
    
    class Meta:
        abstract = True


class Doctor(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    profile_pic = models.ImageField(
        upload_to='profile_pic/DoctorProfilePic/',
        null=True,
        blank=True,
        help_text='Upload a professional profile picture'
    )
    address = models.CharField(max_length=200, help_text='Full address')
    mobile = models.CharField(
        max_length=20,
        validators=[phone_validator],
        help_text='Contact number'
    )
    department = models.CharField(
        max_length=50,
        choices=departments,
        default='Cardiologist',
        db_index=True,
        help_text='Medical specialization'
    )
    status = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Approved status'
    )
    qualifications = models.TextField(
        blank=True,
        null=True,
        help_text='Educational qualifications and certifications'
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        help_text='Years of medical practice'
    )
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Consultation fee in USD'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        indexes = [
            models.Index(fields=['department', 'status']),
        ]
    
    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.department})"


class Patient(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    profile_pic = models.ImageField(
        upload_to='profile_pic/PatientProfilePic/',
        null=True,
        blank=True,
        help_text='Upload profile picture'
    )
    address = models.CharField(max_length=200, help_text='Full address')
    mobile = models.CharField(
        max_length=20,
        validators=[phone_validator],
        help_text='Contact number'
    )
    symptoms = models.TextField(
        help_text='Describe your symptoms'
    )
    assigned_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients',
        help_text='Assigned doctor'
    )
    admit_date = models.DateField(
        auto_now_add=True,
        help_text='Date of admission'
    )
    status = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Approved/Admitted status'
    )
    blood_group = models.CharField(
        max_length=5,
        blank=True,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        help_text='Blood group'
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text='Date of birth'
    )
    emergency_contact = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        help_text='Emergency contact number'
    )
    
    # Backward compatibility field (deprecated)
    assignedDoctorId = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
        help_text='Legacy field - use assigned_doctor instead'
    )
    
    class Meta:
        ordering = ['-admit_date']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        indexes = [
            models.Index(fields=['status', 'assigned_doctor']),
        ]
    
    def save(self, *args, **kwargs):
        # Maintain backward compatibility
        if self.assigned_doctor:
            self.assignedDoctorId = self.assigned_doctor.user.id
        super().save(*args, **kwargs)
    
    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def get_id(self):
        return self.user.id
    
    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.symptoms[:30]})"


class Appointment(BaseModel):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        help_text='Patient for appointment',
        null=True
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments',
        help_text='Doctor for appointment',
        null=True
    )
    appointment_date = models.DateTimeField(
        default=timezone.now,
        help_text='Date and time of appointment'
    )
    description = models.TextField(
        max_length=1000,
        help_text='Reason for appointment'
    )
    status = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Approval status'
    )
    
    # Backward compatibility fields (deprecated)
    patientId = models.PositiveIntegerField(null=True, blank=True, editable=False)
    doctorId = models.PositiveIntegerField(null=True, blank=True, editable=False)
    patientName = models.CharField(max_length=100, blank=True, editable=False)
    doctorName = models.CharField(max_length=100, blank=True, editable=False)
    appointmentDate = models.DateField(null=True, blank=True, editable=False)
    
    class Meta:
        ordering = ['-appointment_date']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        indexes = [
            models.Index(fields=['appointment_date', 'status']),
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['patient', 'appointment_date']),
        ]
    
    def save(self, *args, **kwargs):
        # Maintain backward compatibility
        if self.patient:
            self.patientId = self.patient.user.id
            self.patientName = self.patient.get_name
        if self.doctor:
            self.doctorId = self.doctor.user.id
            self.doctorName = self.doctor.get_name
        if self.appointment_date:
            self.appointmentDate = self.appointment_date.date()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.patient.get_name} -> {self.doctor.get_name} on {self.appointment_date}"


class PatientDischargeDetails(BaseModel):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='discharge_records',
        help_text='Patient being discharged',
        null=True
    )
    assigned_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='discharge_records',
        help_text='Doctor who treated the patient'
    )
    admit_date = models.DateField(help_text='Date of admission')
    release_date = models.DateField(help_text='Date of discharge')
    day_spent = models.PositiveIntegerField(help_text='Number of days in hospital')
    room_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Room charges per day'
    )
    medicine_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Total medicine cost'
    )
    doctor_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Doctor consultation fee'
    )
    other_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Other miscellaneous charges'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Total bill amount'
    )
    
    # Backward compatibility fields (deprecated)
    patientId = models.PositiveIntegerField(null=True, blank=True, editable=False)
    patientName = models.CharField(max_length=100, blank=True, editable=False)
    assignedDoctorName = models.CharField(max_length=100, blank=True, editable=False)
    address = models.CharField(max_length=200, blank=True, editable=False)
    mobile = models.CharField(max_length=20, blank=True, editable=False)
    symptoms = models.CharField(max_length=500, blank=True, editable=False)
    admitDate = models.DateField(null=True, blank=True, editable=False)
    releaseDate = models.DateField(null=True, blank=True, editable=False)
    daySpent = models.PositiveIntegerField(null=True, blank=True, editable=False)
    roomCharge = models.PositiveIntegerField(null=True, blank=True, editable=False)
    medicineCost = models.PositiveIntegerField(null=True, blank=True, editable=False)
    doctorFee = models.PositiveIntegerField(null=True, blank=True, editable=False)
    OtherCharge = models.PositiveIntegerField(null=True, blank=True, editable=False)
    
    class Meta:
        ordering = ['-release_date']
        verbose_name = 'Patient Discharge Detail'
        verbose_name_plural = 'Patient Discharge Details'
    
    def save(self, *args, **kwargs):
        # Maintain backward compatibility
        if self.patient:
            self.patientId = self.patient.user.id
            self.patientName = self.patient.get_name
            self.address = self.patient.address
            self.mobile = self.patient.mobile
            self.symptoms = self.patient.symptoms
        if self.assigned_doctor:
            self.assignedDoctorName = self.assigned_doctor.get_name
        self.admitDate = self.admit_date
        self.releaseDate = self.release_date
        self.daySpent = self.day_spent
        self.roomCharge = int(self.room_charge)
        self.medicineCost = int(self.medicine_cost)
        self.doctorFee = int(self.doctor_fee)
        self.OtherCharge = int(self.other_charge)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Discharge: {self.patient.get_name} on {self.release_date}"


# Developed By : sumit kumar
# facebook : fb.com/sumit.luv
# Youtube :youtube.com/lazycoders
# Enhanced and improved by MadScie254
