from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor, Patient, Appointment, PatientDischargeDetails


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'department', 'mobile', 'status', 'experience_years', 'consultation_fee', 'created_at']
    list_filter = ['status', 'department', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'mobile', 'department']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'status')
        }),
        ('Profile', {
            'fields': ('profile_pic', 'mobile', 'address')
        }),
        ('Professional Details', {
            'fields': ('department', 'qualifications', 'experience_years', 'consultation_fee')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_name(self, obj):
        return obj.get_name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user__first_name'


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'mobile', 'symptoms_short', 'assigned_doctor', 'status', 'admit_date', 'blood_group']
    list_filter = ['status', 'blood_group', 'admit_date', 'assigned_doctor']
    search_fields = ['user__first_name', 'user__last_name', 'mobile', 'symptoms']
    readonly_fields = ['created_at', 'updated_at', 'admit_date', 'age']
    list_editable = ['status']
    list_per_page = 25
    date_hierarchy = 'admit_date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'status')
        }),
        ('Profile', {
            'fields': ('profile_pic', 'mobile', 'address', 'date_of_birth', 'age', 'blood_group', 'emergency_contact')
        }),
        ('Medical Information', {
            'fields': ('symptoms', 'assigned_doctor')
        }),
        ('Timestamps', {
            'fields': ('admit_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_name(self, obj):
        return obj.get_name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user__first_name'
    
    def symptoms_short(self, obj):
        return obj.symptoms[:50] + '...' if len(obj.symptoms) > 50 else obj.symptoms
    symptoms_short.short_description = 'Symptoms'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'doctor', 'created_at']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    list_per_page = 25
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'status')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PatientDischargeDetails)
class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    list_display = ['patient', 'assigned_doctor', 'admit_date', 'release_date', 'day_spent', 'total', 'created_at']
    list_filter = ['release_date', 'admit_date', 'assigned_doctor']
    search_fields = ['patient__user__first_name', 'patient__user__last_name']
    readonly_fields = ['created_at', 'updated_at', 'calculate_total']
    list_per_page = 25
    date_hierarchy = 'release_date'
    
    fieldsets = (
        ('Patient & Doctor', {
            'fields': ('patient', 'assigned_doctor')
        }),
        ('Stay Details', {
            'fields': ('admit_date', 'release_date', 'day_spent')
        }),
        ('Charges', {
            'fields': ('room_charge', 'medicine_cost', 'doctor_fee', 'other_charge', 'total', 'calculate_total')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def calculate_total(self, obj):
        if obj.pk:
            calculated = float(obj.room_charge) + float(obj.medicine_cost) + float(obj.doctor_fee) + float(obj.other_charge)
            if calculated == float(obj.total):
                return format_html('<span style="color: green;">✓ Correct: ${}</span>', calculated)
            else:
                return format_html('<span style="color: red;">⚠ Mismatch: ${} (should be {})</span>', obj.total, calculated)
        return '-'
    calculate_total.short_description = 'Total Verification'
