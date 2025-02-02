
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /app

# Install Python and required packages
RUN apt-get update && apt-get install -y python3 python3-pip \
    && pip install -r requirements.txt

COPY . .
CMD ["python3", "-m", "waitress", "app:app"]
