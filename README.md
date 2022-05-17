# the-evan-blockchain-and-cryptocurrency

The purpose of this project was to learn how blockchain technology and crypto currencies work at a fundamental level. The backend (blockchain) portion as well as the crypto currency elements were written in python whereas the frontend was built using React and Javascript (I know its not pretty but that wasn't the goal of this project).

Viewing blockcahin data:
![](videos/view-blockchain-data.gif)

Conducting a transaction:
![](videos/conduct-transactions.gif)

Mine a block of transactions to the blockchain:
![](videos/mine-block-to-blockchain.gif)

## Backend

**Create and Activate the virtual env**

```bash
Run python3 -m venv <name_of_virtualenv>
source <name_of_virtualenv>/bin/activate
```

**Install the requirements**

```bash
pip3 install -r requirements.txt
```

**Running tests**

Make sure to activate the virtual env
(example for backend directory)

```bash
python3 -m pytest backend/test
```

**Running the applicaiotn and API**

Make sure to activate the virtual env

```bash
python3 -m backend.app
```

**Seed the blockchain with data**

Make sure to activate the virtual env

```bash
export SEED_DATA=True && python3 -m backend.app
```

**Running a peer instance**

Make sure to activate the virtual env

```bash
export PEER=True && python3 -m backend.app
```

## Frontend

**Run the Frontend**

Make sure the backend is running.
In the `frontend` directory, run:

```bash
npm run start
```
