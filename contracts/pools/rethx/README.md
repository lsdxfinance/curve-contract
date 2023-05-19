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

$ brownie test tests/ --pool rethx -s --interactive
```

## Deploy

```sh
$ brownie run deploy_rethx --network <goerli | mainnet>
```

## Deployment Addresses

### Goerli

- rETHx: 0x9A9428E76e004d4331FbF18c3dE808eD40004e0a

- StableSwapRETHx: 0x930B9185b37A6dd051d74098A07da59D487C2963

- DepositRETHx: 0x5a2a0AD7D29939945772b48d2A2F28bC1aD0b2DC