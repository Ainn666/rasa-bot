FROM rasa/rasa-sdk:3.6.2

COPY ./actions /app/actions

WORKDIR /app

USER root

RUN pip install --no-cache-dir google-generativeai fpdf

USER 1001

CMD ["start", "--actions", "actions"]
