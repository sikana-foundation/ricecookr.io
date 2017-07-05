#!/usr/bin/python
import requests
import json

class SikanaApi:
    """
    Class to get data from Sikana's API
    """
    base_url = "https://www.sikana.tv/"
    client_id = None
    secret = None
    token = None

    def __init__(self, client_id, secret, base_url=None):
        self.base_url = base_url or "https://www.sikana.tv/"
        self.client_id = client_id
        self.secret = secret
        self.token = self.__build_token(client_id, secret)

    def __build_token(self, client_id, secret):
        """
        Private method
        Builds an OAuth access token and returns it
        """
        build_token_url = self.base_url + "oauth/v2/token"
        data = {
            'grant_type':'client_credentials',
            'client_id':client_id,
            'client_secret':secret}
        response = requests.post(build_token_url, data=data)
        if response.status_code != 200:
            raise Exception("POST /oauth/v2/token returned code " + format(response.status_code) + ": " + format(response.text))
        resp = response.json()
        return resp['access_token']

    def get_languages(self):
        """
        Returns a Sikana's list of languages
        """
        url = self.base_url + "api/languages?access_token=" + self.token
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("GET /api/languages returned code " + format(response.status_code) + ": " + format(response.text))
        return response.json()

    def get_categories(self, language_code):
        """
        Returns Sikana's categories for a given language
        """
        url = self.base_url + "api/categories/languages/" + language_code + "?access_token=" + self.token + "&version=2"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("GET /api/categories/languages/" + language_code + " returned code " + format(response.status_code) + ": " + format(response.text))
        return response.json()

    def get_programs(self, language_code, category_name):
        """
        Returns Sikana's programs for given language and category
        """
        url = self.base_url + "api/programs/categories/" + category_name + "/languages/" + language_code + "?access_token=" + self.token + "&version=2"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("GET /api/programs/categories/" + category_name + "/languages/" + language_code + " returned code " + format(response.status_code) + ": " + format(response.text))
        return response.json()

    def get_program(self, language_code, name_canonical):
        """
        Returns the prograrm with given name canonical for the given language
        """
        url = self.base_url + "api/programs/" + name_canonical + "/languages/" + language_code + "?access_token=" + self.token + "&version=2"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("GET /api/programs/" + name_canonical + "/languages/" + language_code + " returned code " + format(response.status_code) + ": " + format(response.text))
        return response.json()

    def get_video(self, language_code, name_canonical):
        """
        Returns the video with the asked name canonical for the given language
        """
        url = self.base_url + "api/videos/" + name_canonical + "/languages/" + language_code + "?access_token=" + self.token + "&version=2"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("GET /api/videos/" + name_canonical + "/languages/" + language_code + " returned code " + format(response.status_code) + ": " + format(response.text))
        return response.json()
