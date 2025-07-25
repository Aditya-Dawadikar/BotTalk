# BotTalk Podcast Server

## How to Run

1. Create and activate a virtual environment:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Add a `.env` file in the project root with:
    ```
    MONGO_DB_NAME=bot_talks
    MONGO_PODCAST_COLLECTION=podcasts
    MONGO_JOBS_COLLECTION=jobs
    MONGO_URI=<your_mongodb_uri>
    ```

4. Start the server (from the `podcast_server` directory):
    ```
    uvicorn src.main:app --reload
    ```
    or run the main file directly:
    ```
    python src/main.py
    ```

The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API

- `POST /podcasts` and `GET /podcasts`
- `POST /jobs` and `GET