# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install apt requirements
RUN apt update -y && apt upgrade -y && \ 
    apt install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/* 

# Cloning the repository
RUN git clone https://github.com/tyburd/mangabot /app

WORKDIR /app

# Install pip requirements
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["bash", "start.sh"]
