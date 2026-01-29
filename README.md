## Usage

1. create a `.env` file with the following information in `/mail`:

```
LISTMONK_PWD=listmonk-api-user-pwd
LISTMONK_USR=listmonk-api-username
```

These credentials can be created on the superadmin page of listmonk by creating a new user specifically for the API.

2. Then modify the `config.cfg` file to match your own config. Here is a breakdown of each config option:
- `LOCATION` is simply the name used in the title of the template. It can be anything you want. It you want to apply this script to a different gym, you need to change the `LIST_TARGET` url.
- `LIST_TARGET` is the URL to the page containing the list of all the routes.
- `COLOR_TARGE` is the base URL of where the hold colours images are hosted. This is used to downloaded and upload to listmonk.
- `EMAIL_TEMPLATE_PATH` is the local path of the template for the emails content. This is not to be confused with the listmonk template.
- `CSV_PATH` is the local file where the CSV of the route will be downloaded to each day. You can leave it as is or point to a specific folder if you which (e.g. `/sources/routes.csv`)
- `BASE_URL` is the URL of your listmonk installation.
- `API_URL` is the URL of your listmonk API.
- `LIST_ID` is the id of the mailing list to use. You can find this id in your listmonk dashboard.
- `TEMPLATE_ID` is the id of the template to use when sending a campaign. Again, find it in your listmonk dashboard.

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

- Potentially move from python to ...? This is just a challenge for myself to learn something new and probably more adapted than python.