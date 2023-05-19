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

$ brownie test tests/ --pool ethx -s
```

## Deploy

```sh
$ brownie run deploy_ethx --network <mainnet-fork | goerli | mainnet>
```

## Deployment Addresses

### Goerli

- ETHx: 0xF4C911C395DB0b993AD2909c0135cbd4D31D89CA

- StableSwapETHxPool: 0x3f1bE9EE10024EE5D3463eE0b407e56A1cC2E45E