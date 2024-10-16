from fastapi                                              import Request
from osbot_fast_api.api.Fast_API_Routes                   import Fast_API_Routes
from osbot_serverless_flows.flows.dev.Flow__Testing_Tasks import Flow__Testing_Tasks

ROUTES__EXPECTED_PATHS__DEV = ['/dev/flow-testing-tasks' ]

class Routes__Dev(Fast_API_Routes):
    tag : str = 'dev'

    async def flow_testing_tasks(self, request: Request):
        #
        try:
            post_data = await request.json()
        except Exception as error:
            post_data = {'error': str(error)}

        with Flow__Testing_Tasks() as _:
            flow_result = _.run(post_data).flow_return_value
        return dict(post_data=post_data, flow_result=flow_result)
        # return post_data
        #

    def setup_routes(self):
        self.add_route_post(self.flow_testing_tasks)