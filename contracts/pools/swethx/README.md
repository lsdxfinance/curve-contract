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

### Mainnet

- swETHx: 0xEeda0FD97340796C2295296d6fE9826F32E8fDdD

- StableSwapSWETHx: 0xD10fCe89a130cF71FD2E0CBfb792d0a4F5272F9A

- DepositSWETHx: 0xA6245f77A76508EfA4Af48e432F0fD8169c18314


### Goerli

- swETHx: 0x1B99Ad576AF352A8BF02397AA4A6860E44DE7690

- StableSwapSWETHx: 0xa804Acaf123BAb88e2D2D6fa6D0B2EE316DA3F45

- DepositSWETHx: 0xFa68d86197Df51F34Ac5290bbc8658FD57f3B761