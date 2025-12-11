## Usage

1. create a `config.cfg` file with the following minimum requirements:

```
[MAIL]
MAIL_SERVER = mail.server.com
MAIL_PORT = 587
ADDRESS = address@domain.com
PASSWORD = password
```

2. Then create a `recipients.txt` file containing the destination email addresses:

```
email1@gmail.com
email2@epfl.ch
email3@outlook.fr
...
```

3. Run 
```
python3 send_update.py
```

No arguments are required. You can then simply make this into a cron tab. 

_Note_: the script will generate logs in a file called `logging.log`. This is particularly useful when the script is used in a crontab.

## Misc

This program is made to work for Beaulieu but it should be easy to adapt for any other climbing gym available on https://climbingroute.app.

Also, there are a lot of potential for improving this. It is just a minimal working concept that I might improve in the future. For instance managing the list of recipients the way it works now is not ideal but I only intend to use it with a few friends so it sufficient as is. Below is a list of improvements I want to work on, if you are interested.

## Futur improvements

- Make it easier to remove/add subscribers. Possibly automate it. 

    My vision is that there should exist some self hosted newlsletter software that I could use to automate this part.
- Improve how grade and holds images are handled. 
    
    Right now, they are downloaded each time the program is run. It would be nice to have the set locally. Even better, it would be nice to have them available via the internet so that they don't need to be sent as attachements. I am just afraid that the website might change someday and the images change. The way it works now is by using the images directly on the website so if they change, the script will adapt.
- Improve the location map. Right now it only highlight the relevant bloc but not the specific part of the wall.