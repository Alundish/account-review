# Account Review

This project accepts a CSV file as input that includes data describing client organizations, iterates through them, and assigns a "trust score" based on several variables.
It leverages OpenAI's API to perform additional evaluation to help identify violations of the acceptable use policy and other potential items of concern.

## Installation
#### Clone the repository

```
git clone https://github.com/Alundish/account-review
cd account-review
```

#### (Optional) Create and activate a virtual environment

```
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

#### Install dependencies

```
pip install -r requirements.txt
```

#### Create an .env file

Create an `.env` file in the root of the repository which includes a working OpenAI API Key

```
OPENAI_API_KEY='your api key here'

```
#### Prepare input data

Modify example_data.csv to include real customer data with resolvable domains


## Usage

Run the script

```
python main.py
```


## Roadmap

Some plans for future iterations:
- Add tests
- Add documentation/comments
- Comprehensive error handling and logging
- Performance improvements (apply suggestions from an AI coding assistant)
- Explore automation options
- A dashboard for viewing findings
- Fine tune scoring weights
- Test LLM scoring results with alternate language models
- Switch to a scraping solution that renders JS or leverage a scraping API, Google SERP, or an AI search engine (Brave/Perplexity)
- Parse social media feeds
- Score for future_annual_revenue, and previous_annual_revenue
- Score for terms like recurring and subscription
- Ensure customer submitted description aligns with URL scrape results
- Whois information, when domain was registered
- Domain reputation, e.g. virustotal.com
- Scan for abnormally high amount of sales in a short period of time (sales history not available in sample csv)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
