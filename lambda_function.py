import json
import re
import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; NewsSummarizerBot/1.0)'}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return None, f"Error fetching URL: {str(e)}"

    soup = BeautifulSoup(resp.text, 'html.parser')
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    title = soup.title.string.strip() if soup.title else "No title found"
    text = ' '.join(paragraphs)
    return (title, text)


def summarize_text(text, max_sentences=5):
    sentences = re.split(r'(?<=[.!?]) +', text)
    if len(sentences) <= max_sentences:
        return text

    from collections import Counter
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    common = set([w for w, _ in word_counts.most_common(200)])

    scores = {}
    for s in sentences:
        scores[s] = sum(1 for w in re.findall(r'\w+', s.lower()) if w in common)
    top = sorted(scores, key=scores.get, reverse=True)[:max_sentences]
    return ' '.join(top)


def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Requested-With',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }

    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'CORS OK'})}

    try:
        body = json.loads(event.get('body') or '{}')
        url = body.get('url', '').strip()
    except Exception as e:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid JSON body'})}

    if not url:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'No URL provided'})}

    title, text_or_error = extract_text_from_url(url)
    if not title:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': text_or_error})}

    summary = summarize_text(text_or_error)

    # ✅ Always return JSON
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'title': title,
            'summary': summary,
            'url': url
        })
    }
