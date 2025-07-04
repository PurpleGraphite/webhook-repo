from flask import Blueprint, request
import logging
from app.extensions import mongo

pollDB = Blueprint('PollDB', __name__)


@pollDB.route('/poll-events')
def getEvents():
    lastProcessedDataTimestamp = request.args.get('latest-timestamp')

    query = {}
    if lastProcessedDataTimestamp:
        query = {"timestamp": {"$gt": lastProcessedDataTimestamp}}
   
    events = list(mongo.db.github_events.find(query).sort("timestamp", 1))

    if events:
        print(f"Found {len(events)} new events")
        lastProcessedDataTimestamp = events[-1]["timestamp"]
        print(f"Updated last processed timestamp to {lastProcessedDataTimestamp}")
    else:
        print("No new events found")
    
    return events, 200