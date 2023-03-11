# Discord Proxy Bot
Discord bot intended to distribute proxies in a single server.

This is highly specialized for Kazwire, however this would provide admins of proxy sites/networks with a great head start with development.

**Commands:**

> `/proxy service: [service]`
> -> Returns a proxy link for that service.

> `/premium get service: [service]`
> -> Returns a premium proxy link. (Ensure that the correct permissions are set for this if you choose to use it.)

> `/premium get_pass`
> -> Returns the password for the main proxy.

> `/admin add service: [service] domain: [domain]`
> -> Adds a domain to the service's domain list. You can add multiple domains added if you have a space in between each domain.

> `/admin remove service: [service] domain: [domain]`
> -> Removes a domain from the service's domain list. You can remove multiple domains if you have a space in between each domain.

> `/admin listall service: [service]`
> -> Lists all domains for the given service.

> `/admin add_premium service: [service] domain: [domain]`
> -> Adds a domain to the service's premium domain list.

> `/admin remove_premium service: [service] domain: [domain]`
> -> Removes a domain from the service's premium domain list.

> `/admin list_premium service: [service]`
> -> Lists all premium domains for the given service.

> `/admin set_cooldown service: [service] max_uses: [max_uses] cooldown: [cooldown]`
> -> Set the cooldown for a service.

> `/admin set_user_cooldown user: [user] service: [service] count: [count]`
> -> Set the user's cooldown for a service if the bot breaks for whatever reason you can reset their count.

> `/admin get_info service: [service]`
> -> Get's information about your service like the total times used.

> `/admin add_service service: [service] url: [url] description: [description]`
> -> Add a service. (Only accessible if you have access to manage the main service)

> `/admin add_manager service: [service] user: [user]`
> -> Add a manager to a service. (Only accessible if you have access to manage the main service)