"""Flask Routes for GasPot HMI Dashboard

Provides web endpoints for:
- Main dashboard with tank overview
- Trends page with historical charts
- Alarms page with alarm history
- API endpoints for AJAX data refresh
"""

from flask import Blueprint, render_template, jsonify, current_app
from datetime import datetime, timedelta
from sqlalchemy import desc, text

from app import get_db_session
from app.models import Tank, TankReading, Alarm
from app.atg_client import ATGClient

bp = Blueprint('main', __name__)


def get_atg_client() -> ATGClient:
    """Get ATG client with current configuration."""
    return ATGClient(
        host=current_app.config['GASPOT_HOST'],
        port=current_app.config['GASPOT_PORT']
    )


@bp.route('/health')
def health():
    """Health check endpoint for container orchestration."""
    return 'OK', 200


@bp.route('/')
def dashboard():
    """Main dashboard showing current tank status."""
    session = get_db_session()

    try:
        # Get tank configuration
        tanks = session.query(Tank).order_by(Tank.tank_id).all()

        # Get live data from GasPot
        atg = get_atg_client()
        live_data = {}
        atg_connected = False

        try:
            readings = atg.poll_all()
            atg_connected = True
            for reading in readings:
                live_data[reading.tank_id] = {
                    'volume': reading.volume,
                    'temperature': reading.temperature,
                    'pressure': reading.pressure,
                    'product_name': reading.product_name
                }
        except Exception:
            # If ATG unavailable, use latest from database
            for tank in tanks:
                latest = session.query(TankReading).filter(
                    TankReading.tank_id == tank.tank_id
                ).order_by(desc(TankReading.timestamp)).first()

                if latest:
                    live_data[tank.tank_id] = {
                        'volume': float(latest.volume) if latest.volume else 0,
                        'temperature': float(latest.temperature) if latest.temperature else 0,
                        'pressure': float(latest.pressure) if latest.pressure else None,
                        'product_name': tank.product_name
                    }

        # Get active alarms count
        active_alarms_count = session.query(Alarm).filter(
            Alarm.acknowledged == False
        ).count()

        return render_template('dashboard.html',
                               tanks=tanks,
                               live_data=live_data,
                               atg_connected=atg_connected,
                               active_alarms_count=active_alarms_count,
                               last_update=datetime.now())
    finally:
        session.close()


@bp.route('/trends')
def trends():
    """Historical trends page with charts."""
    session = get_db_session()

    try:
        tanks = session.query(Tank).order_by(Tank.tank_id).all()

        # Get active alarms count for nav badge
        active_alarms_count = session.query(Alarm).filter(
            Alarm.acknowledged == False
        ).count()

        return render_template('trends.html',
                               tanks=tanks,
                               active_alarms_count=active_alarms_count)
    finally:
        session.close()


@bp.route('/alarms')
def alarms():
    """Alarm history page."""
    session = get_db_session()

    try:
        # Get all alarms, most recent first
        all_alarms = session.query(Alarm).order_by(
            desc(Alarm.timestamp)
        ).limit(100).all()

        # Get active (unacknowledged) alarms
        active_alarms = session.query(Alarm).filter(
            Alarm.acknowledged == False
        ).order_by(desc(Alarm.timestamp)).all()

        # Count for nav badge
        active_alarms_count = len(active_alarms)

        tanks = session.query(Tank).order_by(Tank.tank_id).all()
        tank_names = {t.tank_id: t.product_name for t in tanks}

        return render_template('alarms.html',
                               all_alarms=all_alarms,
                               active_alarms=active_alarms,
                               active_alarms_count=active_alarms_count,
                               tank_names=tank_names)
    finally:
        session.close()


@bp.route('/api/live')
def api_live():
    """API endpoint for live tank data (AJAX refresh)."""
    atg = get_atg_client()

    try:
        readings = atg.poll_all()
        data = []
        for reading in readings:
            data.append({
                'tank_id': reading.tank_id,
                'product_name': reading.product_name,
                'volume': reading.volume,
                'temperature': reading.temperature,
                'pressure': reading.pressure,
                'timestamp': reading.timestamp.isoformat()
            })
        return jsonify({'status': 'ok', 'data': data, 'connected': True})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'connected': False})


@bp.route('/api/trends/<int:tank_id>')
def api_trends(tank_id: int):
    """API endpoint for historical trend data (Chart.js)."""
    session = get_db_session()

    try:
        # Get last 24 hours of readings for this tank
        since = datetime.now() - timedelta(hours=24)

        readings = session.query(TankReading).filter(
            TankReading.tank_id == tank_id,
            TankReading.timestamp >= since
        ).order_by(TankReading.timestamp).all()

        data = {
            'timestamps': [],
            'volume': [],
            'temperature': [],
            'pressure': []
        }

        for reading in readings:
            data['timestamps'].append(reading.timestamp.strftime('%H:%M'))
            data['volume'].append(float(reading.volume) if reading.volume else None)
            data['temperature'].append(float(reading.temperature) if reading.temperature else None)
            data['pressure'].append(float(reading.pressure) if reading.pressure else None)

        return jsonify({'status': 'ok', 'data': data})
    finally:
        session.close()


@bp.route('/api/alarms')
def api_alarms():
    """API endpoint for active alarms."""
    session = get_db_session()

    try:
        active = session.query(Alarm).filter(
            Alarm.acknowledged == False
        ).order_by(desc(Alarm.timestamp)).all()

        data = []
        for alarm in active:
            data.append({
                'id': alarm.id,
                'tank_id': alarm.tank_id,
                'alarm_type': alarm.alarm_type,
                'severity': alarm.severity,
                'message': alarm.message,
                'timestamp': alarm.timestamp.isoformat()
            })

        return jsonify({'status': 'ok', 'count': len(data), 'alarms': data})
    finally:
        session.close()


@bp.route('/api/poller')
def api_poller():
    """API endpoint for poller status."""
    from app.poller import get_poller

    poller = get_poller()
    if poller is None:
        return jsonify({'status': 'error', 'message': 'Poller not initialized'})

    return jsonify({'status': 'ok', 'poller': poller.status})
