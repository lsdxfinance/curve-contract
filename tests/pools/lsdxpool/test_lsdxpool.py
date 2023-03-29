import brownie
from brownie import ETH_ADDRESS

def assert_admin_balances(swap, eth_balance, steth_balance, frxeth_balance, reth_balance):
    assert swap.admin_balances(0) == eth_balance
    assert swap.admin_balances(1) == steth_balance
    assert swap.admin_balances(2) == frxeth_balance
    assert swap.admin_balances(3) == reth_balance
    

def test_lsdx_e2e(alice, bob, swap, wrapped_coins, wrapped_decimals, initial_amounts, pool_token, mint_alice, approve_alice, mint_bob, approve_bob):
    # Initial LP is 0
    assert pool_token.name() == 'LSDx Pool'
    assert pool_token.symbol() == 'ETHx'
    assert pool_token.totalSupply() == 0
    
    # Alice/Bob's initial amounts is 10000 ETH/stETH/frxETH/rETH each (via mint_alice)
    assert wrapped_decimals == [18, 18, 18, 18]
    assert initial_amounts == [10000 * 10 ** i for i in wrapped_decimals]

    # Initial deposit requires all coins
    amounts = [amount // 2 for amount in initial_amounts]
    amounts[1] = 0
    assert amounts == [5000 * 10 ** 18, 0, 5000 * 10 ** 18, 5000 * 10 ** 18]
    with brownie.reverts():
        swap.add_liquidity(amounts, 0, {"from": alice})
    assert pool_token.totalSupply() == 0
    
    # Initial deposit does not require identical coins. Note, `approve_alice` is required
    deposit_amounts = [5000 * 10 ** 18, 4000 * 10 ** 18, 3000 * 10 ** 18, 2000 * 10 ** 18]
    swap.add_liquidity(deposit_amounts, 0, {"from": alice, "value": deposit_amounts[0]})
    # print(pool_token.totalSupply())
    
    # Coins are transfered to swap contract
    for i, coin in enumerate(wrapped_coins):
        if coin == ETH_ADDRESS:
            assert alice.balance() == initial_amounts[i] - deposit_amounts[i]
            assert swap.balance() == deposit_amounts[i]
        else:
            assert coin.balanceOf(alice) == initial_amounts[i] - deposit_amounts[i]
            assert coin.balanceOf(swap) == deposit_amounts[i]

    # Initially, 1 ETHx = 1 ETH/xxETH/...
    assert swap.get_virtual_price() == 1 * 10 ** 18
    # fee and admin_fee are from pool_data
    assert swap.fee() == 10000000  # 0.1%
    assert swap.admin_fee() == 5000000000 # 50% of fee, aka 0.1%
    assert_admin_balances(swap, 0, 0, 0, 0)
    
    # Bob wants to exchange 10 ETH for stETH, estimate the received amount first
    print('LP virtual price before exchange: %s' % (swap.get_virtual_price() / (10 ** 18)))
    dx = 10 * 10 ** 18
    min_dy = swap.get_dy(0, 1, dx)
    bob_prev_steth_balance = wrapped_coins[1].balanceOf(bob)
    swap.exchange(0, 1, dx, min_dy - 1, {"from": bob, "value": dx})
    print('LP virtual price after exchange: %s' % (swap.get_virtual_price() / (10 ** 18)))
    dy = wrapped_coins[1].balanceOf(bob) - bob_prev_steth_balance
    assert abs(dy - min_dy) <= 1
    
    # Check stETH admin fees
    admin_balance_steth = swap.admin_balances(1)
    assert admin_balance_steth > 0
    
    # Bob exchange 10 frxETH for ETH, now we should also have ETH admin fees
    dx = 10 * 10 ** 18
    min_dy = swap.get_dy(2, 0, dx)
    swap.exchange(2, 0, dx, min_dy - 1, {"from": bob})
    admin_balance_eth = swap.admin_balances(0)
    assert admin_balance_eth > 0
    
    # Bob could not withdraw admin balances
    with brownie.reverts():
        swap.withdraw_admin_fees({"from": bob})
    
    # As owner, Alice could withdraw admin balances
    prev_alice_balance_eth = alice.balance()
    prev_alice_balance_steth = wrapped_coins[1].balanceOf(alice)
    swap.withdraw_admin_fees({"from": alice})
    assert_admin_balances(swap, 0, 0, 0, 0)
    assert alice.balance() == prev_alice_balance_eth + admin_balance_eth
    assert wrapped_coins[1].balanceOf(alice) == prev_alice_balance_steth + admin_balance_steth
    
    # Bob add liquidity with only one coin
    # print(pool_token.totalSupply())
    bob_deposit_amounts = [1000 * 10 ** 18, 0, 0, 0]
    swap.add_liquidity(bob_deposit_amounts, 0, {"from": bob, "value": bob_deposit_amounts[0]})
    bob_added_lp_balance = pool_token.balanceOf(bob)
    # print(bob_added_lp_balance / (10 ** 18))
    # Since there are more ETH in the pool, Bob should get less LP tokens
    assert bob_added_lp_balance < 1000 * 10 ** 18
    
    # Bob add liquidity again by depositing token with less balances, shoud get more LP tokens
    bob_deposit_amounts = [0, 0, 1000 * 10 ** 18, 1000 * 10 ** 18]
    swap.add_liquidity(bob_deposit_amounts, 0, {"from": bob})
    bob_added_lp_balance = pool_token.balanceOf(bob) - bob_added_lp_balance
    assert bob_added_lp_balance > 2 * 1000 * 10 ** 18
    
    # Bob withdraw 1/4 of LP, ETH only
    # bob_prev_lp_balance = pool_token.balanceOf(bob)
    # bob_prev_eth_balance = bob.balance()
    bob_withdraw_lp = pool_token.balanceOf(bob) / 4
    expected_withdraw_eth = swap.calc_withdraw_one_coin(bob_withdraw_lp, 0)
    # print(expected_withdraw_eth)
    swap.remove_liquidity_one_coin(bob_withdraw_lp, 0, expected_withdraw_eth, {"from": bob})
    # print(bob_prev_lp_balance, pool_token.balanceOf(bob))
    # print(bob_prev_eth_balance,  bob.balance())
    
    # Bob withdraw 1/4 of LP, balanced, no fee
    print('Pool balances: %s' % ([swap.balances(i) / (10 ** 18) for i in range(4)]))
    print('Total LP: %s, Bob\'s LP: %s' % (pool_token.totalSupply() / (10 ** 18), pool_token.balanceOf(bob) / (10 ** 18)))
    bob_withdraw_lp = pool_token.balanceOf(bob) / 4
    withdraw_amount = [swap.balances(i) * bob_withdraw_lp / pool_token.totalSupply() for i in range(4)]
    withdraw_amount_human_readable = [withdraw_amount[i] / (10 ** 18) for i in range(4)]
    print('Expected withdraw amount: %s' % (withdraw_amount_human_readable))
    bob_prev_balances = [bob.balance() / (10 ** 18), wrapped_coins[1].balanceOf(bob) / (10 ** 18), wrapped_coins[2].balanceOf(bob) / (10 ** 18), wrapped_coins[3].balanceOf(bob) / (10 ** 18)]
    print('Bob\'s balances: %s' % (bob_prev_balances))
    swap.remove_liquidity(bob_withdraw_lp, [0] * 4, {"from": bob})
    bob_balances = [bob.balance() / (10 ** 18), wrapped_coins[1].balanceOf(bob) / (10 ** 18), wrapped_coins[2].balanceOf(bob) / (10 ** 18), wrapped_coins[3].balanceOf(bob) / (10 ** 18)]
    actual_withdraw_amount = [bob_balances[i] - bob_prev_balances[i]for i in range(4)]
    print('Total LP after withdraw: %s, Bob\'s LP after withdraw: %s' % (pool_token.totalSupply() / (10 ** 18), pool_token.balanceOf(bob) / (10 ** 18)))
    print('Bob\'s balances after withdraw: %s' % (bob_balances))
    print('Actual withdraw amount: %s' % (actual_withdraw_amount))
    
    # Bob withdraw imbalanced. Withdraw ETH and stETH only
    withdraw_amount = [0] * 4
    withdraw_amount[0] = swap.balances(0) * bob_withdraw_lp / pool_token.totalSupply() 
    withdraw_amount[1] = swap.balances(1) * bob_withdraw_lp / pool_token.totalSupply() 
    swap.remove_liquidity_imbalance(withdraw_amount, 2 ** 256 - 1, {"from": bob})
    bob_balances = [bob.balance() / (10 ** 18), wrapped_coins[1].balanceOf(bob) / (10 ** 18), wrapped_coins[2].balanceOf(bob) / (10 ** 18), wrapped_coins[3].balanceOf(bob) / (10 ** 18)]
    print('Bob\'s balances after imbalanced withdraw: %s' % (bob_balances))
    
    # Set exchange rate for stETH
    # print('Pool balances: %s' % ([swap.balances(i) / (10 ** 18) for i in range(4)]))
    print('LP virtual price: %s' % (swap.get_virtual_price() / (10 ** 18)))
    wrapped_coins[3].set_exchange_rate(1.1 * 10 ** 18)
    print('LP virtual price after setting exchange rate: %s' % (swap.get_virtual_price() / (10 ** 18)))
    # print('Pool balances after setting exchange rate: %s' % ([swap.balances(i) / (10 ** 18) for i in range(4)]))
