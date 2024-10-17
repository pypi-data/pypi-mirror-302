from fastapi                                      import Depends, Request, Security
from cbr_athena.athena__fastapi.CBR__Session_Auth import cbr_session_auth, api_key_header
from osbot_fast_api.api.Fast_API_Routes           import Fast_API_Routes


class Routes__User_Data(Fast_API_Routes):
    tag = 'user-data'

    def user_details(self, request: Request):
        return cbr_session_auth.session_data__from_cookie(request)


    def setup_routes(self):
        self.add_route_get( self.user_details)
