# the-evan-blockchain-and-cryptocurrency

Implementation of my own blockchain and cryptocurrency.

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

**Running a peer instance**

Make sure to activate the virtual env

```bash
export PEER=True && python3 -m backend.app
```

## Frontend

**Run the Frontend**

In the `frontend` directory, run:

```bash
npm run start
```
