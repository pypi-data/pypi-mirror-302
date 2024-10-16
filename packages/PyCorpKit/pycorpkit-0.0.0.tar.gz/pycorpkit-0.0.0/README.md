#### About
A comprehensive Python library for enterprise management, offering modular functionality for user authentication, role-based access control (RBAC), organizational structure management, billing systems and digital wallet integration. This toolkit streamlines the development of business applications by providing reusable functions for essential corporate operations and hierarchy management

#### Features
- [x] Authentication.
- [x] Roles and Permissions.
- [x] Organisation Hierachy.
- [ ] Wallet.
- [ ] Billing.

#### Installation
- Setup  a virtual environment
- Install dependencies

     ```python
     pip install -r requirements/base.txt
     pip install -r requirements/tests.txt
     ```
- Create a file `env.sh` and paste the below contents, edit the values appropriately
    ```bash
    export DATABASE_NAME="<database_name>"
    export DATABASE_USER="<database_user"
    export DATABASE_PASSWORD="<database_pass>"
    export DATABASE_HOST="<database_host>"
    export DATABASE_PORT="<database_port>"
    export SECRET_KEY="<SECRET_KEY"
    export DJANGO_DEBUG=True
  ```
- Create database 
   - Type `chmod +x  local_setup.sh`
   - Run `sh local_setup.sh`

- Create superuser
    ```
    python manage.py createsuperuser
    ```
- Run server
   ```python 
     python manage.py runserver --noreload
   ```
- Visit `http://localhost:8000` OR `http://localhost:8000/admin` 

### Checkout API docs
- Visit `http://localhost:8000/docs/`

### Running tests coverage
 ```tox -r```

### Running background tasks [celery]
#### Workers
run worker in a separate terminal as
```
celery -A src.config worker -l info
```
#### Periodic tasks 
run beat on a separate terminal as:
  ```
  celery -A src.config beat -l info
  ```

### See below on how to write meaningful tests
`https://abseil.io/resources/swe-book/html/ch11.html
`