import json
import pandas as pd

def account_age(created_at):
    try:
        days = (pd.Timestamp.utcnow() - pd.to_datetime(created_at)).days
        pts = days / 365 * 20
        return min(int(round(pts)), 20)
    except:
        return 0

def website_live(url):
    if pd.isnull(url) or not isinstance(url, str) or not url.strip():
        return -80
    try:
        r = requests.head(url, timeout=5)
        if 200 <= r.status_code < 400:
            return 15
        return 5
    except:
        return 0

def account_socials(text):
    try:
        links = json.loads(text)
        return min(len(links) * 5, 20)
    except:
        return 0

def benefits(row):
    benefit_cols = [c for c in row.index if c.startswith("benefit")]
    total = sum(row[c] for c in benefit_cols)
    pts = total / 10 * 20
    return min(int(round(pts)), 20)

def webhook(text):
    try:
        hooks = json.loads(text)
        if isinstance(hooks, list) and hooks:
            return 10
        else:
            return 0
        # return 10 if isinstance(hooks, list) and hooks else 0
    except:
        return 0

def has_checkout(val):
    if pd.notnull(val):
        return 20
    else:
        return 0
    # return 20 if pd.notnull(val) else 0

def has_details(text):
    try:
        data = json.loads(text)
        if data:
            return 10
        else:
            return 0
    except (json.JSONDecodeError, TypeError):
        return 0

def switching(text):
    try:
        data = json.loads(text)
        if data.get("switching"):
            return 5
        else:
            return 0 
    except (json.JSONDecodeError, TypeError):
        return 0
                          
        
