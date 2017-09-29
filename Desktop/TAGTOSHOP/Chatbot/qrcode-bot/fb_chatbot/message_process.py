import answer_builder
import pandas as pd
from pprint import pprint

from models import FacebookUser, QRCode, Scan

#import product database
input_words = pd.read_csv('./fb_chatbot/static/input_words.csv')
input_meanings = pd.read_csv('./fb_chatbot/static/input_meanings.csv')


def get_response(fbuser, received_message, is_callback):


    if is_callback:     response_msg = get_callback_response(fbuser, received_message.lower())
    else:               response_msg = get_text_response(fbuser, received_message.lower().split())

    return response_msg



def get_callback_response(fbuser, callback):

    if "get_started_payload" in callback:       response = answer_builder.get_salute_text(fbuser)
    elif "image_start" in callback:             response = answer_builder.get_salute_image(fbuser)
    elif "help" in callback:                    response = answer_builder.get_help(fbuser)
    elif "past_qrs" in callback:                response = answer_builder.get_past_scanned_qrs(fbuser)
    elif "qrvalid_" in callback:                response = answer_builder.get_qr(fbuser, callback)
    elif "qrinvalid" in callback:               response = answer_builder.get_text_response_qrinvalid(fbuser) 
    else:                                       response = answer_builder.get_not_understood_response(fbuser)
  
    return response

def get_text_response(fbuser, phrase_words):
    

    input_type = get_highest_priority_word(phrase_words)

    #From the input type and the global variables we determine a situation
    if input_type == "Saluting":                        response = answer_builder.get_salute_text(fbuser)
    elif input_type == "Help_bot":                      response = answer_builder.get_help(fbuser)        
    elif input_type == "QR_valid":                      response = answer_builder.get_product_from_code(fbuser, phrase_words)
    elif input_type == "QR_invalid":                    response = answer_builder.get_text_response_qrinvalid(fbuser)        
    elif input_type == "See_past_purchases":            response = answer_builder.get_past_scanned_qrs(fbuser)
    elif input_type == "Insult":                        response = answer_builder.get_text_response_insult(fbuser)
    elif input_type == "Not_understood":                response = answer_builder.get_not_understood_response(fbuser)

    return response


def get_highest_priority_word(phrase_words):

    
    input_ranking = [1,2,3,4,5]

    array_input_numbers = []

    for word in phrase_words:        
        if word in list(input_words.Word):
            new_input_number = input_words.Type.loc[(input_words.Word == word)]
            array_input_numbers.append(int(new_input_number.iloc[0]))    

    if len(array_input_numbers) < 1:
        array_input_numbers.append(5)
        
    #We only select the input corresponding to the highest ranking
    for i in input_ranking:
        if i in array_input_numbers:
            input_number = i
            break
    
    #From the input number we obtain the input type
    input_type = input_meanings.Type.loc[(input_meanings.Number == input_number)]
    input_type = input_type.iloc[0]

    return input_type
