import json
import re
import datetime


# HISTORY LOGGING
async def log_history(service, user_id, domain):
    with open("history.json", "r") as f:
        history_data = json.load(f)
    if user_id not in history_data:
        history_data[user_id] = {}
    if service not in history_data[user_id]:
        history_data[user_id][service] = []
    history_data[user_id][service].append(domain)
    with open("history.json", "w") as f:
        json.dump(history_data, f, indent=4)
    return f"CONFIG: Logged {domain} to {service} history for {user_id}."

# GET HISTORY
async def get_history(service, user_id):
    with open("history.json", "r") as f:
        history_data = json.load(f)
    if user_id in history_data and service in history_data[user_id]:
        return history_data[user_id][service]
    return []

# POP USER HISTORY FOR SERVICE
async def pop_history(service, user_id):
    with open("history.json", "r") as f:
        history_data = json.load(f)
    if user_id in history_data and service in history_data[user_id]:
        history_data[user_id][service].pop()
        with open("history.json", "w") as f:
            json.dump(history_data, f, indent=4)
        return f"CONFIG: Popped history for {user_id} for {service}."
    return f"CONFIG: No history found for {user_id} for {service}."

# POP USER HISTORY
async def pop_user_history(user_id):
    with open("history.json", "r") as f:
        history_data = json.load(f)
    if user_id in history_data:
        history_data.pop(user_id)
        with open("history.json", "w") as f:
            json.dump(history_data, f, indent=4)
        return f"CONFIG: Popped history for {user_id}."
    return f"CONFIG: No history found for {user_id}."

# SERVICE COUNTER
async def service_counter(service: str, amount: int):
    """Add to the service counter."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            provider["counter"] += amount
            # Write the updated config data back to the file
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            return f"CONFIG: Added {amount} to {service} counter."
    return f"CONFIG: Invalid service."


async def get_service_counter(service: str):
    """Get the service counter."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            return provider["counter"]
    return f"CONFIG: Invalid service."


# GET SERVICE MAX USES
async def get_service_max_uses(service: str):
    """Get the service max uses."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            return provider["max_uses"]
    return f"CONFIG: Invalid service."

# SET SERVICE MAX USES
async def set_service_max_uses(service: str, max_uses: int):
    """Set the service max uses."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            provider["max_uses"] = max_uses
            # Write the updated config data back to the file
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            return f"CONFIG: Set max uses for {service} to {max_uses}."
    return f"CONFIG: Invalid service."


# GET SERVICE COOLDOWN
async def get_service_cooldown(service: str):
    """Get the service cooldown."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            return provider["cooldown"]
    return f"CONFIG: Invalid service."

# SET SERVICE COOLDOWN
async def set_service_cooldown(service: str, cooldown: int):
    """Set the service cooldown."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            provider["cooldown"] = cooldown
            # Write the updated config data back to the file
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            return f"CONFIG: Set cooldown for {service} to {cooldown}."
    return f"CONFIG: Invalid service."

# SET USER COOLDOWN
async def set_cooldown(user_id, cooldown_duration, service):
    # Load the existing cooldown data from the file
    with open("cooldown.json", "r") as f:
        cooldown_data = json.load(f)

    # Check if the user already has a cooldown for this service
    if user_id in cooldown_data and service in cooldown_data[user_id]:
        # Update the existing cooldown for this service
        cooldown_data[user_id][service]["num_uses"] += 1
        cooldown_data[user_id][service]["expiry"] = str(
            datetime.datetime.utcnow() + datetime.timedelta(seconds=cooldown_duration)
        )
    else:
        # Create a new cooldown for this service
        if user_id not in cooldown_data:
            cooldown_data[user_id] = {}
        cooldown_data[user_id][service] = {
            "duration": cooldown_duration,
            "expiry": str(
                datetime.datetime.utcnow() + datetime.timedelta(seconds=cooldown_duration)
            ),
            "num_uses": 1
        }

    # Write the updated cooldown data back to the file
    with open("cooldown.json", "w") as f:
        json.dump(cooldown_data, f, indent=4)

    return f"CONFIG: Cooldown set for {user_id} for {cooldown_duration} for {service}."

# GET USER COOLDOWN
async def get_cooldown(service, user_id):
    # Load the existing cooldown data from the file
    with open("cooldown.json", "r") as f:
        cooldown_data = json.load(f)

    max_uses = await get_service_max_uses(re.sub("_premium", "", service))

    # Check if the user has a cooldown for this service
    # Check if the user has reached the max uses for this service
    # Check if the cooldown has expired and remove it if it has
    # Return the time remaining on the cooldown
    if user_id in cooldown_data and service in cooldown_data[user_id]:
        expiry = datetime.datetime.strptime(
            cooldown_data[user_id][service]["expiry"], "%Y-%m-%d %H:%M:%S.%f"
        )
        if cooldown_data[user_id][service]["num_uses"] >= max_uses and expiry > datetime.datetime.utcnow():
            # Make this in a readable format (Cooldown expires in 1 day, 2 hours, 3 minutes, 4 seconds)
            return [False, f"CONFIG: Max uses reached. Cooldown expires in {expiry - datetime.datetime.utcnow()}"]
        if expiry < datetime.datetime.utcnow():
            del cooldown_data[user_id][service]
            with open("cooldown.json", "w") as f:
                json.dump(cooldown_data, f, indent=4)
            # If the cooldown has expired then the user can use the service
            return [True, 0]
        elif cooldown_data[user_id][service]["num_uses"] < max_uses:
            # If the user hasn't used the max uses for this service then return True
            return [True, 0]
        else:
            # If the cooldown hasn't expired then return the time remaining in readable format
            time_remaining = expiry - datetime.datetime.utcnow()
            return [False, time_remaining]
    else:
        # If the user doesn't have a cooldown then they can use the service
        return [True, 0]

# SET USER NUM USES
async def set_user_num_uses(service, user_id, num_uses):
    # Load the existing cooldown data from the file
    with open("cooldown.json", "r") as f:
        cooldown_data = json.load(f)

    # Check if the user already has a cooldown for this service
    if user_id in cooldown_data and service in cooldown_data[user_id]:
        # Update the existing cooldown for this service
        cooldown_data[user_id][service]["num_uses"] = num_uses
    else:
        # Create a new cooldown for this service
        if user_id not in cooldown_data:
            cooldown_data[user_id] = {}
        cooldown_data[user_id][service] = {
            "duration": 0,
            "expiry": str(
                datetime.datetime.utcnow()
            ),
            "num_uses": num_uses
        }

    # Write the updated cooldown data back to the file
    with open("cooldown.json", "w") as f:
        json.dump(cooldown_data, f, indent=4)

    return f"CONFIG: Set num uses for {user_id} for {service} to {num_uses}."


async def get_service_info(service: str):
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            return provider
    return "CONFIG: Invalid service."


async def get_domains(service: str):
    """Get the list of domains for a service."""
    with open("domains.json", "r") as f:
        domains = json.load(f)
    for provider in domains["services"]:
        if provider["name"] == service:
            return provider["domains"]
    return "CONFIG: Invalid service."


async def get_all_domains():
    """Get the list of all domains."""
    with open("domains.json", "r") as f:
        domains = json.load(f)
    list_domains = []
    for provider in domains["services"]:
        for domain in provider["domains"]:
            list_domains.append(domain)
    return list_domains


async def get_premium_domains(service: str):
    """Get the list of premium domains."""
    with open("domains.json", "r") as f:
        domains = json.load(f)
    for provider in domains["services"]:
        if provider["name"] == service:
            return provider["premium_domains"]
    return "CONFIG: Invalid service."


async def get_all_premium_domains():
    """Get the list of all premium domains."""
    with open("domains.json", "r") as f:
        domains = json.load(f)
    list_domains = []
    for provider in domains["services"]:
        for domain in provider["premium_domains"]:
            list_domains.append(domain)
    return list_domains


async def change_password(password: str):
    """Change the password for the proxy."""
    with open("config.json", "r") as f:
        config = json.load(f)
    config["password"] = password
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    return "CONFIG: Changed the password."


async def get_password():
    """Get the password for the proxy."""
    with open("config.json", "r") as f:
        config = json.load(f)
    return config["password"]


async def get_services():
    """Get the list of services."""
    with open("config.json", "r") as f:
        config = json.load(f)
    services = []
    for service in config["services"]:
        services.append(service["name"])
    return services


async def run_domain_check(domain: str):
    """Run a regex check to see if the domain is valid and ensure there are no duplicates."""
    # Check if the domain is valid
    if (
        re.match(
            r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$",
            domain,
        )
        is None
    ):
        return "CONFIG: Invalid domain."

    # Check if the domain is already in the list
    domains = await get_all_domains()
    if domain in domains:
        return "CONFIG: Domain already exists."

    return True


async def run_premium_domain_check(domain: str):
    """Run a regex check to see if the domain is valid and ensure there are no duplicates."""
    # Check if the domain is valid
    if (
        re.match(
            r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$",
            domain,
        )
        is None
    ):
        return "CONFIG: Invalid domain."

    # Check if the domain is already in the list
    domains = await get_all_premium_domains()
    if domain in domains:
        return "CONFIG: Domain already exists."

    return True


async def add_domain(domain: str, service: str):
    """Add domain to the list of domains."""

    # Check if the domain is valid
    if await run_domain_check(domain) is not True:
        return await run_domain_check(domain)

    with open("domains.json", "r") as f:
        domains = json.load(f)
    for provider in domains["services"]:
        if provider["name"] == service:
            provider["domains"].append(domain)

    with open("domains.json", "w") as f:
        json.dump(domains, f, indent=4)

    return f"CONFIG: Added {domain} to the list of domains."


async def remove_domain(domain: str, service: str):
    """Remove domain from the list of domains."""
    with open("domains.json", "r") as f:
        domains = json.load(f)
    for provider in domains["services"]:
        if provider["name"] == service:
            for domain_ in provider["domains"]:
                if domain_ == domain:
                    provider["domains"].remove(domain_)

    with open("domains.json", "w") as f:
        json.dump(domains, f, indent=4)

    return f"CONFIG: Removed {domain} from the list of domains."


async def add_premium_domain(domain: str, service: str):
    """Add domain to the list of premium domains."""

    # Check if the domain is valid
    if await run_premium_domain_check(domain) is not True:
        return await run_premium_domain_check(domain)

    with open("domains.json", "r") as f:
        domains = json.load(f)
    for provider in domains["services"]:
        if provider["name"] == service:
            provider["premium_domains"].append(domain)

    with open("domains.json", "w") as f:
        json.dump(domains, f, indent=4)

    return f"CONFIG: Added {domain} to the list of premium domains."


async def remove_premium_domain(domain: str, service: str):
    """Remove domain from the list of premium domains."""
    with open("domains.json", "r") as f:
        domains = json.load(f)
    for provider in domains["services"]:
        if domain in provider["premium_domains"]:
            provider["premium_domains"].remove(domain)
    with open("domains.json", "w") as f:
        json.dump(domains, f, indent=4)

    return f"CONFIG: Removed {domain} from the list of premium domains."


async def get_permission_status(service: str, user_id: int):
    """Get the permission status for a user."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            for manager in provider["managers"]:
                if manager == user_id:
                    return True
    return False


async def add_manager(service: str, user_id: int):
    """Add a manager to the list of managers."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for provider in config["services"]:
        if provider["name"] == service:
            provider["managers"].append(user_id)

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    return "CONFIG: Added manager."


async def remove_manager(service: str, user_id: int):
    """Remove a manager from the list of managers."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for service in config["services"]:
        if service["name"] == service:
            service["managers"].remove(user_id)

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    return "CONFIG: Removed manager."


async def add_service(name: str, url: str, description: str):
    """Add a service to the list of services."""
    with open("config.json", "r") as f:
        config = json.load(f)
    config["services"].append(
        {
            "name": name,
            "url": url,
            "description": description,
            "managers": [],
            "counter": 0,
            "cooldown": 3600,
            "max_uses": 1,
        }
    )
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    with open("domains.json", "r") as f:
        domains = json.load(f)

    domains["services"].append(
        {
            "name": name,
            "domains": [],
            "premium_domains": [],
        }
    )
    with open("domains.json", "w") as f:
        json.dump(domains, f, indent=4)

    return "CONFIG: Added service."


async def remove_service(name: str):
    """Remove a service from the list of services."""
    with open("config.json", "r") as f:
        config = json.load(f)
    for service in config["services"]:
        if service["name"] == name:
            config["services"].remove(service)
    
    # Remove all domains for the service
    with open("domains.json", "r") as f:
        domains = json.load(f)
    for service in domains["services"]:
        if service["name"] == name:
            domains["services"].remove(service)
    
    with open("domains.json", "w") as f:
        json.dump(domains, f, indent=4)

    # Remove all history for the service for all users
    with open("history.json", "r") as f:
        history = json.load(f)
    for user in history:
        for service in user:
            if service == name:
                user.remove(service)

    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)

    # Remove all cooldown for the service for all users
    with open("cooldown.json", "r") as f:
        cooldowns = json.load(f)
    for user in cooldowns:
        for service in user:
            if service == name:
                user.remove(service)

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    return f"CONFIG: Removed {name}."


async def get_main_service():
    """Get the main service."""
    with open("config.json", "r") as f:
        config = json.load(f)
    return config["main_service"]
