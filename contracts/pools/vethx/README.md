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

$ brownie test tests/ --pool vethx -s --interactive
```

## Deploy

```sh
$ brownie run deploy_vethx --network <goerli | mainnet>
```

## Deployment Addresses

### Goerli

- vETHx: 0xc315960A68075872B7b9971eDC4b1ef3fb208ae4

- StableSwapVETHx: 0x792e4dd07D115D45ac7cc2F47f48244ad4Ab1C60

- DepositVETHx: 0x2432487BD79fBd5F960FBd0a2037dB6d6120BA07