# AI For Pediatric Education

## Getting Started

### Prerequisites

- Install [Docker](https://www.docker.com/)
- Install [Postman](https://www.postman.com/)

### Build and Run the Application

1. Build the Docker containers:

   ```bash
   docker-compose build
   ```

2. Start the application:

   ```bash
   docker-compose up
   ```

   The application will be available at `http://127.0.0.1:8080`.

### Testing the API

1. Open Postman and create a new POST request.
2. Set the URL to:
   ```
   http://127.0.0.1:8080/query
   ```
3. In the request body, use the following JSON:
   ```json
   {
     "query": "What is Gastroenteritis disease?"
   }
   ```
4. Send the request. You should receive a response similar to:
   ```json
   {
     "query": "What is Gastroenteritis disease?",
     "rephrased_query": "Gastroenteritis disease is a type of illness.",
     "answers_context": "Gastroenteritis in children is most often viral and managed with hydration and supportive care.\n\n---\n\nHand-foot-and-mouth disease is a contagious viral illness common in young children, characterized by mouth sores and skin rash.\n\n---\n\nEczema, or atopic dermatitis, is a chronic skin condition that often begins in childhood.",
     "sources": ["entry_19.json", "entry_26.json", "entry_25.json"]
   }
   ```

### Notes

- Ensure Docker is running before executing the commands.
- The API processes pediatric-related queries and provides answers, their context, and sources.
