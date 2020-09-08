# Idempotency Tester

A demo application to reimplement the "idempotency key" concept described in [Stripe documentation](https://stripe.com/docs/api/idempotent_requests). I couldn't find a similar feature documented for Chargify and thought it could be interesting to develop this concept from scratch. The code serves a web application that is currently deployed at [https://idempotency-tester.herokuapp.com](https://idempotency-tester.herokuapp.com). There, an end user will see a universal account balance amount with an option to deposit a positive dollar amount up to $100,000 to the account. The main feature is an optional checkbox setting beneath the Submit button which ensures the idempotency of a transaction. When checked, a new value for the idempotency key is created and displayed in the view. For any given key displayed, only one deposit transaction can be made, which can be verified by the corresponding balance update. Subsequent deposit attempts with the same key will not update the balance and thus result in a no-op.

## Development

Activate a project-specific virtual environment, preferably using Python 3.7 to match the Heroku runtime version. Since `.env` is gitignored, you can create it like this from the project parent directory:
```
$ python3 -m venv .env --prompt idempotency-venv
$ source .env/bin/activate
```
Install dependencies and run server:
```
$ pip install -r requirements.txt
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ export DATABASE_URL='<DATABASE_URI_from_Heroku_account>'
$ flask run
```
The server will run locally on port 5000.

## Logging

* Running locally: stdout of server process
* Heroku deployment: `heroku logs -t` from  project directory while logged into Heroku CLI

## Testing

* Run `pytest`

## Room for Improvement

* Add a separate module for database connection logic. Move to class-based endpoint handlers with shared properties.
* Add a trigger or cron process to clean up stale idempotency keys in the db, or leverage the EXPIRE feature of a Redis db. I chose relational data storage because it appears likely that transactional data including idempotency keys need to be referenceable by their relation to other properties.
* Increase complexity of key values to avoid potential collisions.
* Give more explicit user feedback when a key has been used.
* Expand test coverage and add mock constructs like a temporary database for use in testing.
