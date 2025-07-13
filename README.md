## 📊 Social Media AI Automation Dashboard

An intelligent web dashboard that leverages **OpenAI's GPT-4o and GPT-4o-mini** models to analyze, categorize, and respond to social media comments. The app also supports **GoHighLevel (GHL)** CRM integration for lead tagging, workflow automation, and contact management.

---

### 🔧 Project Structure

```bash
.
├── app.py                  # Main AI logic using GPT-4o/GPT-4o-mini (OOP structure)
├── dashboard.py           # Streamlit dashboard UI for testing and visualization
├── ghl_integration.py     # Integration with GHL API (lead tagging, contact sync)
├── .env                   # Environment variables (OpenAI + GHL keys)
├── requirements.txt       # Python package dependencies
├── README.md              # Project documentation
```

---

### 🧠 Features

* **Real-time comment processing** with GPT-4o / GPT-4o-mini
* **Auto-categorization**: Lead, Praise, Spam, Question, Complaint
* **Auto-response generation** with ChatGPT
* **GoHighLevel integration**:

  * Contact creation/updating
  * Tag assignment
  * Workflow triggering
* **Interactive dashboard UI** using Streamlit
* **Customizable** comment input and debugging modes
* **Analytics view** for processed message categories

---

### 🚀 Setup Instructions

#### 1. Clone the Repo

```bash
git clone https://github.com/your-username/social-ai-dashboard.git
cd social-ai-dashboard
```

#### 2. Create & Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate     # Mac/Linux
# OR
.venv\Scripts\activate        # Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create `.env` File

```env
OPENAI_API_KEY=your-openai-key
GHL_API_KEY=your-ghl-api-key  # Optional
```

#### 5. Run the App

```bash
streamlit run dashboard.py
```

---

### 🧱 Object-Oriented Backend (`app.py`)

The app uses an OOP architecture to handle OpenAI interactions:

```python
class SocialMediaAI:
    def __init__(self, api_key: str):
        ...
    
    def process_comment(self, comment: str) -> dict:
        ...
```

This class:

* Sends prompts to GPT-4o/4o-mini
* Returns structured JSON output including `reply`, `category`, etc.

---

### 📦 Sample Output Format

```json
{
  "reply": "Thank you for your interest! We'd love to help. Please DM us!",
  "category": "Lead"
}
Thanks for sharing your project details and code. Based on what you've provided, here's a detailed and professional `README.md` file for your **AI Automation Dashboard** project:

---

## 📊 Social Media AI Automation Dashboard

An intelligent web dashboard that leverages **OpenAI's GPT-4o and GPT-4o-mini** models to analyze, categorize, and respond to social media comments. The app also supports **GoHighLevel (GHL)** CRM integration for lead tagging, workflow automation, and contact management.

---

### 🔧 Project Structure

```bash
.
├── app.py                  # Main AI logic using GPT-4o/GPT-4o-mini (OOP structure)
├── dashboard.py           # Streamlit dashboard UI for testing and visualization
├── ghl_integration.py     # Integration with GHL API (lead tagging, contact sync)
├── .env                   # Environment variables (OpenAI + GHL keys)
├── requirements.txt       # Python package dependencies
├── README.md              # Project documentation
```

---

### 🧠 Features

* **Real-time comment processing** with GPT-4o / GPT-4o-mini
* **Auto-categorization**: Lead, Praise, Spam, Question, Complaint
* **Auto-response generation** with ChatGPT
* **GoHighLevel integration**:

  * Contact creation/updating
  * Tag assignment
  * Workflow triggering
* **Interactive dashboard UI** using Streamlit
* **Customizable** comment input and debugging modes
* **Analytics view** for processed message categories

---

### 🚀 Setup Instructions

#### 1. Clone the Repo

```bash
git clone https://github.com/your-username/social-ai-dashboard.git
cd social-ai-dashboard
```

#### 2. Create & Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate     # Mac/Linux
# OR
.venv\Scripts\activate        # Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create `.env` File

```env
OPENAI_API_KEY=your-openai-key
GHL_API_KEY=your-ghl-api-key  # Optional
```

#### 5. Run the App

```bash
streamlit run dashboard.py
```

---

### 🧱 Object-Oriented Backend (`app.py`)

The app uses an OOP architecture to handle OpenAI interactions:

```python
class SocialMediaAI:
    def __init__(self, api_key: str):
        ...
    
    def process_comment(self, comment: str) -> dict:
        ...
```

This class:

* Sends prompts to GPT-4o/4o-mini
* Returns structured JSON output including `reply`, `category`, etc.

---

### 📦 Sample Output Format

```json
{
  "reply": "Thank you for your interest! We'd love to help. Please DM us!",
  "category": "Lead"
}
```

---

### 📈 Dashboard Preview

* Built with **Streamlit**
* Supports live testing of AI prompts
* Categories and responses shown in real-time
* GHL integration status indicators
* Optional debugging + raw response display

---

### 🧪 Sample Comments for Testing

| Type      | Example                          |
| --------- | -------------------------------- |
| Lead      | I'm interested in your services! |
| Praise    | Amazing product!                 |
| Spam      | Click here for free stuff!       |
| Question  | What are your business hours?    |
| Complaint | My order never arrived.          |

---

### 📊 Analytics Section

The right-side panel in the dashboard displays:

* Category-wise message distribution
* Response times
* Total processed count

---

### 🔐 Notes

* This is a **confidential internal project**.
* All work and code is proprietary and may not be shared externally.
* Usage is governed by your subcontractor agreement.

---

### 📎 To Do (Optional Enhancements)

* Add login/authentication
* Connect with actual social media APIs (e.g., Facebook, Instagram)
* Store history in a database (e.g., PostgreSQL)
* Smart auto-reply on real platforms
* Notification system for high-priority leads




