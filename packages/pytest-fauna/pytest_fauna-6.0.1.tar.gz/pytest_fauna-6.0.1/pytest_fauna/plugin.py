import json
import re
from contextlib import suppress
from uuid import uuid4

import pytest
from decouple import UndefinedValueError, config
from fauna import fql
from fauna.client import Client
from tenacity import retry, stop_after_attempt, wait_random_exponential

try:
    from fluctuate.migrations import migrate
except ImportError:
    # Create a mock of the migrate function that will run pytest.skip on any call or
    # attribute access.
    class MigrateMock:
        def __getattr__(self, name):
            pytest.skip(
                "Cannot use fluctuate migrations without installing the `fluctuate`"
                " extra dependencies."
            )

        def __call__(self, *args, **kwargs):
            pytest.skip(
                "Cannot use fluctuate migrations without installing the `fluctuate`"
                " extra dependencies."
            )

    migrate = MigrateMock()


@pytest.fixture(scope="session")
def fauna_admin_key(request):
    """Attempts to return a Fauna DB admin key based on the environment configuration.

    In order to use this fixture, one of `FAUNA_ADMIN_KEY` or
    `FAUNA_ADMIN_KEY_SECRET_ID` must either be set as an environment variable or in a
    .env file. If neither are set, the test requesting this fixture is skipped.

    `FAUNA_ADMIN_KEY` takes precedent over `FAUNA_ADMIN_KEY_SECRET_ID`.

    This fixture is session scoped to reduce potentially hitting SecretsManager multiple
    times to retrieve the same secret value in the same test session.
    """
    with suppress(UndefinedValueError):
        return config("FAUNA_ADMIN_KEY")

    with suppress(UndefinedValueError, pytest.FixtureLookupError):
        secretsmanager_client = request.getfixturevalue("secretsmanager_client")
        secret = secretsmanager_client.get_secret_value(
            SecretId=config("FAUNA_ADMIN_KEY_SECRET_ID")
        )
        secret = json.loads(secret["SecretString"])
        # Return the secret key out of the Key object.
        return secret["secret"]

    pytest.skip(
        "Cannot access FaunaDB without setting `FAUNA_ADMIN_KEY` or"
        " `FAUNA_ADMIN_KEY_SECRET_ID` in an environment variable or .env file. If"
        " FAUNA_ADMIN_KEY_SECRET_ID is set, and you're still seeing this message,"
        " ensure the aws extra dependencies are installed."
    )


@pytest.fixture(scope="session")
def fauna_admin_client(fauna_admin_key):
    """Create an return a FQLv10 admin client for the top level database.

    This fixture is session scoped as the admin key is expected to be set once and not
    changed during the session, so we can save time by not needing to re-instantiate the
    admin client multiple times.
    """
    return Client(secret=fauna_admin_key)


@pytest.fixture
def build_scoped_key():
    """This fixture returns a method to use to construct a scoped key for the provided
    child DB.

    See the following documentation link for more info on scoped keys:
    https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
    """

    def _inner(key, child_db):
        """Build a key scoped to the provided child_db name.

        If the key provided is a top level key, the result will be a scoped key of the
        form f"{key}:{child_db}:admin".

        If the key provided is itself a scoped key *without* a child database defined,
        the result will be a scoped key of the form
        f"{key portion of the scoped key}:{child_db}:{role of the scoped key}".

        If the key provided is itself a scoped key *with* a child database defined, the
        result will be a scoped key of the form
        f"{key portion of the scoped key}:{child database(s) of the scoped key}/{child_db}:{role of the scoped key}".
        """
        scoped_key_regex = r"""
            # Perform a non-greedy match from the beginning of the string to the next
            # `:` to extract the key.
            (?P<key>^.+?)
            # Optional child database group. Performs same non-greedy match as the key
            # group to match to the next `:` to extract the child database this key is
            # scoped to.
            (:(?P<child_database>.+?))?
            # Role group that matches from the last `:` to the end of the string.
            :(?P<role>.+)$
        """
        result = re.match(pattern=scoped_key_regex, string=key, flags=re.VERBOSE)

        # Default to the admin role.
        role = "admin"

        # If the key turns out to be a scoped key, we need to do some extra work.
        if result is not None:
            # Pull the actual key portion out of the scoped key.
            key = result.group("key")
            parents = result.group("child_database")
            # Override the default role with the role provided by the scoped key.
            role = result.group("role")

            # If the key is already scoped to a child database, assume that the `child_db`
            # passed in is a child of the child DB the passed in `key` is scoped to.
            if parents is not None:
                child_db = f"{parents}/{child_db}"

        return f"{key}:{child_db}:{role}"

    return _inner


@pytest.fixture
def test_db_scoped_key(test_db, fauna_admin_key, build_scoped_key):
    """This fixture returns a key scoped to the test db in use.

    See the following documentation link for more info on scoped keys:
    https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
    """
    return build_scoped_key(key=fauna_admin_key, child_db=test_db["name"])


@pytest.fixture
def test_db(fauna_admin_client):
    """Create a randomly named test child database for use in this test module and
    return its name.

    This will delete the test database after the session completes.
    """
    # Create the test database
    test_db_name = f"test_{uuid4().hex}"
    result = fauna_admin_client.query(
        fql(
            "Database.create({name: ${test_db_name}}) {name}", test_db_name=test_db_name
        )
    )

    # Yield the test database.
    yield result.data

    # Use a top level admin key to delete the child database.
    fauna_admin_client.query(
        fql("Database.byName(${test_db_name}).delete()", test_db_name=test_db_name)
    )


@pytest.fixture
def test_db_with_migrations(test_db, test_db_scoped_key):
    """Create a randomly named test child database for use in this test module, apply
    migrations to it, and return it.

    This will delete the test database after the session completes.
    """
    # Apply migrations.
    migrate(key=test_db_scoped_key)

    return test_db


@pytest.fixture
def fauna_test_client(test_db_scoped_key):
    """Returns a FQLv10 test client configured with access to a test fauna database."""
    # Create a fauna client using a scoped key to the child database. See the following
    # documentation link for more info on scoped keys:
    # https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
    return Client(secret=test_db_scoped_key)


@pytest.fixture
# pylint: disable=unused-argument
def fauna_test_client_with_migrations(test_db_with_migrations, test_db_scoped_key):
    """Returns a test client configured with access to a test fauna database that has
    had migrations applied to it.
    """
    # Create a fauna client using a scoped key to the child database. See the following
    # documentation link for more info on scoped keys:
    # https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
    return Client(secret=test_db_scoped_key)


@pytest.fixture
def fsl_dir(pytestconfig):
    """Return the configured FSL directory."""
    try:
        fsl_dir = pytestconfig.getini("FSL_DIR")
    except ValueError:
        try:
            fsl_dir = config("FSL_DIR")
        except UndefinedValueError:
            pytest.skip(
                "FSL_DIR is not defined. Define it in the pytest ini file, as an"
                " environment variable, or in a .env file to run this test."
            )

    path = pytestconfig.rootpath / fsl_dir
    if not path.exists():
        pytest.skip(
            f"FSL_DIR path {path} doesn't appear to exist. FSL_DIR needs to be based on"
            " pytest's rootpath in order to resolve the path to the FSL directory"
            " correctly."
        )

    return str(path)


@pytest.fixture
def fsl_push_with_retry(host):
    """This fixture returns a function that runs `fauna schema push` with a custom
    secret value and FSL directory.

    This fixture requires that fauna shell v3.0 or greater is installed in the
    environment.

    This function will retry failures, as it seems that fauna-shell is flaky when it
    comes to connecting to test databases properly.
    """
    if not host.exists("fauna"):
        pytest.skip(
            "Fauna shell was not found in the PATH. Ensure it is installed in your"
            " environment in order to run this test."
        )

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(5)
    )
    def _inner(secret_key, fsl_directory):
        """This is a function that runs `fauna schema push` with the secret specified in
        the `secret_key` argument, and the FSL directory specified in the
        `fsl_directory` argument.

        This function will retry failures, as it seems that fauna-shell is flaky when it
        comes to connecting to test databases properly.
        """
        host.run_expect(
            [0],
            "fauna schema push --no-input --active --secret %s --dir %s",
            secret_key,
            fsl_directory,
        )

    return _inner


@pytest.fixture
def test_db_with_fsl(test_db, test_db_scoped_key, fsl_push_with_retry, fsl_dir):
    """Create a randomly named test child database for use in this test module, apply
    FSL schema to it, and return it.

    This fixture requires that fauna shell v3.0 or greater is installed in the
    environment.

    This will delete the test database after the session completes.
    """
    # Apply migrations.
    fsl_push_with_retry(secret_key=test_db_scoped_key, fsl_directory=fsl_dir)

    return test_db


@pytest.fixture
# pylint: disable=unused-argument
def fauna_test_client_with_fsl(test_db_with_fsl, test_db_scoped_key):
    """Returns a test client configured with access to a test fauna database that has
    FSL schema applied to it.
    """
    # Create a fauna client using a scoped key to the child database. See the following
    # documentation link for more info on scoped keys:
    # https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
    return Client(secret=test_db_scoped_key)
