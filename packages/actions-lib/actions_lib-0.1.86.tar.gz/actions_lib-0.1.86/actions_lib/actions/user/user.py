def show_account_info(step: any, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor = kwargs.get('executor')
    result = {}
    account_info = get_account_info(redis_client, executor)
    user_assets = get_user_assets(redis_client, executor)
    result['remain_balance'] = account_info['remain_balance']
    result['address'] = executor
    result['assets'] = user_assets

    res = generate_complete_markdown(executor, account_info['remain_balance'], user_assets)
    return {
        'result': {'code': 200, 'content': res},
        'action': None,
        'next_action': None
    } 
    

def get_account_info(redis_client, user_id):
    is_initial = False
    user_id = user_id.lower()
    print(f"user_id: {user_id}")
    account_key = f"user:account:{user_id}"
    default_values = {
        'charge_total': '0',
        'action_fee': '0',
        'tx_fee': '0'
    }
    account_info = redis_client.hgetall(account_key)
    if not account_info:
        init_user_account(user_id)
        is_initial = True
        account_info = redis_client.hgetall(account_key)
    default_values.update(account_info)
    result = {k: int(default_values.get(k, '0')) for k in ['charge_total', 'action_fee', 'tx_fee']}
    extra_fund = get_extra_funds(user_id)
    
    result['remain_balance'] = result['charge_total'] - result['action_fee'] - result['tx_fee'] + extra_fund
    return {
        **result,
        'is_initial': is_initial
    }

def init_user_account(redis_client, user_id):
    user_id = user_id.lower()
    key = f"user:account:{user_id}"
    redis_client.hset(key, "charge_total", 25000)
    redis_client.hset(key, "action_fee", 0)
    redis_client.hset(key, "tx_fee", 0)
    redis_client.hset(key, "waived_tx_fee", 0)
    return f"Account for user {user_id} has been initialized"

def get_extra_funds(account_id, redis_client):
    account_id = account_id.lower()
    extra_funds = redis_client.hget(f'user_funds:{account_id}', 'extra_funds')
    return int(extra_funds or 0)

def get_user_assets(redis_client, user_id):
    user_id = user_id.lower()
    result = []

    # Use a pattern to match all keys related to the user's assets across different chains
    keys_pattern = f"user:asset:{user_id}:*"
    keys = redis_client.keys(keys_pattern)

    # Iterate over each matched key and retrieve its hash content
    for key in keys:
        # Extract the chain name from the key
        chain = key.split(":")[-1]
        
        # Get all key-value pairs from the Redis hash
        assets = redis_client.hgetall(key)
        
        # Format the results into the desired structure
        for token, amount in assets.items():
            result.append({
                'chain': chain,
                'token': token,
                'amount': int(amount)  # Ensure the amount is an integer
            })
    
    return result

def increase_token_amount(redis_client, user_id, chain, token, amount):
    """
    Increase the amount of a specific token for a user on a given chain.

    Args:
        user_id (str): The user ID.
        chain (str): The blockchain network (e.g., 'eth', 'bnb').
        token (str): The token name (e.g., 'usdc', 'eth').
        amount (int): The amount to increase.

    Returns:
        int: The updated amount of the token.
    """
    user_id = user_id.lower()
    chain = chain.lower()
    token = token.lower()
    key = f"user:asset:{user_id}:{chain}"
    # Use HINCRBY to increment the token amount
    new_amount = redis_client.hincrby(key, token, amount)
    return new_amount


def decrease_token_amount(redis_client, user_id, chain, token, amount):
    """
    Decrease the amount of a specific token for a user on a given chain.

    Args:
        user_id (str): The user ID.
        chain (str): The blockchain network (e.g., 'eth', 'bnb').
        token (str): The token name (e.g., 'usdc', 'eth').
        amount (int): The amount to decrease.

    Returns:
        int: The updated amount of the token.

    Raises:
        ValueError: If the token balance is insufficient.
    """
    user_id = user_id.lower()
    chain = chain.lower()
    token = token.lower()

    key = f"user:asset:{user_id}:{chain}"
    # Get the current token amount
    current_amount = redis_client.hget(key, token)
    current_amount = int(current_amount) if current_amount else 0

    # Ensure the balance is sufficient
    if current_amount < amount:
        raise ValueError(f"Insufficient {token} balance. Current balance: {current_amount}")

    # Use HINCRBY to decrement the token amount
    new_amount = redis_client.hincrby(key, token, -amount)
    return new_amount


def generate_markdown_table(assets):
    """
    Generate a Markdown table from a list of assets.

    Args:
        assets (list): A list of dictionaries containing 'chain', 'token', and 'amount'.

    Returns:
        str: A string representing the Markdown table.
    """
    # Define the header of the Markdown table
    header = "| Chain | Token | Amount |\n|-------|-------|--------|\n"
    
    # Generate rows for each asset entry
    rows = [
        f"| {asset['chain']} | {asset['token']} | {asset['amount']} |"
        for asset in assets
    ]
    
    # Combine the header and rows into the final table string
    table = header + "\n".join(rows)
    
    return table


def generate_complete_markdown(user_address, ai_balance, assets):
    """
    Generate a complete Markdown report with user info and assets.

    Args:
        user_address (str): The user's Ethereum address.
        ai_balance (float): The remaining AI balance.
        assets (list): A list of dictionaries with 'chain', 'token', and 'amount'.

    Returns:
        str: A complete Markdown report.
    """
    # Header with user address and AI balance
    header = (
        f"**Account address:** `{user_address}`\n"
        f"**AI remain balance:** {ai_balance}\n"
        f"**Assets:**\n\n"
    )
    
    # Define the table structure
    table_header = "| Chain | Token | Amount |\n|-------|-------|--------|\n"
    rows = [f"| {asset['chain']} | {asset['token']} | {asset['amount']} |" for asset in assets]
    table = table_header + "\n".join(rows)
    
    # Combine the header and table into the final Markdown output
    markdown_output = header + table
    return markdown_output