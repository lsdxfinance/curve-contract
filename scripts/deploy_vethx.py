import json
import os
import argparse

from brownie import accounts
from brownie.network.gas.strategies import LinearScalingStrategy
from brownie.project.main import get_loaded_projects

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('run')
    parser.add_argument('deploy_vethx')
    parser.add_argument('--network', dest='network', type=str, help='network arg')
    args = parser.parse_args()
    network = args.network
    
    if network not in ['goerli', 'mainnet']:
        print('Usage: brownie run deploy_vethx --network <goerli | mainnet>')
        return
    
    DEPLOYER = accounts.add(os.environ['DEPLOYER_ACCOUNT_KEY'])
    print('Deployer account: %s' % (DEPLOYER.address))

    # deployment settings
    # most settings are taken from `contracts/pools/{POOL_NAME}/pooldata.json`
    POOL_NAME = "vethx"
    POOL_OWNER = DEPLOYER.address
    
    tx_params = {
        "from": DEPLOYER,
        "required_confs": 1,
        "gas_price": LinearScalingStrategy(initial_gas_price = "10 gwei", max_gas_price = "100 gwei", increment=1.125, time_duration=30),
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

    wrapped_coins = [i.get("wrapped_address", i.get("underlying_address", "")) for i in pool_data["coins"]]

    # Step 1: deploy LP token
    token_args = pool_data["lp_constructor"]
    token = token_deployer.deploy(token_args["name"], token_args["symbol"], tx_params, publish_source=False)

    # Step2: deploy swap pool
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
    
    # Step 3: deploy Zap Depositer
    zap_name = next((i.stem for i in contracts_path.glob(f"{POOL_NAME}/Deposit*")), None)
    if zap_name is not None:
        zap_deployer = getattr(project, zap_name)

        abi = next(i["inputs"] for i in zap_deployer.abi if i["type"] == "constructor")
        args = {
            "_pool": swap,
            "_token": token,
        }
        deployment_args = [args[i["name"]] for i in abi] + [tx_params]
        zap_deployer.deploy(*deployment_args)

    print(f"Gas used in deployment: {(balance - DEPLOYER.balance()) / 1e18:.4f} ETH")