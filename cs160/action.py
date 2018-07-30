"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urlparse
import datetime
import urllib2
import cookielib
import re


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {
        "main_dialog": True,
        "recipe_dialog": False,
        "direction_dialog": False,
        "ingredient_list": [],
        "ingredient_index": 0,
        "direction_list": [],
        "direction_index": 0
    }
    card_title = "Welcome"
    speech_output = "recipe assistant, what recipe would you like to make?"
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying recipe assistant. "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_help(intent, session):
    session_attributes = session.get('attributes', {})
    speech_output = "You can say find blah, or I'd like to make blah" 
    should_end_session = False
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def search(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False
    reprompt_text = None
    search_term = intent['slots']['Dish']['value']
    
    jar = cookielib.CookieJar()
    cookie = urllib2.HTTPCookieProcessor(jar)       
    opener = urllib2.build_opener(cookie)
    index = 1
    url = 'http://192.155.82.100:25485/detail/'
    search_successful = False
    while not search_successful:
        req = urllib2.Request(url + str(index))
        res = opener.open(req)
        html = res.read()
        if html == '404':
            break
        regex = r"<title>"
        match1 = re.search(regex, html)
        regex = r"\|"
        match2 = re.search(regex, html)
        dish_name = html[match1.end(): match2.start() - 1]
        if dish_name == search_term:
            search_successful = True
            regex = r"<span>"
            match1 = re.search(regex, html)
            regex = r"</span>"
            match2 = re.search(regex, html)
            directions = html[match1.end(): match2.start()]
            direction_list = directions.split('\n')
            
            html = html[match2.end() + 1:]
            regex = r"<span>"
            match1 = re.search(regex, html)
            regex = r"</span>"
            match2 = re.search(regex, html)
            ingredients = html[match1.end(): match2.start()]
            ingredient_list = ingredients.split('\n')
        index += 1
    
    if search_successful:
        speech_output = "I find the dish you want to make."
        session_attributes = {
            "main_dialog": False,
            "recipe_dialog": True,
            "direction_dialog": False,
            "ingredient_list": ingredient_list,
            "ingredient_index": 0,
            "direction_list": direction_list,
            "direction_index": 0
        }
    else:
        speech_output = "I cannot find the dish you want to make."
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def start_reading_ingredients(intent, session):
    session_attributes = session.get('attributes', {})
    speech_output = "I will read ingredients one at a time. The first one is "
    should_end_session = False
    reprompt_text = None
    
    index = session_attributes["ingredient_index"]
    ingredient = session_attributes["ingredient_list"][index]
    speech_output = speech_output + ingredient
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def next_ingredient(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False
    reprompt_text = None
    
    index = session_attributes["ingredient_index"]
    ingredient = session_attributes["ingredient_list"][index + 1]
    speech_output = ingredient
    session_attributes["ingredient_index"] = index + 1
    if (session_attributes["ingredient_index"] + 1) == len(session_attributes["ingredient_list"]):
        speech_output = speech_output + ". This is the last ingredient."
        session_attributes["recipe_dialog"] = False
        session_attributes["direction_dialog"] = True
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def last_ingredient(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False
    reprompt_text = None
    
    index = session_attributes["ingredient_index"]
    if index > 0:
        ingredient = session_attributes["ingredient_list"][index - 1]
        speech_output = ingredient
        session_attributes["ingredient_index"] = index - 1
    else:
        speech_output = "This is the first ingredient. There is no last ingredient."
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def restart_ingredients(intent, session):
    session_attributes = session.get('attributes', {})
    speech_output = "I will start from the first ingredient again. The first one is "
    should_end_session = False
    reprompt_text = None
    
    ingredient = session_attributes["ingredient_list"][0]
    speech_output = speech_output + ingredient
    session_attributes["ingredient_index"] = 0
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def start_reading_directions(intent, session):
    session_attributes = session.get('attributes', {})
    speech_output = "I will read directions one at a time. The first step is "
    should_end_session = False
    reprompt_text = None
    
    index = session_attributes["direction_index"]
    direction = session_attributes["direction_list"][index]
    speech_output = speech_output + direction
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def next_step(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False
    reprompt_text = None
    
    index = session_attributes["direction_index"]
    direction = session_attributes["direction_list"][index + 1]
    speech_output = direction
    session_attributes["direction_index"] = index + 1
    if (session_attributes["direction_index"] + 1) == len(session_attributes["direction_list"]):
        speech_output = speech_output + ". This is the last step. I will exit to main menu."
        session_attributes = {
            "main_dialog": True,
            "recipe_dialog": False,
            "direction_dialog": False,
            "ingredient_list": [],
            "ingredient_index": 0,
            "direction_list": [],
            "direction_index": 0
        }
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def last_step(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False
    reprompt_text = None
    
    index = session_attributes["direction_index"]
    if index > 0:
        direction = session_attributes["direction_list"][index - 1]
        speech_output = direction
        session_attributes["direction_index"] = index - 1
    else:
        speech_output = "This is the first step. There is no last step."
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def restart_directions(intent, session):
    session_attributes = session.get('attributes', {})
    speech_output = "I will start from the first step again. The first step is "
    should_end_session = False
    reprompt_text = None
    
    direction = session_attributes["direction_list"][0]
    speech_output = speech_output + direction
    session_attributes["direction_index"] = 0
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def quit_to_main_menu(intent, session):
    session_attributes = {
        "main_dialog": True,
        "recipe_dialog": False,
        "direction_dialog": False,
        "ingredient_list": [],
        "ingredient_index": 0,
        "direction_list": [],
        "direction_index": 0
    }
    speech_output = "Quit to main menu."
    should_end_session = False
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_error(intent, session):
    session_attributes = session.get('attributes', {})
    speech_output = "Sorry, I didn't get that."
    should_end_session = False
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    session_attributes = session.get('attributes', {})
    try:
        if session_attributes["main_dialog"]:
            if intent_name == "HelpIntent":
                return get_help(intent, session)
            elif intent_name == "SearchIntent":
                return search(intent, session)
            elif intent_name == "QuitIntent":
                return handle_session_end_request(intent, session)
            else:
                raise ValueError("Invalid intent")
        elif session_attributes["recipe_dialog"]:
            if intent_name == "IngredientIntent":
                return start_reading_ingredients(intent, session)
            elif intent_name == "NextIngredient":
                return next_ingredient(intent, session)
            elif intent_name == "LastIngredient":
                return last_ingredient(intent, session)
            elif intent_name == "RestartIntent":
                return restart_ingredients(intent, session)
            elif intent_name == "QuitIntent":
                return quit_to_main_menu(intent, session)
            else:
                raise ValueError("Invalid intent")
        else:
            if intent_name == "DirectionIntent":
                return start_reading_directions(intent, session)
            elif intent_name == "NextStep":
                return next_step(intent, session)
            elif intent_name == "LastStep":
                return last_step(intent, session)
            elif intent_name == "RestartIntent":
                return restart_directions(intent, session)
            elif intent_name == "QuitIntent":
                return quit_to_main_menu(intent, session)
            else:
                raise ValueError("Invalid intent")
    except ValueError:
        return get_error(intent, session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
 