from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

from osbot_serverless_flows.Serverless_Flows__Server_Config import serverless_flows__server_config
from osbot_serverless_flows.utils.Version import version__osbot_serverless_flows

ROUTES__EXPECTED_PATHS__INFO = [ '/info/ping'         ,
                                 '/info/server-config',
                                 '/info/version'      ]

class Routes__Info(Fast_API_Routes):
    tag : str = 'info'

    def ping(self):
        return {"pong": "42"}

    def server_config(self):
        return serverless_flows__server_config.json()

    def version(self):
        return { "version" : version__osbot_serverless_flows}

    def setup_routes(self):
        self.add_route_get(self.ping         )
        self.add_route_get(self.server_config)
        self.add_route_get(self.version      )
        return self