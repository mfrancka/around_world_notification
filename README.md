# around_world_notification
Simple script which will notify by email if on page of Bartek Czarcinśki new post appear.

# Run in docker
Clone repository and create config.ini file in main repository directory.
Run commands:
```bash
docker build -t arround-world-alpine .
docker volume create --name links-db
docker run -v links-db:/usr/src/app/links-db/ -t arround-world-alpine
```
