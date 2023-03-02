import json
import os
import argparse

from brownie import accounts
from brownie.project.main import get_loaded_projects

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('run')
    parser.add_argument('deploy_lsdxpool')
    parser.add_argument('--network', dest='network', type=str, help='network arg')
    args = parser.parse_args()
    network = args.network
    
    if network not in ['mainnet-fork', 'goerli', 'mainnet']:
        print('Usage: brownie run deploy_lsdxpool --network <mainnet-fork | goerli | mainnet>')
        return
    
    if network == 'mainnet-fork':
        DEPLOYER = accounts.add()
    else:
        DEPLOYER = accounts.add(os.environ['DEPLOYER_ACCOUNT_KEY'])

    print('Deployer account: %s' % (DEPLOYER.address))

    # deployment settings
    # most settings are taken from `contracts/pools/{POOL_NAME}/pooldata.json`
    POOL_NAME = "lsdxpool"
    POOL_OWNER = DEPLOYER.address
    
    tx_params = {
        "from": DEPLOYER,
        "required_confs": 1
    }

    project = get_loaded_projects()[0]
    balance = DEPLOYER.balance()

    # load data about the deployment from `pooldata.json`
    contracts_path = project._path.joinpath("contracts/pools")
    POOL_DATA_FILE = 'pooldata_goerli.json' if network == 'goerli' else 'pooldata.json'
    with contracts_path.joinpath(f"{POOL_NAME}/{POOL_DATA_FILE}").open() as fp:
        pool_data = json.load(fp)

    swap_name = next(i.stem for i in contracts_path.glob(f"{POOL_NAME}/StableSwap*"))
    swap_deployer = getattr(project, swap_name)
    token_deployer = getattr(project, pool_data.get("lp_contract"))

    wrapped_coins = [i.get("wrapped_address", i["underlying_address"]) for i in pool_data["coins"]]

    # deploy the token
    token_args = pool_data["lp_constructor"]
    token = token_deployer.deploy(token_args["name"], token_args["symbol"], tx_params, publish_source=False)

    # deploy the pool
    abi = next(i["inputs"] for i in swap_deployer.abi if i["type"] == "constructor")
    args = pool_data["swap_constructor"]
    args.update(
        _coins=wrapped_coins,
        _pool_token=token,
        _owner=POOL_OWNER,
    )
    deployment_args = [args[i["name"]] for i in abi] + [tx_params]

    swap = swap_deployer.deploy(*deployment_args, publish_source=False)

    # set the minter
    token.set_minter(swap, tx_params)

    print(f"Gas used in deployment: {(balance - DEPLOYER.balance()) / 1e18:.4f} ETH")