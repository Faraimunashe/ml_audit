from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
import pandas as pd
import numpy as np
import os
import joblib
from werkzeug.utils import secure_filename
from app.forms import UploadCSVForm
from app.models import AuditLog
from . import db

audit_bp = Blueprint('audit', __name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = joblib.load("app/topnotch_iforest_model.pkl")
scaler = joblib.load("app/topnotch_scaler.pkl")

@audit_bp.route('/audit', methods=['GET', 'POST'])
@login_required
def audit():
    form = UploadCSVForm()
    counts = None
    output_filename = None

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath)
            X = df.drop(columns=[
                'transaction_id', 'account_id', 'timestamp',
                'location', 'transaction_type', 'channel'
            ])
            X_scaled = scaler.transform(X)
            predictions = model.predict(X_scaled)
            df['fraud_flag'] = np.where(predictions == -1, 'Fraudulent', 'Normal')

            output_filename = f"audited_{filename}"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            df.to_csv(output_path, index=False)

            fraud_count = int((df['fraud_flag'] == 'Fraudulent').sum())
            normal_count = int((df['fraud_flag'] == 'Normal').sum())
            counts = {'fraud': fraud_count, 'normal': normal_count}

            # ✅ Log to AuditLog
            log_entry = AuditLog(
                model_name="FraudDetection",
                model_id=None,
                action="audit_run",
                previous_data=None,
                new_data={
                    "input_file": filename,
                    "output_file": output_filename,
                    "counts": counts
                },
                user_id=current_user.get_id()
            )
            db.session.add(log_entry)
            db.session.commit()

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    return render_template('audit.html', form=form, counts=counts, output_file=output_filename)


@audit_bp.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(filepath, as_attachment=True)