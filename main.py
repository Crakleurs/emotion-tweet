import psycopg2
from psycopg2.extras import execute_values
from models.Campaign import CampaignModel
from models.Emotion import EmotionModel
import snscrape.modules.twitter as sntwitter
import requests
import os


API_URL = "https://ai-emotion.etienne-faviere.tech"


dbname = os.getenv("DATABASE_NAME", "db")
user = os.getenv("DATABASE_USER", "root")
password = os.getenv("DATABASE_PASSWORD", "password")
host = os.getenv("DATABASE_HOST", "localhost")
port = os.getenv("DATABASE_PORT", 5432)

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
conn.autocommit = True
cursor = conn.cursor()

# Fetch all actives campaigns

cursor.execute('select * from public."CampaignModels" WHERE status = TRUE ')
results = cursor.fetchall()

for row in results:
    campaign = CampaignModel(row)
    cursor.execute('select count(*) from public."EmotionModels" WHERE "CampaignId" = ' + str(campaign.id))
    count = cursor.fetchone()
    count = count[0]
    res = sntwitter.TwitterHashtagScraper(campaign.hashtag).get_items()

    emotions = []
    for tweet in res:

        res = requests.post(API_URL, json={"content": tweet.content})
        emotions.append(EmotionModel(campaign.id, res.json()))

        count += 1
        if count % 100 == 0:
            execute_values(cursor, 'insert into public."EmotionModels" (joy, optimism, anger, sadness, hate, irony, offensive, positive, neutral, negative, "CampaignId") values %s', [emotion.to_tuple() for emotion in emotions])
            conn.commit()
            emotions = []

        if count == 10000:
            break

    if(len(emotions) > 0):
        execute_values(cursor,'insert into public."EmotionModels" (joy, optimism, anger, sadness, hate, irony, offensive, positive, neutral, negative, "CampaignId") values %s', [emotion.to_tuple() for emotion in emotions])
        conn.commit()
        emotions = []

    cursor.execute('update public."CampaignModels" set status = FALSE where id =  ' + str(campaign.id))
    conn.commit()
