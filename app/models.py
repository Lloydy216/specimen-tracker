from datetime import datetime, timezone
from . import db

class Patient(db.Model):
    __tablename__ = "patient"
    id = db.Column(db.Integer, primary_key=True)
    nhs_number = db.Column(db.String(12), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    samples = db.relationship("Sample", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.full_name} ({self.nhs_number})>"

class Sample(db.Model):
    __tablename__ = "sample"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    sample_type = db.Column(db.String(50), nullable=False)  # e.g. Blood, Urine, Swab
    collection_datetime = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), nullable=False, default="received")  # received|processing|completed|rejected

    patient = db.relationship("Patient", back_populates="samples")
    test_orders = db.relationship("TestOrder", back_populates="sample", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sample {self.sample_type} for patient_id={self.patient_id}>"

class TestOrder(db.Model):
    __tablename__ = "test_order"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey("sample.id"), nullable=False)
    assay = db.Column(db.String(80), nullable=False)  # e.g. FBC, CRP, COVID-PCR
    priority = db.Column(db.String(10), nullable=False, default="routine")  # routine|urgent
    result = db.Column(db.Text, nullable=True)
    result_date = db.Column(db.DateTime, nullable=True)

    sample = db.relationship("Sample", back_populates="test_orders")

    def __repr__(self):
        return f"<TestOrder {self.assay} on sample_id={self.sample_id}>"
