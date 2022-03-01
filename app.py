from flask import Flask, render_template, request
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError
import json
import os

app = Flask(__name__)
load_dotenv()
api_key = os.environ.get("RIOT_API_KEY")
region = os.environ.get("REGION")

lol_watcher = LolWatcher(api_key)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summonerId', methods=['POST'])
def handleSummonerForm():
    summonerID = request.form['summoner_name_input']
    try:
        summonerData = lol_watcher.summoner.by_name(region, summonerID)
        return render_template( 'summonerData.html', jsonfile=json.dumps(summonerData))
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            raise


if __name__ == "__main__":
    app.run()
