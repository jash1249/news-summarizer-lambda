# News Summarizer - Serverless Application

## Objective
A serverless function that takes a news article URL and returns a summarized version using AWS Lambda.

## Features
- ✅ Pure Python implementation (no external dependencies)
- ✅ Deployed on AWS Lambda
- ✅ HTTP API endpoint via Lambda Function URL
- ✅ Simple extractive summarization
- ✅ Web interface for testing
- ✅ CORS enabled for browser access

## Architecture
User → Lambda Function URL → Lambda Function → Article Summary

## Setup Steps

### Prerequisites
- AWS Account
- Python 3.x installed locally

### Deployment

1. Clone this repository
2. Create `lambda_function.zip`:

python -m zipfile -c lambda_function.zip lambda_function.py

3. Log into AWS Console
4. Create new Lambda function with Python 3.11 runtime
5. Upload `lambda_function.zip`
6. Create Function URL with CORS enabled
7. Test using the web interface (`test-ui.html`)

## Usage

### Using cURL

curl -X POST "https://ubvfvqlxvkbyl7252iylcuqqs40jovna.lambda-url.ap-south-1.on.aws/" -H "Content-Type: application/json" -d "{\"url\": \"https://www.bbc.com/news/technology\"}"


### Using Web Interface
1. Open `test-ui.html` in browser
2. Enter article URL
3. Click "Summarize Article"

## Implementation Details

### Technology Stack
- **Language:** Python 3.11
- **Platform:** AWS Lambda
- **API:** Lambda Function URL
- **Libraries:** Built-in Python libraries only (urllib, json, html.parser)

### Code Structure
- `lambda_function.py` - Main Lambda handler
- `test-ui.html` - Web interface for testing
- `README.md` - Documentation

## Challenges & Solutions

### Challenge 1: External Dependencies
**Issue:** Many article extraction libraries (newspaper3k, beautifulsoup4) have complex dependencies that cause installation issues on Windows.

**Solution:** Used only built-in Python libraries (urllib, html.parser) for article extraction.

### Challenge 2: Summarization API Costs
**Issue:** Most NLP APIs have rate limits or require authentication.

**Solution:** Implemented simple extractive summarization using sentence extraction (first N sentences).

### Challenge 3: Deployment Complexity
**Issue:** Frameworks like Serverless and Chalice require Node.js and can have compatibility issues.

**Solution:** Deployed directly via AWS Console using .zip file upload.

## AI Tools Used

### GitHub Copilot
- Helped write the HTMLParser class for article extraction
- Suggested improvements to error handling

### ChatGPT/Perplexity
- Researched AWS Lambda best practices
- Debugged CORS configuration
- Learned about Lambda Function URLs

### How AI Helped
- Reduced development time by 60%
- Provided alternative approaches when external libraries failed
- Helped understand AWS Lambda timeout and memory configurations

## Future Enhancements
- Add caching with DynamoDB
- Integrate advanced NLP API (OpenAI)
- Support multiple languages
- Add sentiment analysis

## License
MIT

## Learning and Tricky

In my college projects i did on fake news detection by as of this one it is very new and made me learn each point and also i found some tricky while implementation and integration part while USING AWS LAMBDA