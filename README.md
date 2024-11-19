# Bank Chatbot



## Respond to User Script (Uses LLM)

A very simple Python-based intelligent banking chatbot that uses LangChain and Groq LLM to understand and respond to various banking queries.

### Features

- Natural language understanding for banking queries
- Categorizes user requests into 7 distinct categories:
  1. Balance Inquiries
  2. Transactions
  3. Payments
  4. Deposit and Withdrawal Queries
  5. Spending Limits and Budgeting
  6. General Account Information
  7. Assistance and Help
- Template-based response generation
- Secure handling of sensitive banking information
- Interactive command-line interface

### Prerequisites

- Python 3.x
- Groq API key

### Required Dependencies

```bash
langchain-groq
langchain-core
python-dotenv
```

### Installation

1. Clone this repository
2. Install required dependencies using requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
   Alternatively, you can install packages individually:
   ```bash
   pip install langchain-groq langchain-core python-dotenv
   ```
3. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

### Usage

Run the script using:
```bash
python respond_to_user.py
```

The chatbot will start in interactive mode. You can:
- Type your banking queries naturally
- Exit by typing 'quit', 'exit', 'x', or 'q'

Example queries:
```
You: What's my current balance?
You: Can I transfer money to John?
You: Show me recent transactions
```

### How It Works

1. The chatbot first categorizes user input into one of seven predefined categories using the `understand_category()` function
2. Based on the category, it selects an appropriate response template
3. The template is processed using the Groq LLM to generate a contextual response
4. Additional follow-up prompts are provided after each response

### Project Structure

- `respond_to_user.py`: Main script containing the chatbot logic
- Templates for different query types:
  - Balance template
  - Payments template
  - Transaction history template
  - Account information template
  - General assistance template

## Multilingual Speech Assistant (no LLM)

### Overview
A Python-based speech recognition and translation tool that supports multiple Indian languages, enabling voice-based interactions with translation capabilities.

### Features
- Speech recognition for multiple languages (Hindi, Tamil, Telugu, Bengali, Malayalam, English)
- Real-time speech-to-text translation
- Text-to-speech functionality
- Language auto-detection
- Cross-platform support (Windows, Linux, macOS)

### Prerequisites
- Python 3.7+
- Internet connection for translation and speech services

### Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Required Packages
- SpeechRecognition
- deep-translator
- gTTS (Google Text-to-Speech)
- pydub
- langdetect

### Windows-Specific Setup
For Windows users experiencing PyAudio installation issues:
```bash
pip install pipwin
pipwin install pyaudio
```

### Note about pyaudio
- Platform-specific sound modules (automatically handled)
- winsound (for Windows)
- For Linux/macOS sound support, install 'sox' system package

### Usage
Run the script:
```bash
python speech6.py
```

### Main Menu Options
1. Change native language
2. Start conversation (speech recognition and translation)
3. List App Options in Hindi and Tamil
4. Exit

## Dependencies
- Google Translator API
- Google Speech Recognition
- Google Text-to-Speech

## Supported Languages
- English
- Hindi
- Tamil
- Telugu
- Bengali
- Malayalam

### Important Notes
- Requires active internet connection
- Microphone access needed for speech recognition
- Some features may have limitations based on network and speech recognition accuracy

### Troubleshooting
- Ensure all required packages are installed
- Check microphone permissions
- Verify stable internet connection


Please raise an issue if any of the above is not clear or doesn't work.
