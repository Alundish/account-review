import pandas as pd
from utils.scoring import (
    account_age,
    website_live,
    account_socials,
    benefits,
    webhook,
    has_checkout,
    switching,
)
from utils.compliance import compliance
from utils.details import (
    detailscontent,
    detailseval,
)    

def main():
    df = pd.read_csv("data/example_data.csv", encoding="utf-8")

    df["trust_score"] = 0
    df["compliance_score"] = 0
    df["compliance_status"] = ""
    df["compliance_reason"] = ""
    df["details_score"] = 0
    df["details_status"] = ""
    df["details_reason"] = ""
    
    df["account_age_score"] = 0
    df["website_live_score"] = 0
    df["account_socials_score"] = 0
    df["benefits_score"] = 0
    df["webhook_score"] = 0
    df["has_checkout_score"] = 0
    df["switching_score"] = 0
    
    for i, row in df.iterrows():
        comp_score, comp_status, comp_reason = compliance(row.get("website", ""))
        df.at[i, "compliance_score"] = comp_score
        df.at[i, "compliance_status"] = comp_status
        df.at[i, "compliance_reason"] = comp_reason

        details_score, details_status, details_reason = detailseval(detailscontent(row.get("details", "{}")))
        df.at[i, "details_score"] = details_score
        df.at[i, "details_status"] = details_status
        df.at[i, "details_reason"] = details_reason

        score = 0
        
        account_age_score = account_age(row.get("created_at", ""))
        df.at[i, "account_age_score"] = account_age_score
        score += account_age_score
        
        website_live_score = website_live(row.get("website", ""))
        df.at[i, "website_live_score"] = website_live_score
        score += website_live_score

        account_socials_score = account_socials(row.get("socials", "[]"))
        df.at[i, "account_socials_score"] = account_socials_score
        score += account_socials_score

        benefits_score = benefits(row)
        df.at[i, "benefits_score"] = benefits_score
        score += benefits_score

        webhook_score = webhook(row.get("webhook_endpoints", "[]"))
        df.at[i, "webhook_score"] = webhook_score
        score += webhook_score

        has_checkout_score = has_checkout(row.get("checkout_first_session_at"))
        df.at[i, "has_checkout_score"] = has_checkout_score
        score += has_checkout_score

        switching_score = switching(row.get("details", "{}"))
        df.at[i, "switching_score"] = switching_score
        score += switching_score

        score += comp_score
        score += details_score
        df.at[i, "trust_score"] = min(max(score, 0), 100)

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.width", None)

    print(df[["id", "trust_score", "compliance_score", "compliance_status", "compliance_reason", "details_score", "details_status", "details_reason", "account_age_score", "website_live_score", "account_socials_score", "benefits_score", "webhook_score", "has_checkout_score", "switching_score"]])
    df.to_csv("data/data_with_compliance.csv", index=False)

if __name__ == "__main__":
    main()

