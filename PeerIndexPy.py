# -*- coding: utf-8 -*-


"""
A Python interface for the PeerIndex API.

To use this you need a PeerIndex API key which 
    you can get at: http://dev.peerindex.com/
    
This script is loosely based on the PyKlout script by 
    https://github.com/marcelcaraciolo
    
https://github.com/guidovo

"""

__author__ = 'Guido van Oorschot'
__version__ = '0.1'


import urllib
import httplib
import json
import urllib2

ERROR_STATUS = {
    # "200: "OK: Success", IS A GOOD STATUS
    202: "Accepted: Your request was accepted and the user was queued for processing.",
    401: "Not Authorized: either you need to provide authentication credentials, or the credentials provided aren't valid.",
    403: "Bad Request: your request is invalid, This is the status code returned if you've exceeded the rate limit or if you are over QPS.",
    404: "Not Found: either you're requesting an invalid URI or the resource in question doesn't exist (ex: no such user in our system).",
    500: "Internal Server Error: we did something wrong.",
    502: "Bad Gateway: returned if PeerIndex is down or being upgraded.",
    503: "Service Unavailable: the PeerIndex servers are up, but are overloaded with requests. Try again later.",
}


class PeerIndexError(Exception):
    def __init__(self, code, msg):
        super(PeerIndexError, self).__init__()
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '%i: %s' % (self.code, self.msg)


class PeerIndex(object):
    '''
    Parameters
    ----------
    api_key : string the PeerIndex API Key.

    '''
    API_URL = 'api.peerindex.net'

    def __init__(self, api_key):
        self._api_key = api_key

    def _remove_empty_params(self, params):
        '''
        Remove all unused parameters

        Parameters
        ----------
        params:  dict object
            A set of parameters key,value

        Returns
        --------
        The set of parameters as dict without empty parameters
        '''
        ret = {}
        for key in params:
            if not params[key] == None:
                ret[key] = params[key]

        return ret

    def make_api_call(self, url, query={}, body={}):
        '''
        Make the API Call to Peer Index

        Parameters
        ----------
        url: the url to call
        query: The GET parameters
        '''

        query = self._remove_empty_params(query)

        if 'api_key' not in query:
            query['api_key'] = self._api_key

        body = self._remove_empty_params(body)
        query_str = urllib.urlencode(query)
        body_str = urllib.urlencode(body)

        if len(query) > 0:
            if url.find('?') == -1:
                url = url + '?' + query_str
            else:
                url = url + '&' + query_str

        try:
            conn = httplib.HTTPConnection(self.API_URL)
            conn.request('GET', url)
            resp = conn.getresponse()
            data = resp.read()
            data = json.loads(data)
            if not data:
                raise ValueError(data)
                
    
        except httplib.HTTPException as err:
            msg = err.read() or ERROR_STATUS.get(err.code, err.message)
            raise PeerIndexError(err.code, msg)
        except ValueError:
            msg = 'Invalida data (probably a nonexisting userid): %s' % data
            raise PeerIndexError(0, msg)

        return data

    def lookup_userid(self, userid):
        """
        This method allows you to retrieve the user object

        Parameters
        ----------
        user: The username from whom fetching the scores

        Returns
        -------
        A dictionary with the returned data.

        """
        url = '/1/profile/show.json'

        if not userid:
            raise PeerIndexError(0, 'No User id given')

        if isinstance(userid, (list, tuple)):
            userid = ','.join(userid)

        query = {'id': userid}

        data = self.make_api_call(url, query)

        return data
