from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.firebase_client import push_report, get_reports
import logging

log = logging.getLogger(__name__)
report_bp = Blueprint("report", __name__)

@report_bp.route("/", methods=["GET"])
def report_view():
    reports = get_reports()
    return render_template("report.html", reports=reports)

@report_bp.route("/submit", methods=["POST"])
def submit_report():
    try:
        lat = request.form.get("latitude", "").strip()
        lon = request.form.get("longitude", "").strip()

        report = {
            "type":        request.form.get("type", "crack"),
            "description": request.form.get("description", "").strip(),
            "latitude":    float(lat) if lat else 0.0,
            "longitude":   float(lon) if lon else 0.0,
            "severity":    request.form.get("severity", "low"),
            "contact":     request.form.get("contact", "").strip(),
        }
    except (ValueError, TypeError) as e:
        flash(f"Invalid form data: {e}", "danger")
        return redirect(url_for("report.report_view"))

    success, error_msg = push_report(report)

    if success:
        flash("Report submitted successfully. Authorities have been notified.", "success")
    else:
        flash(f"Could not submit report — {error_msg}", "danger")

    return redirect(url_for("report.report_view"))
