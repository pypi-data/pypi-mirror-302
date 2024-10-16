# Open5GS API

This package provides a Python API for interacting with Open5GS components and managing PCF configurations.

## Installation

```bash
pip install open5gsapi
```

## Usage

First, import the package and set the configuration path:

```python
from open5gsapi import open5gs

# Set the path to your PCF configuration file
open5gs.set_config_path('/path/to/the/pcf.yaml')
```

If the pcf.yaml file is edited manually after loading:

```python
# Explicitly reload the configuration
open5gs.reload_config()
```

### UE and UPF Operations

#### Getting API URLs

```python
# Get UE API URL
UE_API_URL = open5gs.ue(8080, "send")
# Result: "http://10.10.0.132:8080/send"

# Get UPF API URL
UPF_API_URL = open5gs.upf(8081, "receive", "sensor")
# Result: "http://10.10.0.112:8081/receive/sensor"
```

#### Sending and Receiving Data

```python
# Send data
data = {"sensor_id": 1, "temperature": 25.5, "humidity": 60}
response = open5gs.send_data(UE_API_URL, data)

# Receive data
received_data = open5gs.receive_data(UPF_API_URL)
```

### PCF Configuration Management

#### Listing and Viewing Sessions

```python
# List all sessions
sessions = open5gs.list_sessions()
print("Current sessions:", sessions)

# Get details of a specific session
session_name = "video-streaming"
session_details = open5gs.get_session_details(session_name)
print(f"Details of session '{session_name}':", session_details)
```

#### Modifying Session Parameters

```python
# Modify session parameters
session = open5gs.policy.session('video-streaming')
session.ambr.downlink(value=10000000, unit=1)
session.ambr.uplink(value=20000000, unit=1)
session.qos(index=5)
session.arp(priority_level=7, pre_emption_vulnerability=2, pre_emption_capability=1)

# Modify PCC rule parameters
session.pcc_rule[0].qos(index=3)
session.pcc_rule[0].mbr.downlink(value=2000000, unit=1)
session.pcc_rule[0].gbr.uplink(value=1000000, unit=1)
session.pcc_rule[0].add_flow(direction=2, description="permit out ip from any to assigned")
```

#### Managing Sessions

```python
# Add a new session
new_session = open5gs.policy.add_session('new-session-name')
new_session.ambr.downlink(value=5000000, unit=1)
new_session.ambr.uplink(value=1000000, unit=1)

# Remove a session
open5gs.policy.remove_session('session-to-remove')

# Rename a session
open5gs.rename_session('old-session-name', 'new-session-name')
```

#### Updating Configuration

After making changes to the configuration, you need to call `update_pcf()` to update the PCF YAML file:

```python
open5gs.update_pcf()
```

To restart the PCF service and run initialization scripts:

```python
open5gs.update_config()
```

This method will:
1. Tear down existing Docker containers
2. Redeploy the containers with the new configuration
3. Run initialization scripts in the UE and UPF containers

## API Reference

### UE and UPF Operations

- `open5gs.ue(port: int, endpoint: str) -> str`: Get the UE API URL
- `open5gs.upf(port: int, *args) -> str`: Get the UPF API URL
- `open5gs.send_data(url: str, data: Dict[str, Any]) -> Dict[str, Any]`: Send data to the specified URL
- `open5gs.receive_data(url: str) -> Dict[str, Any]`: Receive data from the specified URL

### PCF Configuration Management

- `open5gs.list_sessions() -> List[str]`: Get a list of all session names
- `open5gs.get_session_details(name: str) -> Dict[str, Any]`: Get details of a specific session
- `open5gs.rename_session(old_name: str, new_name: str)`: Rename a session
- `open5gs.policy.session(name: str) -> Session`: Get or create a session
- `open5gs.policy.add_session(name: str) -> Session`: Add a new session
- `open5gs.policy.remove_session(name: str)`: Remove a session

#### Session Methods

- `session.ambr.downlink(value: int, unit: int)`: Set downlink AMBR
- `session.ambr.uplink(value: int, unit: int)`: Set uplink AMBR
- `session.qos(index: int)`: Set QoS index
- `session.arp(priority_level: int, pre_emption_vulnerability: int, pre_emption_capability: int)`: Set ARP parameters

#### PCC Rule Methods

- `session.pcc_rule[index].qos(index: int)`: Set QoS index for a PCC rule
- `session.pcc_rule[index].mbr.downlink(value: int, unit: int)`: Set downlink MBR for a PCC rule
- `session.pcc_rule[index].mbr.uplink(value: int, unit: int)`: Set uplink MBR for a PCC rule
- `session.pcc_rule[index].gbr.downlink(value: int, unit: int)`: Set downlink GBR for a PCC rule
- `session.pcc_rule[index].gbr.uplink(value: int, unit: int)`: Set uplink GBR for a PCC rule
- `session.pcc_rule[index].add_flow(direction: int, description: str)`: Add a flow to a PCC rule

### Configuration Update

- `open5gs.update_pcf()`: Update the PCF YAML file
- `open5gs.update_config()`: Redeploy containers, run initialization scripts, and activate UE and UPF API codes
