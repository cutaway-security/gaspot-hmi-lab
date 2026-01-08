#!/usr/bin/env python3
"""
ATG Client - TLS-350 Protocol Client for GasPot HMI Lab

A command-line tool for interacting with Veeder-Root TLS-350 compatible
Automatic Tank Gauge (ATG) devices. Designed for cybersecurity training
and ICS/OT security research.

Usage:
    python atg_client.py [options] <command> [args]

Commands:
    inventory       Get tank inventory (I20100)
    delivery        Get delivery report (I20200)
    leak            Get leak test results (I20300)
    shift           Get shift report (I20400)
    status          Get tank status (I20500)
    pressure        Get pressure data (I20600)
    set-name        Set tank product name (S602xx)
    set-volume      Set tank volume (S60210)
    raw             Send raw TLS-350 command

Examples:
    python atg_client.py inventory
    python atg_client.py -H 192.168.1.100 inventory
    python atg_client.py set-name 1 "PREMIUM"
    python atg_client.py set-volume 1 45000
    python atg_client.py raw I20100

Author: GasPot HMI Lab Project
License: CC0 (Public Domain)
"""

import argparse
import socket
import sys
import re
from typing import Optional, Tuple

# Protocol constants
SOH = b'\x01'  # Start of Header (Ctrl+A)
ETX = b'\x03'  # End of Text
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 10001
DEFAULT_TIMEOUT = 5.0


class ATGClient:
    """Client for TLS-350 ATG protocol communication."""

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                 timeout: float = DEFAULT_TIMEOUT, verbose: bool = False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.verbose = verbose

    def _log(self, message: str) -> None:
        """Print verbose log message."""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)

    def send_command(self, command: str) -> Tuple[bool, str]:
        """
        Send a TLS-350 command and return the response.

        Args:
            command: TLS-350 command string (e.g., 'I20100')

        Returns:
            Tuple of (success: bool, response: str)
        """
        try:
            self._log(f"Connecting to {self.host}:{self.port}")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.host, self.port))

                # Build and send command
                cmd_bytes = SOH + command.encode('ascii') + b'\n'
                self._log(f"Sending: {repr(cmd_bytes)}")
                sock.sendall(cmd_bytes)

                # Receive response
                response = b''
                while True:
                    try:
                        chunk = sock.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                        self._log(f"Received chunk: {len(chunk)} bytes")
                        # Check for end of transmission
                        if ETX in chunk or len(response) > 65536:
                            break
                    except socket.timeout:
                        break

                # Decode and clean response
                decoded = response.decode('ascii', errors='replace')
                # Remove control characters but keep newlines
                cleaned = ''.join(c if c == '\n' or (32 <= ord(c) < 127) else '' for c in decoded)

                self._log(f"Response length: {len(cleaned)} chars")
                return True, cleaned.strip()

        except socket.timeout:
            return False, f"Connection timed out ({self.timeout}s)"
        except ConnectionRefusedError:
            return False, f"Connection refused - is ATG running on {self.host}:{self.port}?"
        except socket.gaierror as e:
            return False, f"DNS resolution failed for {self.host}: {e}"
        except socket.error as e:
            return False, f"Network error: {e}"

    def is_error_response(self, response: str) -> bool:
        """Check if response indicates an error."""
        return '9999' in response or 'FF1B' in response


def cmd_inventory(client: ATGClient, args: argparse.Namespace) -> int:
    """Get tank inventory data."""
    success, response = client.send_command('I20100')
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    if client.is_error_response(response):
        print(f"ATG Error: {response}", file=sys.stderr)
        return 1

    print(response)
    return 0


def cmd_delivery(client: ATGClient, args: argparse.Namespace) -> int:
    """Get delivery report."""
    success, response = client.send_command('I20200')
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    if client.is_error_response(response):
        print(f"ATG Error: {response}", file=sys.stderr)
        return 1

    print(response)
    return 0


def cmd_leak(client: ATGClient, args: argparse.Namespace) -> int:
    """Get leak test results."""
    success, response = client.send_command('I20300')
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    if client.is_error_response(response):
        print(f"ATG Error: {response}", file=sys.stderr)
        return 1

    print(response)
    return 0


def cmd_shift(client: ATGClient, args: argparse.Namespace) -> int:
    """Get shift report."""
    success, response = client.send_command('I20400')
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    if client.is_error_response(response):
        print(f"ATG Error: {response}", file=sys.stderr)
        return 1

    print(response)
    return 0


def cmd_status(client: ATGClient, args: argparse.Namespace) -> int:
    """Get tank status."""
    success, response = client.send_command('I20500')
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    if client.is_error_response(response):
        print(f"ATG Error: {response}", file=sys.stderr)
        return 1

    print(response)
    return 0


def cmd_pressure(client: ATGClient, args: argparse.Namespace) -> int:
    """Get pressure data for gas tanks."""
    success, response = client.send_command('I20600')
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    if client.is_error_response(response):
        print(f"ATG Error: {response}", file=sys.stderr)
        return 1

    print(response)
    return 0


def cmd_set_name(client: ATGClient, args: argparse.Namespace) -> int:
    """Set tank product name."""
    tank_id = args.tank_id
    name = args.name

    # Validate tank ID
    if not 1 <= tank_id <= 99:
        print("Error: Tank ID must be between 1 and 99", file=sys.stderr)
        return 1

    # Validate name (alphanumeric and common symbols only)
    if not re.match(r'^[A-Za-z0-9_\-\s]+$', name):
        print("Error: Name must contain only letters, numbers, spaces, hyphens, and underscores", file=sys.stderr)
        return 1

    # Build command: S602xx where xx is tank ID (01-99)
    command = f"S602{tank_id:02d}{name}"

    success, response = client.send_command(command)
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    if client.is_error_response(response):
        print(f"ATG Error: {response}", file=sys.stderr)
        return 1

    print(f"Tank {tank_id} name set to: {name}")
    return 0


def cmd_set_volume(client: ATGClient, args: argparse.Namespace) -> int:
    """Set tank volume."""
    tank_id = args.tank_id
    volume = args.volume

    # Validate tank ID
    if not 1 <= tank_id <= 99:
        print("Error: Tank ID must be between 1 and 99", file=sys.stderr)
        return 1

    # Validate volume
    if volume < 0 or volume > 999999:
        print("Error: Volume must be between 0 and 999999", file=sys.stderr)
        return 1

    # Build command: S60210:TANK:VOLUME
    command = f"S60210:{tank_id}:{int(volume)}"

    success, response = client.send_command(command)
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    if client.is_error_response(response):
        print(f"ATG Error: {response}", file=sys.stderr)
        return 1

    print(f"Tank {tank_id} volume set to: {volume}")
    return 0


def cmd_raw(client: ATGClient, args: argparse.Namespace) -> int:
    """Send raw TLS-350 command."""
    command = args.command

    success, response = client.send_command(command)
    if not success:
        print(f"Error: {response}", file=sys.stderr)
        return 1

    print(response)
    return 0


def main() -> int:
    """Main entry point."""
    # Create top-level parser
    parser = argparse.ArgumentParser(
        prog='atg_client.py',
        description='TLS-350 ATG Client for GasPot HMI Lab',
        epilog='''
Examples:
  %(prog)s inventory                    # Get tank inventory
  %(prog)s -H 10.0.0.1 inventory        # Connect to remote ATG
  %(prog)s pressure                     # Get pressure readings
  %(prog)s set-name 1 "PREMIUM-95"      # Set tank 1 name
  %(prog)s set-volume 2 45000           # Set tank 2 volume
  %(prog)s raw I20100                   # Send raw command

TLS-350 Commands:
  I20100  Tank Inventory Report
  I20200  Tank Delivery Report
  I20300  Tank Leak Test Results
  I20400  Tank Shift Report
  I20500  Tank Status Report
  I20600  Tank Pressure Report (gas tanks only)
  S602xx  Set Tank xx Product Name
  S60210  Set Tank Volume (format: S60210:TANK:VALUE)
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Global options
    parser.add_argument('-H', '--host', default=DEFAULT_HOST,
                        help=f'ATG host address (default: {DEFAULT_HOST})')
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
                        help=f'ATG port (default: {DEFAULT_PORT})')
    parser.add_argument('-t', '--timeout', type=float, default=DEFAULT_TIMEOUT,
                        help=f'Connection timeout in seconds (default: {DEFAULT_TIMEOUT})')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # inventory command
    p_inventory = subparsers.add_parser('inventory', help='Get tank inventory (I20100)')
    p_inventory.set_defaults(func=cmd_inventory)

    # delivery command
    p_delivery = subparsers.add_parser('delivery', help='Get delivery report (I20200)')
    p_delivery.set_defaults(func=cmd_delivery)

    # leak command
    p_leak = subparsers.add_parser('leak', help='Get leak test results (I20300)')
    p_leak.set_defaults(func=cmd_leak)

    # shift command
    p_shift = subparsers.add_parser('shift', help='Get shift report (I20400)')
    p_shift.set_defaults(func=cmd_shift)

    # status command
    p_status = subparsers.add_parser('status', help='Get tank status (I20500)')
    p_status.set_defaults(func=cmd_status)

    # pressure command
    p_pressure = subparsers.add_parser('pressure', help='Get pressure data (I20600)')
    p_pressure.set_defaults(func=cmd_pressure)

    # set-name command
    p_setname = subparsers.add_parser('set-name', help='Set tank product name (S602xx)')
    p_setname.add_argument('tank_id', type=int, help='Tank ID (1-99)')
    p_setname.add_argument('name', help='New product name')
    p_setname.set_defaults(func=cmd_set_name)

    # set-volume command
    p_setvol = subparsers.add_parser('set-volume', help='Set tank volume (S60210)')
    p_setvol.add_argument('tank_id', type=int, help='Tank ID (1-99)')
    p_setvol.add_argument('volume', type=float, help='New volume in gallons')
    p_setvol.set_defaults(func=cmd_set_volume)

    # raw command
    p_raw = subparsers.add_parser('raw', help='Send raw TLS-350 command')
    p_raw.add_argument('command', help='Raw TLS-350 command (e.g., I20100)')
    p_raw.set_defaults(func=cmd_raw)

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command given
    if not args.command:
        parser.print_help()
        return 0

    # Create client and execute command
    client = ATGClient(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        verbose=args.verbose
    )

    return args.func(client, args)


if __name__ == '__main__':
    sys.exit(main())
