import json
from .helpers import scrape_website
from .config import client

ACCEPTABLE_USE = scrape_website('https://docs.paymentprocessor.tld/merchant-of-record/acceptable-use')


def detailscontent(text):
    try:
        data = json.loads(text)
        intended_use = data.get("intended_use", "")
        product_description = data.get("product_description", "")
        content = intended_use + "\n" + product_description
        return content.strip()
    except (json.JSONDecodeError, TypeError):
        return ""


def detailseval(content):
    if not content:
        return -10, "NON-COMPLIANT", "No details available"
    else:
        prompt = (
            f"Acceptable-Use: {ACCEPTABLE_USE}\n\n"
            f"Content:\n\"\"\"\n{content}\n\"\"\"\n"
            "Evaluate 'Content' to determine if the intended use and product description align with the acceptable-use policy described in 'Acceptable-Use'.\n"
            "Respond with one of the following:\n"
            "COMPLIANT – if the services offered do not violate the acceptable-use policy.\n"
            "NON-COMPLIANT – if the services offered violate the acceptable use policy or there is no content to evaluate\n"
            "If the result is NON-COMPLIANT, include a second line starting with REASON: that briefly explains why\n"
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
                score = 20 if status == "COMPLIANT" else -20
            return score, status, reason

        except Exception as e:
            return 0, "UNKNOWN", f"LLM error: {e}"
