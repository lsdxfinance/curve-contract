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

- swETHx: 0xB776E073F359B30D8E19B216983D678f281487a6

- StableSwapSWETHx: 0xefD2fCa091e4bA762A7dd7f0F3FBEF8075A7ca12

- DepositSWETHx: 0x6F18d91b2c3e2F4E7B9C6DeCEd5537863aE43F7e


### Goerli

- swETHx: 0x1B99Ad576AF352A8BF02397AA4A6860E44DE7690

- StableSwapSWETHx: 0xa804Acaf123BAb88e2D2D6fa6D0B2EE316DA3F45

- DepositSWETHx: 0xFa68d86197Df51F34Ac5290bbc8658FD57f3B761