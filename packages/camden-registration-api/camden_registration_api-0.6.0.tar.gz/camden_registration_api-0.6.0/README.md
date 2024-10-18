# Camden Registration Api Client


# About

Wrapper on requests api to simulate user actions
on the Camden Activity Registration portal


## Running environment

Python > 3.9

## Install from source code

```
git clone https://github.com/polovinko1980/camden-registration-api.git

pip install -r requirements.txt

```

# Player credentials

Supporting either passing list of credentials as yaml file config.
In project root folder ```camden_registration_api```:

```

vi master.yml



players:
-   login: test@gmail.com
    password: password
    enroll: true
-   login: test2@gmail.com
    password: password2
    enroll: false
```
If using any other places like ```/tmp/my_file.yml```,
use ```--players-from-file /tmp/my_file.yml``` option.



It is possible to pass single player credentials in the format:
<login>:<password>

```

--player login:password

```


# Usage examples

## To run test registration

```

python3 camden_registration_api/camden_api_client.py --player login:password --test

python3 camden_registration_api/camden_api_client.py --players-from-file /tmp/my_file.yml --test

python3 camden_registration_api/camden_api_client.py --test # will use master.yml from project root folder

```


## To run actual registration

```

python3 camden_registration_api/camden_api_client.py --player login:password

python3 camden_registration_api/camden_api_client.py --players-from-file master.yml

python3 camden_registration_api/camden_api_client.py # will use master.yml by default

```

## Using known activity id

Since Camden activity search might return unpredictable result, it is recommended
to pass activity id directly.
This also will optimize the script performance by skipping search activity api call.

To pass activity id, use ```--activity``` option:

```
python3 camden_registration_api/camden_api_client.py --activity 120589

```




# Install as pip package

It's possible to install

```
pip install camden_registration_api

```

And create your own runner file ```my_camden.py``` like below:

```
from camden_registration_api import CamdenClient

api_client = CamdenClient(
        login=<your login>,
        password=<your password>,
        activity_id=120589,
    )

# to run test registration
api_client.test()


# to run actual registration
api_client.register()
```

Then execute as normal python code:

```python3 my_camden.py```


## Other

To call Camden: 1-408-559-8553



## Special ask

Do not share with Alex K, let him train his fingers
