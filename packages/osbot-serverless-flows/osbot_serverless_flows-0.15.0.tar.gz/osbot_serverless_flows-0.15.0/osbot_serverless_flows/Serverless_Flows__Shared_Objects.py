from osbot_serverless_flows.aws.s3.S3_DB__Flows import S3_DB__Flows
from osbot_utils.base_classes.Type_Safe         import Type_Safe


class Serverless_Flows__Shared_Objects(Type_Safe):

    def s3_db_flows(self):
        s3_db_flows = S3_DB__Flows()
        s3_db_flows.setup()             # will create buckey if needed
        return s3_db_flows

serverless_flows__shared_objects = Serverless_Flows__Shared_Objects()