class CampaignModel:
    id = 0
    name = ""
    hashtag = ""
    date = ""
    running = True

    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.hashtag = row[2]
        self.date = row[3]
        self.running = row[4]

    def isRunning(self):
        return self.running