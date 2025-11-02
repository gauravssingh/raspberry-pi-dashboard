"""MQTT client for controlling Tasmota ESP32 devices"""
import json
import logging
import threading
import time
from typing import Dict, List, Optional, Callable
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class TasmotaDevice:
    """Represents a Tasmota device"""
    
    def __init__(self, name: str, topic: str, device_type: str = "generic"):
        """
        Initialize a Tasmota device
        
        Args:
            name: Friendly name for the device
            topic: MQTT topic prefix for the device (e.g., "tasmota_bedroom")
            device_type: Type of device (switch, sensor, light, etc.)
        """
        self.name = name
        self.topic = topic
        self.device_type = device_type
        self.status = {}
        self.last_seen = None
        self.online = False
    
    def update_status(self, status_data: dict):
        """Update device status from MQTT message"""
        self.status.update(status_data)
        self.last_seen = time.time()
        self.online = True
    
    def to_dict(self) -> dict:
        """Convert device to dictionary"""
        return {
            'name': self.name,
            'topic': self.topic,
            'device_type': self.device_type,
            'status': self.status,
            'last_seen': self.last_seen,
            'online': self.online
        }


class MQTTTasmotaClient:
    """MQTT client for Tasmota device control"""
    
    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883,
                 username: str = None, password: str = None):
        """
        Initialize MQTT client for Tasmota devices
        
        Args:
            broker_host: MQTT broker hostname/IP
            broker_port: MQTT broker port (default: 1883)
            username: MQTT username (optional)
            password: MQTT password (optional)
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        
        self.client = mqtt.Client(client_id="rpi_dashboard", clean_session=True)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        # Set username/password if provided
        if username and password:
            self.client.username_pw_set(username, password)
        
        self.devices: Dict[str, TasmotaDevice] = {}
        self.connected = False
        self.connection_lock = threading.Lock()
        self.message_callbacks: List[Callable] = []
        
        logger.info(f"MQTT client initialized for broker {broker_host}:{broker_port}")
    
    def add_device(self, name: str, topic: str, device_type: str = "generic"):
        """
        Add a Tasmota device to monitor/control
        
        Args:
            name: Friendly name for the device
            topic: MQTT topic prefix for the device
            device_type: Type of device
        """
        device = TasmotaDevice(name, topic, device_type)
        self.devices[topic] = device
        
        # Subscribe to device topics if connected
        if self.connected:
            self._subscribe_device(topic)
        
        logger.info(f"Added Tasmota device: {name} ({topic})")
        return device
    
    def remove_device(self, topic: str):
        """Remove a device from monitoring"""
        if topic in self.devices:
            if self.connected:
                # Unsubscribe from device topics
                self.client.unsubscribe(f"{topic}/tele/#")
                self.client.unsubscribe(f"{topic}/stat/#")
            
            del self.devices[topic]
            logger.info(f"Removed device with topic: {topic}")
            return True
        return False
    
    def get_devices(self) -> List[dict]:
        """Get list of all devices"""
        return [device.to_dict() for device in self.devices.values()]
    
    def get_device(self, topic: str) -> Optional[dict]:
        """Get specific device by topic"""
        if topic in self.devices:
            return self.devices[topic].to_dict()
        return None
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            logger.info(f"Connecting to MQTT broker at {self.broker_host}:{self.broker_port}")
            self.client.connect(self.broker_host, self.broker_port, keepalive=60)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker")
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connected to broker"""
        if rc == 0:
            self.connected = True
            logger.info("Connected to MQTT broker successfully")
            
            # Subscribe to all device topics
            for topic in self.devices.keys():
                self._subscribe_device(topic)
            
            # Subscribe to discovery topics (for auto-discovery)
            self.client.subscribe("tasmota/discovery/#")
        else:
            logger.error(f"Failed to connect to MQTT broker, return code: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from broker"""
        self.connected = False
        if rc != 0:
            logger.warning(f"Unexpected disconnect from MQTT broker (code: {rc})")
        else:
            logger.info("Disconnected from MQTT broker")
    
    def _subscribe_device(self, topic: str):
        """Subscribe to device telemetry and status topics"""
        # Subscribe to telemetry (sensor data, status updates)
        self.client.subscribe(f"{topic}/tele/#")
        # Subscribe to status (command results)
        self.client.subscribe(f"{topic}/stat/#")
        logger.debug(f"Subscribed to topics for {topic}")
    
    def _on_message(self, client, userdata, msg):
        """Callback when message received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            logger.debug(f"Received MQTT message - Topic: {topic}, Payload: {payload}")
            
            # Parse device topic
            parts = topic.split('/')
            if len(parts) >= 2:
                device_topic = parts[0]
                
                # Check if this is a known device
                if device_topic in self.devices:
                    device = self.devices[device_topic]
                    
                    # Try to parse JSON payload
                    try:
                        data = json.loads(payload)
                    except json.JSONDecodeError:
                        data = {'raw': payload}
                    
                    # Update device status
                    device.update_status({
                        'last_message': data,
                        'last_topic': topic
                    })
                    
                    # Handle specific message types
                    if '/tele/STATE' in topic:
                        # Telemetry state update
                        device.update_status(data)
                    elif '/tele/SENSOR' in topic:
                        # Sensor data
                        device.update_status({'sensors': data})
                    elif '/stat/POWER' in topic or '/stat/RESULT' in topic:
                        # Power state or command result
                        device.update_status({'power': data})
                    elif '/tele/LWT' in topic:
                        # Last Will and Testament (online/offline status)
                        device.online = (payload.lower() == 'online')
                    
                    # Call any registered callbacks
                    for callback in self.message_callbacks:
                        try:
                            callback(device_topic, topic, data)
                        except Exception as e:
                            logger.error(f"Error in message callback: {e}")
        
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")
    
    def publish_command(self, device_topic: str, command: str, payload: str = ""):
        """
        Send command to Tasmota device
        
        Args:
            device_topic: Device topic prefix
            command: Tasmota command (e.g., "Power", "Power1", "Status")
            payload: Command payload (optional)
        
        Returns:
            bool: True if command was sent successfully
        """
        if not self.connected:
            logger.error("Cannot send command: Not connected to MQTT broker")
            return False
        
        topic = f"{device_topic}/cmnd/{command}"
        try:
            result = self.client.publish(topic, payload)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Published command to {topic}: {payload}")
                return True
            else:
                logger.error(f"Failed to publish command to {topic}")
                return False
        except Exception as e:
            logger.error(f"Error publishing command: {e}")
            return False
    
    # Convenience methods for common Tasmota commands
    
    def power_on(self, device_topic: str, relay: int = None):
        """Turn on device power (relay)"""
        command = f"Power{relay}" if relay else "Power"
        return self.publish_command(device_topic, command, "ON")
    
    def power_off(self, device_topic: str, relay: int = None):
        """Turn off device power (relay)"""
        command = f"Power{relay}" if relay else "Power"
        return self.publish_command(device_topic, command, "OFF")
    
    def power_toggle(self, device_topic: str, relay: int = None):
        """Toggle device power (relay)"""
        command = f"Power{relay}" if relay else "Power"
        return self.publish_command(device_topic, command, "TOGGLE")
    
    def get_status(self, device_topic: str, status_type: int = 0):
        """
        Request status from device
        
        Args:
            device_topic: Device topic prefix
            status_type: Status type (0=all, 1=device params, 2=firmware, etc.)
        """
        return self.publish_command(device_topic, "Status", str(status_type))
    
    def set_dimmer(self, device_topic: str, level: int):
        """Set dimmer level (0-100)"""
        return self.publish_command(device_topic, "Dimmer", str(level))
    
    def set_color(self, device_topic: str, color: str):
        """Set RGB color (hex format: RRGGBB)"""
        return self.publish_command(device_topic, "Color", color)
    
    def restart(self, device_topic: str):
        """Restart the device"""
        return self.publish_command(device_topic, "Restart", "1")
    
    def add_message_callback(self, callback: Callable):
        """Add a callback function for MQTT messages"""
        self.message_callbacks.append(callback)
    
    def is_connected(self) -> bool:
        """Check if connected to MQTT broker"""
        return self.connected


# Global MQTT client instance
_mqtt_client: Optional[MQTTTasmotaClient] = None


def get_mqtt_client() -> Optional[MQTTTasmotaClient]:
    """Get the global MQTT client instance"""
    return _mqtt_client


def init_mqtt_client(broker_host: str, broker_port: int = 1883,
                     username: str = None, password: str = None) -> MQTTTasmotaClient:
    """Initialize the global MQTT client"""
    global _mqtt_client
    
    if _mqtt_client is not None:
        logger.warning("MQTT client already initialized")
        return _mqtt_client
    
    _mqtt_client = MQTTTasmotaClient(broker_host, broker_port, username, password)
    logger.info("Global MQTT client initialized")
    
    return _mqtt_client


def shutdown_mqtt_client():
    """Shutdown the global MQTT client"""
    global _mqtt_client
    
    if _mqtt_client is not None:
        _mqtt_client.disconnect()
        _mqtt_client = None
        logger.info("Global MQTT client shutdown")

