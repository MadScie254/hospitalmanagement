import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospitalmanagement.settings')
django.setup()

from django.contrib.auth.models import User
from hospital.models import Doctor, Patient, Appointment, PatientDischargeDetails

def verify_relationships():
    print("Verifying relationships...")

    # 1. Create Doctor
    print("Creating Doctor...")
    doc_user = User.objects.create_user(username='testdoc', password='password')
    doctor = Doctor.objects.create(
        user=doc_user,
        address="123 Doc St",
        mobile="1234567890",
        department="Cardiologist",
        status=True
    )
    print(f"Doctor created: {doctor}")

    # 2. Create Patient and assign Doctor via FK
    print("Creating Patient...")
    pat_user = User.objects.create_user(username='testpat', password='password')
    patient = Patient.objects.create(
        user=pat_user,
        address="456 Pat St",
        mobile="0987654321",
        symptoms="Fever",
        assigned_doctor=doctor, # Setting FK
        status=True
    )
    print(f"Patient created: {patient}")

    # Verify Legacy Field Sync
    print(f"Patient assignedDoctorId (Legacy): {patient.assignedDoctorId}")
    print(f"Doctor User ID: {doc_user.id}")
    assert patient.assignedDoctorId == doc_user.id, "Patient assignedDoctorId not synced!"
    print("PASS: Patient assignedDoctorId synced correctly.")

    # 3. Create Appointment via FK
    print("Creating Appointment...")
    appointment = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        description="Checkup",
        status=True
    )
    print(f"Appointment created: {appointment}")

    # Verify Legacy Fields Sync
    print(f"Appointment doctorId (Legacy): {appointment.doctorId}")
    print(f"Appointment patientId (Legacy): {appointment.patientId}")
    assert appointment.doctorId == doc_user.id, "Appointment doctorId not synced!"
    assert appointment.patientId == pat_user.id, "Appointment patientId not synced!"
    print("PASS: Appointment legacy fields synced correctly.")

    # 4. Create Discharge Details via FK
    print("Creating Discharge Details...")
    discharge = PatientDischargeDetails.objects.create(
        patient=patient,
        assigned_doctor=doctor,
        admit_date=date.today(),
        release_date=date.today(),
        day_spent=1,
        room_charge=100,
        medicine_cost=50,
        doctor_fee=200,
        other_charge=10,
        total=360
    )
    print(f"Discharge created: {discharge}")

    # Verify Legacy Fields Sync
    print(f"Discharge patientId (Legacy): {discharge.patientId}")
    print(f"Discharge assignedDoctorName (Legacy): {discharge.assignedDoctorName}")
    assert discharge.patientId == pat_user.id, "Discharge patientId not synced!"
    assert discharge.assignedDoctorName == doctor.get_name, "Discharge assignedDoctorName not synced!"
    print("PASS: Discharge legacy fields synced correctly.")

    # Cleanup
    discharge.delete()
    appointment.delete()
    patient.delete()
    doctor.delete()
    pat_user.delete()
    doc_user.delete()
    print("Cleanup complete.")

if __name__ == '__main__':
    try:
        verify_relationships()
        print("ALL TESTS PASSED")
    except Exception as e:
        print(f"TEST FAILED: {e}")
        exit(1)
