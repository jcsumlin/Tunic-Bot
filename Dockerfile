FROM gorialis/discord.py:full
COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt
CMD ["python", "main.py"]
