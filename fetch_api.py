import requests
import time
import firebase_admin
from firebase_admin import db, auth
from datetime import datetime, timedelta
import json

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
start_time = time.time()
boolean_value = True
notification_sent = False
while boolean_value:
    
    current_date = datetime.now()

    current_time = time.time()
    elapsed_time = current_time - start_time

    one_day_before = current_date + timedelta(days=-1)
    formatted_before_date = one_day_before.strftime('%Y-%m-%d')

    two_days_after = current_date + timedelta(days=1)
    formatted_after_date = two_days_after.strftime('%Y-%m-%d')

    url = 'https://cricketapi-icc.pulselive.com/fixtures?tournamentTypes=I%2CWI&startDate={}&endDate={}&pageSize=100'.format(formatted_before_date, formatted_after_date)

    match_id = ''
    # Make an API request
    response = requests.get(url, headers={'Account':'ICC'})

    if response.status_code == 200:
        onesignal_app_id = 'a6803967-4276-4785-bdda-d48455ed72dc'
        onesignal_api_key = 'MzI1MGRjYTItYTEwMy00ZDUwLWE0NzUtZTMyMTEyMGQ1OTVl'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Basic {}'.format(onesignal_api_key)
        }
        data = response.json()
        for content in data.get('content'):
            scheduled_entry_object = content.get('scheduleEntry')
            team1_name = scheduled_entry_object.get('team1').get('team').get('fullName')
            team2_name = scheduled_entry_object.get('team2').get('team').get('fullName')
            match_id = scheduled_entry_object.get('matchId').get('id')
            if scheduled_entry_object.get('matchState') == 'C':
                # will be used for notification
                match_status_text = scheduled_entry_object.get('matchStatus').get('text')
                # checking if match id was available
                match_id_object = ref.child('live_match_status').child(str(match_id)).get()
                if match_id_object is not None:
                    notification_data = {
                        'app_id': onesignal_app_id,
                        'included_segments': ['All'],  # Send to all users
                        'headings': {'en': '{} vs {}'.format(team1_name, team2_name)},
                        'contents': {'en': match_status_text}
                    }
                    json_data = json.dumps(notification_data)
                    response_notification = requests.post('https://onesignal.com/api/v1/notifications', headers=headers, data=json_data)
                    # add sending notification logic (for match completion along with winner)
                    ref.child('live_match_status').child(str(match_id)).delete()
            if scheduled_entry_object.get('matchState') == 'L':
                ref.child('live_match_status').update({str(match_id):'L'})

                while True:
                    commentary_url = 'https://api.icc.cdp.pulselive.com/commentary/ICC/{}/EN/?direction=descending&maxResults=30'.format(match_id)
                    commentary_response = requests.get(commentary_url)
                    commentary_json = commentary_response.json()
                    if commentary_json is not None:
                        commentary_json_first_item = commentary_json['commentaries']['content'][0]
                        if 'ballDetails' in commentary_json_first_item:
                            first_commentary_ball_details = commentary_json_first_item['ballDetails']
                            if first_commentary_ball_details is not None:
                                ball_activity = first_commentary_ball_details['activity']
                                if ball_activity == 'W':
                                    if not notification_sent:
                                        activity_message = first_commentary_ball_details['message'] # this will be sent in the notification
                                        wicket_match_notification_data = {
                                            'app_id': onesignal_app_id,
                                            'included_segments': ['All'],  # Send to all users
                                            'headings': {'en': '{} vs {}'.format(team1_name, team2_name)},
                                            'contents': {'en': activity_message}
                                        }
                                        indian_match_json_data = json.dumps(wicket_match_notification_data)
                                        response_notification = requests.post('https://onesignal.com/api/v1/notifications', headers=headers, data=indian_match_json_data)
                                        notification_sent = True
                                else:
                                    notification_sent = False
                        else:
                            first_commentary_ball_details = commentary_json_first_item['details']
                            inning_over = first_commentary_ball_details.get('over')
                            innings_ball = first_commentary_ball_details.get('inningsBalls')
                            innings_max_balls = first_commentary_ball_details.get('inningsMaxBalls')
                            remaining_balls = innings_max_balls-innings_ball
                            required_runs = first_commentary_ball_details.get('requiredRuns')
                            batting_team = first_commentary_ball_details.get('team').get('fullName')
                            innings_runs = first_commentary_ball_details.get('inningsRuns')
                            innings_wickets = first_commentary_ball_details.get('inningsWickets')
                            # required_runs
                            if inning_over%5==0 and not notification_sent:
                                if team1_name=='India' or team2_name=='India':
                                    message_to_send = '{}: {}/{} after {} over.\n Tap to view full scorecard.'.format(batting_team, innings_runs, innings_wickets, inning_over)
                                    if required_runs is not None:
                                        message_to_send = message_to_send + ' {} requires {} in {}.'.format(batting_team, required_runs, remaining_balls)
                                    indian_match_notification_data = {
                                        'app_id': onesignal_app_id,
                                        'included_segments': ['All'],  # Send to all users
                                        'headings': {'en': '{} vs {}'.format(team1_name, team2_name)},
                                        'contents': {'en': message_to_send}
                                    }
                                    indian_match_json_data = json.dumps(indian_match_notification_data)
                                    response_notification = requests.post('https://onesignal.com/api/v1/notifications', headers=headers, data=indian_match_json_data)
                                    notification_sent = True
                            else:
                                notification_sent = False
                            if innings_ball==innings_max_balls:
                                indian_match_notification_data = {
                                        'app_id': onesignal_app_id,
                                        'included_segments': ['All'],  # Send to all users
                                        'headings': {'en': '{} vs {}'.format(team1_name, team2_name)},
                                        'contents': {'en': '{}: {} after {} over. {} requires {} in {}. {}'.format(batting_team, innings_runs, inning_over, batting_team, required_runs, remaining_balls, first_commentary_ball_details)}
                                    }
                                indian_match_json_data = json.dumps(indian_match_notification_data)
                                response_notification = requests.post('https://onesignal.com/api/v1/notifications', headers=headers, data=indian_match_json_data)
                            # construct notification here
                    time.sleep(5)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
    if elapsed_time >= 6*60*60:
        break
    time.sleep(1)

# check if match is live, if it is live, save the matchID and match status in firebase
# and whenever the match will complete, send the notification of the completion of match and delete that id from firebase
