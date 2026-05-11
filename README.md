© 8th may 2026 Manoj Kumar

🤖 chil – AI Voice Assistant

A Python-based voice assistant that listens, thinks, and acts.
Built to automate everyday tasks like searching, opening apps, and also plays music by finding songs from music folder else chooses youtube.


🚀 Features

🎤 Voice command recognition
🧠 Smart command handling system
🌐 Opens websites like Google, YouTube, system apps
🎵 Music control using pygame (commands like play music,start music)
🔊 Text-to-speech responses
⚡ Fast and lightweight execution
etc.............


## 🙋‍♂️ About the Project

CHIL is a Python-based AI voice assistant designed for real-time desktop interaction and automation on Windows systems.  
The project focuses on combining voice recognition, smart command processing, and friendly conversational responses into a lightweight assistant experience.

The assistant can:

- Open, close, maximize, and minimize Windows applications
- Search and play music directly from the local Music folder
- Automatically play songs on YouTube if files are unavailable locally
- Respond with natural and friendly voice interactions
- Execute desktop tasks through voice commands in real time

This project was built to explore voice automation, modular Python architecture, speech processing, and intelligent task execution while maintaining a simple and extensible code structure.


📁 Project Structure

ai-voice-assistant/
│
├── src/
│   ├── main.py        # Entry point
│   ├── chil_conversation.py    # handling conversation Commands logic
│   └── chil_memory.py       # store the name
│
├── assets/            # Audio / media files
├── requirements.txt
├── README.md
├── .gitignore



▶️ How to Run

Clone the repository
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant
Install dependencies
pip install -r requirements.txt
Run the assistant
python src/main.py

🎙️ Example Commands

“Open YouTube”
“Search for Python tutorials”
“Play music”
"play Ironman scenes"
"play first,second etc... video"
“What is the time”
"close Notepad"


⚙️ How It Works

The assistant follows a simple pipeline:
    Capture voice input
    Convert speech → text
    Process command logic
    Execute task
    Respond via speech


📌 Future Improvements

Add GUI interface
Browser controls
password asking for Shutdown Restart commands


📜 License

This project is open-source and available under the MIT License.