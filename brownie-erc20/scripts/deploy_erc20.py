from brownie import MyToken
from scripts.utils import get_account, get_second_account


def deploy_erc20_token():
    account = get_account()
    my_token = MyToken.deploy(10000 * 10 ** 18, {"from": account})

    my_token.transfer(get_second_account(), 10 * 10 ** 18, {"from": account})

    print(f"Balance of Main account: {my_token.balanceOf(account)}")
    print(f"Balance of Second account: {my_token.balanceOf(get_second_account())}")


def main():
    deploy_erc20_token()
