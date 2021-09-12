from flask import request, url_for


def previous_page(default: str = 'home'):
    return request.referrer or \
           url_for(default)

# original code: https://stackoverflow.com/questions/14277067/redirect-back-in-flask
