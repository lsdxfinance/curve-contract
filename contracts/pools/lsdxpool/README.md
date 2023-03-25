# LSDx Pool

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

$ brownie test tests/ --pool lsdxpool -s
```

## Deploy

```sh
$ brownie run deploy_lsdxpool --network <mainnet-fork | goerli | mainnet>
```

## Deployment Addresses

### Goerli

- ETHx: 0x473B817176E7386F143DdD327E04C0685D5F6fDE

- StableSwapLsdxPool: 0x7dEb766e53750C94d398f5eBc2CABBc1b05c2c3D