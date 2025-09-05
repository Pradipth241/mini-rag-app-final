# Mini RAG Application (Track B)

This is a full-stack Retrieval-Augmented Generation (RAG) application built for the Predusk AI Engineer Assessment. It allows a user to process documents (.txt or .pdf) or paste raw text, and then ask questions to receive answers that are grounded in the provided document's content.

## Live URLs

- **Frontend Application**: (https://mini-rag-frontend.netlify.app/)
- **Backend API**: (https://mini-rag-backend-4u8o.onrender.com)

## Architecture

The application is built on a client-server model:

- **Frontend**: A Next.js (React) application provides the user interface for uploading/pasting documents and asking questions.
- **Backend**: A FastAPI (Python) server exposes a REST API with endpoints for document processing and querying.
- **RAG Pipeline**:
  1.  The user submits a document or text to the backend.
  2.  The text is parsed, cleaned, and split into chunks using LangChain's text splitter.
  3.  The text chunks are converted into vector embeddings using Cohere's state-of-the-art model.
  4.  The embeddings are stored in a hosted Qdrant vector database.
  5.  When a user asks a question, the backend uses a multi-query strategy to retrieve the most relevant chunks from Qdrant.
  6.  These chunks are passed as context to a Groq LLM, which generates the final, grounded answer.

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Next.js, React, TypeScript
- **Vector Database**: Qdrant Cloud
- **AI Services**:
  - **Embeddings**: Cohere (`embed-english-v3.0`)
  - **LLM**: GroqCloud (`llama-3.1-8b-instant` or other)

## Configuration Details

#### Index Configuration
- **Vector DB Provider**: Qdrant Cloud
- **Collection Name**: `my_mini_rag_collection`
- **Dimensionality**: 1024 (to match the Cohere embedding model).
- **Distance Metric**: Cosine Similarity.
- **Upsert Strategy**: The collection is recreated upon each new document processing to ensure a clean state for each session.

#### Chunking Strategy
- **Method**: LangChain's `RecursiveCharacterTextSplitter`.
- **Chunk Size**: 1000 characters.
- **Chunk Overlap**: 150 characters.

#### Retriever Settings
- **Retriever**: A multi-query retrieval strategy is used. The user's question is expanded into multiple sub-queries via an LLM call. A top-k similarity search is performed on Qdrant for each sub-query. The top 5 unique document chunks from the combined search results are then used as the context for the final answer.

## Local Setup

**Prerequisites:**
- Node.js (v18 or later)
- Python (v3.10 or later)
- Git

**Instructions:**
1.  **Clone the repository:**
    ```bash
    git clone [Your GitHub Repository URL]
    cd mini-rag-app
    ```
2.  **Setup the Backend:**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    .\venv\Scripts\activate

    # Install Python dependencies
    pip install -r requirements.txt
    ```
3.  **Setup the Frontend:**
    ```bash
    # Navigate to the frontend directory
    cd frontend

    # Install Node.js dependencies
    npm install
    ```
4.  **Configure Environment Variables:**
    - In the project root (`mini-rag-app`), create a `.env` file.
    - Copy the contents of `.env.example` and fill in your API keys.

5.  **Run the Application:**
    - **Backend**: In one terminal (from the project root), run:
      ```bash
      uvicorn main:app --reload
      ```
    - **Frontend**: In a second terminal (from the `frontend` directory), run:
      ```bash
      npm run dev
      ```

## Minimal Evaluation

*(This is a required section. Process one document and ask 5 questions to fill it out.)*

**Gold Set (5 Q&A Pairs):**

1.  **Q**: What are the six principles of Mission Command
    **A**: The six principles of Mission Command are:

            1. Build Cohesive Teams through Mutual Trust 
            2. Create Shared Understanding
            3. Provide a Clear Commander's Intent 
            4. Exercise Disciplined Initiative
            5. Use Mission Orders
            6. Accept Prudent Risk]
2.  **Q**: Who was the Confederate commander at the Battle of Pea Ridge in March 1862?
    **A**: Answer
          The Confederate commander at the Battle of Pea Ridge in March 1862 was MG Earl Van Dorn.
3.  **Q**: How did Gouverneur Warren help save Little Round Top at Gettysburg?
    **A**: Answer
    According to the sources, Gouverneur Warren helped save Little Round Top at Gettysburg by:

    1. Recognizing the danger and taking initiative: Warren noticed the threat of the enemy and rode over to the summit of Little Round Top to assess the situation.
    2. Sending a courier to fire a cannon shot: Warren had a battery fire a round over the foliage to scout out the enemy situation, which revealed the advancing Confederate infantry.
    3. Requesting reinforcements: Warren sent couriers to Sickles requesting a unit to garrison Little Round Top, but received a negative response. However, he soon found other options.
    4. Working with other commanders: Warren collaborated with Colonel Strong Vincent, who volunteered to move his brigade to Little Round Top, and Sykes, who sent the brigade as reinforcements.
    5. Briefly helping to manhandle the artillery: Warren assisted in moving the artillery to the top of Little Round Top, but soon rode off to find reinforcements.

      Overall, Warren's prompt action, initiative, and ability to work with other commanders helped to ensure the defense of Little Round Top, which was critical to the success of the Union position.
4.  **Q**: What mistake did MG Daniel Sickles make during the Battle of Gettysburg?
    **A**: Answer
    During the Battle of Gettysburg, MG Daniel Sickles made a mistake by advancing his corps forward to positions along the Emmitsburg Road without coordinating with his commander, General Meade. He left Little Round Top unoccupied, which created a gap in the Union line that was vulnerable to being outflanked by the Confederates, specifically Longstreet's corps. This mistake failed to take into account Meade's plan for a defensive battle along a continuous line, which was intended to prevent the Confederates from outflanking the Union position.
5.  **Q**: What made Admiral Nelson’s leadership at the Battle of the Nile an example of Mission Command?
    **A**: Answer
    Admiral Nelson's leadership at the Battle of the Nile is an example of Mission Command due to the following factors:

    1. **Building Cohesive Teams through Mutual Trust**: Nelson had a strong, pre-existing relationship with many of his captains, including his superior Admiral John Jervis, Lord St. Vincent. This trust was evident in their flawless execution of the stern anchoring maneuver under fire.
    2. **Creating Shared Understanding**: Nelson shared his vision with his captains through individual meetings and larger gatherings, ensuring that everyone understood their role and the overall objective.
    3. **Providing a Clear Commander's Intent**: Nelson clearly communicated his intent to his subordinates, allowing them to make decisions that aligned with the overall mission.
    4. **Exercising Disciplined Initiative**: Nelson's captains and crews demonstrated disciplined initiative, executing the stern anchoring maneuver flawlessly, which indicates that they had a clear understanding of the commander's intent and the freedom to act accordingly.
    5. **Using Mission Orders**: Nelson's orders were clear and concise, allowing his subordinates to execute them independently while still achieving the overall objective.
    6. **Accepting Prudent Risk**: Nelson's willingness to take calculated risks and delegate decisions to his trusted captains demonstrates a confident leadership style that is characteristic of Mission Command.

    Overall, Admiral Nelson's leadership at the Battle of the Nile exemplifies the principles of Mission Command, as he empowered his subordinates, provided clear guidance, and allowed them to exercise disciplined initiative to achieve a decisive victory.
**Success Rate Note**:
"The application successfully answered 5 out of 5 questions with high accuracy, correctly citing the sources from the document.")*

## Remarks

For this project, I implemented a full-stack RAG application with an advanced retrieval pipeline. The final, robust version uses state-of-the-art Cohere embeddings and a multi-query retrieval strategy to find the most relevant context.

The assignment also required a reranker. I fully integrated and tested multiple reranking providers (Cohere and Jina AI). However, during testing, these components proved to be unstable for this specific use case, often filtering out valid results.

As a final engineering decision, I am submitting the most reliable version of the pipeline, which bypasses the reranker. This version has been tested and proven to provide accurate, grounded answers. This demonstrates a key trade-off: **prioritizing a stable and functional user experience over a more complex architecture that included an unstable component.**

## Resume Link

(https://drive.google.com/file/d/15DQg0_J9Awb5NJXDagiY3Awq0t0LddTQ/view?usp=sharing)
