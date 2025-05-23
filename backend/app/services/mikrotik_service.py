import routeros_api
# from app.core.config import settings # No longer needed for credentials
from typing import Optional, Dict, Any, List

class MikroTikService:
    def __init__(
        self,
        host: str,
        username: str,
        password: Optional[str], # Password can be optional if device uses other auth or is read-only without it
        port: int,
        use_ssl: bool = True,
        # Optional: device_id for logging or context, if needed later
        # device_id: Optional[str] = None 
    ):
        if not all([host, username, port is not None]): # Password presence check removed from here
            raise ValueError("MikroTik connection details (host, username, port) are required.")
        
        self.host = host
        self.username = username
        self.password = password if password else "" # routeros-api expects a string
        self.port = port
        self.use_ssl = use_ssl
        # self.device_id = device_id
        # self.connection = None # Connection pool is created per operation now for statelessness

    def _connect(self) -> routeros_api.RouterOsApiPool:
        """Establishes a connection to the MikroTik device."""
        try:
            connection = routeros_api.RouterOsApiPool(
                self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                use_ssl=self.use_ssl,
                ssl_verify=False, 
                ssl_verify_hostname=False,
                plaintext_login=True 
            )
            return connection
        except routeros_api.exceptions.RouterOsApiConnectionError as e:
            # Log this error appropriately, perhaps with self.device_id if added
            print(f"Failed to connect to MikroTik {self.host}: {e}")
            raise ConnectionError(f"MikroTik ({self.host}) connection failed: {e}") from e

    def get_api_connection(self) -> routeros_api.RouterOsApiPool:
        """Returns an active API connection pool, creating one if necessary."""
        return self._connect()

    async def get_system_resource(self) -> Optional[Dict[str, Any]]:
        """Fetches system resource information (CPU, memory, disk)."""
        api = None
        try:
            api = self.get_api_connection()
            resource_info_list = api.get_resource('/system/resource').get()
            if resource_info_list:
                return resource_info_list[0]
            return None
        except routeros_api.exceptions.RouterOsApiCommunicationError as e:
            print(f"MikroTik API communication error for {self.host}: {e}")
            return None
        except ConnectionError: 
             return None
        finally:
            if api:
                api.disconnect()
    
    async def get_interfaces(self) -> List[Dict[str, Any]]:
        """Fetches interface information."""
        api = None
        try:
            api = self.get_api_connection()
            interfaces = api.get_resource('/interface').get()
            return interfaces
        except routeros_api.exceptions.RouterOsApiCommunicationError as e:
            print(f"MikroTik API communication error for {self.host} getting interfaces: {e}")
            return []
        except ConnectionError:
            return []
        finally:
            if api:
                api.disconnect()

    async def get_firewall_rules(self) -> List[Dict[str, Any]]:
        """Fetches firewall filter rules."""
        api = None
        try:
            api = self.get_api_connection()
            rules = api.get_resource('/ip/firewall/filter').get()
            return rules
        except routeros_api.exceptions.RouterOsApiCommunicationError as e:
            print(f"MikroTik API communication error for {self.host} getting firewall rules: {e}")
            return []
        except ConnectionError:
            return []
        finally:
            if api:
                api.disconnect()

    async def get_arp_table(self) -> List[Dict[str, Any]]:
        """Fetches ARP table entries."""
        api = None
        try:
            api = self.get_api_connection()
            arp_entries = api.get_resource('/ip/arp').get()
            return arp_entries
        except routeros_api.exceptions.RouterOsApiCommunicationError as e:
            print(f"MikroTik API communication error for {self.host} getting ARP table: {e}")
            return []
        except ConnectionError:
            return []
        finally:
            if api:
                api.disconnect()

    # Add other methods like get_logs, get_routes, etc. as needed.

# No default service instance now, it will be created on-demand with specific device creds. 