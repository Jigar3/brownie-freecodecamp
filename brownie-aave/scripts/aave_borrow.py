from scripts.get_weth import get_weth
from scripts.utils import get_account
from brownie import network, config, interface
from web3 import Web3

AMOUNT = 0.01 * 1e18


def main():
    account = get_account()
    erc20address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    lending_pool = get_lending_pool()

    # Approve sending ERC20 Token
    approve_erc20(lending_pool.address, AMOUNT, erc20address, account)

    # Deposit Function
    print("Depositing...")
    tx = lending_pool.deposit(
        erc20address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited...")

    borrowable_eth, debt_eth = get_borrowable_data(lending_pool, account)

    print("Let's Borrow!")
    # DAI in terms of ETH

    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )

    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.1)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")

    # Borrow Function
    dai_address = config["networks"][network.show_active()]["dai_token"]

    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print(f"Wohoo Borrowed some DAI")

    get_borrowable_data(lending_pool, account)

    dai_balance_in_account = interface.IERC20(
        config["networks"][network.show_active()]["dai_token"]
    ).balanceOf(account)

    repay_all(dai_balance_in_account, lending_pool, account)

    print(
        "You just deposited, borrowed, and repaid all using Aave, Brownie & Chainlink"
    )

    get_borrowable_data(lending_pool, account)


def repay_all(amount, lending_pool, account):
    approve_erc20(
        lending_pool.address,
        amount,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )

    tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    tx.wait(1)

    print("Repaid all")


def get_asset_price(price_feed_address):
    price_feed = interface.AggregatorV3Interface(price_feed_address)

    latest_price = price_feed.latestRoundData()[1] / 1e18
    print(f"The DAI/ETH price is {latest_price}")
    return float(latest_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    available_borrow_eth = available_borrow_eth / 1e18
    total_collateral_eth = total_collateral_eth / 1e18
    total_debt_eth = total_debt_eth / 1e18

    print(f"Available Borrow: {available_borrow_eth}")
    print(f"Total Collateral: {total_collateral_eth}")
    print(f"Total Debt: {total_debt_eth}")

    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(spender, amount, erc20_address, account):
    print("Approving ERC20 Token")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved ERC20 Token")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)

    return lending_pool
