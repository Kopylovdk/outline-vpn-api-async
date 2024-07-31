"""
Integration tests for the API wrapper
"""
import os
import re
import json
import pytest
import pytest_asyncio

from outline_vpn import OutlineServerErrorException
from outline_vpn.outline_vpn import OutlineVPN

pytest_plugins = ("pytest_asyncio", )


@pytest_asyncio.fixture
async def client() -> OutlineVPN:
    """This generates a client from the credentials provided in the environment"""
    if "TEST_CLIENT_API_URL" in os.environ and "TEST_CLIENT_CERT_SHA256" in os.environ:
        api_url = os.environ["TEST_CLIENT_API_URL"]
        cert_sha256 = os.environ["TEST_CLIENT_CERT_SHA256"]
    else:
        install_log = open("outline-install.log", "r").read()
        json_text = re.findall("({[^}]+})", install_log)[0]
        api_data = json.loads(json_text)

        api_url = re.sub("https://[^:]+:", "https://127.0.0.1:", api_data.get("apiUrl"))
        cert_sha256 = api_data.get("certSha256")

    client = OutlineVPN(api_url=api_url)
    await client.init(cert_sha256=cert_sha256)
    return client


@pytest.mark.asyncio
async def test_get_keys(client: OutlineVPN):
    """Test for the get keys method"""
    assert len(await client.get_keys()) >= 1


@pytest.mark.asyncio
async def test_crud_key(client: OutlineVPN):
    """Test creating/reading(getting single key/updating the name/deleting a key"""
    new_key = await client.create_key()
    assert new_key is not None
    assert int(new_key.key_id) > 0

    named_key = await client.create_key(key_name="Test Key")
    assert named_key.name == "Test Key"

    fresh_named_key = await client.get_key(key_id=named_key.key_id)
    assert fresh_named_key is not None
    assert fresh_named_key.name == "Test Key"

    assert await client.rename_key(new_key.key_id, "a_name")

    assert await client.delete_key(new_key.key_id)


@pytest.mark.asyncio
async def test_get_single_key(client: OutlineVPN):
    """Test getting a single key"""
    new_key = await client.get_key(key_id=0)
    assert new_key is not None
    assert int(new_key.key_id) == 0

    assert new_key.access_url is not None


@pytest.mark.asyncio
async def test_raise_on_missing_key_id(client: OutlineVPN):
    with pytest.raises(OutlineServerErrorException):
        await client.get_key(key_id=-1)


@pytest.mark.asyncio
async def test_limits(client: OutlineVPN):
    """Test setting, retrieving and removing custom limits"""
    new_limit = 1024 * 1024 * 20
    target_key_id = 0

    assert await client.add_data_limit(target_key_id, new_limit)

    keys = await client.get_keys()
    for key in keys:
        if key.key_id == target_key_id:
            assert key.data_limit == new_limit

    assert await client.delete_data_limit(target_key_id)


@pytest.mark.asyncio
async def test_server_methods(client: OutlineVPN):
    server_info = await client.get_server_information()
    assert server_info is not None

    new_server_name = "Test Server name"
    assert await client.set_server_name(new_server_name)

    new_hostname = "example.com"
    assert await client.set_hostname(new_hostname)

    new_port_for_access_keys = 11233
    assert await client.set_port_new_for_access_keys(new_port_for_access_keys)

    updated_server_info = await client.get_server_information()
    assert updated_server_info.get("name") == new_server_name
    assert updated_server_info.get("hostnameForAccessKeys") == new_hostname
    assert updated_server_info.get("portForNewAccessKeys") == new_port_for_access_keys

    assert await client.set_server_name(server_info.get("name"))
    assert await client.set_hostname(server_info.get("hostnameForAccessKeys"))
    assert await client.set_port_new_for_access_keys(server_info.get("portForNewAccessKeys"))


@pytest.mark.asyncio
async def test_metrics_status(client: OutlineVPN):
    metrics_status = await client.get_metrics_status()
    assert await client.set_metrics_status(not metrics_status)
    assert await client.get_metrics_status() != metrics_status
    assert await client.set_metrics_status(metrics_status)


@pytest.mark.asyncio
async def test_data_limit_for_all_keys(client: OutlineVPN):
    assert await client.set_data_limit_for_all_keys(1024 * 1024 * 20)
    assert await client.delete_data_limit_for_all_keys()


@pytest.mark.asyncio
async def test_get_transferred_data(client: OutlineVPN):
    """Call the method and assert it responds something"""
    data = await client.get_transferred_data()
    assert data is not None
    assert "bytesTransferredByUserId" in data
