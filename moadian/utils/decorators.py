from datetime import datetime


def token(view_func):
    def wrapper(self, *args, **kwargs):
        now_timestamp = int((datetime.now().timestamp() * 1000))
        if (self.token and self.expires_in <= now_timestamp) or not self.token:
            res = self.get_token()
            self.token = res.get("token")
            self.expires_in = res.get("expires_in")
        return view_func(self, *args, **kwargs)

    return wrapper
