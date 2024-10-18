from cs_ai_common.dynamodb.utils import build_expression_attribute_names, build_expression_attribute_values, build_update_expression
from botocore.exceptions import ClientError
import boto3
import os
from cs_ai_common.logging.internal_logger import InternalLogger

def update_resolver_task(task_id: str, resolver_name: str, **kwargs) -> None:
    dynamodb = boto3.client('dynamodb')
    table_name = os.getenv("RESULTS_TABLE_NAME")
    try:
        dynamodb.update_item(
            TableName=table_name,
            Key={
                'task_id': {
                    'S': task_id
                },
                'resolver': {
                    'S': resolver_name
                }
            },
            UpdateExpression=build_update_expression(kwargs),
            ExpressionAttributeNames=build_expression_attribute_names(kwargs),
            ExpressionAttributeValues=build_expression_attribute_values(kwargs)
        )
        InternalLogger.LogDebug("UpdateItem succeeded")
    except ClientError as e:
        InternalLogger.LogError(f"Unable to update item: {e.response['Error']['Message']}")
        raise e