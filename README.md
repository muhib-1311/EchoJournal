# AI Journal Assistant

A voice-based journal that lets you speak about your day and automatically generates a summarized entry using AI. Powered by Groq’s LLaMA 3 model.

## Features

- Converts speech to text
- Summarizes journal entries using LLaMA 3 via Groq
- Saves entries by date in the journal_entries folder
- Supports keyword-based search across saved entries
- Stores all data locally for privacy

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Create a `.env` file in the project directory with your Groq API key:
   GROQ_API_KEY=your_groq_api_key_here

3. Run the assistant:
   python main.py

## Search

To find entries that mention a specific keyword:
   python search.py

## Project Structure

Journal/
├── main.py  
├── search.py  
├── .env  
├── requirements.txt  
├── README.md  
└── journal_entries/  
  └── 2025-06-19.txt  

## Dependencies

- groq  
- python-dotenv  
- SpeechRecognition  
- pyaudio  

## Example

You say:  
I worked on my resume, helped a friend, and had biryani for dinner.

Saved summary:  
Updated resume, assisted a friend, and enjoyed biryani for dinner.
