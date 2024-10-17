from pymavlink import mavutil
from pymavlink.dialects.v20 import common
import json
import threading
import socket
import sys
import time
import requests

class PioneerAero:
    AUTOPILOT_STATE = {
        0: 'ROOT',
        1: 'DISARMED',
        2: 'IDLE',
        3: 'TEST_ACTUATION',
        4: 'TEST_PARACHUTE',
        5: 'TEST_ENGINE',
        6: 'PARACHUTE',
        7: 'WAIT_FOR_LANDING',
        8: 'LANDED',
        9: 'CATAPULT',
        10: 'PREFLIGHT',
        11: 'ARMED',
        12: 'TAKEOFF',
        13: 'WAIT_FOR_GPS',
        14: 'WIND_MEASURE',
        15: 'MISSION',
        16: 'ASCEND',
        17: 'DESCEND',
        18: 'RTL',
        19: 'UNCONDITIONAL_RTL',
        20: 'MANUAL_HEADING',
        21: 'MANUAL_ROLL',
        22: 'MANUAL_SPEED',
        23: 'LANDING',
        24: 'ON_DEMAND'
    }

    def __init__(self, name='pioneer', method=2, ip='192.168.4.1', mavlink_port=8001, device='/dev/serial0',
                 baud=115200, logger=True):
        self.name = name

        self.ip = ip
        self.__heartbeat_send_delay = 0.25
        self.__ack_timeout = 0.2
        self.__logger = logger

        self.__prev_point_id = None

        self.__mavlink_socket = None

        self.t_start = time.time()

        self.cur_state = None
        self.preflight_state = dict(BatteryLow=None,
                                    NavSystem=None,
                                    Area=None,
                                    Attitude=None,
                                    RcExpected=None,
                                    RcMode=None,
                                    RcUnexpected=None,
                                    UavStartAllowed=None)

        if method == 0:
            print('метод соединения', method)
            try:
                print('соединение по wifi', ip, mavlink_port)
                self.__mavlink_socket = mavutil.mavlink_connection('udpin:%s:%s' % (ip, mavlink_port))
            except socket.error:
                print('Can not connect to pioneer. Do you connect to drone wifi?')
                sys.exit()
        elif method == 1:
            print('метод соединения', method)
            try:
                print('соединение по uart', device, baud)
                self.__mavlink_socket = mavutil.mavlink_connection(device=device, baud=baud)

            except socket.error:
                print('serial error')
                sys.exit()
        elif method == 2:
            print('метод соединения', method)
            try:
                print('соединение по wifi', ip, mavlink_port)
                self.__mavlink_socket = mavutil.mavlink_connection('udpout:%s:%s' % (ip, mavlink_port))
            except socket.error:
                print('Can not connect to pioneer. Do you connect to drone wifi?')
                sys.exit()
        else:
            print('Данный метод соединения не поддерживается')

        self.msg_data = dict()
        self.msg_request_events = dict()
        self.msg_response_events = dict()

        self.__init_heartbeat_event = threading.Event()

        self.message_handler_thread = threading.Thread(target=self.message_handler)
        self.message_handler_thread.daemon = True
        self.message_handler_thread.start()

        while not self.__init_heartbeat_event.is_set():
            pass
        while not self.point_reached():
            pass
        time.sleep(0.5)

    def get_autopilot_state(self):
        return self.cur_state

    def __initialize_msg(self, msg_type: str):
        self.msg_data.update({msg_type: None})
        self.msg_request_events.update({msg_type: threading.Event()})
        self.msg_response_events.update({msg_type: threading.Event()})

    def __request_msg(self, msg_type: str, timeout=None):
        if timeout is None:
            timeout = self.__ack_timeout
        if not (msg_type in self.msg_data.keys()):
            self.__initialize_msg(msg_type)
        start_time = time.time()
        while self.msg_request_events.get(msg_type).is_set() and time.time() - start_time <= timeout:
            pass
        if self.msg_request_events.get(msg_type).is_set():
            print("None due to requested already event")
            return None
        self.msg_request_events.get(msg_type).set()
        while not self.msg_response_events.get(msg_type).is_set() and time.time() - start_time <= timeout:
            pass
        if self.msg_response_events.get(msg_type).is_set():
            msg = self.msg_data.get(msg_type)
            self.msg_response_events.get(msg_type).clear()
            return msg
        else:
            self.msg_request_events.get(msg_type).clear()
            return None

    def __send_heartbeat(self):
        self.__mavlink_socket.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
                                                 mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
        if self.__logger:
            print('send heartbeat')

    def __receive_heartbeat(self, he):
        try:
            if he._header.srcComponent == 1:
                custom_mode = he.custom_mode
                custom_mode_buf = format(custom_mode, "032b")
                status_autopilot = custom_mode_buf[24:]
                self.cur_state = Pioneer.AUTOPILOT_STATE[int(status_autopilot, 2)]
        except Exception:
            pass

        if self.__logger:
            print("Heartbeat from system (system %u component %u)" % (self.__mavlink_socket.target_system,
                                                                      self.__mavlink_socket.target_component))

    def message_handler(self):
        self.__send_heartbeat()
        time_start_heartbeat_sending = time.time()
        while True:
            if time.time() - time_start_heartbeat_sending >= 1:
                self.__send_heartbeat()
                time_start_heartbeat_sending = time.time()
            msg = self.__mavlink_socket.recv_msg()
            if msg is not None:
                if msg.get_type() == "HEARTBEAT":
                    self.__receive_heartbeat(msg)
                    if not self.__init_heartbeat_event.is_set():
                        self.__init_heartbeat_event.set()
                elif msg.get_type() in self.msg_data.keys():
                    if self.msg_request_events.get(msg.get_type()).is_set():
                        self.msg_data.update({msg.get_type(): msg})
                        self.msg_request_events.get(msg.get_type()).clear()
                        self.msg_response_events.get(msg.get_type()).set()
                # if msg.get_type() == "DISTANCE_SENSOR":
                #     print(msg)

    def __get_ack(self, ack_timeout=0.1):
        msg = self.__request_msg("COMMAND_ACK", ack_timeout)
        if msg is not None:
            command_ack = msg
            if command_ack.result == 0:  # MAV_RESULT_ACCEPTED
                if self.__logger:
                    print('MAV_RESULT_ACCEPTED')
                return True, command_ack.command
            elif command_ack.result == 1:  # MAV_RESULT_TEMPORARILY_REJECTED
                if self.__logger:
                    print('MAV_RESULT_TEMPORARILY_REJECTED')
                return None, command_ack.command
            elif command_ack.result == 2:  # MAV_RESULT_DENIED
                if self.__logger:
                    print('MAV_RESULT_DENIED')
                return True, command_ack.command
            elif command_ack.result == 3:  # MAV_RESULT_UNSUPPORTED
                if self.__logger:
                    print('MAV_RESULT_UNSUPPORTED')
                return False, command_ack.command
            elif command_ack.result == 4:  # MAV_RESULT_FAILED
                if self.__logger:
                    print('MAV_RESULT_FAILED')
                if command_ack.result_param2 is not None:
                    self.preflight_state.update(BatteryLow=command_ack.result_param2 & 0b00000001)
                    self.preflight_state.update(NavSystem=command_ack.result_param2 & 0b00000010)
                    self.preflight_state.update(Area=command_ack.result_param2 & 0b00000100)
                    self.preflight_state.update(Attitude=command_ack.result_param2 & 0b00001000)
                    self.preflight_state.update(RcExpected=command_ack.result_param2 & 0b00010000)
                    self.preflight_state.update(RcMode=command_ack.result_param2 & 0b00100000)
                    self.preflight_state.update(RcUnexpected=command_ack.result_param2 & 0b01000000)
                    self.preflight_state.update(UavStartAllowed=command_ack.result_param2 & 0b10000000)
                return False, command_ack.command
            elif command_ack.result == 5:  # MAV_RESULT_IN_PROGRESS
                if self.__logger:
                    print('MAV_RESULT_IN_PROGRESS')
                return self.__get_ack()
            elif command_ack.result == 6:  # MAV_RESULT_CANCELLED
                if self.__logger:
                    print('MAV_RESULT_CANCELLED')
                return None, command_ack.command
        else:
            return None, None

    def poweroff(self):
        i = 0
        if self.__logger:
            print('poweroff command send')
        while True:
            self.__mavlink_socket.mav.command_long_send(
                self.__mavlink_socket.target_system,  # target_system
                self.__mavlink_socket.target_component,
                mavutil.mavlink.MAV_CMD_USER_2,  # command
                i,  # confirmation
                0,  # param1
                0,  # param2
                0,  # param3
                0,  # param4
                0,  # param5
                0,  # param6
                0)  # param7
            ack = self.__get_ack()
            if ack is not None:
                if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_USER_2:
                    if self.__logger:
                        print('poweroff complete')
                    return True
                else:
                    i += 1
                    if i > 25:
                        return False
            else:
                i += 1
                if i > 25:
                    return False

    def reboot(self):
        i = 0
        if self.__logger:
            print('reboot command send')
        while True:
            self.__mavlink_socket.mav.command_long_send(
                self.__mavlink_socket.target_system,  # target_system
                self.__mavlink_socket.target_component,
                mavutil.mavlink.MAV_CMD_USER_4,  # command
                i,  # confirmation
                0,  # param1
                0,  # param2
                0,  # param3
                0,  # param4
                0,  # param5
                0,  # param6
                0)  # param7
            ack = self.__get_ack()
            if ack is not None:
                if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_USER_4:
                    if self.__logger:
                        print('reboot complete')
                    return True
                else:
                    i += 1
                    if i > 25:
                        return False

            else:
                i += 1
                if i > 25:
                    return False

    def arm(self):
        try:
            i = 0
            if self.__logger:
                print('arm command send')
            while True:
                self.__mavlink_socket.mav.command_long_send(
                    self.__mavlink_socket.target_system,  # target_system
                    self.__mavlink_socket.target_component,
                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # command
                    i,  # confirmation
                    1,  # param1
                    0,  # param2 (all other params meaningless)
                    0,  # param3
                    0,  # param4
                    0,  # param5
                    0,  # param6
                    0)  # param7
                ack = self.__get_ack(0.5)
                if ack is not None:
                    if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM:
                        if self.__logger:
                            print('arming complete')
                        return True
                    else:
                        i += 1
                        if i > 45: #15
                            return False
                else:
                    i += 1
                    if i > 45: #15
                        return False
        except:
            pass

    def disarm(self):
        try:
            i = 0
            if self.__logger:
                print('disarm command send')
            while True:
                self.__mavlink_socket.mav.command_long_send(
                    self.__mavlink_socket.target_system,  # target_system
                    self.__mavlink_socket.target_component,
                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # command
                    i,  # confirmation
                    0,  # param1
                    0,  # param2 (all other params meaningless)
                    0,  # param3
                    0,  # param4
                    0,  # param5
                    0,  # param6
                    0)  # param7
                ack = self.__get_ack(0.5)
                if ack is not None:
                    if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM:
                        if self.__logger:
                            print('disarming complete')
                        return True
                    else:
                        i += 1
                        if i > 75: #25
                            return False
                else:
                    i += 1
                    if i > 75: #25
                        return False
        except:
            pass

    def takeoff(self):
        i = 0
        if self.__logger:
            print('takeoff command send')
        while True:
            self.__mavlink_socket.mav.command_long_send(
                self.__mavlink_socket.target_system,  # target_system
                self.__mavlink_socket.target_component,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  # command
                i,  # confirmation
                0,  # param1
                0,  # param2
                0,  # param3
                0,  # param4
                0,  # param5
                0,  # param6
                0)  # param7
            ack = self.__get_ack(0.5)
            if ack is not None:
                if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_NAV_TAKEOFF:
                    if self.__logger:
                        print('takeoff complete')
                    return True
                else:
                    i += 1
                    if i > 15:
                        return False
            else:
                i += 1
                if i > 15:
                    return False

    def land(self):
        i = 0
        if self.__logger:
            print('land command send')
        while True:
            self.__mavlink_socket.mav.command_long_send(
                self.__mavlink_socket.target_system,  # target_system
                self.__mavlink_socket.target_component,
                mavutil.mavlink.MAV_CMD_NAV_LAND,  # command
                i,  # confirmation
                0,  # param1
                0,  # param2
                0,  # param3
                0,  # param4
                0,  # param5
                0,  # param6
                0)  # param7
            ack = self.__get_ack(0.5)
            if ack is not None:
                if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_NAV_LAND:
                    if self.__logger:
                        print('landing complete')
                    return True
                else:
                    i += 1
                    if i > 150: #50
                        return False
            else:
                i += 1
                if i > 150: #50
                    return False

    def reboot_board(self):
        try:
            i = 0
            if self.__logger:
                print('arm command send')
            while True:
                self.__mavlink_socket.mav.command_long_send(
                    self.__mavlink_socket.target_system,  # target_system
                    self.__mavlink_socket.target_component,
                    mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,  # command
                    i,  # confirmation
                    1,  # param1
                    0,  # param2 (all other params meaningless)
                    0,  # param3
                    0,  # param4
                    0,  # param5
                    0,  # param6
                    0)  # param7
                ack = self.__get_ack()
                if ack is not None:
                    if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN:
                        if self.__logger:
                            print('arming complete')
                        return True
                    else:
                        i += 1
                        if i > 750: #255
                            return False
                else:
                    i += 1
                    if i > 750: #255
                        return False
        except:
            pass

    def lua_script_control(self, input_state='Stop'):
        i = 0
        target_component = 25
        state = dict(Stop=0, Start=1)
        command = state.get(input_state)
        if command is not None:
            if self.__logger:
                print('LUA script command: %s send' % input_state)
            while True:
                self.__mavlink_socket.mav.command_long_send(
                    self.__mavlink_socket.target_system,  # target_system
                    target_component,
                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # command
                    i,  # confirmation
                    command,  # param1
                    0,  # param2
                    0,  # param3
                    0,  # param4
                    0,  # param5
                    0,  # param6
                    0)  # param7
                ack = self.__get_ack()
                if ack is not None:
                    if ack:
                        if self.__logger:
                            print('LUA script command: %s complete' % input_state)
                        return True
                    else:
                        i += 1
                        if i > 25:
                            return False
                else:
                    i += 1
                    if i > 25:
                        return False
        else:
            if self.__logger:
                print('wrong LUA command value')

    def led_control(self, led_id=255, r=0, g=0, b=0):  # 255 all led
        max_value = 255.0
        all_led = 255
        first_led = 0
        last_led = 3
        i = 0
        led_value = [r, g, b]
        command = True

        try:
            if led_id != all_led and (led_id < first_led or led_id > last_led):
                command = False
            for i in range(len(led_value)):
                led_value[i] = float(led_value[i])
                if led_value[i] > max_value or led_value[i] < 0:
                    command = False
                    break
                led_value[i] /= max_value
        except ValueError:
            command = False

        if command:
            if led_id == all_led:
                led_id_print = 'all'
            else:
                led_id_print = led_id
            if self.__logger:
                print('LED id: %s R: %i ,G: %i, B: %i send' % (led_id_print, r, g, b))
            while True:
                self.__mavlink_socket.mav.command_long_send(
                    self.__mavlink_socket.target_system,  # target_system
                    self.__mavlink_socket.target_component,
                    mavutil.mavlink.MAV_CMD_USER_1,  # command
                    i,  # confirmation
                    led_id,  # param1
                    led_value[0],  # param2
                    led_value[1],  # param3
                    led_value[2],  # param4
                    0,  # param5
                    0,  # param6
                    0)  # param7
                ack = self.__get_ack()
                if ack is not None:
                    if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_USER_1:
                        if self.__logger:
                            print('LED id: %s RGB send complete' % led_id_print)
                        return True
                    else:
                        i += 1
                        if i > 25:
                            return False
                else:
                    i += 1
                    if i > 25:
                        return False
        else:
            if self.__logger:
                print('wrong LED RGB values or id')

    def led_custom(self, mode=1, timer=0, color1=(0, 0, 0), color2=(0, 0, 0)):
        param2 = (((color1[0] << 8) | color1[1]) << 8) | color1[2]
        param3 = (((color2[0] << 8) | color2[1]) << 8) | color2[2]
        param5 = mode
        param6 = timer
        i = 0
        while True:
            self.__mavlink_socket.mav.command_long_send(
                0,  # target_system
                0,
                mavutil.mavlink.MAV_CMD_USER_3,  # command
                i,  # confirmation
                0,  # param1
                param2,  # param2
                param3,  # param3
                0,  # param4
                param5,  # param5
                param6,  # param6
                0)  # param7
            ack = self.__get_ack()
            if ack is not None:
                if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_USER_3:
                    if self.__logger:
                        print("Custom led sent message")
                    return True
                else:
                    i += 1
                    if i > 25:
                        return False
            else:
                i += 1
                if i > 25:
                    return False

    def send_rc_channels(self, channel_1=0xFF, channel_2=0xFF, channel_3=0xFF, channel_4=0xFF,
                         channel_5=0xFF, channel_6=0xFF, channel_7=0xFF, channel_8=0xFF):
        """ Отправка сигнала пульта """
        # channel_1 = изменение значения throttle
        # channel_2 = изменение значения yaw
        # channel_3 = изменение значения pitch
        # channel_4 = изменение значения roll
        # channel_5 = mode. 2000 - program

        self.__mavlink_socket.mav.rc_channels_override_send(self.__mavlink_socket.target_system,
                                                            self.__mavlink_socket.target_component, channel_1,
                                                            channel_2, channel_3, channel_4, channel_5, channel_6,
                                                            channel_7, channel_8)

    def start_capture(self, interval=0.1, total_images=0, sequence_number=0):
        """ Начало съемки камерой """
        # param2 interval - время в секундах между снимками
        # param3 total_images - кол-во изобрадений для захвата. 0 = делать снимки до команды остановки (вызова stop_capture)
        # param4 sequence_number - используется если total_images = 1, в противном случае  = 0

        try:
            i = 0
            if self.__logger:
                print('start_capture send')

            while True:
                self.__mavlink_socket.mav.command_long_send(
                    self.__mavlink_socket.target_system,  # target_system
                    self.__mavlink_socket.target_component,
                    mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE,  # command
                    i,  # confirmation
                    0,  # param1
                    interval,  # param2
                    total_images,  # param3
                    sequence_number,  # param4
                    0,  # param5
                    0,  # param6
                    0)  # param7

                ack = self.__get_ack()
                if ack is not None:
                    if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE:
                        if self.__logger:
                            print('start_capture complete, iter:', i)
                        return True
                    else:
                        i += 1
                        if i > 15:
                            return False
                else:
                    i += 1
                    if i > 15:
                        return False
        except:
            pass

    def stop_capture(self):
        """ Конец съемки камерой """

        try:
            i = 0
            if self.__logger:
                print('start_capture send')

            while True:
                self.__mavlink_socket.mav.command_long_send(
                    self.__mavlink_socket.target_system,  # target_system
                    self.__mavlink_socket.target_component,
                    mavutil.mavlink.MAV_CMD_IMAGE_STOP_CAPTURE,  # command
                    i,  # confirmation
                    0,  # param1
                    0,  # param2
                    0,  # param3
                    0,  # param4
                    0,  # param5
                    0,  # param6
                    0)  # param7

                ack = self.__get_ack()
                if ack is not None:
                    if ack[0] and ack[1] == mavutil.mavlink.MAV_CMD_IMAGE_STOP_CAPTURE:
                        if self.__logger:
                            print('stop_capture complete, iter:', i)
                        return True
                    else:
                        i += 1
                        if i > 15:
                            return False
                else:
                    i += 1
                    if i > 15:
                        return False
        except:
            pass


    def go_to_local_point(self, x=None, y=None, z=None, vx=0.1, vy=0.1, vz=0.1, afx=0.1, afy=0.1, afz=0.1,
                          yaw=0, yaw_rate=0):

        """ Полет в точку в коо-тах системы навигации """

        ack_timeout = 0.1
        send_time = time.time()
        parameters = dict(x=x, y=-y, z=-z, vx=vx, vy=vy, vz=vz, afx=afx, afy=afy, afz=afz, force_set=0, yaw=yaw,
                          yaw_rate=yaw_rate)  # 0-force_set
        mask = 0b0000111111111111
        element_mask = 0b0000000000000001
        for n, v in parameters.items():
            if v is not None:
                mask = mask ^ element_mask
            else:
                parameters[n] = 0.0
            element_mask = element_mask << 1
        if self.__logger:
            print('sending local point :', end=' ')
            first_output = True
            for n, v in parameters.items():
                if parameters[n] != 0.0:
                    if first_output:
                        print(n, ' = ', v, sep="", end='')
                        first_output = False
                    else:
                        print(', ', n, ' = ', v, sep="", end='')
            print(end='\n')
        counter = 1
        while True:
            if (time.time() - send_time) >= ack_timeout:
                counter += 1
                self.__mavlink_socket.mav.set_position_target_local_ned_send(0,  # time_boot_ms
                                                                             self.__mavlink_socket.target_system,
                                                                             self.__mavlink_socket.target_component,
                                                                             mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                                                                             mask, parameters['x'], parameters['y'],
                                                                             parameters['z'], parameters['vx'],
                                                                             parameters['vy'], parameters['vz'],
                                                                             parameters['afx'], parameters['afy'],
                                                                             parameters['afz'], parameters['yaw'],
                                                                             parameters['yaw_rate'])
                send_time = time.time()
            if counter > 75: 
                return False
            if not self.__ack_receive_point():
                continue
            else:
                return True

    def __ack_receive_point(self, blocking=False, ack_timeout=0.1):
        """ Возвращает точку, в которую летит кооптер при автономном полете """
        msg = self.__request_msg("POSITION_TARGET_LOCAL_NED", ack_timeout)
        if msg is not None:
            if msg._header.srcComponent == 1:
                return True
            else:
                return False
        else:
            return False

    def point_reached(self, blocking=False):
        point_reached = self.__request_msg("MISSION_ITEM_REACHED")
        if not point_reached:
            return False
        else:
            point_id = point_reached.seq
            if self.__prev_point_id is None:
                self.__prev_point_id = point_id
                new_point = True
            elif point_id > self.__prev_point_id:
                self.__prev_point_id = point_id
                new_point = True
            else:
                new_point = False
            if new_point:
                if self.__logger:
                    print("point reached, id: ", point_id)
                return True
            else:
                return False

    def get_local_position_opt(self, blocking=False):
        """ Возвращает данные от системы навигации OPT """
        position = self.__request_msg("LOCAL_POSITION_NED")
        if not position:
            return None
        if position.get_type() == "BAD_DATA":
            if mavutil.all_printable(position.data):
                sys.stdout.write(position.data)
                sys.stdout.flush()
        else:
            if position._header.srcComponent == 1:
                return [position.x, position.y, position.z]
            else:
                return None

    def get_local_position_lps(self, blocking=False):
        """ Возвращает данные от системы навигации LPS """
        position = self.__request_msg("LOCAL_POSITION_NED")
        if position is None:
            return None
        else:
            if position._header.srcComponent == 26:
                return [position.x / 1000, position.y / 1000, position.z / 1000]
            else:
                return None

    def get_dist_sensor_data(self, blocking=False):
        """ Возвращает данные с дальномера """
        dist_sensor_data = self.__request_msg("DISTANCE_SENSOR")
        if not dist_sensor_data:
            return None
        if dist_sensor_data.get_type() == "BAD_DATA":
            if mavutil.all_printable(dist_sensor_data.data):
                sys.stdout.write(dist_sensor_data.data)
                sys.stdout.flush()
                return None
        else:
            curr_distance = float(dist_sensor_data.current_distance) / 100  # cm to m
            if self.__logger:
                print("get dist sensor data: %5.2f m" % curr_distance)
            return curr_distance

    def get_optical_data(self, blocking=False):
        """ Возвращает сырые данные от системы навигации OPT """
        optical_data = self.__request_msg("OPTICAL_FLOW_RAD")
        if not optical_data:
            return None
        if optical_data.get_type() == "BAD_DATA":
            if mavutil.all_printable(optical_data.data):
                sys.stdout.write(optical_data.data)
                sys.stdout.flush()
                return
        else:
            return optical_data

    def get_battery_status(self, blocking=False):
        """ Возвращает заряд батареи """
        bat_state = self.__request_msg("BATTERY_STATUS")
        if bat_state is None:
            return None
        if bat_state.get_type() == "BAD_DATA":
            if mavutil.all_printable(bat_state.data):
                sys.stdout.write(bat_state.data)
                sys.stdout.flush()
                return None
        else:
            voltage = bat_state.voltages[0]
            if self.__logger:
                print("voltage %f" % voltage)
            return voltage

    def get_preflight_state(self):
        return self.preflight_state

    def get_autopilot_version(self, blocking=False):
        """ Возвращает версию автопилота """
        i = 0
        while True:
            self.__mavlink_socket.mav.command_long_send(
                self.__mavlink_socket.target_system,  # target_system
                1,
                mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,  # command
                i,  # confirmation
                mavutil.mavlink.MAVLINK_MSG_ID_AUTOPILOT_VERSION,  # param1
                0,  # param2
                0,  # param3
                0,  # param4
                0,  # param5
                0,  # param6
                0)  # param7
            ap_ver = self.__request_msg("AUTOPILOT_VERSION")

            if ap_ver is None:
                i += 1
                if i > 15:
                    return None
                else:
                    continue
            else:
                if ap_ver.get_type() == "AUTOPILOT_VERSION":
                    return [ap_ver.flight_sw_version, ap_ver.board_version, ap_ver.flight_custom_version]
                else:
                    i += 1
                    if i > 15:
                        return None

    def get_piro_sensor_data(self, blocking=False):
        """ Возвращает температуру с пирометра """
        piro_sensor_data = self.__request_msg("DISTANCE_SENSOR", timeout=0.1)
        if not piro_sensor_data:
            return None
        if piro_sensor_data.get_type() == "BAD_DATA":
            if mavutil.all_printable(piro_sensor_data.data):
                sys.stdout.write(piro_sensor_data.data)
                sys.stdout.flush()
                return None
        else:
            if piro_sensor_data.id == 0: # Если данные от пирометра
                if piro_sensor_data.type == mavutil.mavlink.MAV_DISTANCE_SENSOR_UNKNOWN:
                    current_temp = piro_sensor_data.current_distance
                    return current_temp
            else:
                return None

    def get_qr_reader_data(self, blocking=False):
        """ Возвращает данные qr метки"""
        qr_reader_data = self.__request_msg("DISTANCE_SENSOR", timeout=0.2)
        if not qr_reader_data:
            return None
        if qr_reader_data.get_type() == "BAD_DATA":
            if mavutil.all_printable(qr_reader_data.data):
                sys.stdout.write(qr_reader_data.data)
                sys.stdout.flush()
                return None
        else:
            if qr_reader_data.id == 1:
                if qr_reader_data.type == mavutil.mavlink.MAV_DISTANCE_SENSOR_UNKNOWN:
                    qr_data = qr_reader_data.current_distance
                    if qr_data != 0:
                        return int(qr_data)
                    else:
                        return None
            else:
                return None

    def emergency_detection(self):
        """ Мигание красной индикацией """
        url = f"http://10.1.100.6:31222/game?target=set&type_command=player&command=fire_action&param={self.ip}"
        requests.get(url)

    def __flasher(self, color=(255, 0, 0), t=5, period=0.5):
        t_start = time.time()
        while True:
            self.led_control(255, color[0], color[1], color[2])
            time.sleep(period)
            self.led_control(255, 0, 0, 0)
            time.sleep(period)
            if time.time() - t_start >= t:
                print("flasher stop")
                return
