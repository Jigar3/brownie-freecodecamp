from brownie import network, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import (
    LOCAL_BLOCKCHAIN_NETWORK,
    get_account,
    fund_with_link,
    get_contract,
)
import pytest


def test_get_entrance_fee():

    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORK:
        pytest.skip()

    lottery = deploy_lottery()
    entranceFee = lottery.getEntranceFee()
    print(f"Entrance Fee {entranceFee/1e18}")
    expect_entrance_fee = 0.0125 * 1e18
    assert entranceFee == expect_entrance_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORK:
        pytest.skip()

    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enterLottery({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORK:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enterLottery({"from": account, "value": lottery.getEntranceFee()})
    print(f"Account {lottery.players(0)} has entered the lottery")
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORK:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})
    lottery.enterLottery({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})

    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORK:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})
    lottery.enterLottery({"from": account, "value": lottery.getEntranceFee()})
    lottery.enterLottery(
        {"from": get_account(index=1), "value": lottery.getEntranceFee()}
    )
    lottery.enterLottery(
        {"from": get_account(index=2), "value": lottery.getEntranceFee()}
    )

    fund_with_link(lottery)

    tx = lottery.endLottery({"from": account})
    request_id = tx.events["RequestedRandomness"]["requestId"]
    STATIC_RANDOM_NUMBER = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RANDOM_NUMBER, lottery.address, {"from": account}
    )

    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
