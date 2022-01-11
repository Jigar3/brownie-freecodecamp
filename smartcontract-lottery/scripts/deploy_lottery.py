from brownie import Lottery, network, config
from scripts.utils import get_account, get_contract, fund_with_link
import time


def deploy_lottery(force=False):
    account = get_account()

    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print("Deployed Lottery!!")

    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print("Lottery started!!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 1 * 1e8
    tx = lottery.enterLottery({"from": account, "value": value})
    tx.wait(1)
    print("Entered lottery!!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund contract with Link Token
    tx = fund_with_link(lottery.address)
    tx.wait(1)

    ending_lottery_txn = lottery.endLottery({"from": account})
    ending_lottery_txn.wait(1)
    time.sleep(60)

    print(f"{lottery.recentWinner()} is the winner!!")


def main():
    # deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
