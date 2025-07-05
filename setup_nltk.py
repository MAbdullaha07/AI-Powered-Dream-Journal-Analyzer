#!/usr/bin/env python3
"""
Script to download all required NLTK data for the Dream Journal AI application.
Run this script once before using the application to ensure all NLP components work properly.
"""

import nltk
import sys

def download_nltk_data():
    """Download all required NLTK datasets"""
    
    required_data = [
        'punkt',           # Sentence tokenizer
        'stopwords',       # Stop words corpus
        'vader_lexicon',   # Sentiment analysis lexicon
        'wordnet',         # WordNet lexical database
        'omw-1.4',         # Open Multilingual Wordnet
        'averaged_perceptron_tagger',  # POS tagger (optional but useful)
    ]
    
    print("🧠 Setting up NLTK data for Dream Journal AI...")
    print("=" * 50)
    
    total = len(required_data)
    success_count = 0
    
    for i, data_name in enumerate(required_data, 1):
        try:
            print(f"[{i}/{total}] Downloading {data_name}...", end=" ")
            nltk.download(data_name, quiet=True)
            print("✅ Success")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    print("=" * 50)
    if success_count == total:
        print(f"🎉 All NLTK data downloaded successfully! ({success_count}/{total})")
        print("\nYou can now run the Dream Journal AI application:")
        print("   python app.py")
    else:
        print(f"⚠️  Downloaded {success_count}/{total} datasets. Some may have failed.")
        print("The application may still work, but some features might be limited.")
    
    return success_count == total

def test_imports():
    """Test if all required NLTK components can be imported"""
    print("\n🔍 Testing NLTK components...")
    
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize, sent_tokenize
        from nltk.stem import WordNetLemmatizer
        
        # Test basic functionality
        sia = SentimentIntensityAnalyzer()
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        
        # Test tokenization
        test_text = "This is a test sentence for Dream Journal AI."
        tokens = word_tokenize(test_text)
        sentences = sent_tokenize(test_text)
        
        # Test sentiment analysis
        sentiment = sia.polarity_scores(test_text)
        
        print("✅ All NLTK components are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing NLTK components: {e}")
        return False

if __name__ == "__main__":
    print("Dream Journal AI - NLTK Setup")
    print("This script will download the required language processing data.\n")
    
    # Download data
    download_success = download_nltk_data()
    
    if download_success:
        # Test imports
        test_success = test_imports()
        
        if test_success:
            print("\n🚀 Setup complete! You're ready to use Dream Journal AI.")
            print("\nTo start the application:")
            print("   python app.py")
            print("\nThen open your browser to: http://localhost:5000")
        else:
            print("\n⚠️  Setup completed but testing failed. The app might still work.")
    else:
        print("\n❌ Setup incomplete. Please check your internet connection and try again.")
        sys.exit(1)
