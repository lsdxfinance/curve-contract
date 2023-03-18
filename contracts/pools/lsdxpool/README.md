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

- StableSwapLsdxPool: 0x32e94C6e95053AE3A4c71Ac5Db04703781830Dfe

- CurveTokenV3: 0x77FDf827e337324699fe7e12bA50CA846FdA57D6