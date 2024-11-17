import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# 사용자와의 대화를 종료한다.
def close(session_attributes, active_contexts, fulfillment_state, intent, message):
    response = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': active_contexts,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': fulfillment_state
            },
            'intent': intent
        },
        'messages': [{'contentType': 'PlainText', 'content': message}]
    }

    return response


# Intent의 슬롯을 채우기 위해 사용자에게 정보를 요청한다.
def elicit_slot(session_attributes, active_contexts, intent, slot_to_elicit, message):
    return {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': active_contexts,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit
            },
            'intent': intent,
        }
    }


# 사용자에게 intent의 fulfillment를 confirm 받는다.
def confirm_intent(active_contexts, session_attributes, intent, message):
    return {
        'sessionState': {
            'activeContexts': [active_contexts],
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ConfirmIntent'
            },
            'intent': intent
        }
    }


# lex가 다음 작업을 수행하도록 지시한다.
def delegate(session_attributes, active_contexts, intent, message):
    return {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': active_contexts,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate',
            },
            'intent': intent,
        },
        'messages': [{'contentType': 'PlainText', 'content': message}]
    }


# 사용자에게 초기 메시지를 보낸다.
def initial_message(intent_name):
    response = {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': 'Location' if intent_name == 'BookHotel' else 'PickUpCity'
            },
            'intent': {
                'confirmationState': 'None',
                'name': intent_name,
                'state': 'InProgress'
            }
        }
    }

    return response
