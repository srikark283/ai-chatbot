# AI Chatbot with Gemini

A simple chatbot application built with Python, Streamlit, and Google's Gemini LLM. Features in-memory session context and SQLite database for persistent chat history storage.

## Features

- 💬 Chat with Google's Gemini AI model
- 💾 Persistent chat history stored in SQLite database
- 🔄 Session management with multiple chat sessions
- 📜 Load previous chat sessions
- 🗑️ Clear and manage sessions

## Setup

### Prerequisites

- Python 3.8 or higher
- Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ai-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
   - Create a `.env` file in the project root
   - Add your API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

1. **Start a new chat**: Type your message in the chat input box
2. **New session**: Click "🆕 New Session" in the sidebar to start a fresh conversation
3. **Load history**: Click "📜 Load History" to reload messages from the database
4. **View sessions**: Browse and load previous sessions from the sidebar
5. **Clear session**: Delete the current session and its messages

## Database Schema

The SQLite database (`chatbot.db`) contains two tables:

- **sessions**: Stores chat session metadata
  - `session_id`: Unique identifier for each session
  - `created_at`: Session creation timestamp
  - `updated_at`: Last update timestamp

- **messages**: Stores individual chat messages
  - `id`: Auto-incrementing primary key
  - `session_id`: Foreign key to sessions table
  - `role`: Message role (user/assistant)
  - `content`: Message content
  - `timestamp`: Message timestamp

## Project Structure

```
ai-chatbot/
├── app.py              # Main Streamlit application
├── database.py         # SQLite database operations
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── chatbot.db         # SQLite database (created automatically)
```

## Technologies Used

- **Streamlit**: Web framework for the chatbot UI
- **Google Generative AI (Gemini)**: LLM for generating responses
- **SQLite**: Database for storing chat history
- **Python-dotenv**: Environment variable management

## Notes

- Chat history is automatically saved to the database
- Each session maintains its own conversation context
- The database file (`chatbot.db`) is created automatically on first run