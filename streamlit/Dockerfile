FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD streamlit run app.py --server.fileWatcherType="poll" --server.runOnSave=true