# Automated Micro-Influencer Outreach System

An AI-powered system that helps find relevant micro-influencers, filter them based on campaign requirements, collect useful profile information, generate personalized messages, and track outreach.

## Project Workflow

Discovery → Filtering → Enrichment → AI Personalization → Sending → Tracking

## 1. Technology Stack

- **Programming Language:** Python 3
- **Discovery API:** YouTube Data API v3
- **AI:** Claude API using Anthropic SDK
- **Email:** Gmail SMTP using Python `smtplib`
- **Database:** SQLite
- **Data Storage:** CSV files
- **Notebook:** Jupyter Notebook
- **Configuration:** Environment variables

## 2. How the System Works

The system is divided into different modules. Each module handles one part of the outreach process.

### Step 1: Influencer Discovery

The system searches for influencers based on different niches such as:

- Fitness
- Fintech
- Beauty
- Fashion
- Technology

In live mode, the YouTube Data API is used to collect channel information such as name, followers, profile URL, and other available details.

For testing, the project also provides a demo mode with sample influencer records.

### Step 2: Filtering

The discovered influencers are checked against predefined conditions.

The current filtering rules are:

- Followers between **5,000 and 100,000**
- Engagement rate of at least **1.5%**
- Influencer niche should match the selected categories
- Beauty and Fashion influencers should have at least one audience demographic field available

Each influencer receives:

- `PASS` — if the influencer meets the requirements
- `FAIL` — if the influencer does not meet the requirements

The system also stores the reason for passing or failing.

## 3. Data Sources

The project supports YouTube Data API v3 for live influencer discovery.

For Instagram and TikTok, direct third-party discovery APIs are limited. Therefore, the project does not bypass platform restrictions or perform unauthorized scraping.

A demo mode is also available for testing the complete pipeline without requiring API keys.

Demo records are clearly marked as:

`SAMPLE_DEMO`

They are not presented as real influencers.

## 4. Profile Enrichment

After filtering, influencer information is converted into a common format.

The system stores information such as:

- Influencer name
- Platform
- Profile URL
- Follower count
- Engagement rate
- Niche
- Content themes
- Contact email
- Website
- Audience information

If information is not available, the system stores:

`Not Found`

The system does not guess or create email addresses.

An enrichment completeness percentage is also calculated to show how much information is available for each influencer.

## 5. AI Personalization

Claude API is used to create personalized outreach messages.

The AI receives available influencer information such as:

- Name
- Niche
- Content themes
- Engagement rate
- Audience geography

It then generates two messages.

### Email Pitch

The generated email is designed to be between **60–90 words**.

It can include:

- Influencer's niche
- Content style
- Audience relevance
- Collaboration idea
- Brand value proposition

### Instagram DM

The generated Instagram DM is designed to be between **15–30 words**.

The message is short and personalized according to the influencer's content.

The system does not use exactly the same message for every influencer.

## 6. AI Prompt

The prompt is implemented in:

`personalization.py`

The prompt asks Claude to:

1. Use the available influencer information.
2. Create a personalized email.
3. Create a short Instagram DM.
4. Select a suitable collaboration type.
5. Return the result in JSON format.
6. Avoid creating information that is not available.

Possible collaboration types include:

- Sponsorship
- Affiliate marketing
- UGC
- Brand ambassador
- Paid placement
- Barter collaboration

If the Claude API key is not available, the project uses a simple fallback message generator so that the complete pipeline can still be tested.

The generated messages are marked with their generation method.

## 7. Sending System

The sending logic is implemented in:

`sending.py`

Before sending an email, the system checks:

1. Whether the influencer passed the filter.
2. Whether a valid email is available.
3. Whether the influencer has already been contacted.

If the influencer was already contacted, the system skips the email.

This helps prevent duplicate outreach.

### Dry Run Mode

The project uses:

`DRY_RUN=true`

by default.

In this mode, emails are not actually sent. Instead, the system records:

`SIMULATED_SENT`

This is useful while testing the project.

Real SMTP sending can be enabled by providing the required email credentials and setting:

`DRY_RUN=false`

Instagram DMs are not automatically sent. The generated DM is stored so it can be reviewed or sent manually.

## 8. Outreach Tracking

The project uses SQLite to maintain an outreach history.

The tracker records information such as:

- Influencer
- Email
- Message generated
- Sent status
- Date
- Outreach status

The tracker is also exported to:

`data/outreach_tracker.csv`

This allows the user to easily check which influencers were contacted and prevents duplicate emails.

## 9. Output Files

After running the project, the following files are created inside the `data` folder:

### `influencers.csv`

Contains the discovered and filtered influencer information.

### `personalized_messages.csv`

Contains:

- Email pitch
- Instagram DM
- Influencer information
- Message generation method

### `outreach_tracker.csv`

Contains the outreach history and sending status.

### `outreach_tracker.db`

SQLite database used to store the outreach records.


