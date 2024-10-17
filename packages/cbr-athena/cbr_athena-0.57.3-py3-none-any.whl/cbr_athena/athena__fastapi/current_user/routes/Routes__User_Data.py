from fastapi                                        import Depends, Request, Security
from cbr_athena.athena__fastapi.CBR__Session_Auth   import cbr_session_auth, api_key_header
from cbr_shared.cbr_backend.users.DB_Users          import DB_Users
from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes


class Routes__User_Data(Fast_API_Routes):
    tag      : str = 'user-data'
    db_users : DB_Users

    def user_details(self, request: Request):
        return cbr_session_auth.session_data__from_cookie(request)

    def user_profile(self, request: Request):
        user_details = self.user_details(request)
        if user_details:
            user_id = user_details.get('data', {}).get('user_name')
            db_user = self.db_users.db_user(user_id)
            return db_user.user_profile()
        #return cbr_session_auth.session_data__from_cookie(request)

    def setup_routes(self):
        self.add_route_get(self.user_details)
        self.add_route_get(self.user_profile)
