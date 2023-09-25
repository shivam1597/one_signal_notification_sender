import requests
import time
import firebase_admin
from firebase_admin import db, auth
from datetime import datetime, timedelta

cred_obj = firebase_admin.credentials.Certificate('cricverse-40c18-firebase-adminsdk-yqsud-8b62e05743.json')
firebase_admin.initialize_app(cred_obj, {'databaseURL':'https://cricverse-40c18-default-rtdb.firebaseio.com/'})

email = 'golumaths100@gmail.com'
password = 'Shivam@15'

try:
    user = auth.get_user_by_email(email)
    user = auth.update_user(
        user.uid,
        password=password
    )
except auth.AuthError as e:
    print(f"Error: {e}")

ref = db.reference()

boolean_value = True
while boolean_value:
    timestamp_seconds = time.time()

    timestamp_milliseconds = int(timestamp_seconds * 1000)
    ref.child('timeStamp').set(timestamp_milliseconds)
    # print(timestamp_milliseconds)
    # current_date = datetime.now()

    # one_day_before = current_date + timedelta(days=-1)
    # formatted_before_date = one_day_before.strftime('%Y-%m-%d')

    # two_days_after = current_date + timedelta(days=1)
    # formatted_after_date = two_days_after.strftime('%Y-%m-%d')

    # url = 'https://cricketapi-icc.pulselive.com/fixtures?tournamentTypes=I%2CWI&startDate={}&endDate={}&pageSize=100'.format(formatted_before_date, formatted_after_date)

    # match_id = ''
    # # Make an API request
    # response = requests.get(url)
    # # ref.child().set()
    # if response.status_code == 200:
    #     data = response.json()
    #     for content in data.get('content'):
    #         scheduled_entry_object = content.get('scheduleEntry')
    #         team1_name = scheduled_entry_object.get('team1').get('team').get('fullName')
    #         team2_name = scheduled_entry_object.get('team2').get('team').get('fullName')
    #         match_id = scheduled_entry_object.get('matchId').get('id')
    #         if scheduled_entry_object.get('matchState') == 'C':
    #             # will be used for notification
    #             match_status_text = scheduled_entry_object.get('matchStatus').get('text')
    #             # checking if match id was available
    #             match_id_object = ref.child('live_match_status').child(str(match_id)).get()
    #             if match_id_object is not None:
    #                 # add sending notification logic (for match completion along with winner)
    #                 ref.child('live_match_status').child(str(match_id)).delete()
    #         if content.get('scheduleEntry').get('matchState') == 'L':

    #             ref.child('live_match_status').update({str(match_id):'L'})

    #             while True:
    #                 commentary_url = 'https://api.icc.cdp.pulselive.com/commentary/ICC/{}/EN/?direction=descending&maxResults=30'.format(match_id)
    #                 commentary_response = requests.get(commentary_url)
    #                 commentary_json = commentary_response.json()
    #                 first_commentary_ball_details = commentary_json['content'][0]['ballDetails']

    #                 if first_commentary_ball_details is not None:
    #                     ball_activity = first_commentary_ball_details['activity']
    #                     if ball_activity == 'W':
    #                         activity_message = first_commentary_ball_details['message'] # this will be sent in the notification
    #                         if team1_name=='India' or team2_name=='India':
    #                             print('send notification')
    #                 elif first_commentary_ball_details is None:
    #                     first_commentary_ball_details = commentary_json['content'][0]['details']
    #                     inning_over = first_commentary_ball_details.get('over')
    #                     innings_ball = first_commentary_ball_details.get('inningsBalls')
    #                     innings_max_balls = first_commentary_ball_details.get('inningsMaxBalls')
    #                     remaining_balls = innings_max_balls-innings_ball
    #                     required_runs = first_commentary_ball_details.get('requiredRuns')
    #                     batting_team = first_commentary_ball_details.get('team').get('fullName')
    #                     innings_runs = first_commentary_ball_details.get('inningsRuns')
    #                     innings_wickets = first_commentary_ball_details.get('inningsWickets')
    #                     if inning_over%5==0:
    #                         if team1_name=='India' or team2_name=='India':
    #                             print('send notification')
    #                     if innings_ball==innings_max_balls:
    #                         print('send notification to non Indian countries about Innings break')
    #                         # construct notification here
    #                 # time.sleep(10)
    #             else:
    #                 print()
    #             # below_commentary_cursor = 'below/{messageOrder}'
    #             # send wicket notification and notification after every 5 overs. (only Indian matches)
                
    #             # add sending notification logic
    #     # None if no child available
        

    # else:
    #     print(f"Failed to fetch data. Status code: {response.status_code}")

    # boolean_value = False
    
    time.sleep(17)


# check if match is live, if it is live, save the matchID and match status in firebase
# and whenever the match will complete, send the notification of the completion of match and delete that id from firebase