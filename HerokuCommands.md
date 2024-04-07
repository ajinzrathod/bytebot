## Heroku

### Our Heroku App URL
https://bytebot-heroku-0969326889b3.herokuapp.com/ask

### Open heroku in terminal
heroku run bash --app bytebot-heroku

## Add Redis
Add Heroku Redis to Your App: Use the Heroku dashboard to add the Redis add-on. Go to your app's dashboard on Heroku, navigate to the "Resources" tab, and search for "Redis" in the "Add-ons" section. 
Select the plan that suits your needs

### Get redis server url
heroku config:get REDISCLOUD_URL -a your-heroku-app-name
    