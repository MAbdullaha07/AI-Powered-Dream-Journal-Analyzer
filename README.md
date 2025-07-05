# Dream Journal AI

An intelligent dream analysis application that uses artificial intelligence to analyze your dreams, identify patterns, emotions, and themes, and provide personalized insights.

## Features

🧠 **AI-Powered Analysis**: Advanced natural language processing to understand dream content
📊 **Pattern Recognition**: Identify recurring themes and emotions across multiple dreams
📈 **Sentiment Analysis**: Analyze the emotional tone of your dreams
💡 **Personalized Insights**: Get recommendations based on your unique dream patterns
📚 **Dream Journal**: Store and organize all your dreams in one place
🔒 **Secure**: User authentication and private dream storage

## Technologies Used

- **Backend**: Python Flask
- **AI/NLP**: NLTK (Natural Language Toolkit)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Styling**: Custom CSS with gradient backgrounds and animations

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project**
   ```bash
   cd dream-journal-ai
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### Getting Started

1. **Register**: Create a new account with a username and password
2. **Login**: Sign in to access your personal dream journal
3. **Add Dreams**: Record your dreams with detailed descriptions
4. **View Analysis**: Get instant AI analysis of emotions, themes, and sentiment
5. **Track Patterns**: Visit the insights page to see patterns over time

### Features Overview

#### Dream Recording
- Add descriptive titles for your dreams
- Write detailed dream descriptions
- Get real-time character count
- Instant AI analysis upon submission

#### AI Analysis
- **Emotion Detection**: Identifies emotions like joy, fear, anger, sadness, etc.
- **Theme Recognition**: Detects common dream themes like water, flying, animals, etc.
- **Sentiment Analysis**: Measures overall positive, negative, or neutral tone
- **Dream Structure**: Analyzes narrative complexity and word usage
- **Interpretation**: Provides meaningful insights based on detected patterns

#### Insights Dashboard
- View your most common emotions and themes
- Track emotional trends over time
- Get personalized recommendations
- See comprehensive dream statistics

## AI Analysis Capabilities

### Emotion Detection
The AI can identify various emotions in your dreams:
- Joy, happiness, excitement
- Fear, anxiety, worry
- Anger, frustration, irritation
- Sadness, depression, melancholy
- Surprise, amazement, shock
- Love, affection, romance
- Confusion, bewilderment

### Theme Recognition
Common dream themes that are automatically detected:
- **Water**: Ocean, rivers, swimming, flooding
- **Flying**: Soaring, floating, wings
- **Animals**: Dogs, cats, snakes, wild animals
- **People**: Family, friends, strangers
- **Places**: Home, school, work, nature
- **Transportation**: Cars, planes, traveling
- **Fear-based**: Nightmares, scary situations
- **Success/Failure**: Achievements, mistakes

### Sentiment Analysis
- Uses VADER sentiment analysis for accurate emotion scoring
- Provides compound scores from -1 (very negative) to +1 (very positive)
- Shows visual progress bars for easy understanding

## Project Structure

```
dream-journal-ai/
│
├── app.py                 # Main Flask application
├── dream_analyzer.py      # AI analysis engine
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Landing page
│   ├── dashboard.html   # User dashboard
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── add_dream.html   # Dream input form
│   ├── dreams.html      # Dream listing page
│   └── insights.html    # Analytics dashboard
│
└── dream_journal.db     # SQLite database (created automatically)
```

## Database Schema

### Users Table
- `id`: Unique user identifier
- `username`: User's chosen username
- `password_hash`: Securely hashed password
- `created_at`: Account creation timestamp

### Dreams Table
- `id`: Unique dream identifier
- `user_id`: Reference to user
- `title`: Dream title
- `content`: Dream description
- `date_recorded`: When the dream was recorded
- `emotions`: JSON array of detected emotions
- `themes`: JSON array of detected themes
- `analysis`: Complete AI analysis results

## Security Features

- Password hashing using Werkzeug security
- Session management for user authentication
- SQL injection prevention with parameterized queries
- User data isolation (users can only see their own dreams)

## Customization

### Adding New Themes
Edit the `dream_themes` dictionary in `dream_analyzer.py`:

```python
self.dream_themes = {
    'new_theme': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing themes
}
```

### Adding New Emotions
Edit the `emotion_keywords` dictionary in `dream_analyzer.py`:

```python
self.emotion_keywords = {
    'new_emotion': ['happy', 'joyful', 'excited'],
    # ... existing emotions
}
```

## Troubleshooting

### Common Issues

1. **NLTK Download Errors**
   - The app automatically downloads required NLTK data
   - If issues persist, manually run: `python -c "import nltk; nltk.download('all')"`

2. **Port Already in Use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

3. **Database Errors**
   - Delete `dream_journal.db` to reset the database
   - The app will recreate it automatically

## Future Enhancements

- Export dream data to PDF or CSV
- Advanced visualization with charts and graphs
- Dream sharing with friends (optional)
- Mobile app version
- Integration with sleep tracking devices
- Lucid dreaming detection and tips
- Dream symbol dictionary
- Multilingual support

## Contributing

This is an educational project demonstrating AI integration with web applications. Feel free to fork and enhance!

## License

This project is open source and available under the MIT License.

## Acknowledgments

- NLTK for natural language processing capabilities
- Bootstrap for responsive UI components
- Font Awesome for beautiful icons
- Flask for the lightweight web framework

---

**Happy Dreaming! 🌙**

Start recording your dreams today and discover the hidden patterns in your subconscious mind.
