import re
import json
from collections import Counter
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np

class DreamAnalyzer:
    def __init__(self):
        # Download required NLTK data
        self._ensure_nltk_data()
        
    def _ensure_nltk_data(self):
        """Ensure all required NLTK data is downloaded"""
        required_data = {
            'tokenizers/punkt': 'punkt',
            'corpora/stopwords': 'stopwords', 
            'vader_lexicon': 'vader_lexicon',
            'corpora/wordnet': 'wordnet',
            'corpora/omw-1.4': 'omw-1.4'
        }
        
        for data_path, download_name in required_data.items():
            try:
                nltk.data.find(data_path)
            except LookupError:
                print(f"Downloading NLTK data: {download_name}...")
                nltk.download(download_name, quiet=True)
        
        # Initialize NLTK components after ensuring data is available
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
        # Common dream themes and symbols
        self.dream_themes = {
            'water': ['water', 'ocean', 'sea', 'lake', 'river', 'swimming', 'drowning', 'flood', 'rain'],
            'flying': ['flying', 'flight', 'wings', 'soaring', 'floating', 'levitating'],
            'falling': ['falling', 'drop', 'cliff', 'abyss', 'plummet'],
            'death': ['death', 'dying', 'dead', 'funeral', 'grave', 'cemetery'],
            'animals': ['dog', 'cat', 'bird', 'snake', 'spider', 'lion', 'wolf', 'bear', 'horse'],
            'people': ['family', 'friend', 'stranger', 'crowd', 'mother', 'father', 'child'],
            'places': ['house', 'home', 'school', 'work', 'forest', 'mountain', 'city', 'beach'],
            'transportation': ['car', 'plane', 'train', 'bus', 'bike', 'driving', 'traveling'],
            'nature': ['tree', 'flower', 'garden', 'forest', 'mountain', 'sun', 'moon', 'stars'],
            'fear': ['scared', 'afraid', 'terror', 'nightmare', 'panic', 'anxiety', 'worried'],
            'love': ['love', 'romantic', 'kiss', 'relationship', 'wedding', 'romance'],
            'success': ['winning', 'achievement', 'success', 'victory', 'celebration', 'prize'],
            'failure': ['failing', 'lose', 'mistake', 'embarrassment', 'shame', 'defeat']
        }
        
        self.emotion_keywords = {
            'joy': ['happy', 'joy', 'excited', 'elated', 'cheerful', 'delighted', 'blissful'],
            'fear': ['scared', 'afraid', 'terrified', 'anxious', 'worried', 'nervous', 'panic'],
            'anger': ['angry', 'mad', 'furious', 'rage', 'irritated', 'annoyed', 'frustrated'],
            'sadness': ['sad', 'depressed', 'melancholy', 'gloomy', 'sorrowful', 'grief'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'startled'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'nauseated'],
            'love': ['love', 'affection', 'caring', 'tender', 'romantic', 'passionate'],
            'confusion': ['confused', 'puzzled', 'bewildered', 'perplexed', 'lost']
        }
    
    def analyze_dream(self, dream_text):
        """Comprehensive dream analysis"""
        # Clean and tokenize text
        clean_text = self._clean_text(dream_text)
        tokens = word_tokenize(clean_text.lower())
        
        # Remove stopwords and lemmatize
        filtered_tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                          if token not in self.stop_words and token.isalpha()]
        
        # Analyze sentiment
        sentiment = self.sia.polarity_scores(dream_text)
        
        # Identify emotions
        emotions = self._identify_emotions(dream_text, filtered_tokens)
        
        # Identify themes
        themes = self._identify_themes(filtered_tokens)
        
        # Generate interpretation
        interpretation = self._generate_interpretation(emotions, themes, sentiment)
        
        # Analyze dream structure
        structure = self._analyze_dream_structure(dream_text)
        
        return {
            'sentiment': sentiment,
            'emotions': emotions,
            'themes': themes,
            'interpretation': interpretation,
            'structure': structure,
            'word_count': len(tokens),
            'unique_words': len(set(filtered_tokens)),
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _identify_emotions(self, text, tokens):
        """Identify emotions in the dream"""
        emotions = {}
        text_lower = text.lower()
        
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                emotions[emotion] = count
        
        # Sort by frequency
        return dict(sorted(emotions.items(), key=lambda x: x[1], reverse=True))
    
    def _identify_themes(self, tokens):
        """Identify themes and symbols in the dream"""
        themes = {}
        
        for theme, keywords in self.dream_themes.items():
            count = sum(1 for token in tokens if token in keywords)
            if count > 0:
                themes[theme] = count
        
        return dict(sorted(themes.items(), key=lambda x: x[1], reverse=True))
    
    def _generate_interpretation(self, emotions, themes, sentiment):
        """Generate dream interpretation based on analysis"""
        interpretation = []
        
        # Sentiment interpretation
        if sentiment['compound'] >= 0.05:
            interpretation.append("This dream appears to have a positive overall tone, suggesting feelings of hope, joy, or satisfaction.")
        elif sentiment['compound'] <= -0.05:
            interpretation.append("This dream has a negative emotional tone, which may indicate stress, anxiety, or unresolved concerns.")
        else:
            interpretation.append("This dream has a neutral emotional tone, suggesting a balanced state of mind.")
        
        # Emotion interpretation
        if emotions:
            primary_emotion = list(emotions.keys())[0]
            interpretation.append(f"The primary emotion in this dream is {primary_emotion}, which may reflect your current emotional state or inner conflicts.")
        
        # Theme interpretation
        if themes:
            primary_theme = list(themes.keys())[0]
            theme_meanings = {
                'water': "Water in dreams often represents emotions, the unconscious mind, or life changes.",
                'flying': "Flying dreams typically symbolize freedom, ambition, or a desire to escape limitations.",
                'falling': "Falling dreams may indicate feelings of losing control or anxiety about failure.",
                'death': "Death in dreams often represents transformation, endings, or new beginnings rather than literal death.",
                'animals': "Animals in dreams can represent instincts, desires, or aspects of your personality.",
                'people': "People in dreams often represent different aspects of yourself or your relationships.",
                'places': "Familiar places in dreams may represent comfort zones or past experiences.",
                'transportation': "Transportation dreams often relate to your life's journey and direction.",
                'nature': "Nature elements in dreams typically represent growth, renewal, or connection to your natural self.",
                'fear': "Fear-based dreams may indicate anxiety, stress, or confronting difficult emotions.",
                'love': "Love themes in dreams often reflect your need for connection, intimacy, or self-acceptance.",
                'success': "Success dreams may represent confidence, achievement, or aspirations.",
                'failure': "Failure themes might indicate self-doubt, fear of disappointment, or perfectionism."
            }
            
            if primary_theme in theme_meanings:
                interpretation.append(theme_meanings[primary_theme])
        
        return " ".join(interpretation)
    
    def _analyze_dream_structure(self, text):
        """Analyze the structure and narrative of the dream"""
        sentences = sent_tokenize(text)
        
        return {
            'sentence_count': len(sentences),
            'avg_sentence_length': len(text.split()) / len(sentences) if sentences else 0,
            'narrative_flow': self._analyze_narrative_flow(sentences)
        }
    
    def _analyze_narrative_flow(self, sentences):
        """Analyze the narrative flow of the dream"""
        if len(sentences) < 2:
            return "Brief narrative"
        elif len(sentences) < 5:
            return "Simple narrative structure"
        else:
            return "Complex narrative with multiple scenes"
    
    def generate_insights(self, dreams_data):
        """Generate insights from multiple dreams"""
        if not dreams_data:
            return {'message': 'No dreams to analyze yet. Start by adding some dreams!'}
        
        all_emotions = []
        all_themes = []
        sentiment_scores = []
        
        for dream in dreams_data:
            if dream[2]:  # analysis field
                try:
                    analysis = json.loads(dream[2])
                    if 'emotions' in analysis:
                        all_emotions.extend(analysis['emotions'].keys())
                    if 'themes' in analysis:
                        all_themes.extend(analysis['themes'].keys())
                    if 'sentiment' in analysis:
                        sentiment_scores.append(analysis['sentiment']['compound'])
                except (json.JSONDecodeError, KeyError):
                    continue
        
        # Calculate insights
        emotion_frequency = Counter(all_emotions)
        theme_frequency = Counter(all_themes)
        
        insights = {
            'total_dreams': len(dreams_data),
            'most_common_emotions': dict(emotion_frequency.most_common(5)),
            'most_common_themes': dict(theme_frequency.most_common(5)),
            'average_sentiment': np.mean(sentiment_scores) if sentiment_scores else 0,
            'emotional_trend': self._analyze_emotional_trend(sentiment_scores),
            'recommendations': self._generate_recommendations(emotion_frequency, theme_frequency)
        }
        
        return insights
    
    def _analyze_emotional_trend(self, sentiment_scores):
        """Analyze emotional trend over time"""
        if len(sentiment_scores) < 2:
            return "Insufficient data for trend analysis"
        
        recent_avg = np.mean(sentiment_scores[:5]) if len(sentiment_scores) >= 5 else np.mean(sentiment_scores)
        older_avg = np.mean(sentiment_scores[-5:]) if len(sentiment_scores) >= 10 else np.mean(sentiment_scores)
        
        if recent_avg > older_avg + 0.1:
            return "Emotional tone improving over time"
        elif recent_avg < older_avg - 0.1:
            return "Emotional tone declining over time"
        else:
            return "Emotional tone stable over time"
    
    def _generate_recommendations(self, emotions, themes):
        """Generate personalized recommendations"""
        recommendations = []
        
        if 'fear' in emotions and emotions['fear'] > 2:
            recommendations.append("Consider relaxation techniques before bed to reduce anxiety-related dreams.")
        
        if 'water' in themes and themes['water'] > 2:
            recommendations.append("Water themes suggest you may be processing emotional changes. Consider journaling about current life transitions.")
        
        if 'flying' in themes:
            recommendations.append("Flying dreams often indicate a desire for freedom. Consider what areas of your life might need more independence.")
        
        if not recommendations:
            recommendations.append("Keep recording your dreams to identify patterns and gain deeper insights.")
        
        return recommendations
