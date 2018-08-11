#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module works with IBM Watson Personality Insights
The module supports caching of the results returned by the service

@author: vadim, iangow
"""

# %%

import hashlib
import json
import os
import sys

# importing custom modules
import config
import watson_developer_cloud.personality_insights_v3 as PI

# %%

class PersonalityInsights:
    '''
    :Description: A class for working with IBM Watson Personality Insights
    :Usage:
            pi = PersonalityInsights()
            json = pi.get_profile(text)
    :Note: Credentials to access the service are taken from config.py,
           which should be coppied from config.example.py
    '''

    def __init__(self):

        # creating the PersonalityInsightsV3 object
        print('Creating the Personality Insights object.')
        self.pi = PI.PersonalityInsightsV3(
            username=config.bluemix_pi_username,
            password=config.bluemix_pi_password,
            version=config.bluemix_pi_version,
            url=config.bluemix_pi_url
        )
        self.pi.set_default_headers({"x-watson-learning-opt-out": "1"})

    def get_profile(self, text):
        '''
        :param text: The text passed to the IBM Watson Personality Insights service
        :return: A dictionary containing the scores returned by the service
        '''
        # otherwise we call the Watson Personality Insights API
        # note that if the service cannot calculate scores for any reason
        # (such as too few words, for example), it raises an exception
        print('Obtaining Personality Insights scores from the service...')
        try:
            json_data = self.pi.profile(text,
                                        content_type = "text/plain;charset=utf-8",
                                        accept = "application/json",
                                        raw_scores = True,
                                        consumption_preferences = False
                                       )
        except Exception as e:
            print('! Error: ' + str(e))
            json_data = { 'error': str(e) }
            pass
        return json.dumps(json_data)

