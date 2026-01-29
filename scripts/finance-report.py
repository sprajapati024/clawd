#!/usr/bin/env python3
"""
Clarke's Finance Report Generator
Generates weekly summaries and monthly PDF reports
"""

import json
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

FINANCE_DIR = Path("/root/clawd/finance")
BUDGET_FILE = FINANCE_DIR / "budget.json"
TRANSACTIONS_DIR = FINANCE_DIR / "transactions"
REPORTS_DIR = FINANCE_DIR / "reports"

REPORTS_DIR.mkdir(exist_ok=True)

def load_budget():
    """Load budget configuration"""
    with open(BUDGET_FILE) as f:
        return json.load(f)

def get_current_cycle_dates():
    """Get start and end dates for current cycle (27th to 27th)"""
    today = datetime.now()
    
    # If we're before the 27th, cycle started last month
    if today.day < 27:
        cycle_start = datetime(today.year, today.month - 1 if today.month > 1 else 12, 27)
        if today.month == 1:
            cycle_start = cycle_start.replace(year=today.year - 1)
        cycle_end = datetime(today.year, today.month, 27)
    else:
        # After 27th, cycle started this month
        cycle_start = datetime(today.year, today.month, 27)
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year if today.month < 12 else today.year + 1
        cycle_end = datetime(next_year, next_month, 27)
    
    return cycle_start, cycle_end

def load_transactions(start_date, end_date):
    """Load all transactions within date range"""
    transactions = []
    
    # Check all CSV files in the date range
    current = start_date
    while current <= end_date:
        month_file = TRANSACTIONS_DIR / f"{current.strftime('%Y-%m')}.csv"
        if month_file.exists():
            with open(month_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    trans_date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                    if start_date <= trans_date <= end_date:
                        row['date_obj'] = trans_date
                        row['amount'] = float(row['amount'])
                        transactions.append(row)
        
        # Move to next month
        if current.month == 12:
            current = datetime(current.year + 1, 1, 1)
        else:
            current = datetime(current.year, current.month + 1, 1)
    
    return transactions

def generate_weekly_summary():
    """Generate weekly summary (last 7 days)"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    budget = load_budget()
    transactions = load_transactions(start_date, end_date)
    
    # Group by category
    by_category = {}
    total_spent = 0
    
    for trans in transactions:
        cat = trans['category']
        amount = trans['amount']
        
        if cat not in by_category:
            by_category[cat] = {'count': 0, 'total': 0, 'items': []}
        
        by_category[cat]['count'] += 1
        by_category[cat]['total'] += amount
        by_category[cat]['items'].append(trans)
        total_spent += amount
    
    # Format output
    report = []
    report.append("📊 WEEKLY FINANCE SUMMARY")
    report.append("=" * 50)
    report.append(f"Period: {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}")
    report.append("")
    report.append(f"💰 Total Spent: ${total_spent:,.2f}")
    report.append(f"📝 Transactions: {len(transactions)}")
    report.append("")
    report.append("BY CATEGORY:")
    report.append("-" * 50)
    
    for cat, data in sorted(by_category.items(), key=lambda x: x[1]['total'], reverse=True):
        report.append(f"  {cat:20} ${data['total']:7.2f} ({data['count']} items)")
    
    report.append("")
    report.append("=" * 50)
    
    return "\n".join(report)

def generate_monthly_summary():
    """Generate monthly summary for current cycle (27th-27th)"""
    cycle_start, cycle_end = get_current_cycle_dates()
    budget = load_budget()
    transactions = load_transactions(cycle_start, cycle_end)
    
    # Group by category
    by_category = {}
    total_spent = 0
    
    for trans in transactions:
        cat = trans['category']
        amount = trans['amount']
        
        if cat not in by_category:
            by_category[cat] = {'count': 0, 'total': 0}
        
        by_category[cat]['count'] += 1
        by_category[cat]['total'] += amount
        total_spent += amount
    
    # Calculate vs budget
    budget_summary = budget['summary']
    income = budget_summary['total_income']
    budgeted_expenses = budget_summary['total_expenses']
    
    actual_savings = income - total_spent
    budgeted_savings = budget_summary['net_monthly']
    
    # Format output
    report = []
    report.append("📈 MONTHLY FINANCE REPORT")
    report.append("=" * 50)
    report.append(f"Cycle: {cycle_start.strftime('%b %d')} - {cycle_end.strftime('%b %d, %Y')}")
    report.append("")
    report.append("INCOME vs EXPENSES:")
    report.append("-" * 50)
    report.append(f"  Income (monthly):        ${income:,.2f}")
    report.append(f"  Budgeted Expenses:       ${budgeted_expenses:,.2f}")
    report.append(f"  Actual Spent (so far):   ${total_spent:,.2f}")
    report.append(f"  Projected Savings:       ${actual_savings:,.2f}")
    report.append(f"  Budgeted Savings:        ${budgeted_savings:,.2f}")
    report.append("")
    
    savings_rate = (actual_savings / income) * 100 if income > 0 else 0
    report.append(f"  💰 Current Savings Rate: {savings_rate:.1f}%")
    report.append(f"  🎯 Target Savings Rate:  {budget_summary['savings_rate']*100:.1f}%")
    report.append("")
    report.append("SPENDING BY CATEGORY:")
    report.append("-" * 50)
    
    for cat, data in sorted(by_category.items(), key=lambda x: x[1]['total'], reverse=True):
        report.append(f"  {cat:20} ${data['total']:7.2f} ({data['count']} transactions)")
    
    report.append("")
    report.append(f"📝 Total Transactions: {len(transactions)}")
    report.append("=" * 50)
    
    return "\n".join(report)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "weekly"
    
    if mode == "weekly":
        print(generate_weekly_summary())
    elif mode == "monthly":
        print(generate_monthly_summary())
    else:
        print("Usage: finance-report.py [weekly|monthly]")
        sys.exit(1)

if __name__ == "__main__":
    main()
