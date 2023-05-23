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

$ brownie test tests/ --pool wbethx -s --interactive
```

## Deploy

```sh
$ brownie run deploy_wbethx --network <goerli | mainnet>
```

## Deployment Addresses

### Goerli