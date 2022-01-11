from brownie import config, interface, network
from scripts.utils import get_account


def main():
    get_weth()


def get_weth():
    """Mints WETH by depositing ETH"""
    # ABI
    # Address
    account = get_account()
    weth = interface.WethInterface(
        config["networks"][network.show_active()]["weth_token"]
    )

    value_to_deposit = 0.01 * 1e18

    tx = weth.deposit({"from": account, "value": value_to_deposit})
    tx.wait(1)
    balance = weth.balanceOf(account)
    print(f"Received {balance/1e18} WETH")
    return tx
