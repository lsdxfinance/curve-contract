# @version 0.2.12
"""
@title ETHx Rate Calculator 
@notice Logic for calculating exchange rate between ETHx -> ETH
"""
from vyper.interfaces import ERC20


interface rETH:
    def getExchangeRate() -> uint256: view

interface ETHxPool:
    def coins(i: uint256) -> address: view
    def lp_token() -> address: view
    def balances(i: uint256) -> uint256: view


ethx_pool: public(address)


@external
def __init__(
    _ethx_pool: address,
):
    assert _ethx_pool != ZERO_ADDRESS
    self.ethx_pool = _ethx_pool

@view
@external
def get_rate() -> uint256:
    """
    @notice Calculate the exchange rate for 1 ETHx -> ETH
    @return The exchange rate of 1 ETHx in ETH
    """
    eth_balance: uint256 = ETHxPool(self.ethx_pool).balances(0)
    steth_balance: uint256 = ETHxPool(self.ethx_pool).balances(1)
    frxeth_balance: uint256 = ETHxPool(self.ethx_pool).balances(2)
    reth_balance: uint256 = ETHxPool(self.ethx_pool).balances(3)

    ethx: address = ETHxPool(self.ethx_pool).lp_token()
    ethx_total_supply: uint256 = ERC20(ethx).totalSupply()

    reth: address = ETHxPool(self.ethx_pool).coins(3)
    reth_exchange_rate: uint256 = rETH(reth).getExchangeRate()

    return (10 ** 18 * (eth_balance + steth_balance + frxeth_balance) + reth_balance * reth_exchange_rate) / ethx_total_supply