# outline-vpn-api-async

A Python API wrapper for [Outline VPN](https://getoutline.org/)

This is a fork of https://github.com/jadolg/outline-vpn-api

[![Test](https://github.com/dogekiller21/outline-vpn-api-async/actions/workflows/test.yml/badge.svg)](https://github.com/dogekiller21/outline-vpn-api-async/actions/workflows/test.yml)

## How to use

```python
from outline_vpn import OutlineVPN

async def main():
    # Setup the access with the API URL (Use the one provided to you after the server setup)
    client = OutlineVPN(api_url="https://127.0.0.1:51083/xlUG4F5BBft4rSrIvDSWuw")
    # Init the client with setting cert_sha256
    await client.init(cert_sha256="4EFF7BB90BCE5D4A172D338DC91B5B9975E197E39E3FA4FC42353763C4E58765")
    
    # Get all access URLs on the server
    for key in await client.get_keys():
        print(key.access_url)
    
    # Get a single key by it id
    my_cool_key = await client.get_key(key_id=1337)
    print(my_cool_key.access_url)
    
    # Create a new key
    new_key = await client.create_key()
    
    # [Optional] You can set a name to key while creating it to auto rename
    new_key = await client.create_key(key_name="My cool key")
    
    # Rename it
    await client.rename_key(key_id=new_key.key_id, name="new_key")
    
    # Delete it
    await client.delete_key(key_id=new_key.key_id)
    
    # Set a monthly data limit for a key (20MB)
    await client.add_data_limit(key_id=new_key.key_id, limit_bytes=1000 * 1000 * 20)
    
    # Remove the data limit
    await client.delete_data_limit(key_id=new_key.key_id)

    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```

## Contribution

Install locally
```bash
pip install -e .
```

Fill out test.env with your test server creds
```bash
cp test.env.example test.env
```

Run tests
```bash
pytest
```
