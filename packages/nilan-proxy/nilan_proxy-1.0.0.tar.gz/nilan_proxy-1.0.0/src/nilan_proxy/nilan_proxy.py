import asyncio
from collections.abc import Callable
from enum import Enum
from random import randint
import socket
import threading
import time
from typing import Dict, List, Sequence
import logging

from nilan_proxy.protocol.command_builder import NilanProxyCommandBuilderWriteArgs


from .models import ( NilanProxyDatapointKey, NilanProxySetpointKey, NilanProxyDatapoint, NilanProxySetpoint)
from .nilan_proxy_modeladapter import NilanProxyModelAdapter
from .protocol import (ProxyPacketType,  ProxyPayloadIPX, ProxyPayloadCrypt, ProxyPayloadCP_ID,  ProxyPacketBuilder, NilanProxyCommandBuilder, NilanProxyCommandBuilderReadArgs)

from .const import ( SOCKET_TIMEOUT, SOCKET_MAXSIZE, DATAPOINT_UPDATEINTERVAL, SETPOINT_UPDATEINTERVAL, SECONDS_UNTILRECONNECT, DISCOVERY_PORT)

_LOGGER = logging.getLogger(__name__)

class NilanProxyConnectionErrorType(Enum):
    TIMEOUT = "timeout"
    AUTHENTICATION_ERROR = "authentication_error"
    UNSUPPORTED_MODEL = "unsupported_model"

class NilanProxy():
    _client_id:bytes = randint(0,0xffffffff).to_bytes(4, 'big') # Our client ID can be anything.
    _server_id:bytes = b'\x00\x00\x00\x00' # This is our ID optained from the uNabto service on device.

    _authorized_email:str = ""
    _device_id:str|None = None
    _device_ip:str|None = None
    _device_model:int|None = None
    _device_number:int|None = None
    _device_port:int = 5570
    _slave_device_model:int|None = None
    _slave_device_number:int|None = None

    _model_adapter:NilanProxyModelAdapter|None = None

    _is_connected:bool = False
    _connection_error:NilanProxyConnectionErrorType|None = None
    _last_response:float = 0
    _last_dataupdate:float = 0
    _last_setpointupdate:float = 0

    _socket = None
    _listen_thread = None
    _listen_thread_open = False
    _discovered_devices:Dict[str, tuple[str,int]] =  {}
    """tuple[int,int] = RefAddress from socket aka tuple(host, port)"""
    
    def __init__(self, authorized_email:str = "") -> None:
        self._authorized_email = authorized_email
        self.start_listening()
        return    
    
    def get_email(self): return self._authorized_email
    def set_email(self, email:str): self._authorized_email = email
    """set the email the system was configured with through the official application/app"""
    
    def is_connected(self): return self._is_connected
    def get_connection_error(self): return self._connection_error
    
    def get_device_id(self): return self._device_id
    def get_device_ip(self): return self._device_ip
    def get_device_model(self): return self._device_model
    def get_device_number(self): return self._device_number
    def get_device_port(self): return self._device_port
    def get_slave_device_model(self): return self._slave_device_model
    def get_slave_device_number(self): return self._slave_device_number
    def get_discovered_devices(self): return self._discovered_devices
    def get_device_manufacturer(self): return None if self._model_adapter is None else self._model_adapter.get_manufacturer()
    def get_loaded_model_name(self): return None if self._model_adapter is None else self._model_adapter.get_model_name()
    
    def set_device(self, device_id:str, device_ip:str|None=None, device_port:int|None=None) -> None:
        self._device_id = device_id
        if device_ip is None or device_port is None:
            self.retrieve_device_ip()
        else:
            self._device_ip = device_ip
            self._device_port = device_port
            self._discovered_devices[self._device_id] = (device_ip, device_port)
        
    def start_listening(self) -> bool:
        if self._listen_thread_open: return False
        if self._socket == None: 
            self.open_socket()
        self._listen_thread = threading.Thread(target=self._receive_thread)
        self._listen_thread_open = True
        self._listen_thread.start()
        return True
  
    def open_socket(self) -> None:
        if self._socket is not None: return
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allows for sending broadcasts
        self._socket.settimeout(SOCKET_TIMEOUT)
        self._socket.bind(("", 0))

    def stop_listening(self) -> None:
        self._listen_thread_open = False

    def close_socket(self) -> None:
        if self._socket is None: return
        self._socket.close()
        self._socket = None

    # Broadcasts a discovery packet. Any device listening should respond.
    def send_discovery(self, specificDevice:str|None = None) -> None: 
        if self._socket == None: return
        self._socket.sendto(ProxyPacketBuilder.build_discovery_packet(specificDevice), ("255.255.255.255", DISCOVERY_PORT))

    async def discover_devices(self, clear:bool=False) -> Dict[str, tuple[str, int]]:
        if clear: self._discovered_devices = {}
        self.send_discovery()
        await asyncio.sleep(0.5) # Allow for all devices to reply
        return self._discovered_devices

    def retrieve_device_ip(self) -> None:
        # Check if we already know the IP from earlier
        if self._device_id in self._discovered_devices:
            self._device_ip = self._discovered_devices[self._device_id][0]
            self._device_port = self._discovered_devices[self._device_id][1]
        else:
            self.send_discovery(self._device_id)

    def connect_to_device(self) -> bool:
        if self._socket == None:
            return False
        if self._listen_thread_open == False:
            return False
        self._connection_error = None
        ipx_payload = ProxyPayloadIPX()
        cp_id_payload = ProxyPayloadCP_ID()
        cp_id_payload.set_email(self._authorized_email)
        self._socket.sendto(ProxyPacketBuilder.build_packet(self._client_id, self._server_id, ProxyPacketType.U_CONNECT, 0, [ipx_payload, cp_id_payload]), (self._device_ip, self._device_port))
        return True

    async def wait_for_connection(self) -> None:
        """Wait for connection to be tried"""
        connection_timeout = time.time() + 3
        while self._connection_error is None and self._is_connected is False:
            if time.time() > connection_timeout:
                self._connection_error = NilanProxyConnectionErrorType.TIMEOUT                
            await asyncio.sleep(0.2)

    async def wait_for_discovery(self) -> bool:
        """Wait for discovery of ip to be done"""
        discovery_timeout = time.time() + 3
        while True:
            if self._device_id in self._discovered_devices and self._device_ip is not None:
                return True
            if time.time() > discovery_timeout:
                return False
            await asyncio.sleep(0.2)

    async def wait_for_data(self) -> bool:
        """Wait for data to be available"""
        data_timeout = time.time() + 12
        while True:
            if self._model_adapter is not None:
                if self._model_adapter.has_value(NilanProxyDatapointKey.TEMP_SUPPLY) and self._model_adapter.has_value(NilanProxySetpointKey.TEMP_TARGET):
                    return True
            if time.time() > data_timeout:
                return False
            await asyncio.sleep(0.2)

    def provides_value(self, key: NilanProxyDatapointKey|NilanProxySetpointKey) -> bool:
        if self._model_adapter is None: return False
        return self._model_adapter.provides_value(key)

    def has_value(self, key: NilanProxyDatapointKey|NilanProxySetpointKey) -> bool:
        if self._model_adapter is None: return False
        return self._model_adapter.has_value(key)
    
    def get_value(self, key: NilanProxyDatapointKey|NilanProxySetpointKey) -> float|int|None:
        if self._model_adapter is None: return None
        return self._model_adapter.get_value(key) 
    
    def get_setpoint_min_value(self, key: NilanProxySetpointKey) -> float|int|None:
        if self._model_adapter is None: return None
        return self._model_adapter.get_min_value(key)
    
    def get_setpoint_max_value(self, key: NilanProxySetpointKey) -> float|int|None:
        if self._model_adapter is None: return None
        return self._model_adapter.get_max_value(key)
    
    def get_unit_of_measure(self, key: NilanProxyDatapointKey|NilanProxySetpointKey) -> str|None:
        if self._model_adapter is None: return None
        return self._model_adapter.get_unit_of_measure(key)
    
    def get_setpoint_step(self, key: NilanProxySetpointKey) -> float|int:
        if self._model_adapter is None: return 1
        return self._model_adapter.get_setpoint_step(key)
    
    def notify_all_update_handlers(self) -> None:
        if self._model_adapter is not None:
            self._model_adapter.notify_all_update_handlers()
    
    def register_update_handler(self, key: NilanProxyDatapointKey|NilanProxySetpointKey, updateMethod: Callable[[float|int, float|int], None]) -> None:
        if self._model_adapter is not None:
            self._model_adapter.register_update_handler(key, updateMethod)
    
    def deregister_update_handler(self, key: NilanProxyDatapointKey|NilanProxySetpointKey, updateMethod: Callable[[float|int, float|int], None]) -> None:
        if self._model_adapter is not None:
            self._model_adapter.deregister_update_handler(key, updateMethod)
    
    def set_setpoint(self, setpointKey: NilanProxySetpointKey, new_value:float|int) -> bool:
        if self._socket is None: return False
        if self._model_adapter is None: return False
        setpoint = self._model_adapter.get_setpoint(setpointKey)
        if setpoint is None: return False
        new_value = self._model_adapter.parseToModbusValue(point=setpoint, value=new_value)
        if new_value < self._model_adapter.get_point_min(setpoint) or new_value > self._model_adapter.get_point_max(setpoint):
            _LOGGER.debug(f"Set setpoint: {setpointKey.value} failed, value invalid: {new_value}")
            return False
        Payload = ProxyPayloadCrypt()
        args=self._map_points_to_write_args([setpoint], new_value)
        Payload.set_data(NilanProxyCommandBuilder.build_setpoint_write_command(args))
        _LOGGER.debug(f"Set setpoint: {setpointKey.value} value = {new_value} (args={args})")
        self._socket.sendto(ProxyPacketBuilder().build_packet(self._client_id, self._server_id, ProxyPacketType.DATA, 3, [Payload]), (self._device_ip, self._device_port))
        self._last_dataupdate = time.time() - DATAPOINT_UPDATEINTERVAL + 1 # Ensure updates are check for next thread loop.
        self._last_setpointupdate = time.time() - SETPOINT_UPDATEINTERVAL + 1
        return True

    def _process_ping_payload(self, payload:bytes) -> None:
        self._device_number = int.from_bytes(payload[4:8], 'big')
        self._device_model = int.from_bytes(payload[8:12], 'big')
        self._slave_device_number = int.from_bytes(payload[16:20], 'big')
        self._slave_device_model = int.from_bytes(payload[20:24], 'big')
        _LOGGER.debug(f"Got model: {self._device_model} with device number: {self._device_number}, slavedevice number: {self._slave_device_number} and slavedevice model: {self._slave_device_model}")
        if NilanProxyModelAdapter.provides_model(self._device_model, self._device_number, self._slave_device_number, self._slave_device_model):
            self._is_connected = True
            _LOGGER.debug(f"Going to load model")
            self._model_adapter = NilanProxyModelAdapter(self._device_model, self._device_number, self._slave_device_number, self._slave_device_model)
            _LOGGER.debug(f"Loaded model for {self._model_adapter.get_model_name()}")
            self._send_data_state_request(100)
            self._send_setpoint_state_request(200)
        else:
            _LOGGER.error(f"No model available")
            self._connection_error = NilanProxyConnectionErrorType.UNSUPPORTED_MODEL

    def _process_received_message(self, message:bytes, address:tuple[str,int]) -> None:
        if message[0:4] == b'\x00\x80\x00\x01': # This might be a discovery packet response!
            discovery_response = message[19:len(message)]
            device_id_length = 0
            for b in discovery_response: # Loop until first string terminator
                if b == 0x00:
                    break
                device_id_length += 1
            device_id = discovery_response[0: device_id_length].decode("ascii")
            if "remote.lscontrol.dk" in device_id:
                # This is a valid reponse from a ProxyConnect device!
                # Add the device Id and IP to our list if not seen before.
                if device_id not in self._discovered_devices:
                    self._discovered_devices[device_id] = address
            if device_id == self._device_id:
                self._device_ip = address[0]
            return
        if message[0:4] != self._client_id: # Not a packet intented for us
            return
        self._last_response = time.time()
        packet_type = message[8].to_bytes(1, 'big')
        if (packet_type == ProxyPacketType.U_CONNECT.value):
            _LOGGER.debug("U_CONNECT response packet")
            if (message[20:24] == b'\x00\x00\x00\x01'):
                self._server_id = message[24:28]
                _LOGGER.debug('Connected, pinging to get model number')
                if not self._is_connected:
                    self._send_ping()
            else:
                _LOGGER.error("Received unsucessfull response")
                self._connection_error = NilanProxyConnectionErrorType.AUTHENTICATION_ERROR

        elif (packet_type == ProxyPacketType.DATA.value): # 0x16
            _LOGGER.debug(f"Data packet: {message[16]}")
            # We only care about data packets with crypt payload. 
            if message[16] == 54: # x36
                _LOGGER.debug("Packet with crypt payload!")
                length = int.from_bytes(message[18:20], 'big')
                payload = message[22:20+length]
                sequence_id = int.from_bytes(message[12:14], 'big')
                _LOGGER.debug(f'sequence_id: {sequence_id}, length: {length}, payload: {payload}')
                _LOGGER.debug(f''.join(r'\x'+hex(letter)[2:] for letter in payload))
                if sequence_id == 50: #50
                    self._process_ping_payload(payload)
                else:
                    if self._model_adapter is not None:
                        self._model_adapter.parse_data_response(sequence_id, payload)
                    if sequence_id == 100:                        
                        self._last_dataupdate = time.time()
                    if sequence_id == 200:                        
                        self._last_setpointupdate = time.time()
            else:
                _LOGGER.debug(f"Not an interresting data packet. payload: {message}")
        else:
            _LOGGER.debug("Unknown packet type. Ignoring")

    def _send_ping(self) -> None:
        if self._socket is None: return
        payload = ProxyPayloadCrypt()
        payload.set_data(NilanProxyCommandBuilder.build_ping_command())
        self._socket.sendto(ProxyPacketBuilder().build_packet(self._client_id, self._server_id, ProxyPacketType.DATA, 50, [payload]), (self._device_ip, self._device_port))

    def _send_data_state_request(self, sequence_id:int) -> None:
        if self._socket is None: return
        if self._model_adapter is None: return
        datalist = self._model_adapter.getDatapointRequestList(sequence_id)
        if datalist is None: return
        Payload = ProxyPayloadCrypt()
        readargs=self._map_points_to_read_args(datalist)
        Payload.set_data(NilanProxyCommandBuilder.build_datapoint_read_command(readargs))
        packet=ProxyPacketBuilder().build_packet(self._client_id, self._server_id, ProxyPacketType.DATA, sequence_id, [Payload])
        address=(self._device_ip, self._device_port)
        # _LOGGER.debug(f"Send data state request with args: {readargs}, packet: {packet}, payload: {Payload.data}, address:{address}")
        self._socket.sendto(packet, address)
    
    def _send_setpoint_state_request(self, sequence_id:int) -> None:
        if self._socket is None: return
        if self._model_adapter is None: return
        Payload = ProxyPayloadCrypt()
        datalist = self._model_adapter.get_setpoint_request_list(sequence_id)
        if datalist is None: return
        Payload.set_data(NilanProxyCommandBuilder.build_setpoint_read_command(self._map_points_to_read_args(datalist)))
        self._socket.sendto(ProxyPacketBuilder().build_packet(self._client_id, self._server_id, ProxyPacketType.DATA, sequence_id, [Payload]), (self._device_ip, self._device_port))

    def _handle_receive(self) -> None:
        if self._socket is None: return
        try:
            message, address = self._socket.recvfrom(SOCKET_MAXSIZE)
            if (len(message) < 16): # Not a valid packet
                return 
            self._process_received_message(message, address)
        except socket.timeout:  
            return

    def _receive_thread(self) -> None:
        while self._listen_thread_open:
            self._handle_receive()          
            if self._is_connected:
                if time.time() - self._last_dataupdate > DATAPOINT_UPDATEINTERVAL:
                    _LOGGER.debug("Sending data request..")
                    self._send_data_state_request(100)
                if time.time() - self._last_setpointupdate > SETPOINT_UPDATEINTERVAL:                    
                    self._send_setpoint_state_request(200)
                if time.time() - self._last_response > SECONDS_UNTILRECONNECT:
                    self.connect_to_device()
                    

    def _map_points_to_read_args(self, points: Sequence[NilanProxyDatapoint]) -> List[NilanProxyCommandBuilderReadArgs]:
        adapter = self._model_adapter
        if adapter is None: return []
        return list(map(lambda point: NilanProxyCommandBuilderReadArgs(read_obj=adapter.get_point_read_obj(point), read_address=adapter.get_point_read_address(point)), points))
    
    def _map_points_to_write_args(self, points: Sequence[NilanProxySetpoint], value:int) -> List[NilanProxyCommandBuilderWriteArgs]:
        adapter = self._model_adapter
        if adapter is None: return []
        return list(map(lambda point: NilanProxyCommandBuilderWriteArgs(write_obj=adapter.get_point_write_obj(point), write_address=adapter.get_point_write_address(point), value=value), points))
    