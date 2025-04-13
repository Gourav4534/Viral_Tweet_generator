import os
import random
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TweetGenerator:
    def __init__(self):
        # Get and clean the Hugging Face API key
        self.hf_api_key = os.getenv("HF_API_KEY", "").strip()
        if not self.hf_api_key:
            print("Error: HF_API_KEY not found in environment variables")
            raise ValueError("HF_API_KEY is required")
            
        print(f"Hugging Face API Key: {self.hf_api_key[:8]}...")  # Only show first 8 chars for security
        self.news_api_key = os.getenv("NEWSDATA_API_KEY", "").strip()

    def get_tech_news(self):
        """Fetch latest technology news from NewsData.io"""
        try:
            url = "https://newsdata.io/api/1/news"
            params = {
                "apikey": self.news_api_key,
                "q": "technology",
                "language": "en",
                "category": "technology",
                "country": "us",
                "prioritydomain": "top",  # Get news from top domains
                "size": 10  # Get more results to choose from
            }
            print(f"Fetching news with params: {params}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get('results', [])
            # Sort by date to get the most recent news
            results.sort(key=lambda x: x.get('pubDate', ''), reverse=True)
            # Shuffle the top 5 most recent results
            recent_results = results[:5]
            random.shuffle(recent_results)
            return recent_results
        except Exception as e:
            print(f"Error fetching news: {e}")
            if hasattr(e, 'response'):
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            return []

    def generate_tweet(self, news_item, max_retries=3):
        """Generate a viral tweet using Hugging Face API with retry logic"""
        # Add some randomness to the prompt
        styles = [
            "technical and professional",
            "engaging and viral",
            "informative and shareable",
            "expert and authoritative"
        ]
        style = random.choice(styles)
        
        prompt = f"""
        Create a {style} tweet about this technology news:
        Title: {news_item.get('title', '')}
        Description: {news_item.get('description', '')}
        
        The tweet should be:
        - Technical but accessible
        - Include relevant hashtags
        - Be engaging and shareable
        - Under 280 characters
        - Include emojis where appropriate
        - Sound like a tech expert
        - Use a {style} tone
        
        Format the tweet in a way that would go viral in the tech community.
        """
        
        for attempt in range(max_retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self.hf_api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 280,
                        "temperature": 0.8,  # Increased temperature for more variety
                        "top_p": 0.9,
                        "do_sample": True
                    }
                }
                
                print(f"Attempt {attempt + 1}/{max_retries}: Sending request to Hugging Face API...")
                
                # Increase timeout for each retry
                timeout = 30 * (attempt + 1)
                response = requests.post(
                    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                    headers=headers,
                    json=data,
                    timeout=timeout
                )
                
                print(f"Response status code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0]['generated_text'].strip()
                    return result.get('generated_text', '').strip()
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    wait_time = 10 * (attempt + 1)
                    print(f"Model is loading. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Error generating tweet: Status {response.status_code}")
                    print(f"Response: {response.text}")
                    if attempt < max_retries - 1:
                        time.sleep(5)  # Wait before retry
                        continue
                    return None
                    
            except requests.exceptions.Timeout:
                print(f"Timeout on attempt {attempt + 1}. Retrying...")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
            except Exception as e:
                print(f"Error generating tweet: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
        
        return None

    def generate_viral_tweet(self):
        """Main function to generate a viral tweet"""
        try:
            news_items = self.get_tech_news()
            if not news_items:
                # Fallback to generating a general tech tweet
                return self.generate_fallback_tweet()
                
            news_item = random.choice(news_items)
            tweet = self.generate_tweet(news_item)
            
            if tweet:
                return tweet
            return self.generate_fallback_tweet()
        except Exception as e:
            print(f"Error in generate_viral_tweet: {e}")
            return self.generate_fallback_tweet()

    def generate_fallback_tweet(self):
        """Generate a tweet without news context"""
        tech_topics = [
            "AI and machine learning advancements",
            "Quantum computing breakthroughs",
            "Cybersecurity trends",
            "Cloud computing innovations",
            "Blockchain technology",
            "5G and future networks",
            "Edge computing developments",
            "IoT and smart devices",
            "AR/VR technology",
            "Sustainable tech solutions"
        ]
        
        topic = random.choice(tech_topics)
        prompt = f"""
        Create a viral, engaging, and professional tweet about {topic}.
        
        The tweet should be:
        - Technical but accessible
        - Include relevant hashtags
        - Be engaging and shareable
        - Under 280 characters
        - Include emojis where appropriate
        - Sound like a tech expert
        
        Format the tweet in a way that would go viral in the tech community.
        """
        
        try:
            headers = {
                "Authorization": f"Bearer {self.hf_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 280,
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
            
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0]['generated_text'].strip()
                return result.get('generated_text', '').strip()
            return "Could not generate tweet at this time. Please try again later."
            
        except Exception as e:
            print(f"Error in generate_fallback_tweet: {e}")
            return "Could not generate tweet at this time. Please try again later."

if __name__ == "__main__":
    generator = TweetGenerator()
    viral_tweet = generator.generate_viral_tweet()
    print("\nGenerated Viral Tweet:")
    print("-" * 50)
    print(viral_tweet)
    print("-" * 50) 