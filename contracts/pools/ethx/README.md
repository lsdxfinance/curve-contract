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

- ETHx: 0x1655A0180472545680f8C51aEe53B0B49addb3E7

- StableSwapETHxPool: 0xAe88246F808076F334C24EB68841Fb054db3544e