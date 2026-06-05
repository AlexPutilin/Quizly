# Quizly Backend

Quizly is a Django REST API that turns YouTube videos into interactive quizzes.
The application downloads the audio from a YouTube video, transcribes it with Whisper, and uses Gemini AI to generate a quiz with 10 questions and 4 answer options each.

This project was built as a learning project for a backend development course. The focus is on a clean and understandable Django REST API with JWT authentication, simple project structure, and AI-based quiz generation.

## Features

* User registration and login
* JWT authentication with HTTP-only cookies
* YouTube URL based quiz generation
* Audio extraction with `yt-dlp` and FFmpeg
* Audio transcription with Whisper
* Quiz generation with Gemini AI
* Quiz listing, detail view, update and delete endpoints
* Django Admin support for quizzes and questions

## Tech Stack

* Python
* Django
* Django REST Framework
* SimpleJWT
* yt-dlp
* FFmpeg
* OpenAI Whisper
* Google Gen AI / Gemini API
* SQLite for local development

## Requirements

Before running the project, make sure the following tools are installed:

* Python
* FFmpeg installed globally
* A Gemini API key

FFmpeg is required because the project extracts and processes audio files before transcription.

## Installation


Clone the repository:

```bash
git clone https://github.com/AlexPutilin/Quizly.git
cd Quizly
```


Create and activate a virtual environment:

```bash
python -m venv .venv

# Linux / Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate      
```


Install dependencies:

```bash
pip install -r requirements.txt
```


Create a `.env` file based on `.env.example`:

```bash
# macOS/Linux
cp .env.example .env

# Windows CMD
copy .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

Example `.env.example`:

```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500

GEMINI_API_KEY="YOUR API_KEY"
GEMINI_MODEL="gemini-3.5-flash"
```


Add your own Gemini API key:

```env
GEMINI_API_KEY="your-gemini-api-key"
```


Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```


Create a superuser for the Django Admin panel:

```bash
python manage.py createsuperuser
```


Start the development server:

```bash
python manage.py runserver
```

The backend will usually be available at:

```text
http://127.0.0.1:8000/
```


## Authentication

Authentication is handled with JWT tokens stored in HTTP-only cookies.

After a successful login, the backend sets two cookies:

```text
access_token
refresh_token
```

Protected endpoints require a valid `access_token` cookie.


## API Endpoints

### Authentication

#### Register a new user

```http
POST /api/register/
```

Request body:

```json
{
  "username": "your_username",
  "password": "your_password",
  "confirmed_password": "your_confirmed_password",
  "email": "your_email@example.com"
}
```

Success response:

```json
{
  "detail": "User created successfully!"
}
```

#### Login

```http
POST /api/login/
```

Request body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Success response:

```json
{
  "detail": "Login successfully!",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
  }
}
```

This endpoint sets the `access_token` and `refresh_token` cookies.

#### Logout

```http
POST /api/logout/
```

Success response:

```json
{
  "detail": "Log-Out successfully! All Tokens will be deleted."
}
```

This endpoint removes the authentication cookies.

#### Refresh access token

```http
POST /api/token/refresh/
```

Success response:

```json
{
  "detail": "Token refreshed"
}
```

This endpoint uses the `refresh_token` cookie and sets a new `access_token` cookie.

## Quiz Endpoints

All quiz endpoints require authentication.

### Create a new quiz

```http
POST /api/quizzes/
```

Request body:

```json
{
  "url": "https://www.youtube.com/watch?v=example"
}
```

Success response:

```json
{
  "id": 1,
  "title": "Quiz Title",
  "description": "Quiz Description",
  "created_at": "2023-07-29T12:34:56.789Z",
  "updated_at": "2023-07-29T12:34:56.789Z",
  "video_url": "https://www.youtube.com/watch?v=example",
  "questions": [
    {
      "id": 1,
      "question_title": "Question 1",
      "question_options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Option A",
      "created_at": "2023-07-29T12:34:56.789Z",
      "updated_at": "2023-07-29T12:34:56.789Z"
    }
  ]
}
```

### Get all quizzes of the authenticated user

```http
GET /api/quizzes/
```

Success response:

```json
[
  {
    "id": 1,
    "title": "Quiz Title",
    "description": "Quiz Description",
    "created_at": "2023-07-29T12:34:56.789Z",
    "updated_at": "2023-07-29T12:34:56.789Z",
    "video_url": "https://www.youtube.com/watch?v=example",
    "questions": [
      {
        "id": 1,
        "question_title": "Question 1",
        "question_options": [
          "Option A",
          "Option B",
          "Option C",
          "Option D"
        ],
        "answer": "Option A"
      }
    ]
  }
]
```

### Get a specific quiz

```http
GET /api/quizzes/{id}/
```

Success response:

```json
{
  "id": 1,
  "title": "Quiz Title",
  "description": "Quiz Description",
  "created_at": "2023-07-29T12:34:56.789Z",
  "updated_at": "2023-07-29T12:34:56.789Z",
  "video_url": "https://www.youtube.com/watch?v=example",
  "questions": [
    {
      "id": 1,
      "question_title": "Question 1",
      "question_options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Option A"
    }
  ]
}
```

### Update a quiz

```http
PATCH /api/quizzes/{id}/
```

Request body:

```json
{
  "title": "Updated Quiz Title",
  "description": "Updated Quiz Description"
}
```

Only the quiz title and description can be updated. Questions are not edited through this endpoint.

### Delete a quiz

```http
DELETE /api/quizzes/{id}/
```

Success response:

```text
204 No Content
```

Deleting a quiz permanently removes the quiz and its related questions.

## Notes

* Only YouTube URLs are supported for quiz generation.
* The quiz generation process can take some time because the backend downloads audio, transcribes it, and sends the transcript to Gemini.
* The generated quiz contains the correct answers in the API response because the frontend handles the quiz logic.
