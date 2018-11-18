from flask import g, redirect, url_for, \
     render_template, render_template_string
from app import mail, app
from flask_mail import Message
from takeabeltof.utils import printException, cleanRecordID, looksLikeEmailAddress

def send_message(to_address_list=None,**kwargs):
    """Send an email with the parameters as:
        to_address_list=[list of tuples (recipient name,recipient address)]=None
        
        If the to_address_list is not provided, mail will be sent to the admin
        
        -- all templates must use 'context' as their only context variable
        **kwargs:
            context = {a dictionary like object with data for rendering all emails} = {}
            body = <text for body of email> = None
            body_text_is_html = <True | False> = False
            text_template=<template to render as plain text message> = None
            html_template=<template to render as html message> = None
            subject=<subject text (will be rendered with the current context>)>= a default subject
            subject_prefix=<some text to prepend to the subject: = ''
            from_address=<from address> = app.config['MAIL_DEFAULT_ADDR']
            from_sender=<name of sender> = app.config['MAIL_DEFAULT_SENDER']
            reply_to_address=<replyto address> = from_address
            reply_to_name=<name of reply to account> = from_sender
            
        On completion returns a tuple of:
            success [True or False]
            message "some message"
    """
    context = kwargs.get('context',{})
    body = kwargs.get('body',None)
    body_is_html = kwargs.get('body_is_html',None)
    text_template = kwargs.get('text_template',None)
    html_template = kwargs.get('html_template',None)
    subject_prefix = kwargs.get('subject_prefix','')
    from_address = kwargs.get('from_address',app.config['MAIL_DEFAULT_ADDR'])
    from_sender = kwargs.get('from_address',app.config['MAIL_DEFAULT_SENDER'])
    reply_to = kwargs.get('reply_to',from_address)
    subject = subject_prefix + ' ' +kwargs.get('subject','A message from {}'.format(from_sender))
    
    admin_addr = app.config['MAIL_DEFAULT_ADDR']
    admin_name = app.config['MAIL_DEFAULT_SENDER']
    
    
    if not text_template and not html_template and not body:
        mes = "No message body was specified"
        printException(mes,"error")
        return (False, mes)
        
    if not to_address_list or len(to_address_list) == 0:
        #no valid address, so send it to the admin
        to_address_list = [(admin_name,admin_addr),]
        
        
    with mail.record_messages() as outbox:
        sent_cnt = 0
        err_cnt = 0
        err_list = []
        result = True
        for who in to_address_list:
            #import pdb;pdb.set_trace()
            name = ""
            address = ""
            body_err_head = ""
            if type(who) is tuple:
                name = who[0]
                if len(who) > 1:
                    address = who[1]
            else:
                address = who #assume its a str
                
            if not looksLikeEmailAddress(address) and looksLikeEmailAddress(name):
                # swap values
                temp = address
                address = name
                name = temp
            if not looksLikeEmailAddress(address):
                # still not a good address...
                address = admin_addr
                name = admin_name
                if not body:
                    body = ""
                    
                body_err_head = "Bad Addres: {}\r\r".format(who,)
                
            subject = render_template_string(subject.strip(),context=context)
            #Start a message
            msg = Message( subject,
                          sender=(from_sender, from_address),
                          recipients=[(name, address)])
    
            #Get the text body verson
            if body:
                if body_is_html:
                    msg.html = render_template_string("{}{}".format(body_err_head,body,), context=context)
                else:
                    msg.body = render_template_string("{}{}".format(body_err_head,body,), context=context)
            if html_template:
                msg.html = render_template(html_template, context=context)
            if text_template:
                msg.body = render_template(text_template, context=context) 
            
            msg.reply_to = reply_to
           

            try:
                mail.send(msg)
                sent_cnt += 1
            except Exception as e:
                mes = "Error Sending email"
                printException(mes,"error",e)
                err_cnt += 1
                err_list.append(who,mes,)

        # End Loop
        if sent_cnt == 0:
            mes = "No messages were sent."
            result = False
        else:
            mes = "{} messages sent successfully.".format(sent_cnt)
        if err_cnt > 0:
            mes = mes + " {} messages had errors.\r\r{}".format(err_cnt,err_list)
            
        return (result, mes)
            
            
            
def email_admin(subject=None,message=None):
    """
        Shortcut method to send a quick email to the admin
    """
    if subject == None and message != None:
        # assume the subject is really the message
        message = subject
        subject = None
        
    if subject == None:
        subject = "An alert was sent from {}".format(app.config['SITE_NAME'])
        
    if message == None:
        message = "An alert was sent from {} with no message...".format(app.config['SITE_NAME'])
        
    return send_message(
            None,
            subject=subject,
            body = message,
            )
        
        
def alert_admin(subject=None,message=None):
    # just an alias to email admin
    # usually just ignore the return
    return email_admin(subject,message)
    
    