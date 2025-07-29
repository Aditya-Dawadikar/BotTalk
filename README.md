# BotTalks – Automated Podcast Generation

BotTalks is an AI-driven system for generating podcast-style conversations between virtual agents. It automates research, conversation generation, script creation, audio synthesis, and thumbnail generation — delivering a complete podcast episode pipeline.

---

## **Demo**

[Youtube Video](https://youtu.be/EowingvpOEM)

![img1](./app_view_1.png)
![img2](./app_view_2.png)

---

## **Architecture Overview**

The system integrates multiple AI frameworks and services to create a fully automated workflow:

![img](./Bottalk_arch.png)

### **Key Components**

* **React Frontend** – User interface to trigger podcast generation jobs and stream the results.
* **LangChain + LangGraph** – Core logic to generate podcast outlines and drive agent-based conversations.
* **Gemini (LLM)** – Provides conversational intelligence for host and guest agents. Generates audio files and thumbnails
* **Amazon S3** – Stores generated files like audio, thumbnails, and raw scripts.
* **MongoDB** – Tracks job metadata, research, and conversation states.

---

## **Workflow**

1. **Trigger Job (React Frontend)**
   A podcast generation request is initiated by the user.

2. **Generate Podcast Outline (LangChain + LangGraph)**
   A structured podcast plan is created with segments and key points.

4. **Host-Guest Conversation (Gemini)**

   * Host and guest agents simulate a dialogue based on the outline and research.
   * The conversation continues until the topic is fully discussed.

5. **Script Polishing and Summarization**

   * Raw conversation script is refined into a final version.
   * A summary is generated for metadata.

6. **Audio and Visual Generation**

   * **Google's Gemini** converts the script into audio (TTS).
   * A thumbnail image is created.

7. **Storage and Delivery**

   * All outputs (outline, raw script, final script, summary, audio, thumbnail) are stored in **Amazon S3**.
   * Job details and states are recorded in **MongoDB**.
   * Generated files are accessible for playback and download via the React UI.

---

## **Storage Layer**

* **Amazon S3** – For all generated files (audio `.wav`, images `.png`, raw/final scripts `.json`).
* **MongoDB** – For tracking job states (`flow_generated`, `audio_generated`, `summary_generated`, etc.).

---

## **Tech Stack**

* **Frontend:** React (TypeScript), Material UI
* **Backend:** FastAPI (Python)
* **AI/ML:** LangChain, LangGraph, Gemini LLM
* **Database:** MongoDB
* **Storage:** Amazon S3
* **Cloud:** AWS

---

## **Setup Instructions**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Aditya-Dawadikar/bottalks.git
   cd bottalks
   ```

2. **Environment Variables**
   Create a Backend `.env` file:

   ```env
   MONGODB_CONNECTION_STRING=mongodb://localhost:27017/
   MONGO_DB_NAME=bot_talks
   MONGO_PODCAST_COLLECTION=podcasts
   MONGO_JOBS_COLLECTION=podcast_create_jobs
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_S3_BUCKET=your_bucket
   GEMINI_API_KEY=<GEMINI_API_KEY>
   S3_BUCKET_NAME=bottalk
   AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY>
   AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
   AWS_DEFAULT_REGION=us-east-2
   ```

   Create a Frontend `.env` file:

   ```env
   VITE_SERVER_URL=http://localhost:8000
   ```

3. **Backend Setup**

   From the root folder

   ```bash
   pip install -r requirements.txt
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Frontend Setup**

   From the frontend folder
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

