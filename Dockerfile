# שימוש ב- Python קליל
FROM python:3.9-slim

# העתקת קבצי הפרויקט
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# הרצת Flask דרך Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
