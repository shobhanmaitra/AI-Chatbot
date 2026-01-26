# AI Chatbot with LLM and Data Visualization

A simple AI chatbot project with backend API and frontend interface.

## 🚀 Project Structure

```
ai-chatbot-llm-dataviz/
│
├── backend/              # Backend server (Python + Flask)
│   ├── app.py           # Main Flask application
│   └── requirements.txt # Python dependencies
│
├── frontend/            # Frontend interface
│   └── index.html      # Chat UI
│
├── data/               # Data files
│   └── sample.csv     # Sample dataset
│
├── notebooks/          # Jupyter notebooks
│   └── data_analysis.ipynb
│
├── README.md          # This file
└── .gitignore        # Git ignore file
```

## 📋 Week 1 Goals

- ✅ Set up project structure
- ✅ Create simple rule-based chatbot
- ✅ Build backend API with Flask
- ✅ Create frontend chat interface
- ✅ Test API using browser

## 🛠️ Setup Instructions

### 1. Install Python

Make sure Python 3.8+ is installed on your system.

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run Backend Server

```bash
cd backend
python app.py
```

Server will start at: http://localhost:5000

### 4. Open Frontend

Simply open `frontend/index.html` in your web browser.

## 🧪 Testing the API

### Using Browser

Visit: http://localhost:5000

### Using Postman or curl

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

## 📝 Current Features

- Simple rule-based responses
- Chat interface
- Backend API endpoint
- Sample data for future visualization

## 🔜 Next Steps

- Integrate real LLM (OpenAI, Hugging Face)
- Add data visualization features
- Enhance UI/UX
- Add conversation history

## 📚 Technologies Used

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: HTML, CSS, JavaScript
- **Data**: Pandas, NumPy

## 🤝 Contributing

Feel free to fork this project and submit pull requests!

## 📄 License

MIT License
