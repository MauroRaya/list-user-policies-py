import boto3


def list_user_policy_names(client: boto3.client, username: str) -> list[str]:
    response = client.list_user_policies(UserName=username)
    return response['PolicyNames']


def list_attached_user_policy_names(client: boto3.client, username: str) -> list[str]:
    response = client.list_attached_user_policies(UserName=username)
    policies = response['AttachedPolicies']
    return [policy['PolicyName'] for policy in policies]