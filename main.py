import boto3
import csv
from aioboto3.session import Session


async def list_user_policy_names(client: Session.client, username: str) -> list[str]:
    response = await client.list_user_policies(UserName=username)
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


def main():
    client = boto3.client('iam')

    with open('status_reports.csv', 'r') as f:
        reader = csv.DictReader(f)

        for _, line in enumerate(reader):
            username = line['user']
            policies = set()

            try:
                policies.update(list_user_policy_names(client, username))
                policies.update(list_attached_user_policy_names(client, username))

                group_names = list_group_names_for_user(client, username)

                for group_name in group_names:
                    policies.update(list_group_policy_names(client, group_name))
                    policies.update(list_attached_group_policy_names(client, group_name))

                print(f'{username} - {policies}')
            except:
                continue


if __name__ == '__main__':
    main()