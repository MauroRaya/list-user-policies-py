import boto3


def list_user_policy_names(client: boto3.client, username: str) -> list[str]:
    response = client.list_user_policies(UserName=username)
    return response['PolicyNames']


def list_attached_user_policy_names(client: boto3.client, username: str) -> list[str]:
    response = client.list_attached_user_policies(UserName=username)
    policies = response['AttachedPolicies']
    return [policy['PolicyName'] for policy in policies]


def list_group_names_for_user(client: boto3.client, username: str) -> list[str]:
    response = client.list_groups_for_user(UserName=username)
    groups = response['Groups']
    return [group['GroupName'] for group in groups]


def list_group_policy_names(client: boto3.client, group_name: str) -> list[str]:
    response = client.list_group_policies(GroupName=group_name)
    return response['PolicyNames']


def list_attached_group_policy_names(client: boto3.client, group_name: str) -> list[str]:
    response = client.list_attached_group_policies(GroupName=group_name)
    policies = response['AttachedPolicies']
    return [policy['PolicyName'] for policy in policies]