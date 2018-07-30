'use strict';

// --------------- Helpers that build all of the responses -----------------------

function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: 'PlainText',
            text: output,
        },
        card: {
            type: 'Simple',
            title: `SessionSpeechlet - ${title}`,
            content: `SessionSpeechlet - ${output}`,
        },
        reprompt: {
            outputSpeech: {
                type: 'PlainText',
                text: repromptText,
            },
        },
        shouldEndSession,
    };
}

function buildResponse(sessionAttributes, speechletResponse) {
    return {
        version: '1.0',
        sessionAttributes,
        response: speechletResponse,
    };
}


// --------------- Functions that control the skill's behavior -----------------------

function getWelcomeResponse(callback) {
    var sessionAttributes = {};
    const cardTitle = 'Welcome';
    const speechOutput = 'First Aid here. ' +
        'What can I help you with?';
    const repromptText = 'First Aid here. ' +
        'What can I help you with?';
    const shouldEndSession = false;
    sessionAttributes = {
        "cpr": false,
        "cycle": 1,
        "phase": 1,
        "stop": false
    };

    callback(sessionAttributes,
        buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function handleSessionEndRequest(callback) {
    const cardTitle = 'Session Ended';
    const speechOutput = 'Thank you for trying First Aid. Have a nice day!';
    const shouldEndSession = true;

    callback({}, buildSpeechletResponse(cardTitle, speechOutput, null, shouldEndSession));
}

function otherResponse(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Call 911.';

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function helpResponse(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'You can ask about checking an injured adult, choking, CPR, AED, controlling bleeding, burns, poisoning, neck injuries, spinal injuries or stroke.';

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function readyResponse(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Start counting.';

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function cprHelpResponse(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'You can ask about chest compression and rescue breath.';

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function ccHelpResponse(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Push hard, push fast in the middle of the chest at least 2 inches deep and at least 100 compressions per minute.';

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function rbHelpResponse(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Tilt the head back and lift the chin up. Pinch the nose shut then make a complete seal over the person’s mouth. Blow in for about 1 second to make the chest clearly rise. Give rescue breaths, one after the other.';

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function ccRestart(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Restart chest compressions. When you are done, say done.';
    if (sessionAttributes.phase == 1) {
        sessionAttributes.cycle = sessionAttributes.cycle - 1;
    }
    sessionAttributes.phase = 2;

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function rbRestart(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Restart rescue breaths. When you are done, say done.';

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function chokingResponse(intent, session, callback) {
    const cardTitle = intent.name;
    const repromptText = null;
    let sessionAttributes = session.attributes;
    let shouldEndSession = false;
    let speechOutput = 'Is the person conscious or unconscious?';

    callback(sessionAttributes,
         buildSpeechletResponse(intent.name, speechOutput, repromptText, shouldEndSession));
}

function chestCompression(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let howToChestCompression = 'Push hard, push fast in the middle of the chest at least 2 inches deep and at least 100 compressions per minute. ';
    let speechOutput = 'Lay the person on a firm, flat surface. ' + 'You will give 30 chest compressions. '
    if (session.attributes.cycle == 1) {
        speechOutput = speechOutput + howToChestCompression;
    }
    speechOutput = speechOutput + 'When you are ready to begin, say ready. ' + 'When you are done with 30 compressions, say done.';
    sessionAttributes.cpr = true;
    sessionAttributes.phase = 2;
    callback(sessionAttributes,
         buildSpeechletResponse(intent.name, speechOutput, repromptText, shouldEndSession));
}

function rescueBreath(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let howToRescueBreath = 'Tilt the head back and lift the chin up. Pinch the nose shut then make a complete seal over the person’s mouth. Blow in for about 1 second to make the chest clearly rise. Give rescue breaths, one after the other. ';
    let speechOutput = 'You will give 2 rescue breaths. '
    if (session.attributes.cycle == 1) {
        speechOutput = speechOutput + howToRescueBreath;
    }
    speechOutput = speechOutput  + 'When you are done with rescue breaths, say done.';
    sessionAttributes.cycle = sessionAttributes.cycle + 1;
    sessionAttributes.phase = 1;
    callback(sessionAttributes,
         buildSpeechletResponse(intent.name, speechOutput, repromptText, shouldEndSession));
}

function stopPrompt(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Are you sure you want to stop?';
    sessionAttributes.stop = true;

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function stopCPR(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Stop CPR.';
    sessionAttributes.stop = false;
    sessionAttributes.cpr = false;
    sessionAttributes.cycle = 1;
    sessionAttributes.phase = 1;

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function continueCPR(intent, session, callback) {
    const cardTitle = intent.name;
    let repromptText = '';
    let sessionAttributes = session.attributes;
    const shouldEndSession = false;
    let speechOutput = 'Continue CPR.';
    sessionAttributes.stop = false;

    callback(sessionAttributes,
         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}


// --------------- Events -----------------------

function onSessionStarted(sessionStartedRequest, session) {
    console.log(`onSessionStarted requestId=${sessionStartedRequest.requestId}, sessionId=${session.sessionId}`);
}


function onLaunch(launchRequest, session, callback) {
    console.log(`onLaunch requestId=${launchRequest.requestId}, sessionId=${session.sessionId}`);

    getWelcomeResponse(callback);
}

function onIntent(intentRequest, session, callback) {
    console.log(`onIntent requestId=${intentRequest.requestId}, sessionId=${session.sessionId}`);

    const intent = intentRequest.intent;
    const intentName = intentRequest.intent.name;


    if (intentName === 'ChokingIntent') {
        chokingResponse(intent, session, callback);
    } else if (intentName === 'CPRIntent') {
        chestCompression(intent, session, callback);
    } else if (intentName === 'HelpIntent') {
        if (! session.attributes.cpr) {
            helpResponse(intent, session, callback);    
        } else {
            cprHelpResponse(intent, session, callback);
        }
    } else if (intentName === 'ReadyIntent') {
        readyResponse(intent, session, callback);
    } else if (intentName === 'DoneIntent') {
        if (session.attributes.phase == 2) {
            rescueBreath(intent, session, callback);
        } else {
            chestCompression(intent, session, callback);
        }
    } else if (intentName === 'StopIntent') {
        if (session.attributes.cpr) {
            stopPrompt(intent, session, callback);
        } else {
            throw new Error('Invalid Intent');
        }
    } else if (intentName === 'ccHelpIntent') {
        ccHelpResponse(intent, session, callback);    
    } else if (intentName === 'rbHelpIntent') {
        rbHelpResponse(intent, session, callback);
    } else if (intentName === 'ccRestartIntent'){
        ccRestart(intent, session, callback);
    } else if (intentName === 'rbRestartIntent'){
        rbRestart(intent, session, callback);
    } else if (intentName === 'AMAZON.YesIntent') {
        if (session.attributes.stop) {
            stopCPR(intent, session, callback);
        } else {
            throw new Error('Invalid Intent');
        }
    } else if (intentName === 'AMAZON.NoIntent') {
        if (session.attributes.stop) {
            continueCPR(intent, session, callback);
        } else {
            throw new Error('Invalid Intent');
        }
    } else if ((intentName === 'CheckingIntent') || (intentName === 'AEDIntent') || (intentName === 'BleedingIntent') || (intentName === 'BurnsIntent') || (intentName === 'PoisoningIntent') || (intentName === 'NeckIntent') || (intentName === 'SpinalIntent') || (intentName === 'StrokeIntent') || (intentName === 'ConsciousIntent') || (intentName === 'UnconsciousIntent')) {
        otherResponse(intent, session, callback);
    } else {
        throw new Error('Invalid Intent');
    }
}

function onSessionEnded(sessionEndedRequest, session) {
    console.log(`onSessionEnded requestId=${sessionEndedRequest.requestId}, sessionId=${session.sessionId}`);
}


// --------------- Main handler -----------------------

exports.handler = (event, context, callback) => {
    try {
        console.log(`event.session.application.applicationId=${event.session.application.applicationId}`);

        /**
         * Uncomment this if statement and populate with your skill's application ID to
         * prevent someone else from configuring a skill that sends requests to this function.
         */
        
        if (event.session.application.applicationId !== 'amzn1.ask.skill.80236db0-3b97-432d-beef-a1d371ba7b49') {
             callback('Invalid Application ID');
        }
        

        if (event.session.new) {
            onSessionStarted({ requestId: event.request.requestId }, event.session);
        }

        if (event.request.type === 'LaunchRequest') {
            onLaunch(event.request,
                event.session,
                (sessionAttributes, speechletResponse) => {
                    callback(null, buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === 'IntentRequest') {
            onIntent(event.request,
                event.session,
                (sessionAttributes, speechletResponse) => {
                    callback(null, buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === 'SessionEndedRequest') {
            onSessionEnded(event.request, event.session);
            callback();
        }
    } catch (err) {
        callback(err);
    }
};
