from brownie import accounts, network, config


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_NETWORK = ["development", "ganache-local"]


def get_account(index=0, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.get(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_NETWORK
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def get_second_account():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORK:
        return "0xEdEFD888C62211248A2058159fF4587F7B2A269d"
    else:
        return get_account(1)
