# vETHx Pool

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

### Mainnet

- vETHx: 0xEf4218F106a33CD8A75594967d1E498F760544a8

- StableSwapVETHx: 0xde14B4a4A83dB5e506A62f06079ED3E85862A06B

- DepositVETHx: 0x5B30ff28728bC82f78677F8053ECc47500eE6582

### Goerli

- vETHx: 0x0Ad7d395A9E2bD403a64F9fe208Bf77B5A46551B

- StableSwapVETHx: 0x96f432e7b743a6a7fa823ba90485492a36beb3a8

- DepositVETHx: 0xF5204b0c60ad8d47F87380352c0FA4a0c3331371