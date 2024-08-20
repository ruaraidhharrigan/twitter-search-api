# Twitter Scraper API

This project is a FastAPI-based REST API that fetches tweets based on a search query using the `twscrape` library. It is designed to be clean, maintainable, and scalable.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [Running Tests](#running-tests)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8+
- pip

### Clone the Repository

```bash
git clone https://github.com/yourusername/twitter-scrapper-api.git
cd twitter-scrapper-api
```

### Setting Up a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Create a .env file in the twitter-scrapper-api/ directory and add your environment variables:

```txt
USERNAME=your_twitter_username
PASSWORD=your_twitter_password
EMAIL=your_email_address
```

### Usage

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.

To search for tweets related to "ETH"

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/search?query=eth'
```

### Endpoints

/search

	•	Description: Fetches tweets based on a search query.
	•	Method: GET
	•	Query Parameters:
	•	query: The search term (e.g., eth).
	•	Response: JSON array of tweets with filtered information including:
	•	date: The date of the tweet.
	•	username: The Twitter username of the author.
	•	displayname: The display name of the author.
	•	followers_count: The number of followers of the author.
	•	raw_content: The content of the tweet.
	•	reply_count: The number of replies to the tweet.
	•	quote_count: The number of times the tweet was quoted.
	•	like_count: The number of likes the tweet received.
	•	bookmark_count: The number of times the tweet was bookmarked.

Example response
```json
{
    "query": "eth",
    "tweets": [
        {
            "date": "2024-08-20T14:14:18+00:00",
            "username": "jasperturing",
            "displayname": "yJasper.eth",
            "followers_count": 239,
            "raw_content": "@wickhunterr Approximately 400K 😌",
            "reply_count": 0,
            "quote_count": 0,
            "like_count": 0,
            "bookmark_count": 0
        },
        ...
    ]
}
```

### License

This is the complete `README.md` file that provides a full overview of your project, including installation, configuration, usage, and more.