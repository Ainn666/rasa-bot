FROM rasa/rasa:3.6.16-full

# Copy project files
COPY . /app
WORKDIR /app

# Install custom dependencies
RUN pip install -r requirements.txt

# Expose port used by RASA
EXPOSE 5005

# Start the RASA server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]
