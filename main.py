
import customtkinter as ctk
from openai import OpenAI
from PIL import Image
import json

API_KEY = " "
BASE_URL = "https://bothub.chat/api/v2/openai/v1"
MODEL = "gemini-3.1-flash-lite"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

SYSTEM_PROMPT = """
You are a personal teacher for any educational subject.

Your tasks:
1. Explain topics in simple words.
2. Provide clear examples.
3. Ask the student questions.
4. Check the student's answers.
5. Correct mistakes.
6. Gradually increase the difficulty.

You have four emotions:

happy - The student answered correctly or made a good effort.

angry - The student made a mistake.
Do not insult the student. Express your frustration in a funny way.

shocked - The student gave an unexpected or very interesting answer.

normal - Nothing particularly interesting happened.

You must be an interesting and engaging teacher.

Always respond in English.

Always return your response strictly as JSON:

{
    "emotion": "happy",
    "message": "Teacher's response",
    "progress": 10
}

progress - Learning progress from 0 to 100.
"""

window = ctk.CTk()
window.title("AI Personal Teacher")
window.geometry("1200x700")

history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

current_topic = ""
progress = 0

emotions = {
    "happy": "happy.jpg",
    "angry": "angry.jpg",
    "shocked": "shocked.jpg",
    "normal": "normal.jpg"
}


def change_emotion(emotion):
    image_name = emotions.get(emotion, "normal.jpg")

    image = Image.open("assets/" + image_name)

    avatar = ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=(250, 250)
    )

    teacher_image.configure(
        image=avatar,
        text=""
    )

    teacher_image.image = avatar

    mood_label.configure(
        text="Mood: " + emotion
    )


def add_message(sender, message):
    chat.configure(state="normal")

    chat.insert("end", sender + "\n")
    chat.insert("end", message + "\n\n")

    chat.see("end")
    chat.configure(state="disabled")


def ask_ai():
    global current_topic

    user_message = input_field.get()

    if user_message.strip() == "":
        return

    input_field.delete(0, "end")

    add_message("You", user_message)

    if current_topic == "":
        topic = user_message

        user_message = (
            f"The student wants to learn about: {topic}. "
            "Start teaching and ask a question."
        )

        current_topic = topic

        topic_label.configure(
            text="Topic: " + topic
        )

    history.append({
        "role": "user",
        "content": user_message
    })

    send_button.configure(state="disabled")

    add_message("System", "The teacher is thinking...")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        answer = response.choices[0].message.content

        if not answer or not answer.strip():
            raise ValueError("The AI returned an empty response.")

        answer = answer.strip()

        if answer.startswith("```"):
            answer = answer.split("\n", 1)[1]
            answer = answer.rsplit("```", 1)[0].strip()

        try:
            data = json.loads(answer)
        except json.JSONDecodeError:
            raise ValueError(
                f"The AI returned invalid JSON:\n{answer}"
            )

        emotion = data.get("emotion", "normal")

        if emotion not in emotions:
            emotion = "normal"

        message = data.get(
            "message",
            "Let's continue learning!"
        )

        new_progress = int(data.get("progress", progress))

        history.append({
            "role": "assistant",
            "content": answer
        })

        show_response(emotion, message, new_progress)

    except Exception as error:
        show_error(str(error))


def show_response(emotion, message, new_progress):
    global progress

    change_emotion(emotion)

    progress = max(0, min(100, new_progress))

    progress_bar.set(progress / 100)

    progress_label.configure(
        text=f"{progress}%"
    )

    add_message("Professor", message)

    send_button.configure(state="normal")


def show_error(error):
    add_message("Error", error)

    send_button.configure(state="normal")


# LEFT PANEL

left_panel = ctk.CTkFrame(
    window,
    width=320,
    corner_radius=15
)

left_panel.pack(
    side="left",
    fill="y",
    pady=15,
    padx=15
)

left_panel.pack_propagate(False)

title_label = ctk.CTkLabel(
    left_panel,
    text="AI TEACHER",
    font=("Arial", 25, "bold")
)

title_label.pack(pady=20)

teacher_image = ctk.CTkLabel(
    left_panel,
    text="Teacher"
)

teacher_image.pack(pady=15)

mood_label = ctk.CTkLabel(
    left_panel,
    text="Mood: normal",
    font=("Arial", 16)
)

mood_label.pack(pady=10)

progress_title = ctk.CTkLabel(
    left_panel,
    text="Learning Progress",
    font=("Arial", 15, "bold")
)

progress_title.pack(pady=5)

progress_bar = ctk.CTkProgressBar(
    left_panel,
    width=250
)

progress_bar.pack(pady=5)
progress_bar.set(0)

progress_label = ctk.CTkLabel(
    left_panel,
    text="0%"
)

progress_label.pack()

topic_label = ctk.CTkLabel(
    left_panel,
    text="Topic: Not selected",
    wraplength=250
)

topic_label.pack(pady=25)


# RIGHT PANEL

right_panel = ctk.CTkFrame(
    window,
    corner_radius=15
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(0, 15),
    pady=15
)

chat_title = ctk.CTkLabel(
    right_panel,
    text="Learning Chat",
    font=("Arial", 22, "bold")
)

chat_title.pack(pady=15)

chat = ctk.CTkTextbox(
    right_panel,
    font=("Arial", 15),
    wrap="word"
)

chat.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

chat.configure(state="disabled")

input_field = ctk.CTkEntry(
    right_panel,
    height=45,
    placeholder_text="Enter a topic or your answer..."
)

input_field.pack(
    fill="x",
    padx=15,
    pady=10
)

send_button = ctk.CTkButton(
    right_panel,
    text="Send",
    height=45,
    command=ask_ai
)

send_button.pack(
    fill="x",
    padx=15,
    pady=(0, 15)
)


# INITIALIZATION

change_emotion("normal")

add_message(
    "Professor",
    "Hello! What would you like to learn today?"
)

window.mainloop()
