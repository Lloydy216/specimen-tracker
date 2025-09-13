from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Patient, Sample, TestOrder

bp = Blueprint("main", __name__)

# Home
@bp.route("/")
def index():
    total_patients = Patient.query.count()
    total_samples = Sample.query.count()
    total_tests = TestOrder.query.count()
    
    # Count pending results (tests without results)
    pending_results = TestOrder.query.filter(TestOrder.result.is_(None)).count()
    
    # Get status counts for samples
    status_counts = {
        'received': Sample.query.filter_by(status='received').count(),
        'processing': Sample.query.filter_by(status='processing').count(),
        'completed': Sample.query.filter_by(status='completed').count(),
        'rejected': Sample.query.filter_by(status='rejected').count()
    }
    
    recent_samples = Sample.query.order_by(Sample.collection_datetime.desc()).limit(5).all()
    
    return render_template("index.html", 
                           total_patients=total_patients, 
                           total_samples=total_samples,
                           total_tests=total_tests, 
                           pending_results=pending_results,
                           status_counts=status_counts,
                           recent_samples=recent_samples)

# ---------- Patients CRUD ----------
@bp.route("/patients")
def patients_list():
    q = request.args.get("q", "").strip()
    if q:
        patients = Patient.query.filter(
            (Patient.full_name.ilike(f"%{q}%")) | (Patient.nhs_number.ilike(f"%{q}%"))
        ).all()
    else:
        patients = Patient.query.order_by(Patient.full_name.asc()).all()
    return render_template("patients_list.html", patients=patients, q=q)

@bp.route("/patients/new", methods=["GET", "POST"])
def patients_new():
    if request.method == "POST":
        nhs_number = request.form.get("nhs_number", "").strip()
        full_name = request.form.get("full_name", "").strip()
        dob = request.form.get("date_of_birth", "").strip()
        
        if not nhs_number or not full_name or not dob:
            flash("All fields are required.", "error")
            return redirect(url_for("main.patients_new"))
        
        if Patient.query.filter_by(nhs_number=nhs_number).first():
            flash("NHS number must be unique.", "error")
            return redirect(url_for("main.patients_new"))
        
        try:
            dob_dt = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            flash("Date of birth must be YYYY-MM-DD.", "error")
            return redirect(url_for("main.patients_new"))
        
        p = Patient(nhs_number=nhs_number, full_name=full_name, date_of_birth=dob_dt)
        db.session.add(p)
        db.session.commit()
        flash("Patient created successfully.", "success")
        return redirect(url_for("main.patients_list"))
    
    return render_template("patients_form.html", patient=None)

@bp.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
def patients_edit(patient_id):
    p = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        p.nhs_number = request.form.get("nhs_number", "").strip()
        p.full_name = request.form.get("full_name", "").strip()
        dob = request.form.get("date_of_birth", "").strip()
        
        try:
            p.date_of_birth = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            flash("Date of birth must be YYYY-MM-DD.", "error")
            return redirect(url_for("main.patients_edit", patient_id=patient_id))
        
        db.session.commit()
        flash("Patient updated successfully.", "success")
        return redirect(url_for("main.patients_list"))
    
    return render_template("patients_form.html", patient=p)

@bp.route("/patients/<int:patient_id>/delete", methods=["POST"])
def patients_delete(patient_id):
    p = Patient.query.get_or_404(patient_id)
    db.session.delete(p)
    db.session.commit()
    flash("Patient deleted successfully.", "success")
    return redirect(url_for("main.patients_list"))

# ---------- Samples CRUD ----------
@bp.route("/samples")
def samples_list():
    q = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "").strip()
    
    query = Sample.query
    
    if q:
        query = query.join(Patient).filter(
            (Patient.full_name.ilike(f"%{q}%")) | (Sample.sample_type.ilike(f"%{q}%"))
        )
    
    if status_filter:
        query = query.filter(Sample.status == status_filter)
    
    samples = query.order_by(Sample.collection_datetime.desc()).all()
    patients = Patient.query.order_by(Patient.full_name.asc()).all()
    
    return render_template("samples_list.html", samples=samples, patients=patients, q=q, status_filter=status_filter)

@bp.route("/samples/new", methods=["GET", "POST"])
def samples_new():
    patients = Patient.query.order_by(Patient.full_name.asc()).all()
    if not patients:
        flash("Please add a patient first.", "error")
        return redirect(url_for("main.patients_new"))
    
    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        sample_type = request.form.get("sample_type", "").strip()
        collection_datetime = request.form.get("collection_datetime", "").strip()
        status = request.form.get("status", "received")
        
        if not patient_id or not sample_type:
            flash("Patient and sample type are required.", "error")
            return redirect(url_for("main.samples_new"))
        
        try:
            if collection_datetime:
                collection_dt = datetime.strptime(collection_datetime, "%Y-%m-%dT%H:%M")
            else:
                collection_dt = datetime.now(timezone.utc)
        except ValueError:
            flash("Invalid collection date/time format.", "error")
            return redirect(url_for("main.samples_new"))
        
        s = Sample(
            patient_id=patient_id,
            sample_type=sample_type,
            collection_datetime=collection_dt,
            status=status
        )
        db.session.add(s)
        db.session.commit()
        flash("Sample created successfully.", "success")
        return redirect(url_for("main.samples_list"))
    
    return render_template("samples_form.html", patients=patients, sample=None)

@bp.route("/samples/<int:sample_id>/edit", methods=["GET", "POST"])
def samples_edit(sample_id):
    s = Sample.query.get_or_404(sample_id)
    patients = Patient.query.order_by(Patient.full_name.asc()).all()
    
    if request.method == "POST":
        s.patient_id = request.form.get("patient_id")
        s.sample_type = request.form.get("sample_type", "").strip()
        collection_datetime = request.form.get("collection_datetime", "").strip()
        s.status = request.form.get("status", "received")
        
        try:
            if collection_datetime:
                s.collection_datetime = datetime.strptime(collection_datetime, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Invalid collection date/time format.", "error")
            return redirect(url_for("main.samples_edit", sample_id=sample_id))
        
        db.session.commit()
        flash("Sample updated successfully.", "success")
        return redirect(url_for("main.samples_list"))
    
    return render_template("samples_form.html", patients=patients, sample=s)

@bp.route("/samples/<int:sample_id>/delete", methods=["POST"])
def samples_delete(sample_id):
    s = Sample.query.get_or_404(sample_id)
    db.session.delete(s)
    db.session.commit()
    flash("Sample deleted successfully.", "success")
    return redirect(url_for("main.samples_list"))

# ---------- Tests CRUD ----------
@bp.route("/tests")
def tests_list():
    q = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "").strip()
    
    query = TestOrder.query.join(Sample).join(Patient)
    
    if q:
        query = query.filter(
            (Patient.full_name.ilike(f"%{q}%")) | 
            (TestOrder.assay.ilike(f"%{q}%")) |
            (Sample.sample_type.ilike(f"%{q}%"))
        )
    
    if status_filter == "pending":
        query = query.filter(TestOrder.result.is_(None))
    elif status_filter == "completed":
        query = query.filter(TestOrder.result.isnot(None))
    
    tests = query.order_by(TestOrder.id.desc()).all()
    samples = Sample.query.order_by(Sample.collection_datetime.desc()).all()
    
    return render_template("tests_list.html", tests=tests, samples=samples, q=q, status_filter=status_filter)

@bp.route("/tests/new", methods=["GET", "POST"])
def tests_new():
    samples = Sample.query.order_by(Sample.collection_datetime.desc()).all()
    if not samples:
        flash("Please add a sample first.", "error")
        return redirect(url_for("main.samples_new"))
    
    if request.method == "POST":
        sample_id = request.form.get("sample_id")
        assay = request.form.get("assay", "").strip()
        priority = request.form.get("priority", "routine")
        
        if not sample_id or not assay:
            flash("Sample and assay are required.", "error")
            return redirect(url_for("main.tests_new"))
        
        t = TestOrder(sample_id=sample_id, assay=assay, priority=priority)
        db.session.add(t)
        db.session.commit()
        flash("Test order created successfully.", "success")
        return redirect(url_for("main.tests_list"))
    
    return render_template("tests_form.html", samples=samples, test=None)

@bp.route("/tests/<int:test_id>/edit", methods=["GET", "POST"])
def tests_edit(test_id):
    t = TestOrder.query.get_or_404(test_id)
    samples = Sample.query.order_by(Sample.collection_datetime.desc()).all()
    
    if request.method == "POST":
        t.sample_id = request.form.get("sample_id")
        t.assay = request.form.get("assay", "").strip()
        t.priority = request.form.get("priority", "routine")
        t.result = request.form.get("result", "").strip() or None
        
        result_date = request.form.get("result_date", "").strip()
        if result_date and t.result:
            try:
                t.result_date = datetime.strptime(result_date, "%Y-%m-%d")
            except ValueError:
                flash("Invalid result date format.", "error")
                return redirect(url_for("main.tests_edit", test_id=test_id))
        elif t.result:
            t.result_date = datetime.now(timezone.utc)
        else:
            t.result_date = None
        
        db.session.commit()
        flash("Test order updated successfully.", "success")
        return redirect(url_for("main.tests_list"))
    
    return render_template("tests_form.html", samples=samples, test=t)

@bp.route("/tests/<int:test_id>/delete", methods=["POST"])
def tests_delete(test_id):
    t = TestOrder.query.get_or_404(test_id)
    db.session.delete(t)
    db.session.commit()
    flash("Test order deleted successfully.", "success")
    return redirect(url_for("main.tests_list"))
