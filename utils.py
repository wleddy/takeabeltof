"""takeabeltof.utils
    Some utility functions
"""

from flask import g, render_template_string
from takeabeltof.date_utils import nowString
import linecache
import sys
import re
import random
import mistune # for Markdown rendering
import os


def cleanRecordID(id):
    """ return the integer version of id or else -1 """
    if id is None:
        return -1
    if type(id) is str: # or type(id) is unicode:
        if id.isdigit():
            # a negative number like "-1" will fail this test, which is what we want
            return int(id)
        else:
            return -1
            
    #already a number 
    return id
    
def looksLikeEmailAddress(email=""):
    """Return True if str email looks like a normal email address else False"""
    if type(email) is not str:
        return False
        
    return re.match(r"[^@]+@[^@]+\.[^@]+", email.strip())
    
def printException(mes="An Unknown Error Occured",level="error",err=None):
    from app import app
    exc_type, exc_obj, tb = sys.exc_info()
    debugMes = None
    if tb is not None:
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        try:
            debugMes = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
        except ValueError:
            debugMes = "Could not get error location info."
            
    if level=="error" or app.config["DEBUG"]:
        #always log errors
        if debugMes:
            app.logger.error(nowString() + " - " + debugMes)
        app.logger.error(nowString() + "   " + mes)
        if err:
            app.logger.error(nowString() + "    " + str(err))
        
    if app.config["DEBUG"]:
        if debugMes:
            mes = mes + " -- " +debugMes
        return mes
    else:
        return mes
    
    
def render_markdown_for(source_script,module,file_name):
    """Try to find the file to render and then do so"""
    from app import app
    
    rendered_html = None
    # use similar search approach as flask templeting, root first, then local
    # try to find the root templates directory
    markdown_path = os.path.dirname(os.path.abspath(__name__)) + '/templates/{}'.format(file_name)
    if not os.path.isfile(markdown_path):
        # look in the templates directory of the calling blueprint
        markdown_path = os.path.dirname(os.path.abspath(source_script)) + '/{}/{}'.format(module.template_folder,file_name)
    if os.path.isfile(markdown_path):
        f = open(markdown_path)
        rendered_html = f.read()
        f.close()
        
        # treat the markdown as a template and render url_for and app.config values
        rendered_html = render_template_string(rendered_html)
        
        rendered_html = render_markdown_text(rendered_html)
    elif app.config['DEBUG']:
        rendered_html = "Because you're in DEBUG mode, you should know that there was no file found at {} called from {}".format(file_name,source_script,)

    return rendered_html


def render_markdown_text(text_to_render):
    return mistune.markdown(text_to_render)
      