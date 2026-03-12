# 🗄️ TalkDB: Natural Language to SQL Interface

TalkDB is an intelligent, full-stack database interface that translates plain English queries into executable SQL statements. Built to bridge the gap between complex relational databases and user-friendly interfaces, this application leverages Large Language Models (LLMs) to dynamically query a local SQLite database and render the results in real-time.

## ✨ Features
* **Natural Language Processing:** Converts conversational English into syntactically correct SQL queries.
* **Complex Query Handling:** Successfully processes relational queries, including multi-table `JOIN` operations and `WHERE` filtering.
* **Secure Execution Environment:** Implements query validation to strictly permit `SELECT` operations, preventing destructive commands (`DROP`, `DELETE`, `UPDATE`).
* **Interactive Web UI:** Features a clean, responsive frontend built with Streamlit for seamless user interaction and data visualization.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Frontend:** Streamlit, Pandas
* **Backend & Database:** SQLite3
* **AI Integration:** Google GenAI SDK (Gemini 2.5 Flash)
* **Environment Management:** python-dotenv

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Vivoboy11/TalkDB.git](https://github.com/Vivoboy11/TalkDB.git)
   cd TalkDB