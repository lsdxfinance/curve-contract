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

$ brownie test tests/ --pool lsdxpool
```

## Deploy

```sh
$ brownie run deploy_lsdxpool --network <mainnet-fork | goerli | mainnet>
```