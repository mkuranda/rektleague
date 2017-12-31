import requests, json

api_key = 'RGAPI-4d17443e-45b5-4599-bfaa-71f39e02eb61'

url_base = 'https://na1.api.riotgames.com'


class RiotApiError(Exception) :
    """Raised when we receive an error status code from the Riot API"""
    pass

class RiotRateLimitExceeded(RiotApiError) :
    """Raised when we receive 429 (Rate Limit Exceeded)"""
    pass

class RiotBadRequest(RiotApiError) :
    """Raised when we receive a 400 (Bad Request)"""
    pass

class RiotForbidden(RiotApiError) :
    """Raised when we receive a 403 (Forbidden)"""
    pass

class RiotNotFound(RiotApiError) :
    """Raised when we receive a 404 (Not Found)"""
    pass

class RiotUnsupportedMediaType(RiotApiError) :
    """Raised when we receive a 415 (Unsupported Media Type)"""
    pass

class RiotInternalServerError(RiotApiError) :
    """Raised when we receive a 500 (Internal Server Error)"""
    pass

class RiotServiceUnavailable(RiotApiError) :
    """Raised when we receive a 503 (Service Unavailable)"""
    pass


riot_errors = {
    400: RiotBadRequest,
    403: RiotForbidden,
    404: RiotNotFound,
    415: RiotUnsupportedMediaType,
    429: RiotRateLimitExceeded,
    500: RiotInternalServerError,
    503: RiotServiceUnavailable
}


class RiotRequester :

    def __init__(self, request_base):
        self.api_key = api_key
	self.request_base = url_base + request_base
	self.tag_list = []

    def add_tag(self, tag):
	self.tag_list.append(tag)

    def request(self, request_url):
        url = self.request_base + request_url + "?api_key=" + self.api_key
	for tag in self.tag_list:
	    url += "&tags=" + tag
	r = requests.get(url).json()
	if 'status' in r:
	    raise riot_errors[r['status']['status_code']]
	return r
        
