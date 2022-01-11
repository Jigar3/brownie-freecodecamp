import pytest
from brownie import network
import time
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import LOCAL_BLOCKCHAIN_NETWORK, fund_with_link, get_account


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORK:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})
    lottery.enterLottery({"from": account, "value": lottery.getEntranceFee()})
    lottery.enterLottery({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(60)

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
