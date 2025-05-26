from flask import Blueprint, render_template
from app.models import User
from flask_login import login_required
import pandas as pd
import json

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    df = pd.read_csv('app/dataset.csv')

    # Basic counts
    total = len(df)
    fraud = df['is_fraud'].sum()
    normal = total - fraud

    # Transaction types
    tx_counts = df['transaction_type'].value_counts()

    # Fraud by transaction type
    fraud_tx = df[df['is_fraud'] == 1]['transaction_type'].value_counts()

    # Channel usage
    channel_counts = df['channel'].value_counts()

    # Summary statistics
    summary_table = df.describe().round(2).to_html(classes="table-auto text-sm", border=0)

    
    return render_template("dashboard.html",
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
