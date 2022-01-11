from brownie import FlashloanV2, accounts, config, network, interface

MINIMUM_FLASHLOAN_WETH_BALANCE = 0.000009 * 1e18
ETHERSCAN_TX_URL = "https://kovan.etherscan.io/tx/{}"


def main():

    acct = accounts.add(config["wallets"]["from_key"])
    flashloan = FlashloanV2[-1]
    weth = interface.WethInterface(config["networks"][network.show_active()]["weth"])

    print(f"WETH Balance in Flashloan contract: {weth.balanceOf(flashloan)/1e18}")
    print(f"WETH Balance in Your Account: {weth.balanceOf(acct)/1e18}")

    # Do a flashloan of 0.01 WETH, you will need to return 0.0100009 WETH back
    # So 0.0000009 WETH should be present in our contract

    if weth.balanceOf(flashloan) < MINIMUM_FLASHLOAN_WETH_BALANCE:
        print(f"Depositing {MINIMUM_FLASHLOAN_WETH_BALANCE/1e18} WETH")
        deposit_weth(weth, MINIMUM_FLASHLOAN_WETH_BALANCE, flashloan, acct)

    # Executing Flashloan
    print("Executing flashloan")
    amount_to_flashloan = 0.01 * 1e18
    print(f"Before Balance of flashloan: {weth.balanceOf(flashloan)}")
    tx = flashloan.flashloan([weth], [amount_to_flashloan], {"from": acct})
    tx.wait(1)
    print(f"After Balance of flashloan: {weth.balanceOf(flashloan)}")
    print(f"Flashloan Success")

    return flashloan


def deposit_weth(weth_contract, amount, send_to, account):
    tx = weth_contract.transfer(send_to, amount, {"from": account})
    tx.wait(1)
    return tx
