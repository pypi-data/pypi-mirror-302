# -*- coding: utf-8 -*-
import time, os  #내장모듈
import pyperclip
import pywinauto, chardet
import win32api, win32gui
import pygetwindow as gw
import paho.mqtt.client as mqtt

from unittest.mock import patch
with patch("ctypes.windll.user32.SetProcessDPIAware", autospec=True):
    import pyautogui


class pyclick:
	"""
	여러가지 사무용에 사용할 만한 메소드들을 만들어 놓은것이며,
	좀더 특이한 것은 youtil2로 만들어서 사용할 예정입니다
	
	2024-09-11 : 전체적으로 유사한것들을 변경함
	"""

	def __init__(self):
		self.vars = {}
		self.vars["keyboard_action_list_all"] = ['\\t', '\\n', '\\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
												 ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6',
												 '7',
												 '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_',
												 '`',
												 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
												 'o',
												 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}',
												 '~',
												 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
												 'browserback', 'browserfavorites', 'browserforward', 'browserhome',
												 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
												 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
												 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1',
												 'f10',
												 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2',
												 'f20',
												 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
												 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert',
												 'junja',
												 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
												 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
												 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
												 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause',
												 'pgdn',
												 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
												 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select',
												 'separator',
												 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop',
												 'subtract', 'tab',
												 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft',
												 'winright', 'yen',
												 'command', 'option', 'optionleft', 'optionright']


	def calculate_pixel_size_for_input_text_2(self, input_text, target_pixel, font_name="malgun.ttf", font_size=12, fill_char=" "):
		"""
		원하는 길이만큼 텍스트를 근처의 픽셀값으로 만드는것
		원래자료에 붙이는 문자의 픽셀값
		"""
		fill_px = self.calculate_pixel_size_for_input_text(fill_char, font_size, font_name)[0]
		total_length =0
		for one_text in input_text:
			#한글자씩 필셀값을 계산해서 다 더한다
			one_length = self.calculate_pixel_size_for_input_text(fill_char, font_size, font_name)[0]
			total_length = total_length + one_length

		# 원하는 길이만큼 부족한 것을 몇번 넣을지 게산하는것
		times = round((target_pixel - total_length)/fill_px)
		result = input_text + " "*times

		#최종적으로 넣은 텍스트의 길이를 한번더 구하는것
		length = self.calculate_pixel_size_for_input_text(result, font_size, font_name)[0]

		#[최종변경문자, 총 길이, 몇번을 넣은건지]
		return [result, length, times]

	def check_input_action_key(self, input_value):
		"""
		키보드의 액션을 하기위해 사용해야할 용어를 확인하는 부분이다
		:param input_value:
		:return:
		"""
		input_value = str(input_value).lower()
		if input_value in self.vars["keyboard_action_list_all"]:
			result = input_value
		else:
			result = ""
		return result

	def click_mouse_button(self, click_type="click", input_clicks=1, input_interval=0.25):
		"""
		"""
		if click_type == "click":
			pyautogui.click()
		elif click_type \
				== "doubleclick":
			pyautogui.doubleClick()
		else:
			pyautogui.click(button=click_type, clicks=input_clicks, interval=input_interval)

	def click_mouse_general(self, click_type="click", input_clicks=1, input_interval=0.25):
		"""
		마우스 클릭에 대한 일반적인것
		입력형태 : pyautogui.click(button=’right', clicks=3, interval =0.25)

		:param click_type: 오른쪽인지, 왼쪽인지등의 위치
		:param click_times: 클릭횟수
		:param interval_time: 클릭당 시간간격
		:return:
		"""
		if click_type in ["click", ""]:
			pyautogui.click()
		elif click_type in ["doubleclick", "dbclick", "dclick"]:
			pyautogui.doubleClick()
		else:
			pyautogui.click(button=click_type, clicks=input_clicks, interval=input_interval)

	def click_mouse_left(self, click_times = 1):
		"""
		왼쪽 마우스 버튼을 누르는 것

		:param click_times: 누르는 횟수
		:return:
		"""
		pyautogui.click(button="left", clicks= click_times)

	def click_mouse_left_down(self):
		"""
		왼쪽 마우스 버튼 눌른상태로 멈춤
		드리그등을 위한것
		"""
		pyautogui.mouseDown(button='left')

	def click_mouse_left_up(self):
		"""
		왼쪽 마우스 버튼 눌럿다 올린것
		"""
		pyautogui.mouseUp(button='left')

	def click_mouse_right(self, click_times = 1):
		"""
		오른쪽 마우스 클릭
		:param click_times:
		"""
		pyautogui.click(button="right", clicks=click_times)

	def click_mouse_right_down(self):
		"""
		오른쪽 마우스 눌름
		"""
		pyautogui.mouseDown(button='right')

	def click_mouse_right_up(self):
		"""
		오른쪽 마우스 올림
		:return:
		"""
		pyautogui.mouseUp(button='right')

	def connect_mqtt(self, client, userdata, flags, rc):
		"""
		connect_mqtt
		"""
		if rc == 0:
			print("connected OK")
		else:
			print("Bad connection Returned code=", rc)

	def copy(self):
		"""
		현재 선택된 것을 복사하기
		"""
		pyautogui.hotkey('ctrl', "c")

	def data_keyboard_action_list(self):
		"""
		키보드 액션의 종류들
		:return:
		"""
		result =self.vars["keyboard_action_list_all"]
		return result

	def dclick_mouse(self):
		"""
		double click
		:return:
		"""
		pyautogui.click(button="left", clicks=2, interval=0.25)

	def dclick_mouse_left(self, interval_time=0.25):
		"""
		왼쪽 마우스 더블 클릭
		:param interval_time: 클릭 시간 간격
		:return:
		"""
		pyautogui.click(button="left", clicks=2, interval=interval_time)

	def dclick_mouse_right(self, interval_time=0.25):
		"""
		오른쪽 마우스 더블 클릭
		:param interval_time:클릭 시간 간격
		:return:
		"""
		pyautogui.click(button="right", clicks=2, interval=interval_time)

	def doubleclick_mouse(self):
		pyautogui.doubleClick()

	def drag_mouse_from_pxy1_to_pxy2(self, pxy1, pxy2, drag_speed=0.5):
		"""
		마우스 드레그

		:param pxy1:
		:param pxy2:
		:param drag_speed:
		:return:
		"""
		pyautogui.moveTo(pxy1[0], pxy1[1])
		pyautogui.dragTo(pxy2[0], pxy2[1], drag_speed)

	def drag_mouse_to_pwh(self, phw, drag_speed=0.5):
		"""
		현재 마우스위치에서 상대적인 위치인 pxy로 이동
		상대적인 위치의 의미로 width 와 height 의 개념으로 pwh 를 사용 duration 은 드레그가 너무 빠를때 이동하는 시간을 설정하는 것이다

		:param phw:
		:param drag_speed: 드레그 속도
		"""
		pyautogui.drag(phw[0], phw[1], drag_speed)

	def drag_mouse_to_pxy(self, pxy, drag_speed=0.5):
		"""
		현재 마우스위치에서 절대위치인 머이로 이동	duration 은 드레그가 너무 빠를때 이동하는 시간을 설정하는 것이다

		:param pxy:
		:param drag_speed: 드레그 속도
		"""
		pyautogui.dragTo(pxy[0], pxy[1], drag_speed)

	def file_change_ecoding_type(self, path, filename, original_type="EUC-KR", new_type="UTF-8", new_filename=""):
		"""
		텍스트가 안 읽혀져서 확인해보니 인코딩이 달라서 안되어져서
		이것으로 전체를 변경하기위해 만듦
		"""
		full_path = path + "\\" + filename
		full_path_changed = path + "\\" + new_filename + filename
		try:
			aaa = open(full_path, 'rb')
			result = chardet.detect(aaa.read())
			print(result['encoding'], filename)
			aaa.close()

			if result['encoding'] == original_type:
				print("화일의 인코딩은 ======> {}, 화일이름은 {} 입니다".format(original_type, filename))
				aaa = open(full_path, "r", encoding=original_type)
				file_read = aaa.readlines()
				aaa.close()

				new_file = open(full_path_changed, mode='w', encoding=new_type)
				for one in file_read:
					new_file.write(one)
				new_file.close()
		except:
			print("화일이 읽히지 않아요=====>", filename)

		path = "C:\Python39-32\Lib\site-packages\myez_xl\myez_xl_test_codes"
		file_lists = os.listdir(path)
		for one_file in file_lists:
			self.file_type_change(path, one_file, "EUC-KR", "UTF-8", "_changed")

	def focus_on(self, original_xy, move_xy=[10, 10]):
		"""
		많이 사용하는 마우스와 키보드의 기능을 다시 만들어 놓은 것이다
		"""
		pyautogui.moveTo(original_xy[0] + move_xy[0], original_xy[1] + move_xy[1])
		pyautogui.mouseDown(button='left')

	def focus_to_window(self, window_title="Excel.Application"):
		window = gw.getWindowsWithTitle(window_title)
		print()
		if window.isActive == False:
			try:
				pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()
			except:
				print('No permission')

	def get_monitor_size(self):
		"""
		모니터의 해상도를 읽어오는 것

		:return:
		"""
		result = pyautogui.size()
		return result

	def get_pxy_for_mouse(self):
		"""
		마우스 위치
		:return:
		"""
		pxy = pyautogui.position()
		return [pxy.x, pxy.y]

	def get_pxy_for_mouse_rev1(self):
		"""
		현재 마우스의 위치를 읽어온다

		:return:
		"""
		result = win32api.GetCursorPos()
		return result

	def get_pxy_for_selected_image(self, input_file_name):
		"""
		화면에서 저장된 이미지랑 같은 위치를 찾아서 돌려주는 것

		:param input_file_name:
		:return:
		"""
		button5location = pyautogui.locateOnScreen(input_file_name)
		center = pyautogui.center(button5location)
		return center

	def get_screen_size(self):
		"""
		화면 사이즈

		:return:
		"""
		px =  win32api.GetSystemMetrics(0)
		py =  win32api.GetSystemMetrics(1)
		return [px, py]


	def get_information_for_monitor(self):
		result = []
		monitor = win32api.EnumDisplayMonitors()
		result = list()

		for info in monitor:
			# 주 모니터와 서브 모니터 구분
			if info[2][0] == 0 and info[2][1] == 0:
				monitorType = "주모니터"
			else:
				monitorType = "서브모니터"

			result.append({'type': monitorType, '모니터의 영역(왼쪽위, 오른쪽아래)': info[2]})

		result.append({'총모니터갯수': len(monitor)})
		return result


	def search_px_for_same_picture_in_monitor(self, input_picture):
		"""
		화면위에서 들어온 그림의 위치를 찾아서 중간 위치를 알려주는 것

		:param input_picture:
		:return:
		"""

		pxywh = pyautogui.locateOnScreen(input_picture)
		pxy = pyautogui.center(pxywh)
		result = [pxy[0], pxy[1]]
		return result


	def get_information_for_mouse(self):
		result = []
		pxy = self.get_pxy_for_mouse()
		result.append({"마우스의 현재 위치":pxy})
		monitors = win32api.EnumDisplayMonitors()
		"""
		[(PyHANDLE:65537, PyHANDLE:0, (0, 0, 1920, 1080)), (PyHANDLE:65539, PyHANDLE:0, (-1920, 1, 0, 1081))]
		1 : 모니터의 핸들값
		2 : unknown
		3 : 위치와 해상도, ( left, top, width, height )
		0, 0 이 주모니터
		left : - 일 경우 주 모니터 왼쪽에 위치, 모니터가 상하로 위치할 경우 top 의 +- 로 판단
		"""



		for info in monitors:
			# 주 모니터와 서브 모니터 구분
			if info[2][0] == 0 and info[2][1] == 0:
				monitorType = "주모니터"
			else:
				monitorType = "서브모니터"

			if info[2][0] <= pxy[0] <= info[2][2] and info[2][1] <= pxy[1] <= info[2][3]:
				result.append({"모니터에서의 위치":monitorType})
				break

		return result

	def input_message_box(self, button_list):
		"""
		메세지박스의 버튼을 만드는 것

		:param button_list:
		:return:
		"""
		press_button_name = pyautogui.confirm('Enter option', buttons=['A', 'B', 'C'])
		return press_button_name

	def input_message_box_by_password_style(self, input_text, input_title="", input_default_text =""):
		"""
		메세지박스 : 암호 입력용
		:param input_text:
		:param input_title:
		:param input_default_text:
		:return:
		"""
		a = pyautogui.password(text=input_text, title=input_title, default=input_default_text, mask='*')
		print(a)

	def keyboard_input_for_hotkey(self, input_keys=['ctrl', 'c']):
		"""
		pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
		"""
		text = ""
		for one in input_keys:
			text = text + "'" + str(one) + "',"
		pyautogui.hotkey(text[:-1])

	def keyboard_type_action(self, action, key):
		"""
		pyautogui.keyDown('ctrl')  # ctrl 키를 누른 상태를 유지합니다.
		pyautogui.press('c')  # c key를 입력합니다.
		pyautogui.keyUp('ctrl')  # ctrl 키를 뗍니다.
		"""
		if action == "keydown":
			pyautogui.keyDown(key)
		if action == "keyup":
			pyautogui.keyUp(key)
		if action == "press":
			pyautogui.press(key)

	def move_cursor(self, direction, press_times = 1):
		"""
		마우스커서를 기준으로 이동하는것

		:param direction:
		:param press_times:
		:return:
		"""
		for no in range(press_times):
			pyautogui.press(direction)

	def move_mouse_as_pwh(self, pwh):
		"""
		현재의 위치에서 이동시키는것
		마우스의 위치를 이동시킨다
		"""
		pyautogui.move(pwh[0], pwh[1])

	def move_mouse_as_pxy(self, pxy):
		"""
		마우스의 위치를 이동시킨다

		:param pxy:
		:return:
		"""
		pyautogui.moveTo(pxy[0], pxy[1])

	def move_mouse_to_pwh(self, pwh):
		"""
		마우스의 위치를 이동시킨다
		"""
		pyautogui.move(pwh[0], pwh[1])

	def move_mouse_to_px_rev1(self, xy):
		# 원하는 위치로 마우스를 이동시킨다
		pos = (xy[0], xy[1])
		win32api.SetCursorPos(pos)

	def move_mouse_to_pxy(self, pxy):
		"""
		마우스의 위치를 이동시킨다
		"""
		pyautogui.moveTo(pxy[0], pxy[1])

	def move_screen_by_scroll(self, input_no):
		"""
		현재 위치에서 상하로 스크롤하는 기능 #위로 올리는것은 +숫자，내리는것은 -숫자로 사용

		:param input_no:
		:return:
		"""
		pyautogui.scroll(input_no)

	def mqtt_connect(self, client, userdata, flags, rc):
		"""
		"""
		if rc == 0:
			print("connected OK")
		else:
			print("Bad connection Returned code=", rc)

	def mqtt_receive_data(self, topic='halmoney/data001'):
		"""
		mqtt의 서버에서 자료받기
		"""
		self.topic = topic
		client = mqtt.Client()
		client.on_connect = self.on_connect
		client.on_disconnect = self.on_disconnect
		client.on_subscribe = self.on_subscribe
		client.on_message = self.on_message

		client.connect(self.broker, self.port, 60)
		client.subscribe(self.topic, 1)
		client.loop_forever()

	def mqtt_send_data(self, input_text="no message", topic='halmoney/data001'):
		"""
		"""
		self.topic = topic
		client = mqtt.Client()
		# 새로운 클라이언트 생성

		# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
		client.on_connect = self.on_connect
		client.on_disconnect = self.on_disconnect
		client.on_publish = self.on_publish
		client.connect(self.broker, self.port)
		client.loop_start()

		client.publish(self.topic, str(input_text), self.qos)
		client.loop_stop()
		client.disconnect()

	def mqtt_start(self, broker="broker.hivemq.com", port=1883, qos=0):
		"""
		"""
		self.broker = broker
		self.port = port
		self.qos = qos

	def on_connect(self, client, userdata, flags, rc):
		"""
		on_connect
		"""
		if rc == 0:
			print("connected OK")
		else:
			print("Bad connection Returned code=", rc)

	def on_disconnect(self, client, userdata, flags, rc=0):
		"""
		on_disconnect
		"""
		print(str(rc))

	def on_message(self, client, userdata, msg):
		"""
		on_message
		"""
		print(str(msg.payload.decode("utf-8")))

	def on_publish(self, client, userdata, mid):
		"""
		on_publish
		"""
		print("In on_pub callback mid= ", mid)

	def on_subscribe(self, client, userdata, mid, granted_qos):
		"""
		on_subscribe
		"""
		print("subscribed: " + str(mid) + " " + str(granted_qos))

	def paste(self):
		"""
		복사후 붙여넣기
		:return:
		"""
		pyautogui.hotkey('ctrl', "v")

	def paste_clibboard_data(self):
		"""
		클립보드에 저장된 텍스트를 붙여넣습니다.

		:return:
		"""
		pyperclip.paste()

	def paste_for_clibboard_data(self):
		"""
		클립보드에 저장된 텍스트를 붙여넣습니다.

		:return:
		"""
		pyperclip.paste()

	def paste_text_from_clipboard(self):
		"""
		클립보드에서 입력된 내용을 복사를 하는 것이다

		:return:
		"""
		result = pyperclip.paste()
		return result

	def press_key_down(self, one_key):
		"""
		어떤키의 키보드를 눌름

		:param one_key:
		:return:
		"""
		pyautogui.keyDown(one_key)

	def press_key_general(self, action='enter', times=1, input_interval=0.1):
		"""
		pyautogui.press('enter', presses=3, interval=3) # enter 키를 3초에 한번씩 세번 입력합니다.
		"""
		pyautogui.press(action, presses=times, interval=input_interval)

	def press_key_up(self, one_key):
		"""
		어떤키의 키보드를 눌렀다 땜
		:param one_key:
		:return:
		"""
		pyautogui.keyUp(one_key)

	def press_one_key(self, input_key="enter"):
		"""
		기본적인 키를 누르는 것을 설정하는 것이며
		기본값은 enter이다
		press의 의미는 down + up이다

		:param input_key:
		:return:
		"""
		pyautogui.press(input_key)

	def receive_mqtt_data(self, topic='halmoney/data001'):
		"""
			mqtt의 서버에서 자료받기
			"""
		self.topic = topic
		client = mqtt.Client()
		client.on_connect = self.on_connect
		client.on_disconnect = self.on_disconnect
		client.on_subscribe = self.on_subscribe
		client.on_message = self.on_message

		client.connect(self.broker, self.port, 60)
		client.subscribe(self.topic, 1)
		client.loop_forever()

	def save(self):
		"""
		저장하기
		:return:
		"""
		pyautogui.hotkey('ctrl', "s")

	def screen_capture(self, filename="D:Wtemp_101.jpg"):
		# 스크린 캡쳐를 해서, 화면을 저장하는 것
		pyautogui.screenshot(filename)
		return filename

	def screen_capture_with_save_file(self, file_name="D:Wtemp_101.jpg"):
		"""
		스크린 캡쳐를 해서, 화면을 저장하는 것

		:param file_name:
		:return:
		"""
		pyautogui.screenshot(file_name)
		return file_name

	def screen_capture_with_size(self, pxyxy):
		"""
		화면캡쳐를 지정한 크기에서 하는것
		:return:
		"""
		im3 = pyautogui.screenshot('my_region.png', region=(pxyxy[0], pxyxy[1], pxyxy[2], pxyxy[3]))

	def screen_scroll(self, input_no):
		""" 현재 위치에서 상하로 스크롤하는 기능 #위로 올리는것은 +숫자，내리는것은 -숫자로 사용 """
		pyautogui.scroll(input_no)

	def select_from_curent_cursor(self, direction, press_times):
		"""
		현재위치에서 왼쪽이나 오른쪽으로 몇개를 선택하는 것

		:param direction:
		:param press_times:
		:return:
		"""
		pyautogui.keyDown("shift")
		for one in range(press_times):
			self.key_down_with_one_key(direction)
		pyautogui.keyUp("shift")

	def send_mqtt_data(self, input_text="no message", topic='halmoney/data001'):
		"""
		send_mqtt_data
		"""
		self.topic = topic
		client = mqtt.Client()
		# 새로운 클라이언트 생성

		# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
		client.on_connect = self.on_connect
		client.on_disconnect = self.on_disconnect
		client.on_publish = self.on_publish
		client.connect(self.broker, self.port)
		client.loop_start()

		client.publish(self.topic, str(input_text), self.qos)
		client.loop_stop()
		client.disconnect()

	def show_message(self):
		"""

		:return:
		"""
		pyautogui.alert(text='내용입니다', title='제목입니다', button='OK')

	def show_message_box(self, input_text, input_title="", input_default_text =""):
		"""
		일반 메세지 박스

		:param input_text:
		:param input_title:
		:param input_default_text:
		:return:
		"""
		a = pyautogui.prompt(text=input_text, title=input_title, default=input_default_text)
		print(a)


	def start_mqtt(self, broker="broker.hivemq.com", port=1883, qos=0):
		"""
		start_mqtt
		"""
		self.broker = broker
		self.port = port
		self.qos = qos


	def type_1000times_delete_key(self):
		"""
		현재위치에서 자료를 지우는것
		최대 한줄의 자료를 다 지워서 x 의 위치가 변거나 textbox 안의 자료가 다지워져 위치이동이 없으면 종료

		:return:
		"""
		for no in range(0, 1000):
			position = pyautogui.position()
			pxy_old = [position.x, position.y]
			pyautogui.press('delete')
			position = pyautogui.position()
			pxy_new = [position.x, position.y]
			if pxy_old == pxy_new or pxy_old[1] != pxy_new[1]:
				break

	def type_N_times_backspace(self, number = 10):
		"""
		현재위치에서 자료를 지우는것
		죄대 한줄의 자료를 다 지워서 x 의 위지가 변거나 textbox 안의 자료가 다지워져 위지이동이 없으면 종료

		:param number:
		:return:
		"""
		for no in range(0, number):
			pyautogui.press('backspace')
			time.sleep(0.2)

	def type_action(self, action, key):
		"""
		pyautogui.keyDown('ctrl')  # ctrl 키를 누른 상태를 유지합니다.
		pyautogui.press('c')  # c key를 입력합니다.
		pyautogui.keyUp('ctrl')  # ctrl 키를 뗍니다.

		:param action:
		:param key:
		:return:
		"""
		if action == "keydown":
			pyautogui.keyDown(key)
		if action == "keyup":
			pyautogui.keyUp(key)
		if action == "press":
			pyautogui.press(key)

	def type_action_key(self, action, times=1, input_interval=0.1):
		"""
		키타이핑

		:param action:
		:param times:
		:param input_interval:
		:return:
		"""
		pyautogui.press(action, presses=times, interval=input_interval)

	def type_action_key_with_keyboard(self, action, times=1, input_interval=0.1):
		"""

		:param action:
		:param times:
		:param input_interval:
		:return:
		"""
		pyautogui.press(action, presses=times, interval=input_interval)

	def type_backspace_until_empty(self):
		"""
		자료를 다 삭제할때까지 지우는것
		최대 1000번까지 한다

		:return:
		"""
		for no in range(0, 1000):
			position = pyautogui.position()
			pxy_old = [position.x, position.y]
			pyautogui.press('backspace')
			position = pyautogui.position()
			pxy_new = [position.x, position.y]
			if pxy_old == pxy_new or pxy_old[1] != pxy_new[1]:
				break
			time.sleep(0.2)

	def type_ctrl_n_one_letter(self, input_text):
		"""
		ctrl + 키를 위한것

		:param input_text:
		:return:
		"""
		pyautogui.hotkey('ctrl', input_text)

	def type_ctrl_plus_letter(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		pyautogui.hotkey('ctrl', input_text)

	def type_each_letter_by_interval_with_keyboard(self, input_text, input_interval=0.1):
		"""
		그저 글자를 타이핑 치는 것이다
		pyautogui.pressfenter', presses=3z interval=3) # enter 키를 3 초에 한번씩 세번 입력합니다.

		:param input_text:
		:param input_interval:
		:return:
		"""
		pyautogui.typewrite(input_text, interval=input_interval)

	def type_hotkey(self, input_keys=['ctrl', 'c']):
		"""
		pyautogui.hotkey(’ctrl’, *c')
		ctrl-c to copy

		:param input_keys:
		:return:
		"""
		pyautogui.hotkey(input_keys[0], input_keys[1])

	def type_hotkey_n_char(self, input_keys=['ctrl', 'c']):
		"""
		pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
		"""
		text = ""
		for one in input_keys:
			text = text + "'" + str(one) + "',"
		pyautogui.hotkey(text[:-1])

	def type_hotkey_n_key(self, input_hotkey, input_key):
		"""
		pyautogui.hotkey(’ctrl’, *c') ==> ctrl-c to copy

		:param input_hotkey:
		:param input_key:
		:return:
		"""
		pyautogui.hotkey(input_hotkey, input_key)

	def type_hotkey_with_keyboard(self, input_keys):
		"""
		pyautogui.hotkey(’ctrl’, *c')
		ctrl-c to copy

		:param input_keys:
		:return:
		"""
		pyautogui.hotkey(input_keys[0], input_keys[1])

	def type_keyboard(self, action='enter', times=1, input_interval=0.1):
		"""
		pyautogui.press('enter', presses=3, interval=3) # enter 키를 3초에 한번씩 세번 입력합니다.
		"""
		pyautogui.press(action, presses=times, interval=input_interval)

	def type_keyboard_general(self, action='enter', times=1, input_interval=0.1):
		"""
		pyautogui.press('enter', presses=3, interval=3) # enter 키를 3초에 한번씩 세번 입력합니다.
		"""
		pyautogui.press(action, presses=times, interval=input_interval)

	def type_letter(self, input_text, input_interval=0.1):
		"""
		그저 글자를 타이핑 치는 것이다
		pyautogui.press('enter', presses=3, interval=3) # enter 키를 3초에 한번씩 세번 입력합니다.

		:param input_text:
		:param input_interval:
		:return:
		"""
		pyautogui.typewrite(input_text, interval=input_interval)

	def type_n_time_backspace_key_with_keyboard(self, number=10):
		# 현재위치에서 자료를 지우는것
		# 죄대 한줄의 자료를 다 지워서 x 의 위지가 변거나 textbox 안의 자료가 다지워져 위지이동이 없으면 종료
		for no in range(0, number):
			pyautogui.press('backspace')
			time.sleep(0.2)

	def type_normal_key(self, input_text="enter"):
		"""

		:param input_text:
		:return:
		"""
		pyautogui.press(input_text)

	def type_text(self, input_text="enter"):
		"""
		기본적인 키를 누르는 것을 설정하는 것이며
		기본값은 enter이다

		:param input_text:
		:return:
		"""
		pyautogui.press(input_text)

	def type_text_for_hangul(self, input_text):
		"""
		영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		pyautogui 가 unicode 는 입력이 안됩니다

		:param input_text:
		:return:
		"""
		pyperclip.copy(input_text)
		pyautogui.hotkey('ctrl', "v")

	def type_text_one_by_one(self, input_text):
		"""
		영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		어떤경우는 여러개는 않되어서 한개씩 들어가는 형태로 한다

		:param input_text:
		:return:
		"""
		for one_letter in input_text:
			pyperclip.copy(one_letter)
			pyautogui.hotkey("ctrl", "v")

	def type_text_one_by_one_with_keyboard(self, input_text):
		"""
		영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		어떤경우는 여러개는 않되어서 한개씩 들어가는 형태로 한다

		:param input_text:
		:return:
		"""
		for one_letter in input_text:
			pyperclip.copy(one_letter)
			pyautogui.hotkey("ctrl", "v")

	def type_text_with_interval(self, input_text, input_interval=0.1):
		"""
		글자를 시간 간격으로 글쓰기
		pyautogui.pressfenter', presses=3z interval=3)
		enter 키를 3 초에 한번씩 세번 입력합니다.

		:param input_text:
		:param input_interval:
		:return:
		"""
		pyautogui.typewrite(input_text, interval=input_interval)

	def type_text_with_keyboard(self, input_text):
		self.write_text_at_cursor(input_text)

	def write_text_at_cursor(self, input_text):
		"""
		암호나 글자를 입력하는 데 사용하는것이다
		이것은 대부분 마우스를 원하는 위치에 옮기고, 클릭을 한번한후에 사용하는것이 대부분이다
		그저 글자를 타이핑 치는 것이다
		"""
		time.sleep(1)
		pyperclip.copy(input_text)
		pyautogui.hotkey("ctrl", "v")

	def write_text_at_previous_window(self, input_text ="가나다라abcd$^&*", start_window_no=1, next_line = 0):
		"""
		바로전에 활성화 되었던 윈도우에 글씨 써넣기

		:param input_text:
		:param start_window_no:
		:param next_line:
		:return:
		"""
		window_list = []
		for index, one in enumerate(gw.getAllTitles()):
			if one:
				window_list.append(one)
		previous_window = gw.getWindowsWithTitle(window_list[start_window_no])[0]
		previous_window.activate()
		if next_line==1:
			self.type_text_for_hangul(input_text)
			pyautogui.press('enter')
		else:
			self.type_text_for_hangul(input_text)


	def get_information_for_active_window(self):
		def callback(hwnd, hwnd_list: list):
			activeTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow())
			title = win32gui.GetWindowText(hwnd)
			if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
				if title == activeTitle:
					rect = win32gui.GetWindowRect(hwnd)
					hwnd_list.append((title, hwnd, rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]))

		output = []
		win32gui.EnumWindows(callback, output)
		return output[0]

	def scroll_mouse_down(self, input_click_no=10):
		pyautogui.scroll(input_click_no*-1) # scroll down 10 "clicks"

	def scroll_mouse_up(self, input_click_no=10):
		pyautogui.scroll(input_click_no) # scroll up 10 "clicks"

	def screenshot_for_full_screen(self, input_full_path=""):
		#스크린샷
		result = pyautogui.screenshot()
		if input_full_path:
			result.save(input_full_path)
		return result

	def screenshot_for_full_screen_with_file_name(self, input_full_path):
		#스크린샷
		result = pyautogui.screenshot(input_full_path)
		return result
	def screenshot_with_pxywh(self, input_pxywh, input_full_path=""):
		#스크린샷
		x,y,w,h  = input_pxywh
		result = pyautogui.screenshot(region=(x,y,w,h))
		if input_full_path:
			result.save(input_full_path)
		return result

	def search_all_same_xyxy_for_picture_in_screen(self, input_file_path):
		#화면에서 같은 그림의 위치 찾기
		result = []
		for pos in pyautogui.locateAllOnScreen(input_file_path):
			result.append(pos)
		return result


	def search_all_same_xyxy_for_picture_in_screen_by_gray_scale(self, input_file_path):
		#그레이 스케일로 변경해서 찾기
		result = []
		for pos in pyautogui.locateAllOnScreen(input_file_path, grayscale=True):
			result.append(pos)
		return result


	def get_rgb_for_pxy(self, input_pxy=""):
		"""
		입력으로 들어오는 pxy위치의 rgb값을 갖고온다
		만약 "" 이면, 현재 마우스가 위치한곳의 rgb를 갖고온다
		:param input_pxy:
		:return:
		"""
		if input_pxy:
			x, y = input_pxy
		else:
			x, y = pyautogui.position()
		r, g, b = pyautogui.pixel(x, y)
		return [r,g,b]

	def get_mouse_pos(self):
		# 현재 마우스의 위치를 읽어온다
		result = win32api.GetCursorPos()
		return result


	def get_screen_size(self):
		# 화면 사이즈를
		result = win32api.GetSystemMetrics()
		return result

