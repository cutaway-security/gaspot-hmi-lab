"""TLS-350 ATG Client Library

Provides communication with Veeder-Root TLS-350 compatible ATG devices.
Used by the HMI to poll current tank values from GasPot.
"""

import socket
import re
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


# TLS-350 Protocol Constants
SOH = b'\x01'  # Start of Header
ETX = b'\x03'  # End of Text
TIMEOUT = 5.0  # Socket timeout in seconds


@dataclass
class TankReading:
    """Represents a single tank reading from TLS-350."""
    tank_id: int
    product_name: str
    volume: float
    tc_volume: float
    ullage: float
    height: float
    water_content: float
    temperature: float
    pressure: Optional[float]
    timestamp: datetime


class ATGClient:
    """Client for communicating with TLS-350 compatible ATG devices."""

    def __init__(self, host: str, port: int = 10001):
        """Initialize ATG client.

        Args:
            host: Hostname or IP of ATG device
            port: TCP port (default 10001)
        """
        self.host = host
        self.port = port

    def _send_command(self, command: str) -> str:
        """Send a TLS-350 command and return the response.

        Args:
            command: TLS-350 command (e.g., 'I20100')

        Returns:
            Response string from ATG

        Raises:
            ConnectionError: If connection fails
            TimeoutError: If response times out
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(TIMEOUT)
                sock.connect((self.host, self.port))

                # Send command with SOH prefix and newline suffix
                sock.sendall(SOH + command.encode('ascii') + b'\n')

                # Receive response
                response = b''
                while True:
                    try:
                        chunk = sock.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                        # Check for end of transmission
                        if ETX in chunk or len(response) > 65536:
                            break
                    except socket.timeout:
                        break

                return response.decode('ascii', errors='replace')

        except socket.timeout:
            raise TimeoutError(f"Connection to {self.host}:{self.port} timed out")
        except socket.error as e:
            raise ConnectionError(f"Connection to {self.host}:{self.port} failed: {e}")

    def get_inventory(self) -> List[TankReading]:
        """Get inventory data for all tanks (I20100 command).

        Returns:
            List of TankReading objects for all tanks
        """
        response = self._send_command("I20100")
        return self._parse_inventory(response)

    def get_pressure(self) -> dict:
        """Get pressure data for gas tanks (I20600 command).

        Returns:
            Dictionary mapping tank_id to pressure value (or None if N/A)
        """
        response = self._send_command("I20600")
        return self._parse_pressure(response)

    def poll_all(self) -> List[TankReading]:
        """Poll all tank data including pressure.

        Returns:
            List of TankReading objects with pressure data included
        """
        # Get base inventory
        readings = self.get_inventory()

        # Get pressure data
        pressure_data = self.get_pressure()

        # Merge pressure into readings
        for reading in readings:
            reading.pressure = pressure_data.get(reading.tank_id)

        return readings

    def _parse_inventory(self, response: str) -> List[TankReading]:
        """Parse I20100 inventory response.

        Response format (tabular):
        TANK PRODUCT             VOLUME TC VOLUME   ULLAGE   HEIGHT    WATER     TEMP
          1  NG-MAIN              38420     38421    11580    73.77     15.2     58.2
          2  NG-RESERVE           44850     44849     5150    86.11     18.2     56.8
        """
        readings = []
        timestamp = datetime.now()

        lines = response.strip().split('\n')

        for line in lines:
            # Look for lines starting with tank ID (1-6 digits after whitespace)
            # Format: "  1  PRODUCT_NAME  vol  tc_vol  ullage  height  water  temp"
            match = re.match(r'^\s*(\d+)\s+(\S+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', line)
            if match:
                try:
                    tank_id = int(match.group(1))
                    product_name = match.group(2)
                    volume = float(match.group(3))
                    tc_volume = float(match.group(4))
                    ullage = float(match.group(5))
                    height = float(match.group(6))
                    water_content = float(match.group(7))
                    temperature = float(match.group(8))

                    reading = TankReading(
                        tank_id=tank_id,
                        product_name=product_name,
                        volume=volume,
                        tc_volume=tc_volume,
                        ullage=ullage,
                        height=height,
                        water_content=water_content,
                        temperature=temperature,
                        pressure=None,
                        timestamp=timestamp
                    )
                    readings.append(reading)
                except (ValueError, IndexError):
                    pass  # Skip malformed data

        return readings

    def _parse_pressure(self, response: str) -> dict:
        """Parse I20600 pressure response.

        Response format (tabular):
        TANK PRODUCT             PRESSURE    STATUS
          1  NG-MAIN              485.2 PSI  NORMAL
          2  NG-RESERVE           520.8 PSI  NORMAL
          4  DIESEL-PRI             N/A      ATMOSPHERIC
        """
        pressure_data = {}
        lines = response.strip().split('\n')

        for line in lines:
            # Look for lines with tank data
            # Format: "  1  PRODUCT_NAME  pressure PSI  STATUS" or "  1  PRODUCT_NAME  N/A  STATUS"
            match = re.match(r'^\s*(\d+)\s+\S+\s+([\d.]+)\s*PSI', line)
            if match:
                tank_id = int(match.group(1))
                pressure_data[tank_id] = float(match.group(2))
            else:
                # Check for N/A pressure
                na_match = re.match(r'^\s*(\d+)\s+\S+\s+N/A', line)
                if na_match:
                    tank_id = int(na_match.group(1))
                    pressure_data[tank_id] = None

        return pressure_data

    def is_connected(self) -> bool:
        """Check if ATG device is reachable.

        Returns:
            True if connection succeeds, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2.0)
                sock.connect((self.host, self.port))
                return True
        except (socket.error, socket.timeout):
            return False
