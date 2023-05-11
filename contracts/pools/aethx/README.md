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

$ brownie test tests/ --pool aethx -s
```

## Deploy

```sh
$ brownie run deploy_aethx --network <mainnet-fork | goerli | mainnet>
```

## Deployment Addresses
