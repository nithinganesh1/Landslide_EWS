from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.firebase_client import push_report, get_reports

report_bp = Blueprint("report", __name__)

@report_bp.route("/", methods=["GET"])
def report_view():
    reports = get_reports()
    return render_template("report.html", reports=reports)

@report_bp.route("/submit", methods=["POST"])
def submit_report():
    report = {
        "type":        request.form.get("type", "crack"),
        "description": request.form.get("description", ""),
        "latitude":    float(request.form.get("latitude") or 0),
        "longitude":   float(request.form.get("longitude") or 0),
        "severity":    request.form.get("severity", "low"),
        "contact":     request.form.get("contact", ""),
    }
    success = push_report(report)
    if success:
        flash("Report submitted successfully. Authorities have been notified.", "success")
    else:
        flash("Error submitting report. Please try again.", "danger")
    return redirect(url_for("report.report_view"))
