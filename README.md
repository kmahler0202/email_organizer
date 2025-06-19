# Developed by Kyle Mahler

This is my first post-grad project, made specifically for my own purposes to assist in sorting, organizing, and slimming down my inbox.
Currently, it is designed specifically for my inbox, but I would like to eventually scale the software up to work for any individual. Potentially even creating a GUI or web interface for full consumer scalability.

This tool and 'README' file were created with the help of ChatGPT.

# DISCLAIMER

This tool reads your emails and uses an AI model to process them. It is built for personal use only and not intended to be deployed in production without further security and privacy review.

# 📬 AI Email Organizer

Automatically sort and label your Gmail inbox using GPT-4.1-mini OpenAI Reponse API and the Gmail API.

## 🔍 What It Does

This tool connects to your Gmail account, scans your emails, and uses GPT-4o to intelligntly classify each message into categories like:

- Work
- Personal
- Promotions
- Spam
- Newsletter
- Receipt
- Sportsbook
- Subscriptions
- Social
- Updates
- Forums
- Other

Once categorized, the tool applies a label to each email — creating labels if needed — to help you stay organized automatically.

## 🚀 How It Works

1. **Gmail API Integration**: Authenticates your Gmail account securely using OAuth2.
2. **Email Retrieval**: Downloads recent messages using the Gmail API.
3. **AI Classification**: Sends the email subject and snippet to OpenAI's GPT-4o for smart categorization.
4. **Labeling**: Applies or creates labels in Gmail based on the AI’s response.
5. **Smart Filtering**: Automatically filters frequent senders (like LinkedIn or NYT) without reclassification.

## 🛠️ Tech Stack

- **Python**
- **OpenAI GPT-4.1-mini API**
- **Gmail API**
- **OAuth2 (Google Authentication)**
- **Logging for easy debugging**
- **Environment variables managed via `.env`**

## Setup

To be completed.

