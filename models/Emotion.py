class EmotionModel:
    joy = 0
    optimism = 0
    anger = 0
    sadness = 0
    hate = 0
    irony = 0
    offensive = 0
    positive = 0
    neutral = 0
    negative = 0
    campaign_id = 0

    def __init__(self, campaign_id, json):
        print(json)
        self.joy = json["joy"]
        self.optimism = json["optimism"]
        self.anger = json["anger"]
        self.sadness = json["sadness"]
        self.hate = json["hate"]
        self.irony = json["irony"]
        self.offensive = json["offensive"]
        self.positive = json["positive"]
        self.neutral = json["neutral"]
        self.negative = json["negative"]
        self.campaign_id = campaign_id

    def to_tuple(self):
        return self.joy, self.optimism, self.anger, self.sadness, self.hate, self.irony, self.offensive, self.positive, self.neutral, self.negative, self.campaign_id
