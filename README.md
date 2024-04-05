## Clone the repo

### SSH
```bash
git@github.com:ajinzrathod/bytebot.git
```

OR

### HTTPS
```bash
https://github.com/ajinzrathod/bytebot.git
```

## Start the application

### Prerequisite
* You should have docker installed on your machine

### Go inside the directory
```bash
cd bytebot
```

### Create a file named `.env` which has all these details
```.env
PROD=0
ASSISTANT_ID=assistant_id
INCUBYTE_BYTE_BOT_API_KEY=API_KEY
ASSISTANT_SERVICE_ENABLED=1
```

### Build image and start your applicant using Docker
```bash
docker-compose up
```

Visit [localhost:5000](localhost:5000) on your system and check if you see the welcome screen
