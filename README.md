# latbot
Telegram bot for managing a linux server

![image](https://user-images.githubusercontent.com/5521684/146973011-362764f5-fe9b-48a9-9e99-2a8d3ced63b4.png)

## Prerequisite
- Linux server;
- Docker;
- Docker-compose.

## Installation
1. Clone this repo into your server;
2. Copy docker-compose.yml.example to docker-compose.yml end edit it: 
   1. Enter your bot token in APP_TOKEN field;
   2. Enter your chat ID in APP_MASTER_CHAT_ID field;
3. Install dopipe service:
    <pre>
    chmod u=rwx,go= dopipe-install.sh
    sudo ./dopipe-install.sh
    </pre>
5. Create ./scripts folder and put your scripts there if you want.
6. Build and run container, by running: 
    <pre>docker-compose up --build -d</pre>

If you did everything correctly, the bot will send you a message: Latbot online...


## How to create bots on Telegram
Use the [Bot Father](https://t.me/BotFather) /newbot command to create a new bot. 

The [Bot Father](https://t.me/BotFather) will ask you for a name and username, then generate an authorization token for your new bot.

[Telegram FAQ](https://telegra.ph/Awesome-Telegram-Bot-11-11)

## How to obtain chat_id
Send message to [@RawDataBot](https://t.me/RawDataBot), and you will get an JSON reply

It will be .message.chat.id, looks like this:

<pre>
{
  "message": {
    "chat": {
      "id": 109780439,  // This is your chat_id
    }
  }
}
</pre>

[Telegram FAQ](https://telegra.ph/Awesome-Telegram-Bot-11-11)