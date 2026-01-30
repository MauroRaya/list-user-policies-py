from aioboto3.session import Session
from csv import DictReader
from contextlib import suppress
from asyncio import run


async def list_user_policy_names(client: Session.client, username: str) -> list[str]:
    response = await client.list_user_policies(UserName=username)
    return response['PolicyNames']


async def list_attached_user_policy_names(client: Session.client, username: str) -> list[str]:
    response = await client.list_attached_user_policies(UserName=username)
    policies = response['AttachedPolicies']
    return [policy['PolicyName'] for policy in policies]


async def list_group_names_for_user(client: Session.client, username: str) -> list[str]:
    response = await client.list_groups_for_user(UserName=username)
    groups = response['Groups']
    return [group['GroupName'] for group in groups]


async def list_group_policy_names(client: Session.client, group_name: str) -> list[str]:
    response = await client.list_group_policies(GroupName=group_name)
    return response['PolicyNames']


async def list_attached_group_policy_names(client: Session.client, group_name: str) -> list[str]:
    response = await client.list_attached_group_policies(GroupName=group_name)
    policies = response['AttachedPolicies']
    return [policy['PolicyName'] for policy in policies]


async def get_policies(client: Session.client, username: str) -> set[str]:
    policies = set()

    try:
        policies.update(await list_user_policy_names(client, username))
        policies.update(await list_attached_user_policy_names(client, username))

        group_names = await list_group_names_for_user(client, username)

        for group_name in group_names:
            policies.update(await list_group_policy_names(client, group_name))
            policies.update(await list_attached_group_policy_names(client, group_name))
    finally:
        return policies


async def main():
    session = Session()
    async with session.client('iam') as client:
        with open('status_reports.csv', 'r') as f:
            reader = DictReader(f)

            for _, line in enumerate(reader):
                username = line['user']
                policies = await get_policies(client, username)

                print(f'{username} - {policies}')


if __name__ == '__main__':
    run(main())