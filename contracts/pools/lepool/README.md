# Leviosa LSD Pool

## Prepare .env file

Create `.env` file based on `.env-example`, and 

```sh
$ source .env
```

## Test

```sh
$ pipx inject eth-brownie brownie-token-tester

$ brownie test tests/ --pool lepool
```

## Deploy

```sh
$ brownie run deploy_lepool --network <mainnet-fork | goerli | mainnet>
```