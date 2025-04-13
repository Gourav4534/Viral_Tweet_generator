# 🚀 Viral Tech Tweet Generator

A powerful tool that generates viral, engaging, and professional technology tweets using Hugging Face's AI models and NewsData.io for real-time tech news.

## Features

- 📰 Fetches latest technology news from NewsData.io
- 🤖 Generates viral tweets using Hugging Face's Mistral model
- 🎨 Creates professional and technical content
- 🏷️ Includes relevant hashtags and emojis
- 📱 Ensures tweets are under 280 characters
- 💻 Beautiful Streamlit web interface
- 🔄 Automatic retry logic for API calls
- 📋 Tweet history and copy functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/viral-tech-tweet-generator.git
cd viral-tech-tweet-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
HF_API_KEY=your_hugging_face_api_key
NEWSDATA_API_KEY=your_newsdata_api_key
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (usually http://localhost:8501)

3. Click "Generate New Tweet" to create a viral tech tweet

## API Keys

You'll need two API keys:

1. **Hugging Face API Key**:
   - Sign up at [Hugging Face](https://huggingface.co/)
   - Go to Settings -> Access Tokens
   - Create a new token

2. **NewsData.io API Key**:
   - Sign up at [NewsData.io](https://newsdata.io/)
   - Get your API key from the dashboard

## Project Structure

```
viral-tech-tweet-generator/
├── app.py              # Streamlit web interface
├── tweet_generator.py  # Core tweet generation logic
├── requirements.txt    # Python dependencies
├── .env               # API keys (not in repo)
└── README.md          # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for the AI models
- [NewsData.io](https://newsdata.io/) for the news API
- [Streamlit](https://streamlit.io/) for the web interface 