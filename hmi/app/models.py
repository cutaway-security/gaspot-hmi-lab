"""SQLAlchemy Models for Historian Database

Maps to tables defined in historian/init.sql:
- tanks: Tank configuration (6 tanks)
- tank_readings: Time-series sensor data
- alarms: Alarm history
"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Tank(Base):
    """Tank configuration table."""
    __tablename__ = 'tanks'

    tank_id = Column(Integer, primary_key=True)
    product_name = Column(String(20), nullable=False)
    tank_type = Column(Enum('NATURAL_GAS', 'DIESEL', 'WATER'), nullable=False)
    max_capacity = Column(Numeric(10, 2), nullable=False)
    capacity_unit = Column(String(10), nullable=False)
    has_pressure = Column(Boolean, default=False)

    # Relationship to readings
    readings = relationship("TankReading", back_populates="tank")
    alarms = relationship("Alarm", back_populates="tank")

    @property
    def is_gas_tank(self) -> bool:
        """Check if this is a natural gas tank."""
        return self.tank_type == 'NATURAL_GAS'

    def __repr__(self):
        return f"<Tank {self.tank_id}: {self.product_name}>"


class TankReading(Base):
    """Tank readings time-series table."""
    __tablename__ = 'tank_readings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tank_id = Column(Integer, ForeignKey('tanks.tank_id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    volume = Column(Numeric(10, 2))
    tc_volume = Column(Numeric(10, 2))
    ullage = Column(Numeric(10, 2))
    height = Column(Numeric(6, 2))
    water_content = Column(Numeric(6, 2))
    temperature = Column(Numeric(5, 2))
    pressure = Column(Numeric(6, 2))

    # Relationship to tank
    tank = relationship("Tank", back_populates="readings")

    def __repr__(self):
        return f"<TankReading tank={self.tank_id} time={self.timestamp}>"


class Alarm(Base):
    """Alarm history table."""
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tank_id = Column(Integer, ForeignKey('tanks.tank_id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    alarm_type = Column(String(50), nullable=False)
    severity = Column(Enum('INFO', 'WARNING', 'CRITICAL'), nullable=False)
    message = Column(String(255))
    acknowledged = Column(Boolean, default=False)

    # Relationship to tank
    tank = relationship("Tank", back_populates="alarms")

    @property
    def severity_class(self) -> str:
        """Return CSS class for severity."""
        return {
            'INFO': 'alarm-info',
            'WARNING': 'alarm-warning',
            'CRITICAL': 'alarm-critical'
        }.get(self.severity, 'alarm-info')

    def __repr__(self):
        return f"<Alarm {self.severity}: {self.alarm_type}>"
