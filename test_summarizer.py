#!/usr/bin/env python3
"""
Test script for the local LLM summarizer.
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Force use of local LLM by unsetting API keys
os.environ.pop('OPENAI_API_KEY', None)
os.environ.pop('GROK_API_KEY', None)
os.environ.pop('GEMINI_API_KEY', None)
os.environ.pop('HF_API_TOKEN', None)

# Set local model
os.environ['LOCAL_MODEL_NAME'] = 'distilgpt2'

from summarizer import generate_briefing

# Test with dummy data
market_articles = [
    {"title": "Stock Market Rises on Tech Earnings", "description": "Major tech stocks surged after strong quarterly results."},
    {"title": "Fed Signals Rate Cuts", "description": "Federal Reserve hints at potential interest rate reductions."}
]

political_articles = [
    {"title": "New Trade Agreement Signed", "description": "Countries agree on new trade terms to boost economy."},
    {"title": "Election Results Announced", "description": "Final votes counted in key districts."}
]

print("Testing local LLM with dummy news data...")
print("=" * 50)

briefing = generate_briefing(market_articles, political_articles)

print("Generated Briefing:")
print("=" * 50)
print(briefing)