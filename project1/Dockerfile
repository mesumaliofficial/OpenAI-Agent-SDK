# Use Python image
FROM python:3.13.3

# Create and set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Create the .files directory and set permissions
RUN mkdir -p /app/.files/.cache && chmod -R 777 /app/.files

# Install Chainlit
RUN pip install --no-cache-dir chainlit
RUN pip install openai-agents

# Expose the port used by Chainlit
EXPOSE 8000

# Run the Chainlit app
CMD ["chainlit", "run", "main.py"]