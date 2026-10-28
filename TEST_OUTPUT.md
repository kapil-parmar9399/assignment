# Test and verification output

The following commands were run in the project folder on Python 3.14.3 and Django 6.0.3.

## Database migrations

Command:

```text
python manage.py migrate
```

Result: exit code 0. Django applied the built-in admin, authentication, contenttypes, and sessions migrations, followed by `shipping.0001_initial` (all reported `OK`).

## Django system check

Command:

```text
python manage.py check
```

Output:

```text
System check identified no issues (0 silenced).
```

## Migration consistency

Command:

```text
python manage.py makemigrations --check --dry-run
```

Output:

```text
No changes detected
```

## Automated tests

Command:

```text
python manage.py test
```

Output:

```text
Creating test database for alias 'default'...
...............
----------------------------------------------------------------------
Ran 15 tests in 0.063s

OK
Destroying test database for alias 'default'...
Found 15 test(s).
System check identified no issues (0 silenced).
```

The tests cover rotated physical fit, dimensions that do not fit despite a larger box volume, capacity exceeded, lowest-cost eligible selection, no available suitable box, packing multiple products without overlap, an empty order, home-page/form behavior, refreshed product weight after a database update, quantities across multiple products, and the 6 kg product / 5 kg box regression with the valid 6 kg capacity case.
