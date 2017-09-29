import pandas as pd
import response_json_generator, datetime, calendar
from pprint import pprint
from models import FacebookUser, QRCode, Scan

#import product database

nerdemoji = u'\U0001F913'
thinkemoji = u'\U0001F914'
cameraemoji = u'\U0001F4F8'
laughemoji = u'\U0001F602'
happyemoji = u'\U0001F60A'
bookemoji = u'\U0001F4DA'
angryemoji = u'\U0001F620'


situation = pd.read_csv('./fb_chatbot/static/situation.csv')

def get_salute_text(fbuser):
    fbid = fbuser.fb_id    
    output_wording = "Hi " + str(fbuser.first_name) + "! I am your personal QR bot reader " + nerdemoji
    response = response_json_generator.response_msg(fbid,output_wording)    
    return response

def get_salute_image(fbuser):
    fbid = fbuser.fb_id    
    output_wording = "Send me a "+cameraemoji+ " of a QR code to start!"
    response = response_json_generator.response_button_start(fbid,output_wording)    
    return response


def get_help(fbuser):
    fbid = fbuser.fb_id    
    output_wording = "I am here to help! " +happyemoji +happyemoji+"\nTo use me, just send me a picture of a QR code and I will read it for you.\n\nI will also store them securely for you in case you need them again in the future!"
    response = response_json_generator.response_button_help(fbid,output_wording)
    return response


#situations 8 (qrinvalid) and 5 (insult)
def get_text_response_insult(fbuser):
    fbid = fbuser.fb_id    
    output_wording = "I found that offensive! Please respect me, I am a bot but I have feelings ok!? " + angryemoji + angryemoji
    response = response_json_generator.response_msg(fbid, output_wording)
    return response

def get_text_response_qrinvalid(fbuser):
    fbid = fbuser.fb_id    
    output_wording = "Oh dear! I could not identify that as a valid QR code. Please try again and make sure the picture is as clear as possible!"
    response = response_json_generator.response_msg(fbid, output_wording)
    return response

def get_not_understood_response(fbuser):
    fbid = fbuser.fb_id
    situation_type = 6
    output_wording = "I am afraid I did not understand you ... " + thinkemoji+ "  Hey, maybe I am dumb, but can you read QR codes alone? " + laughemoji + laughemoji + laughemoji
    response = response_json_generator.response_button_other(fbid, output_wording)
    return response

def get_qr(fbuser, callback):
    fbid = fbuser.fb_id
    qr_data = callback[8:]
    sentence_first_part = "Great! I got this information from the QR code:\n\n"

    if qr_data[:6] == "smsto:":
        qr_style = "SMS"
        qr_data = qr_data[6:]
        len_number = qr_data.find(':')
        phone_number = qr_data[:len_number]
        message = qr_data[len_number+1:]
        sentence_second_part = " - Type: SMS\n - Phone Number: " + str(phone_number) + "\n - Message: " + str(message)
        output_wording = sentence_first_part + sentence_second_part
        url = "sms:"+phone_number
        url = url.replace(" ","%20")
        url = url.replace("\n","%0A")
        response = response_json_generator.response_sms(fbid, output_wording)
        data_saved = sentence_second_part
        url_saved = url

    elif qr_data[:11] == "begin:vcard":
        qr_style = "Contact Card"
        output_wording = "Sorry, this is a Contact Card and I still do not support this type of QRs."
        response = response_json_generator.response_msg(fbid,output_wording)    
        data_saved = qr_data
        url_saved = "Not supported yet"

    elif qr_data[:7] == "matmsg:":
    
        qr_style = "Email"
        qr_data = qr_data[7:]
        url = 'mailto:'
        sentence_second_part = " - Type: Email"
        
        start_email = qr_data.find('to:')
        end_email = qr_data.find(';',start_email)
        if start_email != -1:
            email = qr_data[start_email+3:end_email]
            url = url + email
            sentence_second_part = sentence_second_part + "\n - To: " + str(email)
            
        start_subject = qr_data.find('sub:')
        end_subject = qr_data.find(';',start_subject)
        if start_subject != -1:
            subject = qr_data[start_subject+4:end_subject]
            url = url + "?subject=" + subject
            sentence_second_part = sentence_second_part + "\n - Subject: " + str(subject)
            
        start_body = qr_data.find('body:')
        end_body = qr_data.find(';',start_body)
        if start_body != -1:
            body = qr_data[start_body+5:end_body]
            url = url + "&body=" + body
            sentence_second_part = sentence_second_part + "\n - Body: " + str(body)
        
        start_cc = qr_data.find('cc:')
        end_cc = qr_data.find(';',start_cc)
        if start_cc != -1:
            cc = qr_data[start_cc+3:end_cc]
            url = url + "&cc=" + cc
            sentence_second_part = sentence_second_part + "\n - CC: " + str(cc)
        
        start_bcc = qr_data.find('bcc:')
        if start_bcc != -1:
            bcc = qr_data[start_bcc+4:]
            url = url + "&bcc=" + bcc
            sentence_second_part = sentence_second_part + "\n - BCC: " + str(bcc)

        output_wording = sentence_first_part + sentence_second_part

        # %20 = space in mailto
        # %0A = new line.
        url = url.replace(" ","%20")
        url = url.replace("\n","%0A")
        response = response_json_generator.response_email(fbid, output_wording)
        data_saved = sentence_second_part
        url_saved = url

    elif (qr_data[len(qr_data)-4:] in [".jpg", ".png", ".svg"]) or (qr_data[len(qr_data)-5:] == ".jpeg"):
        qr_style = "Image"
        output_wording = "This is the image linked to that QR code!"
        response = response_json_generator.response_image(fbid,output_wording,qr_data)
        data_saved = "A link to an image"
        url_saved = qr_data   

    elif ("http://" in qr_data) or ("https://" in qr_data) or ("www." in qr_data) or (".com" in qr_data) or (".us" in qr_data) or (".gov" in qr_data) or (".es" in qr_data) or (".net" in qr_data) or (".org" in qr_data):
        qr_style = "URL"
        sentence_second_part = " - Type: URL\n - Link: " + str(qr_data) + "\n\nDo you want to open it?"
        output_wording = sentence_first_part + sentence_second_part
        response = response_json_generator.response_website(fbid, output_wording, qr_data)
        data_saved = "An URL link"
        url_saved = qr_data

    else:
        pprint("It is text")
        qr_style = "Text"
        sentence_second_part = " - Type: Text\n - Message: " + str(qr_data)
        output_wording = sentence_first_part + sentence_second_part
        response = response_json_generator.response_msg(fbid, output_wording)
        data_saved = sentence_second_part
        url_saved = ""

    pprint(url_saved)
    qrcode = QRCode.objects.create(data=data_saved, style=qr_style, url=url_saved)
    scan = Scan.objects.create(fbuser=fbuser, qrcode=qrcode)
    qrcode.save()
    scan.save()
    pprint(response)

    return response



def get_past_scanned_qrs(fbuser):

    fbid = fbuser.fb_id    
    past_scans = Scan.objects.filter(fbuser=fbuser).order_by('-date')

    #TODO
    if len(past_scans) >= 1:
        situation_type = 3
        output_wording="Hey "+ str(fbuser.first_name) + ", I looked in the archives and found this "+bookemoji+" :\n\n"
        for scan in past_scans:
            output_wording = output_wording + '\nDate: '+str(scan.date.strftime("%Y-%m-%d, %H:%M:%S")) + '\n - Type: '+scan.qrcode.style+'\n - URL: '+ scan.qrcode.url + '\n\n'
    
        if len(output_wording) > 640:
            output_wording = output_wording[:636] + ' ...'
        response = response_json_generator.response_msg(fbid, output_wording)

    else:
        situation_type = 4

        output_wording = "Oh dear! It seems you did not scan QRs before. Send me a pic of a QR you want me to read"
        response = response_json_generator.response_msg(fbid, output_wording)

    return response





