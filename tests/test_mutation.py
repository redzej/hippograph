import pytest

from tests.utils import load_fixtures


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None),
])
@pytest.mark.django_db
def test_mutation_allow_any_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    mutation = """
    mutation{
        addPet(input: {race:"horse", name:"Alex", owner: "VXNlcjoz"}){
            status,
            pet{
                name,
                race,
            }
        }
    }
    """

    response = client.post(data=mutation, **test_kwargs)
    result = response.json()

    assert result['data'] == {
        'addPet': {
            'pet': {
                'name': 'Alex',
                'race': 'horse'
            },
            'status': 201
        }
    }


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None),
])
@pytest.mark.django_db
def test_mutation_allow_authenticated_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    mutation = """
    mutation{
        authenticatedAddPet(input: {race:"horse", name:"Alex", owner: "VXNlcjoz"}){
            status,
            pet{
                name,
                race,
            }
        }
    }
    """

    response = client.post(data=mutation, **test_kwargs)
    result = response.json()

    if login in ('tom', 'kate', 'paul'):
        assert result['data'] == {
            'authenticatedAddPet': {
                'pet': {
                    'name': 'Alex',
                    'race': 'horse'
                },
                'status': 201
            }
        }
    else:
        pass
