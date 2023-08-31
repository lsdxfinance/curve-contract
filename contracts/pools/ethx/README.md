# ETHx Pool

## Env Setup

```sh
$ pyenv install 3.6.15

# Use python 3.6.15
$ cd curve-contracts
$ pyenv local 3.6.15

# Install brownie 1.13.2
$ brew install pipx
$ pipx ensurepath
$ pipx install eth-brownie==1.13.2

# Install dependencies
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

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

- ETHx: 0xE3AA29cC330c5dd28429641Dd50409553f1f4476
- StableSwapETHxPool: 0x0Bd61885112A7415E39c49818aFd9eB41BF4fC39

