# swETHx Pool

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

- swETHx: 0x1B99Ad576AF352A8BF02397AA4A6860E44DE7690

- StableSwapSWETHx: 0xa804Acaf123BAb88e2D2D6fa6D0B2EE316DA3F45

- DepositSWETHx: 0xFa68d86197Df51F34Ac5290bbc8658FD57f3B761