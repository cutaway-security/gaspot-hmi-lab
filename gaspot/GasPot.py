#!/usr/bin/env python3
"""
GasPot - TLS-350 ATG Simulator for ICS/OT Training

Simulates a Veeder-Root TLS-350 Automatic Tank Gauge for a Natural Gas
Distribution Terminal with 6 tanks (3 Natural Gas, 2 Diesel, 1 Water).

Based on original GasPot by Kyle Wilhoit and Stephen Hilt (CC0 License).
Modified for educational use in ICS/OT cybersecurity training.

Supported Commands:
    I20100 - In-Tank Inventory Report
    I20200 - In-Tank Delivery Report
    I20300 - In-Tank Leak Detect Report
    I20400 - In-Tank Shift Report
    I20500 - In-Tank Status Report
    I20600 - Pressure Sensor Report (custom)
    S6020x - Set tank name (x = tank number 1-6, or 0 for all)
    S60210 - Set tank volume (format: S60210:TANK:VALUE)
    S60220 - Set tank pressure (format: S60220:TANK:VALUE)
"""

import socket
import select
import datetime
import random
import configparser
import threading
import time
import sys
import os


class Tank:
    """Represents a single tank with its properties and fluctuation behavior."""

    def __init__(self, tank_id: int, config: configparser.ConfigParser):
        section = f'tank{tank_id}'
        self.tank_id = tank_id
        self.name = config.get(section, 'name').ljust(20)[:20]
        self.tank_type = config.get(section, 'type')
        self.capacity = config.getfloat(section, 'capacity')
        self.capacity_unit = config.get(section, 'capacity_unit')
        self.has_pressure = config.getboolean(section, 'has_pressure')
        self.fluctuation_type = config.get(section, 'fluctuation')

        # Initialize values
        self.volume = config.getfloat(section, 'initial_volume')
        self.pressure = config.getfloat(section, 'initial_pressure') if self.has_pressure else 0.0

        # Get parameters
        params = config['parameters']
        self.decimal_sep = params.get('decimal_separator', '.')

        # Set temperature range based on tank type
        if self.tank_type == 'NATURAL_GAS':
            self.temp_low = params.getint('ng_temp_low')
            self.temp_high = params.getint('ng_temp_high')
            self.water_low = params.getfloat('ng_water_low')
            self.water_high = params.getfloat('ng_water_high')
        elif self.tank_type == 'DIESEL':
            self.temp_low = params.getint('diesel_temp_low')
            self.temp_high = params.getint('diesel_temp_high')
            self.water_low = params.getfloat('diesel_water_low')
            self.water_high = params.getfloat('diesel_water_high')
        else:  # WATER
            self.temp_low = params.getint('water_temp_low')
            self.temp_high = params.getint('water_temp_high')
            self.water_low = 0.0
            self.water_high = 0.0

        # Fluctuation parameters
        self.high_range = params.getint('high_fluctuation_range')
        self.medium_range = params.getint('medium_fluctuation_range')
        self.low_range = params.getint('low_fluctuation_range')
        self.decrease_rate = params.getint('decrease_rate')
        self.sawtooth_increase = params.getint('sawtooth_increase')
        self.sawtooth_threshold = params.getfloat('sawtooth_threshold')

        # Initialize dynamic values
        self.temperature = random.uniform(self.temp_low, self.temp_high)
        self.water_content = random.uniform(self.water_low, self.water_high)
        self.sawtooth_direction = 1  # 1 = increasing, -1 = decreasing

    @property
    def tc_volume(self) -> float:
        """Temperature-corrected volume."""
        # Slight adjustment based on temperature
        correction = 1.0 + (self.temperature - 60) * 0.0001
        return self.volume * correction

    @property
    def ullage(self) -> float:
        """Unfilled space in tank."""
        return self.capacity - self.volume

    @property
    def height(self) -> float:
        """Product height based on fill percentage."""
        fill_pct = self.volume / self.capacity
        if self.tank_type == 'NATURAL_GAS':
            max_height = 96.0  # inches
        elif self.tank_type == 'DIESEL':
            max_height = 96.0
        else:
            max_height = 120.0
        return fill_pct * max_height

    @property
    def pressure_status(self) -> str:
        """Pressure status string."""
        if not self.has_pressure:
            return "ATMOSPHERIC"
        if self.pressure < 300:
            return "LOW"
        elif self.pressure > 700:
            return "HIGH"
        return "NORMAL"

    def fluctuate(self):
        """Apply fluctuation based on tank's fluctuation type."""
        if self.fluctuation_type == 'high':
            delta = random.uniform(-self.high_range, self.high_range)
            self.volume = max(0, min(self.capacity, self.volume + delta))
            if self.has_pressure:
                self.pressure += random.uniform(-5, 5)

        elif self.fluctuation_type == 'medium':
            delta = random.uniform(-self.medium_range, self.medium_range)
            self.volume = max(0, min(self.capacity, self.volume + delta))
            if self.has_pressure:
                self.pressure += random.uniform(-2, 2)

        elif self.fluctuation_type == 'low':
            delta = random.uniform(-self.low_range, self.low_range)
            self.volume = max(0, min(self.capacity, self.volume + delta))
            if self.has_pressure:
                self.pressure += random.uniform(-1, 1)

        elif self.fluctuation_type == 'decrease':
            self.volume = max(0, self.volume - random.uniform(0, self.decrease_rate))

        elif self.fluctuation_type == 'sawtooth':
            if self.sawtooth_direction == 1:
                self.volume += self.sawtooth_increase
                if self.volume >= self.capacity * self.sawtooth_threshold:
                    self.sawtooth_direction = -1
            else:
                self.volume -= self.sawtooth_increase * 0.5
                if self.volume <= self.capacity * 0.3:
                    self.sawtooth_direction = 1
            self.volume = max(0, min(self.capacity, self.volume))

        # Temperature fluctuation (all tanks)
        self.temperature += random.uniform(-0.5, 0.5)
        self.temperature = max(self.temp_low, min(self.temp_high, self.temperature))

        # Clamp pressure
        if self.has_pressure:
            self.pressure = max(200, min(800, self.pressure))

    def format_inventory_line(self) -> str:
        """Format tank data for I20100 inventory report."""
        return (f"  {self.tank_id}  {self.name}"
                f"{self.volume:>10.0f}{self.tc_volume:>10.0f}"
                f"{self.ullage:>9.0f}{self.height:>9.2f}"
                f"{self.water_content:>9.1f}{self.temperature:>8.2f}")

    def format_pressure_line(self) -> str:
        """Format tank data for I20600 pressure report."""
        if self.has_pressure:
            return f"  {self.tank_id}  {self.name}{self.pressure:>10.1f} PSI  {self.pressure_status}"
        else:
            return f"  {self.tank_id}  {self.name}       N/A      {self.pressure_status}"


class GasPotServer:
    """TLS-350 ATG Simulator Server."""

    def __init__(self, config_file: str = 'config.ini'):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(config_file):
            print(f"Configuration file not found: {config_file}")
            sys.exit(1)
        self.config.read(config_file)

        # Server settings
        self.host = self.config.get('host', 'tcp_ip')
        self.port = self.config.getint('host', 'tcp_port')
        self.buffer_size = self.config.getint('host', 'buffer_size')
        self.station_name = self.config.get('station', 'name')

        # Initialize tanks
        self.tanks = {}
        for i in range(1, 7):
            self.tanks[i] = Tank(i, self.config)

        # Timestamps for reports
        self.start_time = datetime.datetime.utcnow()
        self.fill_stop = self.start_time - datetime.timedelta(minutes=303)
        self.fill_start = self.start_time - datetime.timedelta(minutes=313)

        # Fluctuation thread
        self.running = False
        self.fluctuation_thread = None

    def start_fluctuation(self):
        """Start background fluctuation thread."""
        self.running = True
        interval = self.config.getint('parameters', 'fluctuation_interval')

        def fluctuate_loop():
            while self.running:
                for tank in self.tanks.values():
                    tank.fluctuate()
                time.sleep(interval)

        self.fluctuation_thread = threading.Thread(target=fluctuate_loop, daemon=True)
        self.fluctuation_thread.start()

    def stop_fluctuation(self):
        """Stop fluctuation thread."""
        self.running = False

    def get_timestamp(self) -> str:
        """Get formatted timestamp for reports."""
        now = datetime.datetime.utcnow()
        return now.strftime('%b %d, %Y  %I:%M %p').upper()

    def I20100(self) -> str:
        """In-Tank Inventory Report."""
        lines = [
            f"\nI20100",
            f"{self.get_timestamp()}",
            f"",
            f"     {self.station_name}",
            f"",
            f"",
            f"IN-TANK INVENTORY",
            f"",
            f"TANK PRODUCT             VOLUME TC VOLUME   ULLAGE   HEIGHT    WATER     TEMP"
        ]
        for tank in self.tanks.values():
            lines.append(tank.format_inventory_line())
        lines.append("")
        return "\n".join(lines)

    def I20200(self) -> str:
        """In-Tank Delivery Report."""
        tank = self.tanks[1]
        vol_before = tank.volume - 500
        vol_after = tank.volume
        height_before = tank.height - 10

        lines = [
            f"\nI20200",
            f"{self.get_timestamp()}",
            f"",
            f"",
            f"     {self.station_name}",
            f"",
            f"",
            f"DELIVERY REPORT",
            f"",
            f"T 1:{tank.name}",
            f"INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT",
            f"",
            f"      END: {self.fill_stop.strftime('%m/%d/%Y %H:%M')}"
            f"         {vol_after:>7.0f}       {tank.tc_volume:>7.0f}"
            f"   {tank.water_content:>4.1f}      {tank.temperature:>5.1f}   {tank.height:>6.2f}",
            f"    START: {self.fill_start.strftime('%m/%d/%Y %H:%M')}"
            f"         {vol_before:>7.0f}       {vol_before * 0.99:>7.0f}"
            f"   {tank.water_content:>4.1f}      {tank.temperature:>5.1f}   {height_before:>6.2f}",
            f"   AMOUNT:                          {500:>7.0f}       {495:>7.0f}",
            f""
        ]
        return "\n".join(lines)

    def I20300(self) -> str:
        """In-Tank Leak Detect Report."""
        lines = [
            f"\nI20300",
            f"{self.get_timestamp()}",
            f"",
            f"     {self.station_name}",
            f"",
        ]
        for tank in self.tanks.values():
            lines.extend([
                f"",
                f"TANK {tank.tank_id}    {tank.name}",
                f"    TEST STATUS: OFF",
                f"LEAK DATA NOT AVAILABLE ON THIS TANK",
            ])
        lines.append("")
        return "\n".join(lines)

    def I20400(self) -> str:
        """In-Tank Shift Report."""
        now = datetime.datetime.utcnow()
        shift_start = now - datetime.timedelta(hours=8)

        lines = [
            f"\nI20400",
            f"{self.get_timestamp()}",
            f"",
            f"     {self.station_name}",
            f"",
            f"",
            f"SHIFT REPORT",
            f"",
            f"SHIFT 1 TIME: {shift_start.strftime('%m/%d/%Y %H:%M')}",
            f"",
            f"TANK PRODUCT             VOLUME TC VOLUME   ULLAGE   HEIGHT    WATER     TEMP"
        ]
        for tank in self.tanks.values():
            lines.append(tank.format_inventory_line())
        lines.append("")
        return "\n".join(lines)

    def I20500(self) -> str:
        """In-Tank Status Report."""
        lines = [
            f"\nI20500",
            f"{self.get_timestamp()}",
            f"",
            f"     {self.station_name}",
            f"",
            f"",
            f"TANK STATUS REPORT",
            f"",
        ]
        for tank in self.tanks.values():
            fill_pct = (tank.volume / tank.capacity) * 100
            if fill_pct < 20:
                status = "LOW LEVEL"
            elif fill_pct > 90:
                status = "HIGH LEVEL"
            else:
                status = "NORMAL"
            lines.append(f"TANK {tank.tank_id}  {tank.name}  {status}")
        lines.append("")
        return "\n".join(lines)

    def I20600(self) -> str:
        """Pressure Sensor Report (custom command for gas tanks)."""
        lines = [
            f"\nI20600",
            f"{self.get_timestamp()}",
            f"",
            f"     {self.station_name}",
            f"",
            f"",
            f"PRESSURE SENSOR REPORT",
            f"",
            f"TANK PRODUCT             PRESSURE    STATUS"
        ]
        for tank in self.tanks.values():
            lines.append(tank.format_pressure_line())
        lines.append("")
        return "\n".join(lines)

    def handle_s6020x(self, cmd: str, data: bytes) -> str:
        """Handle S6020x tank name change commands."""
        tank_num = cmd[5]  # '0'-'6'

        # Extract new name from data
        try:
            parts = data.decode(errors='replace').split(cmd)
            if len(parts) < 2:
                return "9999FF1B\n"
            new_name = parts[1].strip('\r\n\x00')[:20].ljust(20)
        except (IndexError, ValueError):
            return "9999FF1B\n"

        if tank_num == '0':
            # Set all tanks
            for tank in self.tanks.values():
                tank.name = new_name
        elif tank_num in '123456':
            self.tanks[int(tank_num)].name = new_name
        else:
            return "9999FF1B\n"

        return ""  # Success - no response per protocol

    def handle_s60210(self, data: bytes) -> str:
        """Handle S60210 set volume command (format: S60210:TANK:VALUE)."""
        try:
            decoded = data.decode(errors='replace').strip('\r\n\x00')
            parts = decoded.split(':')
            if len(parts) != 3 or not parts[0].startswith('S60210'):
                return "9999FF1B\n"
            tank_num = int(parts[1])
            value = float(parts[2])
            if tank_num not in self.tanks:
                return "9999FF1B\n"
            tank = self.tanks[tank_num]
            tank.volume = max(0, min(tank.capacity, value))
            return ""
        except (ValueError, IndexError):
            return "9999FF1B\n"

    def handle_s60220(self, data: bytes) -> str:
        """Handle S60220 set pressure command (format: S60220:TANK:VALUE)."""
        try:
            decoded = data.decode(errors='replace').strip('\r\n\x00')
            parts = decoded.split(':')
            if len(parts) != 3 or not parts[0].startswith('S60220'):
                return "9999FF1B\n"
            tank_num = int(parts[1])
            value = float(parts[2])
            if tank_num not in self.tanks:
                return "9999FF1B\n"
            tank = self.tanks[tank_num]
            if not tank.has_pressure:
                return "9999FF1B\n"
            tank.pressure = max(0, min(1000, value))
            return ""
        except (ValueError, IndexError):
            return "9999FF1B\n"

    def process_command(self, data: bytes) -> str:
        """Process incoming TLS-350 command."""
        # Validate command prefix (^A or 0x01)
        if len(data) < 2:
            return "9999FF1B\n"

        if data[0:2] == b"^A":
            cmd = data[2:8].decode(errors='replace')
            raw_data = data[2:]
        elif data[0:1] == b"\x01":
            cmd = data[1:7].decode(errors='replace')
            raw_data = data[1:]
        else:
            return "9999FF1B\n"

        # Command dispatch
        commands = {
            "I20100": self.I20100,
            "I20200": self.I20200,
            "I20300": self.I20300,
            "I20400": self.I20400,
            "I20500": self.I20500,
            "I20600": self.I20600,
        }

        if cmd in commands:
            return commands[cmd]()
        elif cmd.startswith("S6020"):
            return self.handle_s6020x(cmd, raw_data)
        elif cmd.startswith("S60210"):
            return self.handle_s60210(raw_data)
        elif cmd.startswith("S60220"):
            return self.handle_s60220(raw_data)
        else:
            return "9999FF1B\n"

    def run(self):
        """Run the server."""
        # Create socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setblocking(False)

        try:
            server.bind((self.host, self.port))
            server.listen(5)
            print(f"GasPot TLS-350 Simulator listening on {self.host}:{self.port}")
        except socket.error as e:
            print(f"Failed to bind to {self.host}:{self.port}: {e}")
            sys.exit(1)

        # Start fluctuation
        self.start_fluctuation()

        active_sockets = [server]

        try:
            while True:
                readable, _, exceptional = select.select(
                    active_sockets, [], active_sockets, 1.0
                )

                for sock in readable:
                    if sock is server:
                        # New connection
                        conn, addr = server.accept()
                        conn.setblocking(False)
                        active_sockets.append(conn)
                        print(f"Connection from: {addr[0]}")
                    else:
                        # Existing connection
                        try:
                            data = sock.recv(self.buffer_size)
                            if not data:
                                active_sockets.remove(sock)
                                sock.close()
                                continue

                            # Read until newline or null
                            while not (b'\n' in data or b'\x00' in data):
                                more = sock.recv(self.buffer_size)
                                if not more:
                                    break
                                data += more

                            response = self.process_command(data)
                            if response:
                                sock.send(response.encode(errors='replace'))

                            active_sockets.remove(sock)
                            sock.close()

                        except (ConnectionResetError, BrokenPipeError):
                            if sock in active_sockets:
                                active_sockets.remove(sock)
                            sock.close()
                        except Exception as e:
                            print(f"Error handling connection: {e}")
                            if sock in active_sockets:
                                active_sockets.remove(sock)
                            sock.close()

                for sock in exceptional:
                    if sock in active_sockets:
                        active_sockets.remove(sock)
                    sock.close()

        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.stop_fluctuation()
            server.close()


if __name__ == "__main__":
    config_file = os.environ.get('GASPOT_CONFIG', 'config.ini')
    server = GasPotServer(config_file)
    server.run()
