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
$ brownie run deploy_rethx --network <mainnet-fork | goerli | mainnet>
```

## Deployment Addresses