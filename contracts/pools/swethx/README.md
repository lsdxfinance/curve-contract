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

- swETHx: 0x1DcA1f11d85C5Bd2C272abAB4D21DB1ee2fB255f

- StableSwapSWETHx: 0x16a097f539942d48F6e10bbE1903735d2305d5D9

- DepositSWETHx: 0x8d2578387Cb564CBDB605a590b39Fe4c2c3a58A6