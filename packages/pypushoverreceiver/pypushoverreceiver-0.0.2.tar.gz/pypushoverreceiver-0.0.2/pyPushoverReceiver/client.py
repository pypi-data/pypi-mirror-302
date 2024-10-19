from __future__ import annotations

import logging
from typing import Any

import requests
import threading as thread
import time


from .websocket import WebsocketClient
from .exceptions import HTTPError, InvalidURL, PushoverApiError

_LOGGER = logging.getLogger(__name__)

API_ENDPOINT_LOGIN = "https://api.pushover.net/1/users/login.json"
API_ENDPOINT_DEVICE_REGISTRATION = "https://api.pushover.net/1/devices.json"
API_ENDPOINT_DOWNLOAD_MESSAGES =  "https://api.pushover.net/1/messages.json"

DEFAULT_TIMEOUT = 30

API_ENDPOINT_DELETE_MESSAGE_PREFIX =  "https://api.pushover.net/1/devices/"
API_ENDPOINT_DELETE_MESSAGE_SUFFIX = "/update_highest_message.json"
API_ENDPOINT_ACKNOWLEDGE_EMERGENCY_MESSAGE_PREFIX =  "https://api.pushover.net/1/receipts/"
API_ENDPOINT_ACKNOWLEDGE_EMERGENCY_MESSAGE_SUFFIX = "/acknowledge.json"

from .constants import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_USER_ID,
    CONF_SECRET,
    CONF_DEVICE_NAME,
    CONF_DEVICE_ID,
    CONF_AUTO_ACKNOWLEDGE_EMERGENCY,
)


class PushoverClient:
    """Initialize api client object."""

    def __init__(
        self,
        email: str,
        password: str,
        timeout: int = DEFAULT_TIMEOUT,
        user_id: str | None = None,
        secret: str | None = None,
        device_name: str = "pythonClient",
        device_id: str | None = None,
        auto_acknowledge_emergency: bool = False
    ) -> None:
        
        """Initialize the client object."""
        self.email = email
        self.password = password
        self.device_name = device_name
        self.os = "O"
        self.timeout = timeout
        self.user_id = user_id
        self.secret = secret
        self.device_id = device_id
        self.callback_to_hass = None
        self.auto_acknowledge_emergency = auto_acknowledge_emergency
        self.ready = False
        
        
    def login(self, two_factor_token = None) -> Any:
        
        
        # self.register_callback_to_hass(callback=self.test_test) ##test test test test!!!!!!!!!!!
        
        if self.user_id and self.secret and not self.device_id:
            #skip the login, already have tokens
            print("skipping login")
            self.password = None
            self.device_id = self.register_device()
            return self.build_auth_data_token()
        if self.device_id:
            print("skipping registration")
            return self.build_auth_data_token()
        
        data = {'email':self.email,
                  'password':self.password,
                }
        
        if two_factor_token is not None:
            data['twofa'] = two_factor_token
        
        try:
             
            resp_data = requests.post(url=API_ENDPOINT_LOGIN, data=data, timeout=DEFAULT_TIMEOUT)
            resp_data.raise_for_status()
        
        except requests.ConnectionError as err:
            raise InvalidURL(err)
        
        except requests.HTTPError as err:
            raise HTTPError(err)
        

        if resp_data.status_code == 412:
            print("Try again with TFA")
            #retry with TFA
            
        if not resp_data.ok:
            print("Error")
            #return with some error
            
        try:
            self.password = None
            self.user_id = resp_data.json()['id']
            self.secret = resp_data.json()['secret']
        except KeyError as err:
            raise PushoverApiError(err)
        
        self.device_id = self.register_device()
             

        return self.build_auth_data_token()




    def build_auth_data_token(self):
        auth_data = {CONF_EMAIL:self.email,
                          CONF_PASSWORD:self.password,
                          CONF_USER_ID:self.user_id,
                          CONF_SECRET:self.secret,
                          CONF_DEVICE_NAME:self.device_name,
                          CONF_DEVICE_ID:self.device_id,
                          CONF_AUTO_ACKNOWLEDGE_EMERGENCY:self.auto_acknowledge_emergency,
        }
        return auth_data
    
    def register_device(self):
        if self.device_id:
            #Already registered the device
            print("ALready registered, skipping register")
            return
        
        data = {'secret':self.secret,
                'name':self.device_name,
                'os':self.os,
                }
        try:
            resp_data = requests.post(url=API_ENDPOINT_DEVICE_REGISTRATION, data=data, timeout=DEFAULT_TIMEOUT)
            resp_data.raise_for_status()
        
        except requests.ConnectionError as err:
            raise InvalidURL(err)
        
        except requests.HTTPError as err:
            raise HTTPError(err) 
       
        if not resp_data.ok:
            print("SOmething is wrong") 
            #return with some error
        
        if not resp_data.json()['status']:
            print(resp_data.json()['error'])
            raise PushoverApiError(resp_data.json()['error'])
            
        try:
            return resp_data.json()['id']
        except KeyError as err:
            print("Keyerror")
            PushoverApiError(err)

            
    def download_undelivered_messages(self):
        
        data = {'secret':self.secret,
                'device_id':self.device_id,
        }
        
        try:
            resp_data = requests.get(url=API_ENDPOINT_DOWNLOAD_MESSAGES, data=data, timeout=DEFAULT_TIMEOUT)
            resp_data.raise_for_status()
        
        except requests.ConnectionError as err:
            raise InvalidURL(err)
        
        except requests.HTTPError as err:
            raise HTTPError(err) 
        
        if not resp_data.ok:
            print("SOmething is wrong")
            
        try:
            messages = resp_data.json()['messages']
        except KeyError as err:
            print("Keyerror")
            PushoverApiError(err)
            
            

        if not messages:
            return
        
        [highest_msg_id, processed_messages] = self.process_delivered_messages(in_messages=messages)
        
        
        if self.callback_to_hass:     
            self.callback_to_hass(processed_messages) 
        
        self.delete_messages(message_id=highest_msg_id)
       

        # return messages
    
    
    
    
    def process_delivered_messages(self, in_messages):
        msg_id = 0
        out_messages = []
        #do a check for "old messages to ignore"

        for i in range(len(in_messages)):
            current_message_out = {}
            if in_messages[i]['id'] > msg_id:                      
                msg_id = in_messages[i]['id']
            if 'sound' in in_messages[i]:
                current_message_out.update({"sound":in_messages[i]['sound']})
            if 'title' in in_messages[i]:
                current_message_out.update({"title":in_messages[i]['title']})
            if 'url' in in_messages[i]:
                current_message_out.update({"url":in_messages[i]['url']})
            if 'icon' in in_messages[i]:
                current_message_out.update({"icon":in_messages[i]['icon']})
                
            if 'receipt' in in_messages[i]:
                current_message_out.update({"emergency":in_messages[i]['receipt']})
                if in_messages[i]['acked']:
                    continue
                if self.auto_acknowledge_emergency:
                    self.acknowledge_emergency_message(receipt_id=in_messages[i]['receipt'])
                      
            current_message_out.update({"message":in_messages[i]['message']})
            current_message_out.update({"queued_timestamp":in_messages[i]['queued_date']})
            current_message_out.update({"now_timestamp":time.time()})
            out_messages.append(current_message_out)
              
          
        return [msg_id, out_messages]
        
    
    def delete_messages(self, message_id):
        
        data = {'secret':self.secret,
                'message':message_id,
                }

        url_full = API_ENDPOINT_DELETE_MESSAGE_PREFIX + self.device_id + API_ENDPOINT_DELETE_MESSAGE_SUFFIX
        
        try:
            resp_data = requests.post(url=url_full, data=data, timeout=DEFAULT_TIMEOUT)
            resp_data.raise_for_status()
        
        except requests.ConnectionError as err:
            raise InvalidURL(err)
        
        except requests.HTTPError as err:
            raise HTTPError(err) 
            
        return resp_data
    
    def acknowledge_emergency_message(self, receipt_id):
        
        data = {'secret':self.secret,
                }
        url_full = API_ENDPOINT_ACKNOWLEDGE_EMERGENCY_MESSAGE_PREFIX + receipt_id + API_ENDPOINT_ACKNOWLEDGE_EMERGENCY_MESSAGE_SUFFIX
        try:
            resp_data = requests.post(url=url_full, data=data, timeout=DEFAULT_TIMEOUT)
            resp_data.raise_for_status() 
        except requests.ConnectionError as err:
            raise InvalidURL(err)
        except requests.HTTPError as err:
            raise HTTPError(err) 
        
        return resp_data
    
    def websocket_message_received_callback(self, websocket, message):
        
        message = message.decode()
        if message == "#":
            print("keep alive")
            return
        if message == "!":
            print("sync")
            self.download_undelivered_messages()
            return
        if message == "R":
            print("Reconnect")
            websocket.close()
            self.initialize_websocket_client()
            return
        if message == "E":
            print("SOmething is wrong, DO not reconnect. Log in again or enable the device")
            _LOGGER.error("An error occurred with the pushover service. Please log in again or enable the device.")
            raise PushoverApiError("Another session has logged into this account somewhere else. Closing connection.")
        
        if message == "A":
            print("Device logged in someone else, closing connection")
            websocket.close()
            _LOGGER.error("Another session has logged into this account somewhere else. Closing connection. Please close that connection and log in again.")
            raise PushoverApiError("Another session has logged into this account somewhere else. Closing connection.")
        
    
    def initialize_websocket_client(self):
        self.websocket_client = WebsocketClient(device_id=self.device_id, secret=self.secret)
        thread.Thread(target=self.websocket_client.listen,
                      kwargs={"on_message_callback":self.websocket_message_received_callback}).start()
        
        
    def register_callback_to_hass(self, callback):
        self.callback_to_hass = callback
        
    def test_test(self, message):
        print("Send this to hass VVVVVVVVVVVVVV")
        print(message)