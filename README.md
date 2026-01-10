Overview

Every morning (e.g. 8:00 AM), an automation will:

Fetch raw news articles

Select the most relevant stories

Generate a smart AI-written briefing

Post it to your Telegram channel

Architecture

Scheduler (Daily)
   ↓
News APIs (Market + Politics)
   ↓
Article Filtering & Deduplication
   ↓
AI Summarization (LLM)
   ↓
Telegram Bot API → Channel
