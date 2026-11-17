# AI Personal Teacher

## Description
AI Personal Teacher is an interactive educational application powered by Artificial Intelligence.

It works as a personal teacher that can explain different subjects, ask questions, check answers, correct mistakes, and track learning progress.

The application also features an animated-style teacher avatar with four different emotions.

## Features
- AI-powered teaching assistant
- Simple explanations of educational topics
- Interactive questions and answers
- Automatic answer checking
- Four teacher emotions:
  - Happy
  - Angry
  - Shocked
  - Normal
- Learning progress tracking (0–100%)
- Chat interface built with CustomTkinter
- AI responses in JSON format

## Technologies Used
- Python
- CustomTkinter
- OpenAI API
- Pillow (PIL)
- JSON

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/ai-personal-teacher.git
```

2. Install the required libraries:

```bash
pip install customtkinter openai pillow
```

3. Add your API key to the `API_KEY` variable.

4. Make sure your project contains the following folder:

```text
AI-Personal-Teacher/
│
├── main.py
├── assets/
│   ├── happy.jpg
│   ├── angry.jpg
│   ├── shocked.jpg
│   └── normal.jpg
│
└── README.md
```

5. Run the application:

```bash
python main.py
```

## How to Use

1. Launch the application.
2. Enter a subject you want to study.
3. The AI teacher will explain the topic and ask questions.
4. Answer the questions in the chat.
5. Watch the teacher's emotions change depending on your answers.
6. Track your learning progress using the progress bar.

## Author
Created as a Python AI project.
