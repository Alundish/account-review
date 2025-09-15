from .helpers import scrape_website
from .config import client

ACCEPTABLE_USE = scrape_website('https://docs.paymentprocessor.tld/merchant-of-record/acceptable-use')

def compliance(url):
    content = scrape_website(url)
    if not content:
        return -10, "NON-COMPLIANT", "Could not fetch or parse site"
    else:
        snippet = content[:2000]
        prompt = (
            f"Acceptable-Use: {ACCEPTABLE_USE}\n\n"
            f"Content:\n\"\"\"\n{snippet}\n\"\"\"\n"
            "Evaluate 'Content' to determine what products or services the organization offers, and determine if they align with the acceptable-use policy described in 'Acceptable-Use'.\n"
            "Respond with one of the following:\n"
            "COMPLIANT – if the services offered do not violate the acceptable-use policy.\n"
            "NON-COMPLIANT – if the services offered violate the acceptable use policy, JavaScript is disabled, or the content is missing or empty.\n"
            "If the result is NON-COMPLIANT, include a second line starting with REASON: that briefly explains why, including any of the following: policy violations, JavaScript issues, or lack of content.\n"
            "If the result is COMPLIANT, do not include a reason or explanation.\n"
        )

        try:
            resp = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            text = resp.choices[0].message.content.strip()
            status = "UNKNOWN"
            reason = ""

            for line in text.splitlines():
                up = line.upper().strip()
                if up == "COMPLIANT":
                    status = "COMPLIANT"
                elif up == "NON-COMPLIANT":
                    status = "NON-COMPLIANT"
                elif up.startswith("REASON:"):
                    reason = line.split(":", 1)[1].strip()
                score = 20 if status == "COMPLIANT" else -25
            return score, status, reason
            # return score, status, reason, snippet

        except Exception as e:
            return 0, "UNKNOWN", f"LLM error: {e}"

