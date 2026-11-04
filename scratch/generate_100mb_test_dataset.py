import os
import sys
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TARGET_BYTES = 100 * 1024 * 1024  # 100 MB (104,857,600 bytes)
OUTPUT_FILE = ROOT / "data" / "batch_test_complaints_100mb.csv"

# Pre-defined realistic domain values
COMPANIES = [
    "Cedar Ridge Bank", "Riverbend Consumer Finance", "Blue Mesa Servicing",
    "Apex Crest Financial", "Horizon Trust", "Summit Mutual", "Beacon Community Bank",
    "Vanguard Credit Union", "Pinnacle Auto Lending", "Cascade National Bank"
]

PRODUCTS = [
    ("Credit card", "General-purpose credit card"),
    ("Checking or savings account", "Checking account"),
    ("Checking or savings account", "Savings account"),
    ("Mortgage", "Conventional fixed mortgage"),
    ("Student loan", "Federal student loan"),
    ("Vehicle loan or lease", "Loan"),
    ("Debt collection", "Credit card debt"),
    ("Credit reporting", "Credit reporting errors")
]

CHANNELS = ["Web", "Mobile app", "Branch", "Phone", "Postal Mail", "Email"]
STATES = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "WA", "NC", "GA", "MI", "VA", "AZ", "MA", "CO"]

NARRATIVE_TEMPLATES = [
    "I am writing to formally dispute an unauthorized charge of ${amount:.2f} that posted to my {product} account on {date}. Despite contacting customer care on three separate occasions, the charge has not been credited back to my available balance. I am requesting an immediate reversal and written explanation.",
    "My monthly statement shows an exorbitant overdraft fee of ${fee:.2f} assessed while my mobile application showed a positive settled balance. I promptly called phone support, but representatives were unhelpful and refused to escalate to a supervisor. Please remove this fee and adjust my account status.",
    "I submitted a full payoff amount of ${amount:.2f} for my vehicle financing account over three weeks ago. However, the lending department has failed to release the title or update my credit report to show paid in full. This severe delay is blocking my ability to register the vehicle in my home state.",
    "A debt collection agency identified as {company} has repeatedly called my workplace and contacted family members regarding an alleged delinquent balance that was already settled two years ago. I have submitted written cease-and-desist notices, but harassment continues in direct violation of the FDCPA.",
    "There is an inaccurate late payment remark appearing on my credit bureau report for account ending in {acct}. I have consistently maintained automatic bill payments and provided proof of timely remittance. This erroneous derogatory reporting has severely dropped my credit score.",
    "My checking account has been unexpectedly frozen without prior warning or reasonable justification, restricting access to my direct deposited payroll of ${amount:.2f}. As a result, critical household utilities and mortgage payments are bouncing. Immediate resolution and reinstatement is demanded.",
    "I requested an interest rate APR review and billing correction for my revolving credit line after promotional terms were prematurely cancelled. The customer service department has repeatedly provided contradictory explanations regarding fee schedules.",
    "Funds transferred via wire transfer on {date} for ${amount:.2f} have not been credited to the recipient's account, nor were they returned to my originating balance. Both institutions claim the other party is responsible for tracing the missing funds.",
    "I was charged recurring subscription fees of ${fee:.2f} per month from a vendor I explicitly cancelled six months ago. The bank promised a merchant block on my debit card, but subsequent transactions continued processing unimpeded.",
    "The escrow analysis conducted on my mortgage statement resulted in an unexpected monthly payment increase of ${fee:.2f}. When I requested a detailed breakdown of property tax and homeowner insurance disbursements, the documentation provided was incomplete and inconsistent."
]

print(f"Generating 100 MB test dataset at: {OUTPUT_FILE}")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

start_date = datetime(2023, 1, 1)

row_count = 0
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # Write CSV Header matching app expectation
    writer.writerow([
        "complaint_id",
        "date_received",
        "product",
        "sub_product",
        "company",
        "channel",
        "state",
        "complaint_narrative"
    ])

    while True:
        row_count += 1
        cid = f"TEST-BATCH-{row_count:07d}"
        d_offset = random.randint(0, 700)
        rec_date = (start_date + timedelta(days=d_offset)).strftime("%Y-%m-%d")
        prod, sub_prod = random.choice(PRODUCTS)
        comp = random.choice(COMPANIES)
        chan = random.choice(CHANNELS)
        state = random.choice(STATES)
        tmpl = random.choice(NARRATIVE_TEMPLATES)

        narrative = tmpl.format(
            amount=random.uniform(85.0, 4850.0),
            fee=random.uniform(15.0, 75.0),
            product=prod.lower(),
            date=rec_date,
            company=comp,
            acct=random.randint(1000, 9999)
        )

        writer.writerow([cid, rec_date, prod, sub_prod, comp, chan, state, narrative])

        # Check file size every 1,000 rows
        if row_count % 1000 == 0:
            f.flush()
            curr_size = os.fstat(f.fileno()).st_size
            if curr_size >= TARGET_BYTES:
                break

final_size = os.path.getsize(OUTPUT_FILE)
final_size_mb = final_size / (1024 * 1024)

print(f"\n✓ Completed successfully!")
print(f"  File: {OUTPUT_FILE}")
print(f"  Rows generated: {row_count:,}")
print(f"  Exact size: {final_size:,} bytes ({final_size_mb:.2f} MB)")
