# INFANITE — AI Powered Smart Assistant
**Built with Flask, Wikipedia, Google Search, and OpenAI**

---

## Overview

INFANITE is an intelligent AI web assistant built using Flask (Python).  
It combines the power of:
- Wikipedia for knowledge-based answers  
- Google Search for latest and external information  
- OpenAI GPT (optional) for conversational intelligence  
- Google Translator for Hinglish/Hindi to English translation  
- Weather API and Voice input support (demo)

This assistant acts as a smart chatbot, search engine, and translator — all in one place.

---

## Features

| Feature | Description |
|----------|--------------|
| Conversational Mode | Responds to greetings and personal questions like “hi”, “who are you?”, “help”, etc. |
| Time & Date Info | Displays the current system time and date. |
| Wikipedia Search | Fetches concise summaries from Wikipedia automatically. |
| Google Search Integration | Fetches top web results (title, description, and link). |
| OpenAI GPT Integration | (Optional) Gives human-like, natural answers using GPT model if API key is set. |
| Weather Info | Fetches current weather of any city using `wttr.in` API. |
| Translator | Translates Hinglish or Hindi to English using `googletrans`. |
| Image Upload | Demo route to accept image uploads (processing feature coming soon). |
| Voice Input Support | Demo route to simulate voice command processing. |

---

## Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/INFANITE-AI-Assistant.git
cd INFANITE-AI-Assistant
