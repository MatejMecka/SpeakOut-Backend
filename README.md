# SpeakOut - Backend ![pipeline](https://gitlab.com/andrometa/website/badges/master/pipeline.svg)
SpeakOut is an app developed to help victims of Bullying based on the original idea pitched on the first Generation Unlimited Youth challenge organized in Macedonia.

We have a great journey developing and working on our first project to help make an impact and we believe that by Open Sourcing this project others can help us reach that goal and work together on making SpeakOut a platform where everyone will want to ask for help.

# Requirements
* Flask
* Slack Workspace
* Sentry Workspace

# Installation
`pip install -r requirements.txt`

Set up the Environment Variables

Populate the Database using `flask db_init`

Open Flask Shell and type
`flask run`

You've successfully started the Development Server


# Contribution
Read Contributing.md

# Contact
Facebook: @speakoutappmk

# Environment Variables
```bash
FLASK_APP=manage.py
SENTRY_API_KEY # Reporting Errors to Sentry
SLACK_API_TOKEN # A Personal Account that redirects the messages aka the bridge and creates the channels
SLACK_VOLUNTEERS_CHAT_ID # Where all the volunteers will be alerted 
SLACK_VERIFICATION_TOKEN # To Verify if the requests are coming from slack
SLACK_MODERATORS_CHAT_ID # Moderators Channel for moderating info
SLACK_BOT_USERNAME # The Username of the Slack Bot
MESSAGE_RETENTION # How Long to Keep the messages
```
