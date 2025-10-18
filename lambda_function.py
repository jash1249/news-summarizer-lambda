import json
import urllib.request
from html.parser import HTMLParser

class ArticleParser(HTMLParser):
    """Simple HTML parser to extract text from articles"""
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.in_body = False
    
    def handle_starttag(self, tag, attrs):
        if tag in ['p', 'article', 'div']:
            self.in_body = True
    
    def handle_data(self, data):
        if self.in_body and data.strip():
            self.text_content.append(data.strip())
    
    def handle_endtag(self, tag):
        if tag in ['p', 'article', 'div']:
            self.in_body = False
    
    def get_text(self):
        return ' '.join(self.text_content)

def fetch_article(url):
    """Fetch article content from URL using built-in libraries only"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        parser = ArticleParser()
        parser.feed(html)
        text = parser.get_text()
        
        # Extract title (simple approach)
        title_start = html.find('<title>')
        title_end = html.find('</title>')
        title = html[title_start+7:title_end] if title_start != -1 else "Article"
        
        return {
            'success': True,
            'title': title,
            'text': text[:5000]  # Limit to 5000 chars
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def simple_summarize(text, max_sentences=3):
    """Simple extractive summarization - no external API needed"""
    # Split into sentences
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Return first few sentences as summary
    summary = '. '.join(sentences[:max_sentences]) + '.'
    return summary

def lambda_handler(event, context):
    """Main Lambda handler function"""
    try:
        # Parse request
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        url = body.get('url')
        
        if not url:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Missing URL parameter'})
            }
        
        # Fetch article
        article = fetch_article(url)
        
        if not article['success']:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': f"Failed to fetch article: {article['error']}"})
            }
        
        # Generate simple summary
        summary = simple_summarize(article['text'])
        
        # Return response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'url': url,
                'title': article['title'],
                'summary': summary,
                'method': 'Simple extractive summarization'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
