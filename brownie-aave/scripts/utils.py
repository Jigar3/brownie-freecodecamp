from brownie import network, accounts, config

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
