# Secret Santa Telegram Bot

## Installation

First, you need to download the project to your local machine

    git clone https://github.com/Temirln/secret_santa_tg_bot.git

Then install all required Python libraries

    pip install -r requirements.txt

You need to create and configure your .env file in root directory

    BOT_TOKEN=
    ADMIN_ID=

    API_ID=
    API_HASH=
    
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=

    WEB_SERVER_HOST=
    WEB_SERVER_PORT=
    WEBHOOK_PATH=
    WEBHOOK_SECRET=
    BASE_WEBHOOK_URL=

Finally, you can run Project from root directory and see the Results

    python main.py