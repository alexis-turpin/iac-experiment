import requests
import initialization_handler


class Home(initialization_handler.InitializationHandler):
    """Home Handler

    Only implement the GET method at root level. Mainly used to keep
    track of servers involved in each queries.
    """
    def get(self):
        """Get server info by a query at root level.

        Returns:
            local IP4 if hosted on AWS, error message if not.
        """
        try:
            url = "http://169.254.169.254/latest/meta-data/local-ipv4"
            local_ip = requests.get(url).text
        except Exception as e:
            local_ip = "Not AWS hosted" + str(e)
        self.write({"api-ip": local_ip})
