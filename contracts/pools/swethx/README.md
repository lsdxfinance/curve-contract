# ETHx Pool

## Prepare .env file

Create `.env` file based on `.env-example`, and 

```sh
$ source .env
```

## Compile

```sh
$ brownie compile
```

## Test

```sh
$ pipx inject eth-brownie brownie-token-tester

$ brownie test tests/ --pool swethx -s --interactive
```

## Deploy

```sh
$ brownie run deploy_swethx --network <goerli | mainnet>
```

## Deployment Addresses

### Goerli

- swETHx: 0x00cc2072e7A06f192914E81d54031ec01237F869

- StableSwapSWETHx: 0xd7D66d0afA06Cc881A930101FD3ea477f81C9DB8

- DepositSWETHx: 0xB1AeCE9BB153AF05973E512E8B774696b999DbC7