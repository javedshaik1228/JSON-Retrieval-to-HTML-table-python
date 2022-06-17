# Modified from http://rndwww.nce.amadeus.net/grok/xref/ER/errorviewer_webapp/errorviewer/clients/alfv3_controller.py
# Customized parts have been highlighted by CUSTOM_HRE comments

# Note: pseudo-official script referenced from documentation (https://rndwww.nce.amadeus.net/confluence/x/fbHZAw)
# is here https://rndwww.nce.amadeus.net/git/projects/PYF/repos/alf/browse/alf.py

"""
Basic controller to call ALFv3 webservices
Contribution from PNR-SCS Team - 2015
"""


import urllib
import time
import urllib2
import json
import base64
# CUSTOM_HRE: disabled
#from errorviewer import settings
# CUSTOM_HRE: added
import sys


MODE_PROD = 0
MODE_TEST = 1
HTTP_METHOD_GET = 0
HTTP_METHOD_POST = 1
DEFAULTS = {
    'types': ["SI_MSG", "BE", "FE"],
    'duration': "PT1M",
    'fileNamePattern': []
}


class AlfController(object):
    """
    The ALF Controller
    See example usage at bottom of the file
    Documentation of the webservices:
    https://rndwww.nce.amadeus.net/confluence/display/AIOLSI/How+to+use+the+ALF+API
    """

    # CUSTOM_HRE: disabled
    '''
    def __init__(self):
        """
        Instantiate the controller
        """
        if settings.ENV.env in [settings.ENVIRONMENT.PROD, settings.ENVIRONMENT.TEST]:
            self._url = "http://alfapv01.os.amadeus.net:8080/"  # prod instance
        else:
            self._url = "http://alfatv02.os.amadeus.net:8882/"  # test instance
        self.user = settings.ENV.wa_user
        self.password = settings.ENV.wa_pwd
        self.login()
        self.topology = self._auth_request("topology/obe/", {}, HTTP_METHOD_GET)
    '''

    # CUSTOM_HRE: customized constructor for accepting input parameters + hardcoded ALFv3 URL
    def __init__(self, wa_user, wa_pwd):
        """
        Instantiate the controller
        """
        self._url = "https://loggingfacility.amadeus.com/v3/"  # prod instance
        self.user = wa_user
        self.password = wa_pwd
        self.topology = None

        self.login()

    def _auth_request(self, webservice, data, method=HTTP_METHOD_GET, debug=False):
        """
        Helper for HTTP GET/POST authenticated request
        """

        urlreq = self._url + webservice
        if method == HTTP_METHOD_GET:
            urlreq = urlreq + '?' + urllib.urlencode(data)

        request = urllib2.Request(urlreq)
        auth = base64.b64encode('%s:%s' % (self.user, self.password))
        request.add_header("Authorization", "Basic %s" % auth)

        if debug:
            print(method)
            print(urlreq)
            print(data)

        try:
            answer = None
            if method == HTTP_METHOD_GET:
                answer = urllib2.urlopen(request).read()
            elif method == HTTP_METHOD_POST:
                request.add_header('content-type', "application/json")
                params = json.dumps(data)
                answer = urllib2.urlopen(request, params).read()
            json_answer = json.loads(answer) if answer is not None else None
        except urllib2.HTTPError as exception:
            print(exception.read())
            json_answer = None
        return json_answer

    def login(self):
        """
        Log into ALF
        """
        data = {
            'username': self.user,
            'password': self.password
        }
        result = self._auth_request("auth/isAuthenticated", data, HTTP_METHOD_GET)
        if not result['loggedIn']:
            result = self._auth_request("auth/login", data, HTTP_METHOD_POST)
        print('login result=',result)
        return result

    def get_application_full_name(self, application, phase, peak=None):
        """
        Rely on ALF topology service to compute the correct application name
        Example: AML peak 1 is "AML" while LOY peak 1 is "LOY_PK1"
        input parameter 'peak' must be in the form "PK1"
        """
        if self.topology is None:
            self.topology = self._auth_request("topology/obe", {}, HTTP_METHOD_GET)
        application_list = []
        tentative_name = application.upper() + '_' + peak.upper() if peak is not None else ''
        if "phases" in self.topology.keys():
            # Get application list for given phase
            for current_phase_data in self.topology["phases"]:
                if current_phase_data.get("phase", "") == phase.upper():
                    application_list = current_phase_data.get("applications", [])
                    break
            # Check if the application is suffixed for this phase
            for app in application_list:
                if application.upper() in app.get("app", {}).get("id", ""):
                    if tentative_name == app.get("app", {}).get("id", ""):
                        return tentative_name

        return application.upper()

    def start_search(self, data):
        """
        Trigger a new search

        example:
            data = {
                'phase': 'PDT',
                'applications': ['CPL'],
                "startTime": '2015-05-18T08:20:33.900881Z',
                "pattern": 'CsxServerContext',
                "types": ["BE"],
                "fileNamePattern": "PXA_Retrieve",
                "patternIndex": "DcxId"
            }

        Documentation for API:
        https://rndwww.nce.amadeus.net/confluence/display/AIOLSI/How+to+use+the+ALF+API
        Documentation for duration and startTime keys:
            https://docs.oracle.com/javase/8/docs/api/java/time/Duration.html#parse-java.lang.CharSequence-
        """

        # Presence is mandatory for these keys
        for mandatory_key in ['phase', 'applications', 'pattern', 'startTime']:
            if mandatory_key not in data.keys():
                return None

        # These keys must not be None or Empty
        for valid_key in ['phase', 'startTime']:
            if valid_key is None or len(data[valid_key]) == 0:
                return None

        # Special format for startTime - ALF needs a ending Z
        if data['startTime'][-1:] != 'Z':
            data['startTime'] += 'Z'

        # Fill optional keys with defaults
        for optional_key in DEFAULTS.keys():
            if optional_key not in data.keys():
                data[optional_key] = DEFAULTS[optional_key]

        result = self._auth_request("rest/search/start", data, HTTP_METHOD_POST)
        return result

    def get_search_status(self, searchid):
        """
        Get status of a search

        """
        data = {'searchId': searchid}
        status = self._auth_request("rest/info/status", data, HTTP_METHOD_GET)
        return status

    def get_search_details(self, searchid):
        """
        Get full information about a search (details, tasks)
        """
        data = {'searchId': searchid}
        info = self._auth_request("rest/info/search", data, HTTP_METHOD_GET)
        tasks = self._auth_request("rest/info/tasks", data, HTTP_METHOD_GET)
        return {'info': info, 'tasks': tasks}

    def has_search_started(self, searchid):
        """
        Quick helper to check if a search has really started (true) or not (false)
        """
        status = self.get_search_status(searchid)
        return status['taskScheduled'] > 0

    def has_search_finished(self, searchid):
        """
        Quick helper to check if a search has finished (true) or not (false)
        """
        details = self.get_search_details(searchid)
        return details['info']['status'] == 'COMPLETE'

    def get_search_result(self, searchid):
        """
        Get the result of a search
        """
        data = {'searchId': searchid, 'limit': 999999, 'offset': 0}
        result = self._auth_request("rest/search/result", data, HTTP_METHOD_GET)
        return result

    def get_alf_url(self, searchid):
        """
        Get the ALF url to check the result of a search
        """
        return self._url + '#/log-viewer/search-id/' + str(searchid)

    def start_search_and_get_results(self, data, poll_time=1, max_polls=15):
        """
        Trigger a search, wait for result, and returns the result
        "poll_time" argument permits to define the sleeping time (in seconds) between two status polls
        """
        trigger_result = self.start_search(data)
        searchid = trigger_result['searchId'] if trigger_result is not None else None

        if searchid is not None:
            # Waiting search to start
            poll_counter = 0
            while (not self.has_search_started(searchid)) and (poll_counter < max_polls):
                time.sleep(poll_time)
                poll_counter += 1

            if not self.has_search_started(searchid):
                print("Search could not start")
                return None

            # Waiting search to finish
            poll_counter = 0
            while (not self.has_search_finished(searchid)) and (poll_counter < max_polls):
                time.sleep(poll_time)
                poll_counter += 1

            if not self.has_search_finished(searchid):
                print("Search could not finish")
                return None

        else:
            print("Search could not be triggered")
            return None

        return self.get_search_result(searchid)

    def start_search_and_get_url(self, data, error_url=None):
        """
        Trigger a search, and returns the url to view it in ALF
        "poll_time" argument permits to define the sleeping time (in seconds) between two status polls
        "error_url" defines the url to return in case of error (default is ALF search page)
        """
        trigger_result = self.start_search(data)
        searchid = trigger_result['searchId'] if trigger_result is not None else None
        if searchid is not None:
            return self.get_alf_url(searchid)
        elif error_url is not None:
            return error_url
        else:
            self.get_alf_url("")

    def get_logserver_name(self, obe, phase, peak=None, log_type='error'):
        """
        Get the name of a logserver where logs are located
        e.g: http://alfapv01.os.amadeus.net:8080/topology/logservers/?phase=des&application=son_pk3&logType=error
        """
        application = self.get_application_full_name(obe, phase, peak)
        data = {'phase': phase, 'application': application, 'logType': log_type}
        result = self._auth_request("topology/logservers/", data, HTTP_METHOD_GET)
        return result


if __name__ == '__main__':
    # CUSTOM_HRE perform login as default action
    if (len(sys.argv) == 3):
        AlfController(sys.argv[1], sys.argv[2])
    else:
        print("parameters failure")

"""
    print AlfController().start_search_and_get_results({
        'phase': 'PDT',
        'applications': ['CPL'],
        "startTime": '2015-05-18T08:20:33.900881',
        "pattern": 'CsxServerContext',
        "types": ["BE"],
        "fileNamePattern": "PXA_Retrieve"})
"""
