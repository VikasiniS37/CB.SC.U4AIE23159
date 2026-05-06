# stage 2
vechicle maintainance schedular microservce 
the persistent stoarge would be the mongo db , as it is easiler for the noSQL to store the data in binaryjson format. whereas the normal schema would store all the data in the form of rows and columns. the application schema for this would be written in the chromaDB/ mongoDB.
the mongo db can be connected to diffenent applications like big data analystics, in kafka live straming we can use this for connection storage and also to the finest parts of the files.

# stage 1
here, we have to design the json file for this application in an efficient way.
thorugh the postman we can connect the apis that is called in the terminal in vs, when we edit the file in the postman the request thorugh the api connection can be viewed in the localhost (corresponding to the application).

# stage 5
function notify is used to send the notification of the recieved mesaages to the respecte thrid party.
the expanded solution to this problem would be the redesigning of the harcoded copy of the application.


## Stage 1: API Design & Real-Time Mechanism
*   **Core Actions:** You need endpoints for **fetching** notifications (GET), **marking as read** (PATCH/PUT), and potentially **deleting** (DELETE).
*   **Contract:** Define a JSON structure including `id`, `userId`, `message`, `type` (Event/Result/Placement), `isRead`, and `createdAt`.
*   **Real-Time:** Suggest **WebSockets** for a persistent bi-directional connection or **Server-Sent Events (SSE)** for a lighter, uni-directional push from server to client.

## Stage 2: Data Persistence
*   **DB Choice:** 
    *   **PostgreSQL/MySQL:** Good for structured data and complex queries.
    *   **NoSQL (MongoDB/DynamoDB):** Better for high-volume, unstructured notification data and horizontal scaling.
*   **Schema:** Define a `notifications` table with appropriate data types and a foreign key for `studentID`.

## Stage 3: Query Optimization
*   **Why it's slow:** The current query performs a **Full Table Scan** because it lacks proper indexing for 5 million rows.
*   **The Fix:** Create a **Composite Index** on `(studentID, isRead, createdAt DESC)`.
*   **Indexing every column:** This is **ineffective** and "not safe" as it increases storage overhead and slows down `INSERT` operations without helping multi-column filters.
*   **New Query:** 
    ```sql
    SELECT studentID FROM notifications 
    WHERE notificationType = 'Placement' 
    AND createdAt >= NOW() - INTERVAL '7 days';
    ```

## Stage 4: Performance & Scaling
*   **The Problem:** Database "hammering" on every page load.
*   **Solutions:**
    *   **Caching (Redis):** Store the "Unread Count" or the latest 10 notifications in-memory to avoid DB hits.
    *   **Read Replicas:** Distribute traffic across multiple database instances.
    *   **Pagination:** Ensure the API only fetches a small "page" of data at a time.

## Stage 5: Reliable Mass Notifications
*   **Shortcomings:** The current pseudocode is **synchronous and fragile**. If one email fails or takes long, the entire loop hangs or crashes.
*   **Redesign (The "Fast & Reliable" Way):**
    1.  **Decouple with Message Queues:** Use a tool like **RabbitMQ** or **AWS SQS**.
    2.  **Producer:** The HR click just adds 50,000 "jobs" to a queue and returns a "Success" message immediately.
    3.  **Workers:** Independent background processes pick up jobs from the queue and handle the actual sending/DB updates. 
    4.  **Retries:** If an email fails for 200 students, the queue can automatically retry those specific jobs later without affecting others.
```