from flask import Blueprint, render_template
from app.models import User
from flask_login import login_required
import pandas as pd
import json
import os

analyse_bp = Blueprint('analyse', __name__)
OUTPUT_FOLDER = 'static/outputs'

@analyse_bp.route('/analyse/<filename>')
@login_required
def analyse(filename):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    df = pd.read_csv(filepath)

    total = len(df)
    fraud = (df['fraud_flag'] == 'Fraudulent').sum()
    normal = total - fraud

    tx_counts = df['transaction_type'].value_counts()
    fraud_tx = df[df['fraud_flag'] == 'Fraudulent']['transaction_type'].value_counts()
    channel_counts = df['channel'].value_counts()
    summary_table = df.describe().round(2).to_html(classes="table-auto text-sm", border=0)

    return render_template("analyse.html",
        total=total,
        fraud=fraud,
        normal=normal,
        tx_labels=json.dumps(list(tx_counts.index)),
        tx_data=json.dumps([int(v) for v in tx_counts.values]),
        fraud_labels=json.dumps(list(fraud_tx.index)),
        fraud_data=json.dumps([int(v) for v in fraud_tx.values]),
        channel_labels=json.dumps(list(channel_counts.index)),
        channel_data=json.dumps([int(v) for v in channel_counts.values]),
        summary_table=summary_table
    )
