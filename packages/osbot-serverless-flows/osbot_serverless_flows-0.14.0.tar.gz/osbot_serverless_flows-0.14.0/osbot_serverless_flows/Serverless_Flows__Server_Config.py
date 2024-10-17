from osbot_utils.utils.Env import get_env
from osbot_utils.base_classes.Type_Safe import Type_Safe


DEFAULT__SERVERLESS_FLOWS__AWS_ACCOUNT_ID   = '0000111100001111'
ENV_NAME__SERVERLESS_FLOWS__USE_LOCAL_STACK = 'SERVERLESS_FLOWS__USE_LOCAL_STACK'

class Serverless_Flows__Server_Config(Type_Safe):
    aws_account_id  : str   = DEFAULT__SERVERLESS_FLOWS__AWS_ACCOUNT_ID
    use_local_stack : bool  = False

    def setup(self):
        self.use_local_stack = get_env(ENV_NAME__SERVERLESS_FLOWS__USE_LOCAL_STACK) == 'True' or self.use_local_stack
        self.aws_account_id  = get_env('AWS_ACCOUNT_ID')                                      or self.aws_account_id
        return self

    def reset(self):
        self.aws_account_id  = DEFAULT__SERVERLESS_FLOWS__AWS_ACCOUNT_ID
        self.use_local_stack = False
        return self

serverless_flows__server_config = Serverless_Flows__Server_Config()