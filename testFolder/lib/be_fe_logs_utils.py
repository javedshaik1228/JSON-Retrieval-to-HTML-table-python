# Initial inspired from http://rndwww.nce.amadeus.net/grok/xref/ER/errorviewer_webapp/errorviewer/be_fe_logs_utils.py
# Doc here https://rndwww.nce.amadeus.net/confluence/pages/viewpage.action?pageId=64598397#HowtousetheALFAPI?-Startasearch

"""Main module for BE/FE log handling
Module for non error log actions
"""

import datetime

# CUSTOM_HRE: customized
#import settings
#from errorviewer.clients import alfv3_controller
from alfv3_controller import AlfController
from optparse import OptionParser

# CUSTOM_HRE: taken from http://rndwww.nce.amadeus.net/grok/xref/ER/errorviewer_webapp/errorviewer/settings.py
# BE/FE log settings
BE_LOG_TIME_RANGE = 60  # in seconds


class LogHandler(object):
    """Handles the logs other than error logs

    Attributes:
        _log_dict: a dict representing a log line
                    sample:
                    {'backend': 'GHI_Store_GHI',
                     'batch': None,
                     'ctxserv': None,
                     'day': '31',
                     'duwrapper': None,
                     'file': 'InboundEdifactMessageImpl.cpp',
                     'frontend': None,
                     'host': 'obeaa201',
                     'hours': '08',
                     'instance': '5',
                     'line': '266',
                     'minutes': '25',
                     'module': '',
                     'month': '05',
                     'name': 'kOTFError_DecodingError',
                     'nb': '9',
                     'pfx': '07DSLURWIK0001',
                     'pid': '256413',
                     'seconds': '56',
                     'severity': 'ERROR',
                     'type': 'MDW',
                     'year': '2013'}
    """

    def __init__(self, log_dict, phase, iUname, iPwd):
        self._cmd_params = log_dict
        self._phase = phase
        self._alf_controller = AlfController(iUname, iPwd)


    def _build_data(self, input_data):
        """
        Internal method to factorize construction of data to be sent to ALF webservices
        ! Should not be called directly !
        Returns:
            the built data
        """
        timestamp = datetime.datetime(int(self._cmd_params['year']),
                                      int(self._cmd_params['month']),
                                      int(self._cmd_params['day']),
                                      int(self._cmd_params['hours']),
                                      int(self._cmd_params['minutes']),
                                      int(self._cmd_params['seconds']))

        timestamp -= datetime.timedelta(seconds=BE_LOG_TIME_RANGE)
        if 'pfx' in self._cmd_params and self._cmd_params['pfx'] is not None:
            pattern = self._cmd_params['pfx'].split('|')[0].split(',')[0].strip()
        else:
            pattern = ''

        data = {
            'phase': self._phase,
            "startTime": timestamp.isoformat(),
            "pattern":pattern,
            "duration" : "PT"+str(2*BE_LOG_TIME_RANGE)+"S",
        }

        for k in input_data.keys():
            data[k] = input_data[k]

        return data

    def _get_logs_url(self, input_data):
        """
        Triggers a search in ALF and send back url
        ! Should not be called directly, use get_be_logs or get_fe_logs instead !
        Returns:
            the ALF URL to check the results
        """
        data = self._build_data(input_data)
        return self._alf_controller.start_search_and_get_url(data)


    def get_be_logs_url(self):
        """
        Triggers a search in BE logs in ALF
        Returns:
            the ALF URL to check the results
        """
        input_data = {
            "types": ["BE"],
            "fileNamePattern": self._cmd_params['backend'][:-4],
            "applications": ["HOS"]
        }
        return self._get_logs_url(input_data)


    def get_fe_logs_url(self):
        """
        Triggers a search in BE logs in ALF
        Returns:
            the ALF URL to check the results
        """
        input_data = {
            "types": ["FE"],
            "fileNamePattern": "",
            "applications": ["HOS"]
        }
        return self._get_logs_url(input_data)


    def get_si_logs_url(self):
        """
        Triggers a search in BE logs in ALF
        Returns:
            the ALF URL to check the results
        """
        input_data = {
            "types": ["SI_MSG"],
            "fileNamePattern": "",
            "applications": ["SIALT","SICIF","SIDCS","SIDMZ","SIHTH","SITN","SIWEB","SIYBS"]
        }
        return self._get_logs_url(input_data)



'''
CUSTOM_HRE : bypass web.py
'''
kLogBackEnd = 'BE'
kLogFrontEnd = 'FE'
kLogSI = 'SI'

# Build groupdict as expected by LogHandler
def buildGroupdict(iPhase, iDatetimeStr, iPattern, iUname, iPwd):
    aDate = datetime.datetime.strptime(iDatetimeStr, "%Y-%m-%d_%H:%M:%S")
    groupdict = {
        'backend': '', # get all the backends
        'day': aDate.day,
        'hours': aDate.hour,
        'minutes': aDate.minute,
        'month': aDate.month,
        'pfx': iPattern, # set our pattern as PFX to make it considered
        'seconds': aDate.second,
        'year': aDate.year
    }

    return LogHandler(groupdict, iPhase, iUname, iPwd)


# CUSTOM_HRE
# Credentials shall be successfully tested before calling this script
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--datetime", help="datetime (e.g. 2017-03-06_10:05:03, remind the underscore!)")
    parser.add_option("-p", "--phase", help="the phase: {PDT, PRD, ...}")
    parser.add_option("-s", "--searchPattern", help="pattern to search")
    parser.add_option("-t", "--logType", help="log type to search {SI, BE, FE}")
    parser.add_option("-u", "--uname", help="login username")
    parser.add_option("-w", "--pwd", help="login password")
    (options, args) = parser.parse_args()

    iLogType = options.logType
    iPhase = options.phase
    iDatetime = options.datetime
    iPattern = options.searchPattern
    iUname = options.uname
    iPwd = options.pwd

    if not iDatetime or not iPhase or not iPattern or not iLogType or not iUname or not iPwd:
        assert False, "Missing mandatory option(s): all of them are mandatory"

    handler = buildGroupdict(iPhase, iDatetime, iPattern, iUname, iPwd)
    if (iLogType == kLogBackEnd):
        result_url = handler.get_be_logs_url()
    elif (iLogType == kLogFrontEnd):
        result_url = handler.get_fe_logs_url()
    elif (iLogType == kLogSI):
        result_url = handler.get_si_logs_url()

    if result_url is None:
        print('Could not retrieve the logs')
    else:
        print("{'url': " + result_url + "}")