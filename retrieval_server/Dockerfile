FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Set the OpenAI API key as an environment variable
ENV OPENAI_API_KEY=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

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
