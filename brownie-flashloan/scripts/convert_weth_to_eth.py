from brownie import accounts, config, network, interface


def main():
    convert_weth_to_eth()


def convert_weth_to_eth():
    account = accounts.add(config["wallets"]["from_key"])
    weth = interface.WethInterface(config["networks"][network.show_active()]["weth"])

    balance_amt = weth.balanceOf(account)
    print(f"Before: {balance_amt}")
    tx = weth.withdraw(balance_amt, {"from": account})
    tx.wait(1)
    print(f"After: {weth.balanceOf(account)}")
