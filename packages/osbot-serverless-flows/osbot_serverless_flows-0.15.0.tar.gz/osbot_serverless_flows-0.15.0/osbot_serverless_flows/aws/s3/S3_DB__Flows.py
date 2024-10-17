from osbot_aws.aws.s3.S3__DB_Base import S3__DB_Base


class S3_DB__Flows(S3__DB_Base):                           # todo: refactor the need of this generic class/bucket into specific buckets
    bucket_name__suffix : str = 'flows'
    bucket_name__prefix : str = 'serverless-flows'

