# Meme Generation API

This project is a Django Rest Framework (DRF) API for generating and retrieving memes. It integrates OpenAI's GPT-4-turbo for meme text generation and DALL·E for image creation.

## Features
- Generate meme captions and images automatically.
- Store meme details in a database.
- Retrieve all generated memes via an API endpoint.
- Download and save generated meme images locally.

## Installation



1 Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2 Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3 Set up environment variables:
   - Create a `.env` file in the project root.
   - Add the following:
     ```
     OPENAI_API_KEY=<your_openai_api_key>
     ```

4 Apply migrations:
   ```sh
    python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Retrieve Memes
- **GET** `/memes/`
- Returns all stored memes.

### Generate Meme
- **POST** `/memes/`
- Request body:
  ```json
  {
    "comment_text": "Your input text for meme generation"
  }
  ```


