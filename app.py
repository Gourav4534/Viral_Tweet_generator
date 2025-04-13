import streamlit as st
from tweet_generator import TweetGenerator
import time

# Set page config
st.set_page_config(
    page_title="Viral Tech Tweet Generator",
    page_icon="🚀",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .tweet-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .error-box {
        background-color: #ffebee;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ffcdd2;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🚀 Viral Tech Tweet Generator")
st.markdown("""
Generate engaging, professional tweets about the latest technology news!
""")

# Initialize session state for tweet history
if 'tweet_history' not in st.session_state:
    st.session_state.tweet_history = []

# Create two columns for buttons
col1, col2 = st.columns(2)

# Generate tweet button
if col1.button("Generate New Tweet"):
    # Create a progress container
    progress_container = st.empty()
    progress_container.info("Initializing tweet generation...")
    
    try:
        # Create a new generator instance each time
        generator = TweetGenerator()
        
        # Generate the tweet
        with st.spinner("Fetching latest tech news and generating tweet..."):
            progress_container.info("Fetching latest tech news...")
            time.sleep(1)
            
            progress_container.info("Generating tweet (this may take a few moments)...")
            tweet = generator.generate_viral_tweet()
            
            # Clear the progress container
            progress_container.empty()
            
            if tweet and not tweet.startswith("Could not generate"):
                # Add to history
                st.session_state.tweet_history.append(tweet)
                
                # Display the tweet in a nice box
                st.markdown("""
                <div class="tweet-box">
                    <h3>✨ Your Generated Tweet</h3>
                    <p>{}</p>
                </div>
                """.format(tweet), unsafe_allow_html=True)
                
                # Add copy button
                st.code(tweet, language="text")
                if st.button("Copy Tweet"):
                    st.code(tweet, language="text")
                    st.success("Tweet copied to clipboard!")
            else:
                st.markdown("""
                <div class="error-box">
                    <h3>⚠️ Error Generating Tweet</h3>
                    <p>We couldn't generate a tweet at this time. This might be due to high demand on the AI service. Please try again in a few moments.</p>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        progress_container.empty()
        st.markdown(f"""
        <div class="error-box">
            <h3>⚠️ An Error Occurred</h3>
            <p>Error: {str(e)}</p>
            <p>Please try again later or contact support if the issue persists.</p>
        </div>
        """, unsafe_allow_html=True)

# Clear history button
if col2.button("Clear History"):
    st.session_state.tweet_history = []
    st.success("Tweet history cleared!")

# Display tweet history if any
if st.session_state.tweet_history:
    st.markdown("### 📜 Tweet History")
    for i, tweet in enumerate(reversed(st.session_state.tweet_history), 1):
        st.markdown(f"""
        <div class="tweet-box">
            <h4>Tweet #{i}</h4>
            <p>{tweet}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>Powered by NewsData.io and Hugging Face 🤖</p>
</div>
""", unsafe_allow_html=True) 