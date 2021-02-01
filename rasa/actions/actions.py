# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json
import os
from json.decoder import JSONDecodeError

class ActionWrongMessage(Action):

     def name(self) -> Text:
         return "action_wrong_message"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         # This function writes the previous user message in the given json-file
         def writeData(event):
            jsonFile = 'data.json'  # json-file
            data = {    # json-data-block for the user message
                "message": event.get("text"),   # user message
                "predicted_intent": {   # information about the predicted intent
                    "name": event.get("parse_data").get("intent").get("name"),  # intent name
                    "confidence": event.get("parse_data").get("intent").get("confidence")   # prediction confidence
                }
            }
            with open(jsonFile, 'r') as infile:
                if os.stat('data.json').st_size == 0:   # if json-file is empty: create head-array
                    existingData = {}
                    existingData['wrong'] = []
                    temp = existingData['wrong']
                else:   # else: take the already given data inside the json-file
                    existingData = json.load(infile)
                    temp = existingData['wrong']
                temp.append(data)
                with open(jsonFile, 'w') as outfile:
                    json.dump(existingData, outfile, indent=4)

         reversedEvents = tracker.events[::-1] # reverse the event-list: the needed user-event is the 2. in the list
         counter = 0    # user-event counter
         for event in reversedEvents:   # we have different events (slot, ..., user, ..., action)
            if event.get("event") == "user":    # but we need only the user-events
                if counter == 0:    # we need the 2. user-event: count up to 1
                    counter = 1
                    continue
                writeData(event)
                dispatcher.utter_message("Thanks, please continue to chat with me.")
                break

         return []
