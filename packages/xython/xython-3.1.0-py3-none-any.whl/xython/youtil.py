# -*- coding: utf-8 -*-
import shutil, pickle, inspect, re, string, math
import os, random, collections, sys, stat
from datetime import datetime
import zipfile
import screeninfo
import itertools
########################### 내장모듈 #################################
from collections import Counter
import win32gui, win32con, win32com, chardet, win32api, win32com.client
import pywintypes, difflib
import pyperclip
import bisect

class youtil():
	"""
	여러가지 사무용에 사용할 만한 메소드들을 만들어 놓은것이며,
	좀더 특이한 것은 youtil2로 만들어서 사용할 예정입니다
	"""

	def add_data_by_step(self, input_data, added_data, step):
		"""
		자료에 하나씩 어떤자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3 : 각 3번째 마다 자료를 추가한다면

		:param input_data:
		:param added_data:
		:param step:
		:return:
		"""

		var_1, var_2 = divmod(len(input_data), step)
		for num in range(var_1, 0, -1):
			input_data.insert(num * step - var_2 + 1, added_data)
		return input_data

	def add_serial_no_at_first_value_of_list_2d(self, input_list_2d, start_no=1, special_char=""):
		"""
		엑셀의 제일 앞세로열에 특이한 번호를 넣고싶은 경우가 있다
		이때, 사용하기 위한 목적으로 만들었다.

		2 차원값의 값의 제일 처음값에만 순서가있는 값을 넣기
		값의 맨앞에 1), 2), 3)과같은 순서의 값을 넣고 싶을때

		:param input_list_2d: 2차원 형태의 리스트
		:param start_no:
		:param special_char:
		:return:
		"""
		for x in range(len(input_list_2d)):
			if not start_no == "":
				add_value = str(start_no + x) + special_char
			else:
				add_value = special_char
			input_list_2d[x][0] = add_value + input_list_2d[x][0]
		return input_list_2d

	def add_serial_value(self, input_list_2d, start_no=1, special_char=""):
		"""
		엑셀의 제일 앞세로열에 특이한 번호를 넣고싶은 경우가 있다
		이때, 사용하기 위한 목적으로 만들었다.

		2 차원값의 값의 제일 처음값에만 순서가있는 값을 넣기
		값의 맨앞에 1), 2), 3)과같은 순서의 값을 넣고 싶을때

		:param input_list_2d: 2차원 형태의 리스트
		:param start_no:
		:param special_char:
		:return:
		"""
		for x in range(len(input_list_2d)):
			if not start_no == "":
				add_value = str(start_no + x) + special_char
			else:
				add_value = special_char
			input_list_2d[x][0] = add_value + input_list_2d[x][0]
		return input_list_2d

	def add_text_for_all_file_name_in_folder(self, input_folder, input_text="aaa_", front_or_end="front"):
		"""
		폴더안의 모든 파일이름에 텍스트를 앞이나 뒤에 추가하는 것
		"""
		all_file_name = self.get_all_file_name_in_folder(input_folder)
		for one_file_name in all_file_name:
			changed_file_name = input_text
			if front_or_end == "front":
				changed_file_name = input_text + one_file_name
			elif front_or_end == "end":
				changed_file_name = one_file_name + input_text
			else:
				pass

			full_path_old = input_folder + "\\" + one_file_name
			full_path_new = input_folder + "\\" + changed_file_name
			self.change_file_name(full_path_old, full_path_new)

	def append_value_at_each_list_1d_in_list_2d(self, input_list_2d, input_value):
		"""
		같은 항목으로 되어있는 자료를 제일 처음의 자료를 기준으로 합치는것
		2차원 리스트의 모든 자료끝에 값 추가하기
		2차원 리스트의 모든 자료끝에 값 추가하기
		모든 기존값에 입력되는 값을 추가하는것
		[[1],[2],[3]] ==> [[1,77],[2,77],[3,77]]

		:param input_list_2d:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			result.append(list_1d.append(input_value))
		return result

	def append_value_for_each_list_1d_in_list_2d(self, input_list_2d, input_value):
		"""
		모든 기존값에 입력되는 값을 추가하는것
		[[1],[2],[3]] ==> [[1,77],[2,77],[3,77]]

		같은 항목으로 되어있는 자료를 제일 처음의 자료를 기준으로 합치는것
		2차원 리스트의 모든 자료끝에 값 추가하기

		:param input_list_2d:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			result.append(list_1d.append(input_value))
		return result

	def calculate_container(self, path):
		"""
		폴더안의 크기를 돌려주는 것

		:param path:
		:return:
		"""
		total_size = 0
		for dirpath, dirnames, file_names in os.walk(path):
			for f in file_names:
				fp = os.path.join(dirpath, f)
				total_size += os.path.getsize(fp)
			return total_size

	def calculate_degree_for_xy(self, xy):
		"""
		좌표를 부면, 좌표에대한 각도를 계산해 주는 것

		:param xy:
		:return:
		"""
		pi = 3.1415926535
		result = math.atan2(xy[1], xy[0]) * 180 / pi
		return result

	def calculate_new_position_by_degree_distance(self, degree="입력필요", distance="입력필요"):
		"""
		move_degree_distance( degree="입력필요", distance="입력필요")
		현재 위치 x,y에서 30도로 20만큼 떨어진 거리의 위치를 돌려주는 것
		메뉴에서 제외

		:param degree:
		:param distance:
		:return:
		"""
		degree = degree * 3.141592 / 180
		y = distance * math.cos(degree)
		x = distance * math.sin(degree)
		return [x, y]

	def calculate_similarity_for_two_word(self, a, b):
		"""
		두개의 유사도를 측정
		"""
		return difflib.SequenceMatcher(None, a, b).ratio()

	def calculate_text_pixel(self, input_text, target_pixel, font_name="malgun.ttf", font_size=12, fill_char=" "):
		"""
		원하는 길이만큼 텍스트를 근처의 픽셀값으로 만드는것
		원래자료에 붙이는 문자의 픽셀값
		"""
		fill_px = self.get_pixel_size(fill_char, font_size, font_name)[0]
		total_length =0
		for one_text in input_text:
			#한글자씩 필셀값을 계산해서 다 더한다
			one_length = self.get_pixel_size(fill_char, font_size, font_name)[0]
			total_length = total_length + one_length

		# 원하는 길이만큼 부족한 것을 몇번 넣을지 게산하는것
		times = round((target_pixel - total_length)/fill_px)
		result = input_text + " "*times

		#최종적으로 넣은 텍스트의 길이를 한번더 구하는것
		length = self.get_pixel_size(result, font_size, font_name)[0]

		#[최종변경문자, 총 길이, 몇번을 넣은건지]
		return [result, length, times]

	def calculate_two_list(self, list_1, list_2, result_type="|"):
		"""
		두개의 리스트를 +-/*를 하는것

		:param list_1:
		:param list_2:
		:param result_type:
		:return:
		"""
		if result_type == "|":
			result = list(set(list_1) | set(list_2))
		if result_type == "&":
			result = list(set(list_1) & set(list_2))
		if result_type == "-":
			result = list(set(list_1) - set(list_2))
		if result_type == "^":
			result = list(set(list_1) ^ set(list_2))
		return result

	def calculate_value_text_pixel(self, input_text, target_pixel, font_name="malgun.ttf", font_size=12, fill_char=" "):
		"""
		원하는 길이만큼 텍스트를 근처의 픽셀값으로 만드는것
		원래자료에 붙이는 문자의 픽셀값
		"""
		fill_px = self.calculate_value_pixel_size(fill_char, font_size, font_name)[0]
		total_length = 0
		for one_text in input_text:
			# 한글자씩 필셀값을 계산해서 다 더한다
			one_length = self.calculate_value_pixel_size(fill_char, font_size, font_name)[0]
			total_length = total_length + one_length

		# 원하는 길이만큼 부족한 것을 몇번 넣을지 게산하는것
		times = round((target_pixel - total_length) / fill_px)
		result = input_text + " " * times

		# 최종적으로 넣은 텍스트의 길이를 한번더 구하는것
		length = self.calculate_value_pixel_size(result, font_size, font_name)[0]

		# [최종변경문자, 총 길이, 몇번을 넣은건지]
		return [result, length, times]

	def calculate_xy_position_for_nth_label_printing(self, serial_no, start_xy, size_xy, y_line):
		"""
		한줄의 자료를 라벨로 만드는 경우를 생각할때, 몇번째 자료가 어디부분에서 시작이 되는지를 계산하는 것
		n번째 프린트하는 자료의 시작점을 돌려주는 것이다

		:param serial_no: 몇번째로 출력될 것인지를 아는 것
		:param start_xy: 1번째의 자료가 시작되는 부분
		:param size_xy: 한줄의 자료가 출력되는 크기
		:param y_line: 한페이지에 몇줄로 출력할지를 설정하는 것
		:return:
		"""
		mok, namuji = divmod(serial_no, y_line)
		new_start_x = start_xy[0] + mok * size_xy[0]
		new_start_y = start_xy[1] + namuji * size_xy[1]
		return [new_start_x, new_start_y]

	def calculator_two_list(self, list_1, list_2, result_type="|"):
		"""
		두개의 리스트를 +-/*를 하는것

		:param list_1:
		:param list_2:
		:param result_type:
		:return:
		"""
		if result_type == "|":
			result = list(set(list_1) | set(list_2))
		if result_type == "&":
			result = list(set(list_1) & set(list_2))
		if result_type == "-":
			result = list(set(list_1) - set(list_2))
		if result_type == "^":
			result = list(set(list_1) ^ set(list_2))
		return result

	def callback(self, font, tm, fonttype, names):
		names.append(font.lfFaceName)
		return True

	def change_10jinsu_to_njinsu(self, input_no, jinsu=10):
		"""
		10진수값을 34진수까지의 진수형태로 변환
		진수값을 바꾸면 다른 진수형태로 변경된다

		:param input_no:
		:param jinsu:
		:return:
		"""
		base_letter = "0123456789abcdefghijklmnopqrstuvwxyz"
		q, r = divmod(input_no, jinsu)
		if q == 0:
			return base_letter[r]
		else:
			return self.change_10jinsu_value_to_njinsu_value(q, jinsu) + base_letter[r]

	def change_10jinsu_to_special_letter_jinsu(self, input_no, show_letter="가나다라마바사아자차카타파하"):
		"""
		10진수값을 내가원하는 형식으로 변경하는것
		기본형을 예로들면 14진수이면서, 표현된,모양은 "0123456789abcd"가
		아니고 "가나다라마바사아자차카타파하"로 표현되는것

		:param input_no:
		:param show_letter:
		:return:
		"""
		jinsu = int(len(show_letter))
		q, r = divmod(input_no, jinsu)
		if q == 0:
			return show_letter[r]
		else:
			return self.change_10jinsu_to_special_letter_jinsu(q) + show_letter[r]

	def change_10jinsu_value_to_njinsu_value(self, input_no, jinsu=10):
		"""
		10진수값을 34진수까지의 진수형태로 변환
		진수값을 바꾸면 다른 진수형태로 변경된다

		:param input_no:
		:param jinsu:
		:return:
		"""
		base_letter = "0123456789abcdefghijklmnopqrstuvwxyz"
		q, r = divmod(input_no, jinsu)
		if q == 0:
			return base_letter[r]
		else:
			return self.change_10jinsu_value_to_njinsu_value(q, jinsu) + base_letter[r]

	def change_all_list_element_to_int(self, input_list):
		result = []
		for one in input_list:
			result.append(int(one))
		return result

	def change_all_tuple_n_set_to_list(self, input_any_data):
		"""
		자료안의 모든것을 list로 변경
		:param input_any_data:
		:return:
		"""
		if isinstance(input_any_data, (list, tuple)):
			return [self.change_all_tuple_n_set_to_list(x) for x in input_any_data]
		elif isinstance(input_any_data, set):
			return set(self.change_all_tuple_n_set_to_list(x) for x in input_any_data)
		else:
			return input_any_data

	def change_alpha_to_jamo(self, input_alpha_list):
		"""
		알파벳으로 바꾼 자음과 모음을 다시 자음과 모음으로 바꾸는 것

		:param input_alpha_list:
		:return:
		"""
		changed_value = input_alpha_list
		data_set = self.var["eng_vs_jamo_list"]
		for one_list in data_set:
			for one_data in one_list:
				changed_value = changed_value.replace(one_data[0], one_data[1])
		result = changed_value.split("_")[:-1]
		# 자모를 한글로 만드는 방법
		return result

	def change_alpha_to_korea(self, input_alpha_list):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것
		알파벳으로 바꾸면, 영문의 문자열 다루는 것을 사용할수도 있을것 같아 만들어 보았으며
		동시에 자음과 모음을 한번에 바꿀수있게 되는 것이다
		박 ==> ["ㅂ", "ㅏ", "ㄱ"] => "abc"
		이렇게 자음과 모음으로 구분된영어단어로 바뀌는 것이다
		자음과모음의 연결로도 가능하는데, 문제는 받침이 없는 경우와 space의 구분이 어렵다는 것이다

		:param input_alpha_list:
		:return:
		"""
		changed_value = input_alpha_list
		data_set = [
			[['sox', 'ㅙ'], ['ugx', 'ㅞ'], ],
			[['ox', 'ㅐ'], ['px', 'ㅒ'], ['gx', 'ㅔ'], ['rx', 'ㅖ'], ['so', 'ㅘ'], ['sx', 'ㅚ'], ['wx', 'ㅢ'], ['ug', 'ㅝ'],
			 ['ux', 'ㅟ'], ],
			[['a', 'ㄱ'], ['b', 'ㄴ'], ['c', 'ㄷ'], ['d', 'ㄹ'], ['e', 'ㅁ'], ['f', 'ㅂ'], ['g', 'ㅅ'], ['h', 'ㅇ'], ['i', 'ㅈ'],
			 ['j', 'ㅊ'], ['k', 'ㅋ'], ['l', 'ㅌ'], ['m', 'ㅍ'], ['n', 'ㅎ']],
			[['aa', 'ㄲ'], ['cc', 'ㄸ'], ['ff', 'ㅃ'], ['gg', 'ㅆ'], ['ii', 'ㅉ'], ['ag', 'ㄳ'], ['bi', 'ㄵ'], ['bn', 'ㄶ'],
			 ['da', 'ㄺ'], ['de', 'ㄻ'], ['df', 'ㄼ'], ['dg', 'ㄽ'], ['dl', 'ㄾ'], ['dm', 'ㄿ'], ['dn', 'ㅀ'], ['fg', 'ㅄ'], ],
			[['o', 'ㅏ'], ['p', 'ㅑ'], ['q', 'ㅓ'], ['r', 'ㅕ'], ['s', 'ㅗ'], ['t', 'ㅛ'], ['u', 'ㅜ'], ['v', 'ㅠ'], ['w', 'ㅡ'],
			 ['x', 'ㅣ'], ],
			[['z', '_']],
		]
		for one_list in data_set:
			for one_data in one_list:
				changed_value = changed_value.replace(one_data[0], one_data[1])
		result = changed_value.split("_")[:-1]
		return result

	def change_any_data_type_to_list_2d(self, input_data):
		"""
		어떤 자료형이 오더라도 2차원의 리스트로 만들어 주는 것
		제일 중요한 부분이 리스트의 2차원으로 만들어주는 것이다
		youtil로 이동
		"""
		if type(input_data) == type([]) or type(input_data) == type(()):
			if type(input_data[0]) == type([]) or type(input_data[0]) == type(()):
				result = input_data
			else:
				result = [input_data]
		elif type(input_data) == type("123") or type(input_data) == type(123):
			result = [[input_data]]
		else:
			result = input_data

		revise_result = []
		for list_1 in result:
			temp = []
			for one in list_1:
				if one:
					pass
				elif type(one) == type(None) or one == [] or one == ():
					one = None
				elif type(one) == type([]) or type(one) == type(()):
					one = str(one)
				else:
					one = ""
				temp.append(one)
			revise_result.append(list(temp))

		return revise_result

	def change_any_data_to_list_2d(self, input_data):
		result = self.change_any_data_type_to_list_2d(input_data)
		return result

	def change_any_range_to_xyxy(self, input_range=""):
		"""
		모든 :, ~ 의 스타일을 xyxy스타일로 바꾸는것

		"""
		[x1, y1, x2, y2] = [0,0,0,0]
		if type(input_range) == type("abc"):
			if "~" in input_range:
				if ":" in input_range:
					# 2 차원의 자료 요청건 ["2~3:4~5"]
					value1, value2 = input_range.split(":")
					if "~" in value2:
						start2, end2 = value2.split("~")
						if start2 == "" and end2 == "": #["2~3:~"]
							pass
						elif start2 == "" and end2:#["2~3:~5"]
							y2 = int(end2)
						elif start2 and end2 == "": #["2~3:4~"]
							x2 = int(start2)-1
						elif start2 and end2: #["2~3:4~5"]
							x2 = int(start2)-1
							y2 = int(end2)
						elif value2 == "":  # ["2~3:"]
							pass
						else:
							pass

					if "~" in value1:
						start1, end1 = value1.split("~")
						if start1 == "" and end1 == "": #["~:4~5"]
							pass
						elif start1 and end1 == "": #["2~:4~5"]
							x1 = int(start1)-1
						elif start1 == "" and end1: #["~3:4~5"]
							y1 = int(end1)
						elif start1 and end1: #["2~3:4~5"]
							x1 = int(start1)-1
							y1 = int(end1)
						elif value1 == "":  # [:"2~3"]
							pass
						else:
							pass
					else:
						pass

				else: #["1~2"], ~은 있으나 :이 없을때
					no1, no2 = input_range.split("~")
					if no1 and no2:
						if no1 == no2: #["1~1"]
							x1 = int(no1)-1
							y1 = int(no2)
						else :  # ["1~2"]
							x1 = int(no1)-1
							y1 = int(no2)
					elif no1 == "": #["~2"]
						y1 = int(no2)
					elif no2 == "": #["1~"]
						x1 = int(no1) - 1
					else: #["~"]
						pass

			elif ":" in input_range: # ~은 없고 :만 있을때
				no1, no2 = input_range.split(":")
				if no1 == "" and no2 == "": # [":"]
					pass
				elif no1 == no2: # ["1:1"]
					x1 = int(no1)
					y1 = int(no2)
				elif no1 == "": # [":1"]
					y1 = int(no2)
				elif no2 == "": # ["1:"]
					x1 = int(no1)
				else: # ["1:2"]
					x1 = int(no1)
					y1 = int(no2)

		return [x1, y1, x2, y2]

	def change_any_type_to_cap(self, results):
		"""
		자료중 문자열만 대문자로 변경한다, 그러나 이것은 리스트안에 리스트가있는 2차 리스트까지만 가능하다

		:param results:
		:return:
		"""
		final_datas = []
		temp_datas = []
		for datas in results:
			for data in datas:
				if type(data) == type('a'):
					temp_datas.append(str(data).upper)
				else:
					temp_datas.append(data)
			final_datas.append(temp_datas)
			temp_datas = []
		return final_datas

	def change_base_letter_jinsu_to_10jinsu(self, input_no, show_letter="가나다라마바사아자차카타파하"):
		"""
		입력형식의 값을 10진수값으로 변경하는것
		10진수값을 내가원하는 형식으로 변경하는것
		기본형을 예로들면 14진수이면서, "가나다라마바사아자차카타파하"로 표현되는것

		:param input_no:
		:param show_letter:
		:return:
		"""
		new_dic = {}
		for no, one_value in enumerate(show_letter):
			new_dic[one_value] = no

		total = 0
		checked_no = reversed(input_no)
		for no, one in enumerate(checked_no):
			total = total + len(show_letter) ** (no) * new_dic[one]
		return total

	def change_binary_to_int(self, bits):
		return int(bits, 2)

	def change_binary_to_string(self, bits):
		return ''.join([chr(int(i, 2)) for i in bits])

	def change_char_to_num(self, input_value="입력필요"):
		"""
		문자열 주소를 숫자로 바꿔주는 것 ( b -> 2 )
		문자가 오던 숫자가 오던 숫자로 변경하는 것이다
		주소를 바꿔주는 것이다

		youtil로 이동
		:param input_value: 입력 text
		"""
		aaa = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = aaa.findall(str(input_value))

		bbb = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = bbb.findall(str(input_value))

		if result_str != []:
			no = 0
			result = 0
			for one in input_value.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				result = result + 26 ** no * num
				no = no + 1
		elif result_num != []:
			result = int(input_value)
		else:
			result = "error"
		return result

	def change_data_position_by_two_index_for_list_2d(self, input_list_2d, input_no_list):
		"""
		2차원 리스트의 자료에서 각 라인별 2개의 위치를 바꾼는것
		change_position_for_list_2d_by_two_index([[1,2,3], [4,5,6]], [0,2])
		[[1,2,3], [4,5,6]] ==> [[3,2,1], [6,5,4]]
		메뉴에서 제외

		:param input_list_2d: list type 2dimension, 2차원의 리스트형
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def change_data_row_column(self):
		"""
		자료의 가로와 세로의 자료를바꾸는것

		:return:
		"""
		a = 111
		return a

	def change_data_to_list_2d(self, input_data):
		"""
		입렫된 자료를 2차원으로 만드는 것
		입력자료는 리스트나 듀플이어야 한다
		"""
		if type(input_data[0]) == type([]) or type(input_data[0]) == type(()):
			# 2차원의 자료이므로 입력값 그대로를 돌려준다
			result = input_data
		else:
			# 1차원의 자료라는 뜻으로, 이것을 2차원으로 만들어 주는 것이다
			result = []
			for one in input_data:
				result.append([one])
		return result

	def change_data_to_yline_style(self, input_data):
		"""
		1차원리스트를 2차원으로 만들면, 세로입력을 가로입력으로 바꾸는 것이다
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		result = self.change_list_1d_to_list_2d(input_data)
		return result

	def change_encodeing_type_001_success(self, ):
		"""
		기본적인 시스템에서의 인코딩을 읽어온다
		"""
		system_in_basic_incoding = sys.stdin.encoding
		system_out_basic_incoding = sys.stdout.encoding
		print("시스템의 기본적인 입력시의 인코딩 ====> ", system_in_basic_incoding)
		print("시스템의 기본적인 출력시의 인코딩 ====> ", system_out_basic_incoding)

	def change_eng_to_korea(self, raw_data, status):
		"""
		영문으로된 숫자를 한글이나 서수로 만들어 주는것

		:param raw_data:
		:param status:
		:return:
		"""
		a = 111
		return a

	def change_file_ecoding_type(self, path, file_name, original_type="EUC-KR", new_type="UTF-8", new_file_name=""):
		"""
		텍스트가 안 읽혀져서 확인해보니 인코딩이 달라서 안되어져서
		이것으로 전체를 변경하기위해 만듦
		"""
		full_path = path + "\\" + file_name
		full_path_changed = path + "\\" + new_file_name + file_name
		try:
			aaa = open(full_path, 'rb')
			result = chardet.detect(aaa.read())
			print(result['encoding'], file_name)
			aaa.close()

			if result['encoding'] == original_type:
				print("화일의 인코딩은 ======> {}, 화일이름은 {} 입니다".format(original_type, file_name))
				aaa = open(full_path, "r", encoding=original_type)
				file_read = aaa.readlines()
				aaa.close()

				new_file = open(full_path_changed, mode='w', encoding=new_type)
				for one in file_read:
					new_file.write(one)
				new_file.close()
		except:
			print("화일이 읽히지 않아요=====>", file_name)

		path = "C:\Python39-32\Lib\site-packages\myez_xl\myez_xl_test_codes"
		file_lists = os.listdir(path)
		for one_file in file_lists:
			self.file_type_change(path, one_file, "EUC-KR", "UTF-8", "_changed")

	def change_file_name(self, old_path, new_path):
		"""
		화일이름 변경
		"""
		old_path = self.check_file(old_path)
		new_path = self.check_file(new_path)
		os.rename(old_path, new_path)

	def change_file_path_to_dic_by_method_name(self, file_name):
		aaa = self.get_text_as_list(file_name)
		result = {}
		temp = ""
		title = "___header"
		for one_line in aaa:
			one_line_1 = one_line.strip()
			if one_line_1.startswith("def") and one_line_1.endswith(":"):
				result[title] = temp
				temp = one_line
				title = one_line_1[4:-1]
			else:
				temp = temp + one_line
		result[title] = temp
		return result

	def change_file_to_list_by_def(self, file_name):
		"""
		화일을 넣으면 def를 기준으로 리스트를 만드는것

		:param file_name:
		:return:
		"""
		result = {}
		def_text = ""
		def_name = ""
		f = open(file_name, "r", encoding="UTF8")
		lines = f.readlines()
		for one_text in lines:
			if str(one_text).strip()[0:3] == "def":
				if not def_name == "":
					result[def_name] = def_text
				def_name = str(one_text).strip()[3:].split("(")[0]
				def_text = def_text + one_text
		return result

	def change_float_to_format_text(self, input_value,big_digit,small_digit, fill_empty=" ",align="right",comma1000=True):
		"""
		f-string처럼 실수를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param small_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""
		if comma1000:
			changed_value = f"{round(float(input_value), small_digit):,}"
		else:
			changed_value = str(round(float(input_value), small_digit))

		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def change_folder_name(self, old_path, new_path):
		"""
		폴더이름 변경

		:param old_path:
		:param new_path:
		:return:
		"""
		os.rename(old_path, new_path)

	def change_folder_name_to_dic(self, path):
		folder_dict = {}
		for item in os.listdir(path):
			item_path = os.path.join(path, item)
			if os.path.isdir(item_path):
				# 보안때문에 접근이 거부된 화일들을 읽으려할때 어러나는것을 방지하기 위해
				try:
					folder_dict[item] = self.folder_to_dict(item_path)
				except:
					pass
			else:
				folder_dict[item] = None
		return folder_dict

	def change_group_as_new_step(self, all_data, initial_group, step):
		"""
		기존에 그룹화되어있는것을 기준으로, 최대갯수가 step의 갯수만큼 되도록 다시 그룹화 하는것이다

		:param all_data:
		:param initial_group:
		:param step:
		:return:
		"""
		result = []
		for list_1d in initial_group:
			if len(list_1d) > step:
				repeat_no = int((len(list_1d) + step - 1) / step)
				for no in range(repeat_no - 1):
					result.append(list_1d[no * step:(no + 1) * step])
				result.append(list_1d[(repeat_no - 1) * step:])
			else:
				result.append(list_1d)
		remain_all_data = all_data
		for list_1d in initial_group:
			for one_value in list_1d:
				remain_all_data.remove(one_value)
		result.append(remain_all_data)
		return result

	def change_int_to_format_text(self, input_value, big_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 숫자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""

		if comma1000:
			changed_value = f"{input_value:,}"
		else:
			changed_value = str(input_value)

		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def change_int_to_zerofill_style(self, input_num, total_len, fill_char = "0"):
		"""
		aaa= change_int_to_zerofill_style(3, 10)
		print(aaa)
		"""
		result = str(input_num).rjust(total_len, fill_char)
		return result

	def change_jamo_list_to_alpha(self, input_jamo_list):
		"""
		한글의 자음과 모음의 한글자를 알파벳으로 바꾸는것

		:param input_jamo_list:
		:return:
		"""
		result = ""
		for one_list in input_jamo_list:
			for jamo in one_list:
				eng_one = self.vars["jamo_vs_eng"][jamo]
				result = result + eng_one
			result = result + "z"
		return result

	def change_jamo_list_to_korea(self, input_jamo_list):
		"""
		한글의 자음과 모음을 한글의 글자로 바꾸는것

		:param input_jamo_list:
		:return:
		"""
		result = ""
		for one_list in input_jamo_list:
			for jamo in one_list:
				eng_one = self.vars["jamo_vs_eng"][jamo]
				result = result + eng_one
			result = result + "z"
		return result

	def change_jaum_to_xy_list(self, size=[1, 2], input_text="ㄱ"):
		"""
		자음을 넣고, 엑셀에 나타나는 xy사이즈를 계산하는것

		:param size:
		:param input_text:
		:return:
		"""
		x, y = size
		# x, y는 글자의 크기
		ja_01 = [["ㄱ"], [1, 1, 1, y], [1, y, x, y]]
		ja_02 = [["ㄴ"], [1, 1, x, 1], [x, 1, x, y]]
		ja_03 = [["ㄷ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y]]
		ja_04 = [["ㄹ"], [1, 1, 1, y], [1, y, 0.5 * x, y], [0.5 * x, y, 0.5 * x, 1], [0.5 * x, 1, x, 1], [x, 1, x, y]]
		ja_05 = [["ㅁ"], [1, 1, 1, y], [1, y, x, y], [x, y, x, 1], [x, 1, 1, 1]]
		ja_06 = [["ㅂ"], [1, 1, x, 1], [x, 1, x, y], [x, y, 1, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_07 = [["ㅅ"], [1, 0.5 * y, 0.3 * x, 0.5 * y], [0.3 * x, 0.5 * y, x, 1], [0.3 * x, 0.5 * y, x, y]]
		ja_08 = [["ㅇ"], [0.8 * x, 0.2 * y, 0.8 * x, 0.8 * y], [0.8 * x, 0.8 * y, 0.6 * x, y, ""],
				 [0.6 * x, y, 0.2 * x, y], [0.2 * x, y, 1, 0.8 * y, "/"], [1, 0.8 * y, 1, 0.2 * y],
				 [1, 0.2 * y, 0.2 * x, 1, ""], [0.2 * x, 1, 0.6 * x, 1], [0.6 * x, 1, 0.8 * x, 0.2 * y, "/"]]
		ja_09 = [["ㅈ"], [1, 1, 1, y], [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1, "/"],
				 [0.5 * x, 0.5 * y, x, y, ""]]
		ja_10 = [["ㅊ"], [0.2 * x, 0.5 * y, 1, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.2 * x, 0.5 * y, 0.4 * x, 0.5 * y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1], [0.5 * x, 0.5 * y, x, y, ""]]
		ja_11 = [["ㅋ"], [1, 1, 1, y], [1, y, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_12 = [["ㅌ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_13 = [["ㅍ"], [1, 1, 1, y], [x, 1, x, y], [1, 0.2 * y, x, 0.2 * y], [1, 0.8 * y, x, 0.8 * y]]
		ja_14 = [["ㅎ"], [1, 0.5 * y, 0.2 * x, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.4 * x, 0.3 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, 0.6 * x, y], [0.6 * x, y, 0.8 * x, y], [0.8 * x, y, x, 0.8 * y],
				 [x, 0.8 * y, x, 0.3 * y], [x, 0.3 * y, 0.8 * x, 1], [0.8 * x, 1, 0.6 * x, 1],
				 [0.6 * x, 1, 0.4 * x, 0.3 * y]]
		ja_31 = [["ㄲ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_32 = [["ㄸ"], [1, 1, 1, 0.4 * y], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], ]
		ja_33 = [["ㅃ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_34 = [["ㅆ"], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1], [0.4 * x, 0.3 * y, x, 0.5 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_35 = [["ㅉ"], [1, 1, 1, 0.5 * y], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1],
				 [0.4 * x, 0.3 * y, x, 0.5 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_36 = [["ㄳ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_37 = [["ㄵ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_38 = [["ㄶ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y],
				 [0.2 * x, 0.6 * y, 0.2 * x, y], [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y],
				 [0.6 * x, y, x, 0.9 * y], [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y],
				 [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y], [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_39 = [["ㄺ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_40 = [["ㄻ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], [x, y, x, 0.7 * y],
				 [x, 0.7 * y, 1, 0.7 * y], ]
		ja_41 = [["ㄼ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y],
				 [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_42 = [["ㄽ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y],
				 [0.4 * x, 0.8 * y, x, y], ]
		ja_43 = [["ㄾ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, 0.7 * y, x, 0.7 * y],
				 [x, 0.7 * y, x, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_44 = [["ㄿ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [x, 0.6 * y, x, y],
				 [1, 0.7 * y, x, 0.7 * y], [1, 0.9 * y, x, 0.9 * y], ]
		ja_45 = [["ㅀ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y], [0.2 * x, 0.6 * y, 0.2 * x, y],
				 [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y], [0.6 * x, y, x, 0.9 * y],
				 [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y], [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y],
				 [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_46 = [["ㅄ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]

		jamo1_dic = {"ㄱ": ja_01, "ㄴ": ja_02, "ㄷ": ja_03, "ㄹ": ja_04, "ㅁ": ja_05,
					 "ㅂ": ja_06, "ㅅ": ja_07, "ㅇ": ja_08, "ㅈ": ja_09, "ㅊ": ja_10,
					 "ㅋ": ja_11, "ㅌ": ja_12, "ㅍ": ja_13, "ㅎ": ja_14,
					 "ㄲ": ja_31, "ㄸ": ja_32, "ㅃ": ja_33, "ㅆ": ja_34, "ㅉ": ja_35,
					 "ㄳ": ja_36, "ㄵ": ja_37, "ㄶ": ja_38, "ㄺ": ja_39, "ㄻ": ja_40,
					 "ㄼ": ja_41, "ㄽ": ja_42, "ㄾ": ja_43, "ㄿ": ja_44, "ㅀ": ja_45, "ㅄ": ja_46,
					 }

		result = jamo1_dic[input_text]
		return result

	def change_korea_to_alpha(self, input_han):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것

		:param input_han:
		:return:
		"""
		aa = self.split_jamo_in_korea(input_han)
		result = self.change_jamo_list_to_korea(aa)
		return result

	def change_korea_to_jamo(self, text):
		"""
		한글자의 한글을 자음과 모음으로 구분해 주는것

		:param text:
		:return:
		"""
		one_byte_data = text.encode("utf-8")
		value_sum = 0
		char_type = ""

		if str(text) in "0123456789":
			char_type = "숫자"

		# compile_1 = re.compile("\d")
		# if str(text) in re.:
		#    char_type = "숫자"

		compile_1 = re.compile("\d+")
		no = compile_1.findall(text)

		try:
			no_1 = int(one_byte_data[0])
			no_2 = int(one_byte_data[1])
			no_3 = int(one_byte_data[2])
			new_no_1 = (no_1 - 234) * 64 * 64
			new_no_2 = (no_2 - 128) * 64
			new_no_3 = (no_3 - 128)
			value_sum = new_no_1 + new_no_2 + new_no_3

			if value_sum >= -28367 and value_sum <= -28338:
				char_type = "ja_only"
			if value_sum >= -28337 and value_sum <= -28317:
				char_type = "mo_only"

		except:
			char_type = "no_han"
			# 이것은 영어나 숫자, 특수문자라는 뜻이다
			no_1 = one_byte_data
			no_2 = ""
			no_3 = ""

		return [char_type, text]

	def change_list_1d_as_capital(self, input_list_1d):
		for a in range(len(input_list_1d)):
			try:
				input_list_1d[a] = (input_list_1d[a]).capitalize()
			except:
				pass
		return input_list_1d

	def change_list_1d_as_int(self, input_list):
		result = []
		for one in input_list:
			result.append(int(one))
		return result

	def change_list_1d_as_lower(self, data):
		"""
		모든 리스트의 자료를 소문자로 만드는것이다
		"""
		for a in range(len(data)):
			try:
				data[a] = (data[a]).lower()
			except:
				pass
		return data

	def change_list_1d_as_upper(self, data):
		"""
		1차원자료의 모든 내용물을 대문자로 만들어 주는 것이다
		"""
		for a in range(len(data)):
			try:
				data[a] = (data[a]).upper()
			except:
				pass
		return data

	def change_list_1d_data_to_space_by_step(self, input_list, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 ""으로 만드는것
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []

		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = ""
			result.append(temp_value)

		return result

	def change_list_1d_per_switch_2_data(self, input_data):
		"""
		두개의 자료들에 대해서만 자리를 바꾸는 것이다

		input_data: [a, b, c, d]
		result: [b, a, d, c]

		:param input_data:
		:return:
		"""
		result = []
		for one_data in range(int(len(input_data) / 2)):
			result.append(input_data[one_data * 2 + 1])
			result.append(input_data[one_data * 2])
		return result

	def change_list_1d_to_dic_with_serial_no(self, input_list_1d):
		#1차원리스트자료를 넣으면, 값:번호 형식의 사전을 만들어주는것
		#예 : ['가', '나', '다'] =>['가' :1, '나':2, '다':3]
		result =  []
		for index, one in enumerate(input_list_1d):
			result[one] = index+1
		return result

	def change_list_1d_to_list_2d(self, input_list_1d):
		"""
		1차원의 리스트를  2차원으로 만드는 것
		입력 : [1,2,3,4]
		출력 : [[1], [2], [3], [4],]
		메뉴에서 제외

		:param input_list_1d: list type, 1차원 리스트형
		:return:
		"""
		result = []
		if len(input_list_1d) > 0:
			if type(input_list_1d[0]) != type([]):
				for one in input_list_1d:
					result.append([one, ])
		return result

	def change_list_1d_to_list_2d_as_yline_style(self, input_list_1d):
		"""
		1 차원의 리스트를 2 차원으로 만드는 것
		:param input_list_1d: 1 차원 리스트형, [1,2,3,4]
		:return: [[1], [2], [3], [4],]
		"""
		result = self.change_list_1d_to_list_2d(input_list_1d)
		return result

	def change_list_1d_to_list_2d_by_no(self, input_data, input_no):
		"""
		입력된 1차원 자료를 no갯수만큼씩 짤라서 2차원으로 만드는 것

		:param input_data:
		:param input_no:
		:return:
		"""
		result = []
		total_len = int(len(input_data) / input_no) + 2
		for num in range(total_len):
			start_no = num * input_no
			end_no = (num + 1) * input_no
			result.append(input_data[start_no:end_no])
		return result

	def change_list_1d_to_list_2d_group_by_step(self, input_list_1d, input_no):
		"""
		[1,2,3,4,5,6,7,8] =>[[1,2,3],[4,5,6],[7,8]]

		입력된 1차원 자료를 no갯수만큼씩 묶어서 2차원으로 만드는 것

		:param input_list_1d:
		:param input_no:
		:return:
		"""
		result = []
		if len(input_list_1d) <= input_no:
			result = [input_list_1d]
		else:
			mok, namuji = divmod(len(input_list_1d), input_no)
			for num in range(mok):
				result.append(input_list_1d[num * input_no:(num + 1) * input_no])
			if namuji:
				result.append(input_list_1d[-1 * namuji:])
		return result

	def change_list_1d_to_list_2d_same_with_max_len(self, input_list="", xy=""):
		"""
		입력값이 1차원과 2차원의 자료가 섞여 일을때
		2차원의 자료형태로 모두 같은 크기로 만들어 주는것

		:param input_list:
		:param xy:
		:return:
		"""
		temp_result = []
		x_len, y_len = xy
		list1_max_len = len(input_list)
		list2_max_len = y_len
		count = int(list1_max_len / x_len)

		# 2차원자료중 가장 큰것을 계산한다
		for one_value in input_list:
			if type(one_value) == type([]):
				list2_max_len = max(list2_max_len, len(one_value))

		for one_value in input_list:
			temp_list = one_value
			# 모든 항목을 리스트형태로 만든다
			if type(one_value) != type([]):
				temp_list = [one_value]

			# 최대길이에 맞도록 적은것은 ""으로 갯수를 채운다
			if list2_max_len - len(temp_list) > 0:
				temp_list.extend([""] * (list2_max_len - len(temp_list)))
			temp_result.append(temp_list)

		result = []
		for no in range(count):
			start = no * x_len
			end = start + x_len
			result.append(temp_result[start:end])

		return result

	def change_list_1d_to_list_2d_with_yline_style(self, input_list_1d):
		"""
		1차원의 리스트를  2차원으로 만드는 것
		입력 : [1,2,3,4]
		출력 : [[1], [2], [3], [4],]
		메뉴에서 제외

		:param input_list_1d: list type, 1차원 리스트형
		:return:
		"""
		result = self.change_list_1d_to_list_2d(input_list_1d)
		return result

	def change_list_1d_to_one_text_by_chain_word(self, input_list, chain_word=" ,"):
		"""
		리스트 자료들을 중간문자를 추가하여 하나의 문자열로 만드는 것,
		“aa, bbb, ccc” 이런 식으로 만드는 방법이다
		"""
		result = ""
		for one_word in input_list:
			result = result + str(one_word) + str(chain_word)
		return result[:-len(chain_word)]

	def change_list_1d_to_space_by_step(self, input_list, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 ""으로 만드는것

		:param input_list:
		:param step:
		:param start:
		:return:
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []

		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = ""
			result.append(temp_value)

		return result

	def change_list_1d_to_text(self, input_list_2d, input_len):
		"""
		2차원리스트의 자료들을 정렬해서 텍스트로 만드는 것

		:param input_list_2d: 2차원 형태의 리스트
		:param input_len:
		:return:
		"""
		result_text = ""
		result = []
		len_list = {}
		for index, one in enumerate(input_list_2d[0]):
			len_list[index] = 0

		for list_1d in input_list_2d:
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		# print(len_list)

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				temp = temp + self.new_text_basic(str(one), len_list[index] + input_len)

			result_text = result_text + temp + '\n'
		return result_text

	def change_list_1d_to_text_with_chain_word(self, input_list, chain_word=" ,"):
		"""
		리스트 자료들을 중간문자를 추가하여 하나의 문자열로 만드는 것,
		“aa, bbb, ccc” 이런 식으로 만드는 방법이다
		리스트 자료들을 중간에 문자를 추가하여 한줄의 문자로 만드는 것
		입력형태 : ["aa", "bb","ccc"]
		출력형태 : “aa, bbb, ccc”

		:param input_list:
		:param chain_word:
		:return:
		"""
		result = ""
		for one_word in input_list:
			result = result + str(one_word) + str(chain_word)

		return result[:-len(chain_word)]

	def change_list_2d_as_same_len(self, input_list_2d="입력필요"):
		"""
		2차원 리스트의 최대 길이로 같게 만드는 것
		가끔 자료의 갯수가 달라서 생기는 문제가 발생할 가능성이 있는것을 맞추는것
		추가할때는 ""를 맞는갯수를 채워넣는다
		메뉴에서 제외

		:param input_list_2d: 2차원의 리스트형
		:return:
		"""
		input_text = None
		max_num = max(map(lambda x: len(x), input_list_2d))
		result = []
		for one in input_list_2d:
			one_len = len(one)
			if max_num == one_len:
				result.append(one)
			else:
				one.extend([input_text] * (max_num - one_len))
				result.append(one)
		return result

	def change_list_2d_as_xy_to_yx(self, input_list_2d):
		"""
		입력자료의 xy를 yx로 바꿔서 입력하는 것

		:param input_list_2d:
		:return:
		"""
		result = []
		for y in range(len(input_list_2d[0])):
			temp = []
			for x in range(len(input_list_2d)):
				temp.append(input_list_2d[x][y])
			result.append(temp)
		return result

	def change_list_2d_by_index(self, input_list_2d, input_no_list):
		"""
		2차원자료의 앞뒤를 바꾸는 코드이다
		youtil로 이동

		:param input_list_2d:
		:param input_no_list:
		:return:
		"""
		# input_no_list.sort()
		# input_no_list.reverse()
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def change_list_2d_from_xy_to_yx(self, input_list_2d="입력필요"):
		"""
		trans_list( input_list_2d="입력필요")
		2차원자료를 행과열을 바꿔서 만드는것
		단, 길이가 같아야 한다
		입력형태 :
		출력형태 :
		"""
		checked_list_2d = self.make_list_2d_samelen(input_list_2d)
		result = [list(x) for x in zip(*checked_list_2d)]
		return result

	def change_list_2d_n_title_list_to_dic_style(self, data_list_2d, title_list_1d):
		"""
		2차원리스트 + 제목 리스트 => 사전형식
		제목과 연결해서 사전을 만들어서 다음에 편하게 쓰고 넣을수있도록 만들려고 한다

		[["가가", "나나"], ["ab", "cd"]] + ["한글", "영어"] => [{"한글":"가가", "영어":"ab"}, {"한글":"나나", "영어":"cd"}]

		:param list_2d:
		:param list_title:
		:return:
		"""
		result = []
		if len(data_list_2d[0]) == len(title_list_1d):
			# 입력하는 자료와 제목의 갯수가 같이야 하는것을 확인
			for one in data_list_2d:
				one_dic = {}
				for no in range(len(title_list_1d)):
					one_dic[title_list_1d[no]] = one[no]
				result.append(one_dic)
		else:
			result = False
		return result

	def change_list_2d_to_another_list_2d_by_step_no(self, input_list_2d, index_no=4):
		"""
		2차원자료를 다 1차원으로 만든후, 다시 입력된 갯수만큼씩 묶어서 2차원으로 만든것

		:param input_list_2d: 2차원 형태의 리스트
		:param index_no:
		:return:
		"""
		result = []
		sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
		check_value = sorted_list_2d[0][index_no]
		temp = []
		for one_list in sorted_list_2d:
			if one_list[index_no] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]
				check_value = one_list[index_no]
		if temp:
			result.append(temp)
		return result

	def change_list_2d_to_dic(self, list_2d, list_title):
		"""
		2차원리스트 => 사전형식
		제목과 연결해서 사전을 만들어서 다음에 편하게 쓰고 넣을수있도록 만들려고 한다

		:param list_2d:
		:param list_title:
		:return:
		"""
		result = []
		for one in list_2d:
			my_dic = {}
			for no in range(len(list_title)):
				my_dic[list_title[no]] = one[no]
			result.append(my_dic)
		return result

	def change_list_2d_to_dic_by_first_line(self, input_list_2d):
		result = {}
		for one in input_list_2d[0]:
			result[one]=[]
		for ix, list_1d in enumerate(input_list_2d[1:]):
			for index, one in enumerate(list_1d):
				short_title = input_list_2d[0][index]
				result[short_title].append(one)
		return result

	def change_list_2d_to_dic_by_title(self, list_2d, list_title):
		"""
		2차원리스트를 제목과 연결해서 사전을 만들어서 다음에 편하게 쓰고 넣을수있도록 만들려고 한다

		:param list_2d:
		:param list_title:
		:return:
		"""

		result = []
		for one in list_2d:
			my_dic = {}
			for no in range(len(list_title)):
				my_dic[list_title[no]] = one[no]
			result.append(my_dic)
		return result

	def change_list_2d_to_differnet_xy_size(self, xy_list, resize=[1, 1]):
		"""
		리스트의 크기를 다시 설정하는 것
		메뉴에서 제외

		:param xy_list:
		:param resize:
		:return:
		"""
		result = []
		# 자료의 x갯수를 요청한것과 비교
		if len(xy_list) < resize[0] or resize[0] == 0:
			pass
		else:
			xy_list = xy_list[:resize[0]]
		# 자료의 y갯수를 요청한것과 비교
		for x_list in xy_list:
			if len(x_list) < resize[1] or resize[1] == 0:
				pass
			else:
				x_list = xy_list[:resize[0]]
			result.append(x_list)
		return result

	def change_list_2d_to_list_1d(self, input_data):
		"""
		항목 : ['항목1', '기본값1', '설명', {'입력형태1':'설명1', '입력형태2':'설명1',.... }]
		결과 ['항목1', '기본값1', '설명', '입력형태1:설명1', '입력형태2:설명1',.... }]
		위 형태의 자료를 한줄로 만들기위해 자료를 변경한다
		"""
		result = []
		for one_data in input_data:
			if type(one_data) == type({}):
				for key in list(one_data.Keys()):
					value = str(key) + " : " + str(one_data[key])
					result.append(value)
			elif type(one_data) == type(()) or type(one_data) == type([]) or type(one_data) == type(set()):
				for value in one_data:
					result.append(value)
			else:
				result.append(one_data)
		return result

	def change_list_2d_to_list_1d_by_group_count(self, input_list_2d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것

		:param input_list_2d:
		:param index_no:
		:return:
		"""
		result = []
		print(input_list_2d)
		sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
		print(sorted_list_2d)
		check_value = sorted_list_2d[0][index_no]
		temp = []
		for one_list in sorted_list_2d:
			if one_list[index_no] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]
				check_value = one_list[index_no]
		if temp:
			result.append(temp)
		return result

	def change_list_2d_to_one_text_with_chain_word(self, input_list_2d, chain_word= ""):
		"""
		2차원 리스트를 연결문자를 이용해서 만드는것

		:param input_list_2d:
		:param chain_word:
		:return:
		"""
		temp_text = ""
		for one_list in input_list_2d:
			for one_item in one_list:
				temp_text = temp_text + one_item + chain_word
		return temp_text

	def change_list_2d_to_same_len(self, input_data):
		"""
		가변적인 2차원배열을 최대크기로 모두 같이 만들어 준다
		"""
		result = []
		max_len = max(len(row) for row in input_data)
		for list_x in input_data:
			temp = list_x
			for no in range(len(list_x), max_len):
				temp.append("")
			result.append(temp)
		return result

	def change_list_2d_to_same_max_len(self, input_list_2d="입력필요"):
		"""
		2차원 리스트의 최대 길이로 같게 만드는 것
		가끔 자료의 갯수가 달라서 생기는 문제가 발생할 가능성이 있는것을 맞추는것
		추가할때는 ""를 맞는갯수를 채워넣는다
		메뉴에서 제외

		:param input_list_2d: 2차원의 리스트형
		:return:
		"""
		input_text = None
		max_num = max(map(lambda x: len(x), input_list_2d))
		result = []
		for one in input_list_2d:
			one_len = len(one)
			if max_num == one_len:
				result.append(one)
			else:
				one.extend([input_text] * (max_num - one_len))
				result.append(one)
		return result

	def change_list_2d_to_set_item(self, input_set, input_list_2d):
		"""
		2차원 리스트의 항목들을 set자료형으로 바꾸는 것
		input_list = [["변경전자료1", "변경후자료2"], ["변경전자료11", "변경후자료22"], ]

		:param input_set:
		:param input_list_2d:
		:return:
		"""
		for list_1d in input_list_2d:
			input_set.discard(list_1d[0])
			input_set.add(list_1d[1])
		return input_set

	def change_list_2d_to_set_style(self, input_list_2d):
		"""
		list_2d자료를 set형으로 바꾸는 것

		:param input_list_2d:
		:return:
		"""
		result = set()
		for list_1d in input_list_2d:
			for one in list_1d:
				if one != None and one != "":
					result.add(one)
		return result

	def change_list_2d_to_text(self, input_list_2d, input_len):
		"""
		2차원리스트의 자료들을 정렬해서 텍스트로 만드는 것

		:param input_list_2d: 2차원 형태의 리스트
		:param input_len:
		:return:
		"""
		result_text = ""
		result = []
		len_list = {}
		for index, one in enumerate(input_list_2d[0]):
			len_list[index] = 0

		for list_1d in input_list_2d:
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		# print(len_list)

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				temp = temp + self.new_text_basic(str(one), len_list[index] + input_len)

			result_text = result_text + temp + '\n'
		return result_text

	def change_list_3d_to_list_1d_by_group_count(self, input_list_3d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것

		:param input_list_3d:
		:param index_no:
		:return:
		"""
		result = []
		for input_list_2d in input_list_3d:
			sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
			grouped_list_3d = self.change_list_2d_to_list_1d_by_group_count(sorted_list_2d, index_no)
			result = result + grouped_list_3d
		return result

	def change_mixed_list_to_list_2d_by_step(self, input_list="", xy=""):
		"""
		입력값이 1차원과 2차원의 자료가 섞여 일을때
		2차원의 자료형태로 모두 같은 크기로 만들어 주는것

		:param input_list:
		:param xy:
		:return:
		"""
		temp_result = []
		x_len, y_len = xy
		list1_max_len = len(input_list)
		list2_max_len = y_len
		count = int(list1_max_len / x_len)

		# 2차원자료중 가장 큰것을 계산한다
		for one_value in input_list:
			if type(one_value) == type([]):
				list2_max_len = max(list2_max_len, len(one_value))

		for one_value in input_list:
			temp_list = one_value
			# 모든 항목을 리스트형태로 만든다
			if type(one_value) != type([]):
				temp_list = [one_value]

			# 최대길이에 맞도록 적은것은 ""으로 갯수를 채운다
			if list2_max_len - len(temp_list) > 0:
				temp_list.extend([""] * (list2_max_len - len(temp_list)))
			temp_result.append(temp_list)

		result = []
		for no in range(count):
			start = no * x_len
			end = start + x_len
			result.append(temp_result[start:end])

		return result

	def change_multi_empty_lines_to_one_line_in_file(self, file_name):
		"""
		화일을 읽어 내려가다가 2줄이상의 띄어쓰기가 된것을 하나만 남기는것
		텍스트로 저장된것을 사용하다가 필요해서 만듦

		:param file_name:
		:return:
		"""
		self.delete_over2_emptyline_in_file(file_name)

	def change_njinsu_to_10jinsu(self, input_no, input_jinsu=10):
		"""
		입력형식의 값을 10진수값으로 변경하는것

		:param input_no:
		:param input_jinsu:
		:return:
		"""
		original_letter = "0123456789abcdefghijklmnopqrstuvwxyz"
		base_letter = original_letter[0:input_jinsu]
		new_dic = {}
		for no, one_value in enumerate(base_letter):
			new_dic[one_value] = no
		total = 0
		checked_no = reversed(input_no)
		for no, one in enumerate(checked_no):
			total = total + len(base_letter) ** (no) * new_dic[one]
		return total

	def change_number_to_1000comma_num(self, input_no):
		"""
		입력된 숫자를 1000단위로 콤마를 넣는것

		:param input_no:
		:return:
		"""
		temp = str(input_no).split(".")
		total_len = len(temp[0])
		result = ""
		for num in range(total_len):
			one_num = temp[0][- num - 1]
			if num % 3 == 2:
				result = "," + one_num + result
			else:
				result = one_num + result
		if len(temp) > 1:
			result = result + "." + str(temp[1])
		return result

	def change_number_to_char(self, input_data="입력필요"):
		"""
		숫자를 문자로 바꿔주는 것
		2 -> b

		:param input_data: 입력숫자
		"""
		re_com = re.compile(r"([0-9]+)")
		result_num = re_com.match(str(input_data))

		if result_num:
			base_number = int(input_data)
			result_01 = ''
			result = []
			while base_number > 0:
				div = base_number // 26
				mod = base_number % 26
				if mod == 0:
					mod = 26
					div = div - 1
				base_number = div
				result.append(mod)
			for one_data in result:
				result_01 = string.ascii_lowercase[one_data - 1] + result_01
			final_result = result_01
		else:
			final_result = input_data
		return final_result

	def change_number_to_tel_style(self, input_value):
		"""
		전화번호나 핸드폰 번호 스타일을 바꿔주는것
		전화번호를 21345678 =>02-134-5678 로 변경하는 것

		:param input_value:
		:return:
		"""
		result = input_value
		value = str(int(input_value))
		if len(value) == 8 and value[0] == "2":
			# 22345678 => 02-234-5678
			result = "0" + value[0:1] + "-" + value[1:4] + "-" + value[4:]
		elif len(value) == 9:
			if value[0:2] == "2":
				# 223456789 => 02-2345-6789
				result = "0" + value[0:1] + "-" + value[1:5] + "-" + value[5:]
			elif value[0:2] == "11":
				# 113456789 => 011-345-6789
				result = "0" + value[0:2] + "-" + value[2:5] + "-" + value[5:]
			else:
				# 523456789 => 052-345-6789
				result = "0" + value[0:2] + "-" + value[2:5] + "-" + value[5:]
		elif len(value) == 10:
			# 5234567890 => 052-3456-7890
			# 1034567890 => 010-3456-7890
			result = "0" + value[0:2] + "-" + value[2:6] + "-" + value[6:]
		return result

	def change_position_for_list_2d_by_two_index(self, input_list_2d, input_no_list):
		"""
		2차원 리스트의 자료에서 각 라인별 2개의 위치를 바꾼는것
		change_position_for_list_2d_by_two_index([[1,2,3], [4,5,6]], [0,2])
		[[1,2,3], [4,5,6]] ==> [[3,2,1], [6,5,4]]

		:param input_list_2d: list type 2dimension, 2차원의 리스트형
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def change_price_style(self, budjet):
		if budjet != None and budjet != "":
			if int(budjet) > 100000000:
				#천만원보다 높을때
				changed_budjet = f"[(int(budjet) / 100000000):.1f] 억원"
			else:
				changed_budjet = f"[(int(budjet) / 1000000):.1f] 백만원"
		return changed_budjet

	def change_price_to_text_price(self, input_price):
		"""
		백만원단위, 전만원단위, 억단위로 구분

		:param input_price:
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result

	def change_python_file_to_dic_by_method_name(self, file_name):
		source_code = inspect.getsource(file_name)
		result = {}
		temp = ""
		title = "___header"
		for one_line in source_code.split("\n"):
			one_line_1 = one_line.strip()
			if one_line_1.startswith("def") and one_line_1.endswith(":"):
				# print(one_line_1)
				result[title] = temp
				temp = one_line + "\n"
				title = one_line_1[4:-1]
			else:
				temp = temp + one_line + "\n"
		result[title] = temp
		return result

	def change_python_file_to_dic_group_by_method_name(self, file_name):
		source_code = inspect.getsource(file_name)
		result = {}
		temp = ""
		title = "___header"
		for one_line in source_code.split("\n"):
			one_line_1 = one_line.strip()
			if one_line_1.startswith("def") and one_line_1.endswith(":"):
				# print(one_line_1)
				result[title] = temp
				temp = one_line + "\n"
				title = one_line_1[4:-1]
			else:
				temp = temp + one_line + "\n"
		result[title] = temp
		return result

	def change_python_file_to_list_data(self, file_name):
		"""
        python으로만든 화일을 읽어서 함수이름과 입력변수를 알아내기 위한것
        """
		result = []
		file_pointer = open(file_name, 'r', encoding='utf-8')  # 텍스트 읽어오기
		lines_list = file_pointer.readlines()  # 한번에 다 읽기

		for one_value in lines_list:
			changed_value = one_value.strip()

			if changed_value.startswith("def "):
				var_dic = {}
				split_1 = changed_value[3:].split("(")
				# 함수이름을 찾은것
				func_name = split_1[0].strip()

				if len(split_1) > 1:
					# 여러변수들을 ,로 분리하는것
					element_text = split_1[1].strip()
					element_text = element_text.replace("):", "")
					element_list = element_text.split(",")

					# 각 변수들을 사전으로 만들어서 넣기 위한것
					for one in element_list:
						new_one = one.split("=")
						if len(new_one) == 2:
							value = new_one[1].strip()
							if new_one[1].strip() == "''" or new_one[1].strip() == '""':
								value = ""
							var_dic[new_one[0].strip()] = value
						else:
							var_dic[new_one[0].strip()] = ""
				# var_dic.pop("self")
				result.append([func_name, var_dic])
		return result

	def change_python_file_to_list_group_by_line(self, file_name):
		"""
        python으로만든 화일을 읽어서 함수이름과 입력변수를 알아내기 위한것
        """
		result = []
		file_pointer = open(file_name, 'r', encoding='utf-8')  # 텍스트 읽어오기
		lines_list = file_pointer.readlines()  # 한번에 다 읽기

		for one_value in lines_list:
			changed_value = one_value.strip()

			if changed_value.startswith("def "):
				var_dic = {}
				split_1 = changed_value[3:].split("(")
				# 함수이름을 찾은것
				func_name = split_1[0].strip()

				if len(split_1) > 1:
					# 여러변수들을 ,로 분리하는것
					element_text = split_1[1].strip()
					element_text = element_text.replace("):", "")
					element_list = element_text.split(",")

					# 각 변수들을 사전으로 만들어서 넣기 위한것
					for one in element_list:
						new_one = one.split("=")
						if len(new_one) == 2:
							value = new_one[1].strip()
							if new_one[1].strip() == "''" or new_one[1].strip() == '""':
								value = ""
							var_dic[new_one[0].strip()] = value
						else:
							var_dic[new_one[0].strip()] = ""
				# var_dic.pop("self")
				result.append([func_name, var_dic])
		return result

	def change_python_file_to_sorted_by_def(self, file_name):
		"""
		python으로만든 화일을 읽어서 def를 기준으로 정렬해서 돌려주는 것
		1. 프린트해서 나타냄
		2. 화일로 정렬된것을 만듦
		3. 리스트형태로 돌려주는것

		:param file_name:
		:return:
		"""
		file_pointer = open(file_name, 'r', encoding='utf-8')  # 텍스트 읽어오기
		file_list = file_pointer.readlines()  # 한번에 다 읽기

		all_text = ""
		temp = []
		result = {}
		title = "000"
		for one_line_text in file_list:
			# def로 시작이 되는지 알아 내는것
			if str(one_line_text).strip()[0:3] == "def" and str(one_line_text).strip()[-1] == ":":
				result[title] = temp  # def나오기 전까지의 자료를 저장합니다
				temp = []
				title = str(one_line_text).strip()  # 사전의 key를 def의 이름으로 만드는 것이다
			temp.append(one_line_text)
		result[title] = temp

		sorted_keys = list(result.keys())
		sorted_keys.sort()  # key인 제목을 기준으로 정렬을 하도록 만든것
		write_file = open("output_output_33.txt", 'w', encoding='utf-8')  # 텍스트 읽어오기

		for one_key in sorted_keys:
			for one_line in result[one_key]:
				one_line = one_line.replace("\n", "")
				# print(one_line)  # 별도로 화일로 만들지 않고, 터미널에 나타나는것을 복사해서 사용하는 방법으로 만듦
				all_text = all_text + one_line
				write_file.write(one_line + "\n")
		write_file.close()
		return result

	def change_python_file_to_text_file_sorted_by_def(self, file_name):
		"""
		python으로만든 화일을 읽어서 def를 기준으로 정렬해서 돌려주는 것
		1. 프린트해서 나타냄
		2. 화일로 정렬된것을 만듦
		3. 리스트형태로 돌려주는것

		:param file_name:
		:return:
		"""
		file_pointer = open(file_name, 'r', encoding='utf-8')  # 텍스트 읽어오기
		file_list = file_pointer.readlines()  # 한번에 다 읽기

		all_text = ""
		temp = []
		result = {}
		title = "000"
		for one_line_text in file_list:
			# def로 시작이 되는지 알아 내는것
			if str(one_line_text).strip()[0:3] == "def" and str(one_line_text).strip()[-1] == ":":
				result[title] = temp  # def나오기 전까지의 자료를 저장합니다
				temp = []
				title = str(one_line_text).strip()  # 사전의 key를 def의 이름으로 만드는 것이다
			temp.append(one_line_text)
		result[title] = temp

		sorted_keys = list(result.keys())
		sorted_keys.sort()  # key인 제목을 기준으로 정렬을 하도록 만든것
		write_file = open("output_output_33.txt", 'w', encoding='utf-8')  # 텍스트 읽어오기

		for one_key in sorted_keys:
			for one_line in result[one_key]:
				one_line = one_line.replace("\n", "")
				# print(one_line)  # 별도로 화일로 만들지 않고, 터미널에 나타나는것을 복사해서 사용하는 방법으로 만듦
				all_text = all_text + one_line
				write_file.write(one_line + "\n")
		write_file.close()
		return result

	def change_re_group_by_step(self, all_data, initial_group, step):
		"""
		기존에 그룹화되어있는것을 기준으로, 최대갯수가 step의 갯수만큼 되도록 다시 그룹화 하는것이다

		:param all_data:
		:param initial_group:
		:param step:
		:return:
		"""
		result = []
		for list_1d in initial_group:
			if len(list_1d) > step:
				repeat_no = int((len(list_1d) + step - 1) / step)
				for no in range(repeat_no - 1):
					result.append(list_1d[no * step:(no + 1) * step])
				result.append(list_1d[(repeat_no - 1) * step:])
			else:
				result.append(list_1d)
		remain_all_data = all_data
		for list_1d in initial_group:
			for one_value in list_1d:
				remain_all_data.remove(one_value)
		result.append(remain_all_data)
		return result

	def change_set_item_by_list(self, input_set, input_list_2d):
		"""
		input_list = [["변경전자료1", "변경후자료2"], ["변경전자료11", "변경후자료22"], ]

		:param input_set:
		:param input_list_2d:
		:return:
		"""
		for list_1d in input_list_2d:
			input_set.discard(list_1d[0])
			input_set.add(list_1d[1])
		return input_set

	def change_size_for_list_2d(self, input_list_2d, x_start, y_start, x_len, y_len):
		"""
		2차원 리스트의 사이즈를 변경하는 것
		2차원안의 1차원자료를 몇개씩 줄여서 새롭게 2차원자료를 만드는 것이다

		:param input_list_2d:
		:param x_start:
		:param y_start:
		:param x_len:
		:param y_len:
		:return:
		"""
		result = []
		if len(input_list_2d) >= x_start + x_len and len(input_list_2d[0]) >= y_start + y_len:
			changed_list_2d = input_list_2d[x_start:x_start + x_len - 1]
			for list_1d in changed_list_2d:
				result.append(list_1d[y_start:y_start + y_len - 1])
		return result

	def change_special_letter_jinsu_to_10jinsu(self, input_no, show_letter="가나다라마바사아자차카타파하"):
		"""
		입력형식의 값을 10진수값으로 변경하는것
		10진수값을 내가원하는 형식으로 변경하는것
		기본형을 예로들면 14진수이면서, "가나다라마바사아자차카타파하"로 표현되는것

		:param input_no:
		:param show_letter:
		:return:
		"""
		new_dic = {}
		for no, one_value in enumerate(show_letter):
			new_dic[one_value] = no

		total = 0
		checkednum = reversed(input_no)
		for no, one in enumerate(checkednum):
			total = total + len(show_letter) ** (no) * new_dic[one]
		return total

	def change_string_to_binary_list(self, st):
		result = [bin(ord(i))[2:].zfill(8) for i in st]
		return result

	def change_text_as_cap(self, datas, argue=1):
		"""
		대소문자를 변경하는 것입니다
		이것은 단일 리스트만 가능하게 만들었다,  리스트안에 리스트가있는것은 불가능하다 (2004년 5월 2일 변경)
		기본은 대문자로 바꾸는 것이다

		:param datas:
		:param argue:
		:return:
		"""
		results = []
		for data in datas:
			print(data)
			if argue == 0: result = str(data).lower  # 모두 소문자로
			if argue == 1: result = str(data).upper  # 모두 대문자로
			if argue == 2: result = str(data).capitalize  # 첫글자만 대문자
			if argue == 3: result = str(data).swapcase  # 대소문자 변경
			results.append(result)
		return results

	def change_text_as_reverse(self, input_text):
		text2list = list(input_text)
		text2list.reverse()
		result = "".join(text2list)
		return result

	def change_text_by_encoding_type(self, text, encoding_type):
		"""
		인코딩 상태를 확인하는 것
		text_encoding_data("Hello", "utf-8")

		:param text:
		:param encoding_type:
		:return:
		"""
		byte_data = text.encode(encoding_type)
		hex_data_as_str = "".join("(0)".format(hex(c)) for c in byte_data)
		int_data_as_str = "".join(" (0)").format(int(c) for c in byte_data)
		return int

	def change_text_only_to_cap(self, results):
		"""
		자료중 문자열만 대문자로 변경한다, 그러나 이것은 리스트안에 리스트가있는 2차 리스트까지만 가능하다

		:param results:
		:return:
		"""
		final_datas = []
		temp_datas = []
		for datas in results:
			for data in datas:
				if type(data) == type('a'):
					temp_datas.append(str(data).upper)
				else:
					temp_datas.append(data)
			final_datas.append(temp_datas)
			temp_datas = []
		return final_datas

	def change_text_to_binary_list(self, st):
		"""
		문자열을 바이너리 리스트로 만드는것

		:param st:
		:return:
		"""
		result = [bin(ord(i))[2:].zfill(8) for i in st]
		return result

	def change_text_to_dic_by_len(self, input_text):
		"""
		갯수만큼의 문자열을 사전으로 만드는 것

		:param input_text:
		:return:
		"""
		input_text = input_text.replace(" ", "")
		input_text = input_text.upper()
		result = {}
		for one_letter in input_text:
			if one_letter in list(result.keys()):
				result[one_letter] = result[one_letter] + 1
			else:
				result[one_letter] = 1
		return result

	def change_text_to_list_1d_by_step(self, input_data, input_list):
		"""
		입력문자를 숫자만큼씨 짤라서 리스트로 만드는 것

		:param input_data:
		:param input_list:
		:return:
		"""
		result = []
		total_len = 0
		start_no = 0
		for no in range(len(input_list)):
			if no != 0:
				start_no = total_len
			end_len = input_list[no]
			result.append(input_data[start_no:start_no + end_len])
			total_len = total_len + end_len
		return result

	def change_text_to_text_by_fstring_format(self, input_value, big_digit, fill_empty=" ", align="right"):
		"""
		f-string처럼 문자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:return:
		"""
		changed_value = str(input_value)
		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def change_text_to_text_file(self, file_full_name, input_text):
		"""
		텍스트자료를 화일로 저장하는것

		:param file_full_name:
		:param input_text:
		:return:
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one_line in input_text:
			new_file.write(one_line)

	def change_tuple_to_list(self, input_data):
		if isinstance(input_data, (list, tuple)):
			return [self.tuple_to_list(x) for x in input_data]
		elif isinstance(input_data, set):
			return set(self.tuple_to_list(x) for x in input_data)
		else:
			return input_data

	def change_tuple_to_list_2d(self, input_tuple_2d):
		"""
		튜플의 2차원자료를 리스트 2차로 만드는 것

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		checked_tuple_2d = self.check_list_2d(input_tuple_2d)

		result = []
		for x in range(len(checked_tuple_2d)):
			temp = []
			for y in range(len(checked_tuple_2d[0])):
				value = checked_tuple_2d[x][y]
				if value:
					pass
				else:
					value = ""
				temp.append(value)
			result.append(temp)
		return result

	def change_two_data_position_for_list_1d(self, input_data):
		"""
		input_data : [a, b, c, d]
		result : [b, a, d, c]
		두개의 자료들에 대해서만 자리를 바꾸는 것이다

		:param input_data:
		:return:
		"""
		result = []
		for one_data in range(int(len(input_data) / 2)):
			result.append(input_data[one_data * 2 + 1])
			result.append(input_data[one_data * 2])
		return result

	def change_two_list_1d_to_dic(self, key_list, value_list):
		"""
		두개의 리스트를 받으면 사전으로 만들어 주는 코드

		:param key_list:
		:param value_list:
		:return:
		"""
		result = dict(zip(key_list, value_list))
		return result

	def change_two_list_1d_to_list_2d_group_by_same_xy_data(self, input_list_1, input_list_2):
		"""
		두개의 리스트를 서로 묶어서, 새로운 리스트를 만드는 것
		[1,2,3], ["a","b","c"] ==> [[1, "a"],[2,"b"],[3,"c"]]

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result = []
		for x, y in zip(input_list_1, input_list_2):
			result.append(x + y)
		return result

	def change_two_list_2d_to_one_list_2d_with_samelen(self, input_list_2d_1, input_list_2d_2):
		"""
		선택한 영역이 2개를 서로 같은것을 기준으로 묶을려고하는것이다
		제일앞의 한줄이 같은것이다
		만약 묶을려고 할때 자료가 없을때는 그 기준자료만큼 빈자료를 넣어서 다음자료를 추가하는 것이다

		:param input_list_2d_1:
		:param input_list_2d_2:
		:return:
		"""
		no_of_list_2d_1 = len(input_list_2d_1[0]) - 1
		no_of_list_2d_2 = len(input_list_2d_2[0]) - 1
		empty_list_2d_1 = [""] * no_of_list_2d_1
		empty_list_2d_2 = [""] * no_of_list_2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list_2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list_2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list_2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list_2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def change_two_list_to_dic(self, key_list, value_list):
		"""
		두개의 리스트를 받으면 사전으로 만들어 주는 코드

		:param key_list:
		:param value_list:
		:return:
		"""
		result = dict(zip(key_list, value_list))
		return result

	def change_value(self, raw_data, before, after, status):
		"""
		자료의 들어가있는 값을 바꾸는 기능입니다

		:param raw_data:
		:param before:
		:param after:
		:param status:
		:return:
		"""
		a = 111
		return a

	def change_waste_data(self, original_data):
		"""
		숫자와 문자만 남기는것
		result = []
		입력형태 :
		출력형태 :
		"""
		result = []
		for one_data in original_data:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def change_xylist_to_yxlist(self, input_list_2d="입력필요"):
		"""
		trans_list( input_list_2d="입력필요")
		2차원자료를 행과열을 바꿔서 만드는것
		단, 길이가 같아야 한다

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		checked_list_2d = self.change_list_2d_to_same_max_len(input_list_2d)
		result = [list(x) for x in zip(*checked_list_2d)]
		return result

	def checek_list(self, input_data):
		"""
		입력된 1차원 자료를 2차원으로 만드는 것
		입력자료는 리스트나 듀플이어야 한다

		:param input_data:
		:return:
		"""
		result = []
		for one in input_data:
			if type(one) == type([]) or type(one) == type(()):
				temp = []
				for item in one:
					temp.append(item)
			else:
				temp = one
			result.append(temp)
		return result

	def check_cell_type(self, input_data):
		"""
		하나의 영역으로 들어온 것이 어떤 형태인지를 알아 내는 것이다

		:param input_data:
		:return:
		"""
		result = ""
		if input_data[0][0] in string.ascii_lowercase and input_data[1][0] in string.digits:
			result = "a1"
		if input_data[0][0] in string.ascii_lowercase and input_data[1][0] in string.ascii_lowercase:
			result = "aa"
		if input_data[0][0] in string.digits and input_data[1][0] in string.digits:
			result = "11"
		return result

	def check_char_type_for_one_char(self, text):
		"""
		한글자의 글자 형태를 알아오는것

		:param text:
		:return:
		"""
		one_byte_data = text.encode("utf-8")
		value_sum = 0
		char_type = ""

		if str(text) in "0123456789":
			char_type = "숫자"

		compile_1 = re.compile("\d+")
		no = compile_1.findall(text)

		try:
			no_1 = int(one_byte_data[0])
			no_2 = int(one_byte_data[1])
			no_3 = int(one_byte_data[2])
			new_no_1 = (no_1 - 234) * 64 * 64
			new_no_2 = (no_2 - 128) * 64
			new_no_3 = (no_3 - 128)
			value_sum = new_no_1 + new_no_2 + new_no_3

			if value_sum >= -28367 and value_sum <= -28338:
				char_type = "ja_only"
			if value_sum >= -28337 and value_sum <= -28317:
				char_type = "mo_only"

		except:
			char_type = "no_han"
			# 이것은 영어나 숫자, 특수문자라는 뜻이다
			no_1 = one_byte_data
			no_2 = ""
			no_3 = ""
		# char_type : 글자의 형태, 숫자, 한글

		return [char_type, text]

	def check_data_as_list_1d(self, input_data):
		"""
		입렫된 자료를 2차원으로 만드는 것
		입력자료는 리스트나 듀플이어야 한다
		"""
		if type(input_data[0]) == type([]) or type(input_data[0]) == type(()):
			# 2차원의 자료이므로 입력값 그대로를 돌려준다
			result = input_data
		else:
			# 1차원의 자료라는 뜻으로, 이것을 2차원으로 만들어 주는 것이다
			result = []
			for one in input_data:
				result.append([one])
		return result

	def check_data_type(self, input_data="입력필요"):
		"""
		영역으로 입력된 자료의 형태를 확인해서 돌려주는 것
		입력값으로 들어온것이 리스트형태인지, 영역의 형태인지, 값의 형태인지를 알아보는것이다

		:param input_data: 입력자료
		:return: "list", "range", "value", "error"
		"""
		if type(input_data) == type([]):
			result = "list"
		elif len(str(input_data).split(":")) > 1:
			result = "range"
		elif type(input_data) == type("aaa"):
			result = "value"
		else:
			result = "error"
		return result

	def check_data_type_for_data(self, input_data):
		"""
		입력된 자료형을 확인하는것

		:param input_data: 입력자료
		"""
		if input_data == None or input_data == [] or input_data == ():
			result = "none"

		elif type(input_data) == type([]):
			if type(input_data[0]) == type([]):
				# 2차원의 자료이므로 입력값 그대로를 돌려준다
				result = "list_2d_list"
			elif type(input_data[0]) == type(()):
				result = "list_tuple"
			else:
				result = "list_1d"
		elif type(input_data) == type(()):
			if type(input_data[0]) == type([]):
				# 2차원의 자료이므로 입력값 그대로를 돌려준다
				result = "tuple_list"
			elif type(input_data[0]) == type(()):
				result = "tuple_tuple"
			else:
				result = "tuple1d"
		elif type(input_data) == type(123):
			result = "int"
		elif type(input_data) == type("123"):
			result = "string"
		return result

	def check_data_types_for_list_2d(self, input_list_2d):
		"""
		입력된 2차원자료를 프린트가 가능한 형태로 만든다
		숫자와 문자를 제외하고는 모드 None으로 만드는 것
		"""
		result = []
		for x, list_1d in enumerate(input_list_2d):
			t_list = []
			for y, value in enumerate(list_1d):
				temp = self.check_data_type_for_data(value)
				# print(temp, value)
				if temp in ["int", "string"]:
					t_list.append(value)
				else:
					t_list.append(None)
			result.append(t_list)
		print(result)
		return result

	def check_file(self, file):
		"""
		입력자료가 폴더를 갖고있지 않으면 현재 폴더를 포함해서 돌려준다

		:param file:
		:return:
		"""
		if len(file.split(".")) > 1:
			result = file
		else:
			cur_dir = self.read_current_path()
			result = cur_dir + "\\" + file
		return result

	def check_file_name(self, temp_title):
		"""
		화일의 제목으로 사용이 불가능한것을 제거한다

		:param temp_title:
		:return:
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
						["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return

	def check_file_path(self, file):
		"""
		입력자료가 폴더를 갖고있지 않으면 현재 폴더를 포함해서 돌려준다
		"""
		if len(file.split(".")) > 1:
			result = file
		else:
			cur_dir = self.read_current_path()
			result = cur_dir + "\\" + file
		return result

	def check_font_data(self, input_list):
		result = {}
		for value in input_list:
			if type(value) == type(123):
				result["size"] = value
			elif value in ["bold", "진하게"]:
				result["bold"] = True
			elif value in ["밑줄", "underline"]:
				result["underline"] = True
			elif value in ["italic", "이탈릭채", "기울게", "이탈릭"]:
				result["italic"] = True
			else:
				try:
					rgbint = self.color.change_scolor_to_rgbint(value)
					result["color"] = rgbint
				except:
					pass
		return result

	def check_font_element(self, input_key):
		"""
		단어중 가장 가까운 단어들 찾기
		입력형식은 bold(),진하게(yes).. 이런식으로 입력이 되도록 하면 어떨까??

		:param input_key:
		:return:
		"""
		base_dic = {"bold": "bold", "진하게": "bold",
					"색": "color", "색깔": "color", "색상": "color", "color": "color",
					"크기": "size", "사이즈": "size", "size": "size",
					"밑줄": "underline", "underline": "underline",
					"취소": "strikethrough", "취소선": "strikethrough", "strike": "strikethrough",
					"strikethrough": "strikethrough",
					"이름": "name", "폰트": "name", "폰트명": "name", "name": "name",
					"italic": "italic", "이탈릭채": "italic", "기울게": "italic", "이탈릭": "italic",
					"윗첨자": "superscript", "superscript": "superscript",
					"아래첨자": "subscript", "subscript": "subscript",
					"투명도": "alpha", "alpha": "alpha", "알파": "alpha", "알파값": "alpha",
					"수직정렬": "align_v", "수직": "align_v", "align_v": "align_v",
					"수평정렬": "align_h", "수평": "align_h", "align_h": "align_h",
					"style": "style", "스타일": "style", "type": "style",
					"너비": "width", "넓이": "width", "width": "width", "길이": "width",
					"높이": "height", "height": "height",
					}
		try:
			result = base_dic[input_key]
		except:
			result = False

		return result

	def check_hangul_jamo(self, text):
		"""
		한글자의 한글을 자음과 모음으로 구분해 주는것

		:param text:
		:return:
		"""
		one_byte_data = text.encode("utf-8")
		value_sum = 0
		char_type = ""

		if str(text) in "0123456789":
			char_type = "숫자"

		# compile_1 = re.compile("\d")
		# if str(text) in re.:
		#    char_type = "숫자"

		compile_1 = re.compile("\d+")
		no = compile_1.findall(text)

		try:
			no_1 = int(one_byte_data[0])
			no_2 = int(one_byte_data[1])
			no_3 = int(one_byte_data[2])
			new_no_1 = (no_1 - 234) * 64 * 64
			new_no_2 = (no_2 - 128) * 64
			new_no_3 = (no_3 - 128)
			value_sum = new_no_1 + new_no_2 + new_no_3

			if value_sum >= -28367 and value_sum <= -28338:
				char_type = "ja_only"
			if value_sum >= -28337 and value_sum <= -28317:
				char_type = "mo_only"

		except:
			char_type = "no_han"
			# 이것은 영어나 숫자, 특수문자라는 뜻이다
			no_1 = one_byte_data
			no_2 = ""
			no_3 = ""

		return [char_type, text]

	def check_int_for_list(self, input_list):
		"""
		입력리스트중에 정수만 골라내는 것

		:param input_list:
		"""
		input_list = self.change_xylist_to_list(input_list)
		result = False
		for one in input_list:
			if type(123) == type(one):
				result = one
				break
		return result

	def check_josa(self, front_word, input_josa):
		"""
		끝글자가 모음일때와 자음일때를 구별해서 사용
		앞의 글자에 따라서 맞는 조사를 선택하는 것

		:param front_word:
		:param input_josa:
		:return:
		"""
		result = False
		base_word_set = [["은", "는"], ["이", "가"], ["을", "를"], ["과", "와"], ["으로", "로"]]
		moum_tf = 0
		one_char = str(front_word).strip([-1])
		temp = self.jf.is_match("[한글:1~]", one_char)
		if temp:
			aaa = self.split_korea_to_jamo(one_char)
			if aaa[0][2]:
				moum_tf = 1
			for list_1d in base_word_set:
				if input_josa in list_1d:
					result = list_1d[moum_tf]
					break
		else:
			result = False
		return result

	def check_korea_price_unit(self, input_price):
		"""
		백만원단위, 전만원단위, 억단위로 구분

		:param input_price:
		:return:
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result

	def check_line_element(self, input_key):
		"""
		단어중 가장 가까운 단어들 찾기
		입력형식은 bold(),진하게(yes).. 이런식으로 입력이 되도록 하면 어떨까??

		:param input_key:
		:return:
		"""
		base_dic = {
			"너비": "width", "넓이": "width", "width": "width", "길이": "width",
			"style": "style", "스타일": "style", "type": "style",
			"색": "color", "색깔": "color", "색상": "color", "color": "color",
			"투명도": "alpha", "alpha": "alpha", "알파": "alpha", "알파값": "alpha",
		}
		try:
			result = base_dic[input_key]
		except:
			result = False
		return result

	def check_list(self, input_data):
		"""
		입력된 1차원 자료를 2차원으로 만드는 것
		입력자료는 리스트나 듀플이어야 한다

		:param input_data:
		:return:
		"""
		result = []
		for one in input_data:
			if type(one) == type([]) or type(one) == type(()):
				temp = []
				for item in one:
					temp.append(item)
			else:
				temp = one
			result.append(temp)
		return result

	def check_list_1d(self, input_data):
		if type(input_data) == type([]):
			result = input_data
		else:
			result = [input_data]
		return result

	def check_list_2d(self, input_data):
		"""
		입력된 자료형에 따라서 2차원으로 만들어 주는것
		1차원의 리스트는 [1,2,3,4]의 형태이며
		이것은 같은 가로에 세로의 글자가 다른것이다
		메뉴에서 제외

		:param input_data: 입력자료
		:return:

		"""
		if type(input_data) == type([]) or type(input_data) == type(()):
			if type(input_data[0]) == type([]) or type(input_data[0]) == type(()):
				result = input_data
			else:
				result = [input_data]
		elif type(input_data) == type("123") or type(input_data) == type(123):
			result = [[input_data]]
		else:
			result = input_data
		return result

	def check_list_as_col_name(self, input_list):
		"""
		입력형태 : 제목리스트, 2차원 값리스트형
		출력형태 : dataframe로 바꾼것
		"""
		result = []
		if input_list == "":
			if type(input_list[0]) != type([]):
				for one in input_list:
					result.append([one, ])
		return result

	def check_max_size_for_list_2d(self, list_2d_data):
		"""
		2차원 배열의 제일 큰 갯수를 확인한다
		#an_array = [[1, 2], [3, 4, 5]]
		#print("2차배열 요소의 최대 갯수는 ==>", check_list_maxsize(an_array))
		"""
		max_length = max(len(row) for row in list_2d_data)
		return max_length

	def check_min_result(self, input_dic, except_key=[]):
		"""
		갯수가 제일 적은 것을 찾는 것
		입력된 사전을 기준으로 사전의 키가 except_key는 제외하고,
		사전의 value에서 가장 작은 갯수의 key를 찾는 것이다

		:param input_dic:
		:param except_key:
		:return:
		"""
		selected_key = ""
		temp_count = 999
		for key_value in input_dic.keys():
			if not key_value in except_key:
				if len(input_dic[key_value]) < temp_count:
					temp_count = len(input_dic[key_value])
					selected_key = key_value
		return selected_key

	def check_one_address(self, input_text=""):
		"""
		입력된 1개의 주소를 문자인지, 숫자인지
		숫자로 변경하는 것이다

		:param input_text: 입력 text
		"""
		re_com_1 = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = re_com_1.findall(str(input_text))

		re_com_2 = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = re_com_2.findall(str(input_text))

		if result_num == [] and result_str != []:
			address_type = "string"
			no = 0
			address_int = 0
			for one in input_text.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				address_int = address_int + 26 ** no * num
				no = no + 1
		elif result_str == [] and result_num != []:
			address_type = "num"
			address_int = int(input_text)
		else:
			address_int = "error"
			address_type = "error"
		return [address_int, address_type, input_text]

	def check_price(self, input_price):
		"""
		백만원단위, 천만원단위, 억단위로 구분

		:param input_price:
		:return:
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.1f}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{:.0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.1f}'.format(input_price / 1000000)) + "백만원"
		return result

	def check_range_for_df(self, input_df):
		self.manual["clipboard_paste"] = {
			"분류1": "pandas, dataframe",
			"설명": "df에 들어가는 입력값을 확인하는 것",
			"입력요소": "input_df(dataframe)",
			"기타설명": "내부적으로 사용하는것"
		}
		temp = []
		for one in input_df:
			if ":" in one:
				pass
			elif "~" in one:
				one = one.replace("~", ":")
			elif "all" in one:
				one = one.replace("all", ":")
			else:
				changed_one = one.split(",")
				temp_1 = []
				for item in changed_one:
					temp_1.append(int(item))
				one = temp_1
			temp.append(one)
		return temp

	def check_same_list(self, list_mother, list_son):
		"""
		두개의 리스트를 비교해서 같은것을 찾는 것이다

		:param list_mother:
		:param list_son:
		:return:
		"""
		result = list_mother
		for one in range(len(list_son)):
			found = 0
			for two in range(len(list_mother)):
				if list_son[one][0] == list_mother[two][0]:
					found = 1
			if found == 0:
				result.append(list_son[one])
				print("새로운것 발견 ===>")
		return result

	def check_same_position(self, input_list_2d, list_1d):
		"""
		여러 엑셀의 자료에서 같은 부분을 찾기위해 만든 것이다
		같은 형태를 가진 엑셀화일들을 더하기 위해서는 같은 사이즈를 가져야 하는데, 어떤 경우들은
		사용하다가 틀려지는 부분들이 잇어서, 이것을 확인하기 위해서 만든 것이다

		들어온 자료중에서, 처음으로 list_1d와같은 위치를 돌려준다

		:param input_list_2d: 보통 used_range의 자료를 갖고 옮
		:param list_1d: 제일 처음의 몇개의 자료 ["","제목"]
		:return:
		"""
		result = ""
		repeat_no = len(input_list_2d[0]) - len(list_1d) + 1
		x = -1
		for list_1d in input_list_2d:
			x = x + 1
			y = -1
			for no in range(repeat_no):
				y = y + 1
				if list_1d[no:no + len(list_1d)] == list_1d:
					return [x, y]
		return result

	def check_similar_word(self, basic_list, input_value):
		"""
		앞에서부터 가장 많이 같은 글자가 있는 자료를 돌려준다

		:param basic_list:
		:param input_value:
		:return:
		"""
		result_no = 0
		result_value = ""
		# 공백이 없도록 만든다, 가끔 공백을 2개를 넣거나 하는경우가 있어서 넣은것이다
		checked_value = str(input_value).replace(" ", "")
		# 비교할것중에 작은것을 기준으로 한글짜식 비교하기 위해 길이를 계산한것
		a_len = len(input_value)

		# 폴더의 자료를 하나씩 돌려서 비교한다
		for one_word in basic_list:
			temp_no = 0
			# 공백이 없도록 만든다, 가끔 공백을 2개를 넣거나 하는경우가 있어서 넣은것이다
			checked_one_word = str(one_word).replace(" ", "")
			b_len = len(checked_one_word)
			min_len = min(a_len, b_len)

			# 길이만큼 하나씩 비교를 한다
			for index in range(min_len):
				# 만약 위치마다 한글짜식 비교해서 계속 같은것이 나오면 갯수를 더한다
				if checked_value[index] == checked_one_word[index]:
					temp_no = temp_no + 1
				else:
					# 만약 다른 글자가 나타나면, 제일 긴것인지를 확인한후, 다음 단어로 넘어가도록 한다
					if temp_no > result_no:
						result_no = temp_no
						result_value = one_word
					# print("앞에서부터 같은 갯수 ==> ", temp_no, checked_one_word)
					break
		return result_value

	def check_similar_word_in_basic_list(self, basic_list, input_value):
		"""
		앞에서부터 가장 많이 같은 글자가 있는 자료를 돌려준다

		:param basic_list:
		:param input_value:
		:return:
		"""
		result_no = 0
		result_value = ""
		# 공백이 없도록 만든다, 가끔 공백을 2개를 넣거나 하는경우가 있어서 넣은것이다
		checked_value = str(input_value).replace(" ", "")
		# 비교할것중에 작은것을 기준으로 한글짜식 비교하기 위해 길이를 계산한것
		a_len = len(input_value)

		# 폴더의 자료를 하나씩 돌려서 비교한다
		for one_word in basic_list:
			temp_no = 0
			# 공백이 없도록 만든다, 가끔 공백을 2개를 넣거나 하는경우가 있어서 넣은것이다
			checked_one_word = str(one_word).replace(" ", "")
			b_len = len(checked_one_word)
			min_len = min(a_len, b_len)

			# 길이만큼 하나씩 비교를 한다
			for index in range(min_len):
				# 만약 위치마다 한글짜식 비교해서 계속 같은것이 나오면 갯수를 더한다
				if checked_value[index] == checked_one_word[index]:
					temp_no = temp_no + 1
				else:
					# 만약 다른 글자가 나타나면, 제일 긴것인지를 확인한후, 다음 단어로 넘어가도록 한다
					if temp_no > result_no:
						result_no = temp_no
						result_value = one_word
					# print("앞에서부터 같은 갯수 ==> ", temp_no, checked_one_word)
					break
		return result_value

	def check_start_with_list(self, base_data, input_list):
		result = True
		for one in input_list:
			if base_data.startswith(one):
				result = False
				break
		return result

	def check_text_encoding_data(self, text, encoding_type):
		"""
		입력자료의 인코딩을 확인하는 것

		:param text:
		:param encoding_type:
		:return:
		"""
		byte_data = text.encode(encoding_type)
		hex_data_as_str = " ".os.path.join("{0}".format(hex(c)) for c in byte_data)
		int_data_as_str = " ".os.path.join("{0}".format(int(c)) for c in byte_data)

		print("\"" + text + "\" 전체 문자 길이: {0}".format(len(text)))
		print("\"" + text + "\" 전체 문자를 표현하는 데 사용한 바이트 수: {0} 바이트".format(len(byte_data)))
		print("\"" + text + "\" 16진수 값: {0}".format(hex_data_as_str))
		print("\"" + text + "\" 10진수 값: {0}".format(int_data_as_str))
		# 사용법 : text_encoding_data("Hello", "utf-8")
		return int_data_as_str

	def check_title(self, temp_title):
		"""
		화일의 제목으로 사용이 불가능한것을 제거한다
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
						["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return

	def check_title_name(self, temp_title):
		"""
		각 제목으로 들어가는 글자에 대해서 변경해야 하는것을 변경하는 것이다
		입력형태 :
		출력형태 :
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
						["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return temp_title

	def check_type_for_value(self, one_value):
		"""
		입력으로 들어온 자료를 확인하는 것
		"""
		result = None
		if type(one_value) == type("abc"):
			result = "str"
		elif type(one_value) == type(123):
			result = "int"
		elif type(one_value) == type(123.45):
			result = "real"
		elif type(one_value) == type(True) or type(one_value) == type(False):
			result = "boolen"
		elif type(one_value) == type([]):
			result = "list"
		elif type(one_value) == type(()):
			result = "tuple"
		else:
			result = one_value
		return result

	def check_unique_y_in_list_1d(self, data1, data2):
		"""
		고유한 컬럼만 골라낸다
		"""
		result = []
		columns = self.read_y_names(data1)
		update_data2 = self.change_waste_data(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def check_value_nos_in_dic(self, input_dic):
		"""
		dic안의 value들의 전체 갯수를 더래서 돌려주는 것이다

		:param input_dic:
		:return:
		"""
		result = 0
		for one in input_dic.keys():
			result = result + len(input_dic[one])
		return result

	def check_y_name(self, temp_title):
		"""
		각 제목으로 들어가는 글자에 대해서 변경해야 하는것을 변경하는 것이다
		입력형태 :
		출력형태 :
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
						["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return temp_title

	def combine_two_list_1d_as_list_2d_group_by_same_xy_data(self, input_list_1, input_list_2):
		"""
		두개의 리스트를 서로 묶어서, 새로운 리스트를 만드는 것
		[1,2,3], ["a","b","c"] ==> [[1, "a"],[2,"b"],[3,"c"]]

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result = []
		for x, y in zip(input_list_1, input_list_2):
			result.append(x + y)
		return result

	def combine_two_list_1d_as_list_2dn(self, input_list_2d_1, input_list_2d_2):
		"""
		선택한 영역이 2개를 서로 같은것을 기준으로 묶을려고하는것이다
		제일앞의 한줄이 같은것이다
		만약 묶을려고 할때 자료가 없을때는 그 기준자료만큼 빈자료를 넣어서 다음자료를 추가하는 것이다

		:param input_list_2d_1:
		:param input_list_2d_2:
		:return:
		"""
		no_of_list_2d_1 = len(input_list_2d_1[0]) - 1
		no_of_list_2d_2 = len(input_list_2d_2[0]) - 1
		empty_list_2d_1 = [""] * no_of_list_2d_1
		empty_list_2d_2 = [""] * no_of_list_2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list_2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list_2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list_2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list_2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def compare_list_two_value(self, raw_data, req_number, project_name, vendor_name, nal):
		"""
		위아래비교
		회사에서 사용하는 inq용 화일은 두줄로 구성이 된다
		한줄은 client가 요청한 스팩이며
		나머지 한줄은 vendor가 deviation사항으로 만든 스팩이다
		이두가지의 스팩을 하나로 만드는 것이다
		즉, 두줄에서 아래의 글씨가 있고 그것이 0, None가 아니면 위의것과 치환되는 것이다
		그런후 이위의 자료들만 따로 모아서 돌려주는 것이다

		:param raw_data:
		:param req_number:
		:param project_name:
		:param vendor_name:
		:param nal:
		:return:
		"""
		data = list(raw_data)
		data_set = []
		data_set_final = []
		for a in range(0, len(data), 2):
			for b in range(len(data[1])):
				if not (data[a + 1][b] == data[a][b]) and data[a + 1][b] != None and data[a + 1][b] != 0:
					data_set.append(data[a + 1][b])
				else:
					data_set.append(data[a][b])
			data_set.append(req_number)
			data_set.append(project_name)
			data_set.append(vendor_name)
			data_set.append(nal)
			data_set_final.append(data_set)
			data_set = 0
		return data_set_final

	def compare_two_value(self, raw_data, req_number, project_name, vendor_name, nal):
		"""
		위아래 비교
		회사에서 사용하는 inq용 화일은 두줄로 구성이 된다
		한줄은 client가 요청한 스팩이며
		나머지 한줄은 vendor가 deviation사항으로 만든 스팩이다
		이두가지의 스팩을 하나로 만드는 것이다
		즉, 두줄에서 아래의 글씨가 있고 그것이 0, None가 아니면 위의것과 치환되는 것이다
		그런후 이위의 자료들만 따로 모아서 돌려주는 것이다

		:param raw_data:
		:param req_number:
		:param project_name:
		:param vendor_name:
		:param nal:
		:return:
		"""
		self.data = list(raw_data)
		self.data_set = []
		self.data_set_final = []

		for num_1 in range(0, len(self.data), 2):
			for num_2 in range(len(self.data[1])):
				if not (self.data[num_1 + 1][num_2] == self.data[num_1][num_2]) and self.data[num_1 + 1][num_2] != None and \
						self.data[num_1 + 1][num_2] != 0:
					self.data_set.append(self.data[num_1 + 1][num_2])
				else:
					self.data_set.append(self.data[num_1][num_2])
			self.data_set.append(req_number)
			self.data_set.append(project_name)
			self.data_set.append(vendor_name)
			self.data_set.append(nal)
			self.data_set_final.append(self.data_set)
			self.data_set = []
		return self.data_set_final

	def compare_two_value_in_list(self, raw_data, req_number, project_name, vendor_name, nal):
		"""
		위아래 비교
		회사에서 사용하는 inq용 화일은 두줄로 구성이 된다
		한줄은 client가 요청한 스팩이며
		나머지 한줄은 vendor가 deviation사항으로 만든 스팩이다
		이두가지의 스팩을 하나로 만드는 것이다
		즉, 두줄에서 아래의 글씨가 있고 그것이 0, None가 아니면 위의것과 치환되는 것이다
		그런후 이위의 자료들만 따로 모아서 돌려주는 것이다
		"""
		self.data = list(raw_data)
		self.data_set = []
		self.data_set_final = []

		for self.a in range(0, len(self.data), 2):
			for self.b in range(len(self.data[1])):
				if not (self.data[self.a + 1][self.b] == self.data[self.a][self.b]) and self.data[self.a + 1][
					self.b] != None and self.data[self.a + 1][self.b] != 0:
					self.data_set.append(self.data[self.a + 1][self.b])
				else:
					self.data_set.append(self.data[self.a][self.b])
			self.data_set.append(req_number)
			self.data_set.append(project_name)
			self.data_set.append(vendor_name)
			self.data_set.append(nal)
			self.data_set_final.append(self.data_set)
			self.data_set = []
		return self.data_set_final

	def concate_jfinder_result(self, input_list_2d, chain_word=": "):
		"""
		jfinder에서 찾은 여러개의 자료를 하나의 텍스트로 만들어서 연결하는것
		jfinder에서 찾은 여러개의 자료 : [[찾은글자, 찾은 시작 위치, 끝위치 번호, [그룹1, 그룹2], ....]

		2차원자료로 오는것을 연결되는 문자로 연결해 주는것

		:param input_list_2d:
		:param chain_word:
		:return:
		"""
		result = ""
		if input_list_2d:  # 1
			for list_1d in input_list_2d:
				result = result + list_1d[0] + chain_word
			result = result[:-1 * len(chain_word)]
		return result

	def connect_mqtt(self, client, userdata, flags, rc):
		"""
		connect_mqtt
		"""
		if rc == 0:
			print("connected OK")
		else:
			print("Bad connection Returned code=", rc)

	def convert_data(self, original_data):
		"""
		영문과 숫자와 공백을 제거하고는 다 제거를 하는것
		입력형태 :
		출력형태 :
		"""
		result = []
		for one_data in original_data:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def convert_data_except_number_n_eng(self, original_data):
		"""
		영문과 숫자와 공백을 제거하고는 다 제거를 하는것
		입력형태 :
		출력형태 :
		"""
		result = []
		for one_data in original_data:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def copy_file(self, old_path, new_path, meta=""):
		"""
		화일복사
		"""
		old_path = self.check_file(old_path)
		new_path = self.check_file(new_path)
		if meta == "":
			shutil.copy(old_path, new_path)
		else:
			shutil.copy2(old_path, new_path)

	def copy_file_with_meta(self, old_path, new_path):
		"""
		화일복사
		"""
		old_path = self.check_file(old_path)
		new_path = self.check_file(new_path)
		shutil.copy2(old_path, new_path)

	def copy_folder(self, old_path, new_path):
		"""
		폴더복사
		"""
		shutil.copy(old_path, new_path)

	def copy_to_clipboard(self, input_text):
		"""
		"""
		self.manual["clipboard_copy"] = {
			"분류1": "복사",
			"설명": "클립보드에 텍스트를 복사",
			"입력요소": "input_text(텍스트)",
			"기타설명": ""
		}
		pyperclip.copy(input_text)

	def delete_step(self, num, data):  # 원하는 순서째의 자료를 삭제하기
		data.insert(0, [])
		for a in range(len(data)):
			if (a % num) == 0:
				data[a] = []
		result = data[1:]
		return result

	def count_element_no_for_list(self, input_list_2d):
		"""
		1차원이나 2차원의 리스트가 들어오면,
		값들이 몇번 나왔는지를 계산하는것

		:param input_list_2d:
		:return:
		"""

		result = {}
		if type(input_list_2d[0]) != type([]) and type(input_list_2d[0]) != type(()):
			input_list_2d = [input_list_2d]
		for x in range(len(input_list_2d)):
			for y in range(len(input_list_2d[x])):
				one_value = input_list_2d[x][y]
				if one_value == "" or one_value == None:
					pass
				else:
					if one_value in list(result.keys()):
						result[one_value] = result[one_value] + 1
					else:
						result[one_value] = 1
		return result

	def count_function_number_in_python_file(self, python_file_list):
		"""
		원하는 python화일안에 몇개의 def로 정의된 메소드가 있는지 확인하는 것이다

		:param python_file_list:
		:return:
		"""
		result = []
		num = 0
		for one in python_file_list:
			aaa = self.change_python_file_to_sorted_by_def(one)
			num = num + len(aaa)
			result.append([one, len(aaa)])
		result.append(["총갯수는 ===>", num])
		return result

	def del_step(self, num, data):  # 원하는 순서째의 자료를 삭제하기
		data.insert(0, [])
		for a in range(len(data)):
			if (a % num) == 0:
				data[a] = []
		result = data[1:]
		return result

	def count_list_samevalue_by_ordered(self, input_list):
		"""
		리스트안의 자료들을 반복횟수가 놓은것으로만 확인
		"""
		result_dic = {}
		# 리스트안의 자료가 몇번나오는지 갯수를 센후에
		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in input_list:
			if one in result_dic.keys():
				result_dic[one] = result_dic[one] + 1
			else:
				result_dic[one] = 1

		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in list(result_dic.keys()):
			if result_dic[one] == 1:
				del result_dic[one]

		# 사전자료를 2차원리스트로 만든것
		new_list = []
		for key, val in result_dic.items():
			new_list.append([key, val])

		# 사전자료를 2차원리스트로 만든것을 역순으로 정렬한것
		new_list = sorted(new_list, key=lambda x: x[1], reverse=True)
		return new_list

	def count_list_samevalue_byordered(self, input_list):
		"""
		리스트안의 자료들을 반복횟수가 놓은것으로만 확인
		"""
		result_dic = {}
		# 리스트안의 자료가 몇번나오는지 갯수를 센후에
		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in input_list:
			if one in result_dic.keys():
				result_dic[one] = result_dic[one] + 1
			else:
				result_dic[one] = 1

		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in list(result_dic.keys()):
			if result_dic[one] == 1:
				del result_dic[one]

		# 사전자료를 2차원리스트로 만든것
		new_list = []
		for key, val in result_dic.items():
			new_list.append([key, val])

		# 사전자료를 2차원리스트로 만든것을 역순으로 정렬한것
		new_list = sorted(new_list, key=lambda x: x[1], reverse=True)
		return new_list

	def count_method_no_in_python_file(self, python_file_list, path=""):
		"""
		원하는 python화일안에 몇개의 def로 정의된 메소드가 있는지 확인하는 것이다

		:param python_file_list:
		:param path:
		:return:
		"""
		result = []
		num = 0
		for one in python_file_list:
			aaa = self.change_python_file_to_text_file_sorted_by_def(path + one)
			num = num + len(aaa)
			result.append([one, len(aaa)])
		result.append(["총갯수는 ===>", num])
		return result

	def count_no_of_elements(self, input_2dlist):
		"""
		1차원이나 2차원의 리스트가 들어오면,
		값들이 몇번 나왔는지를 계산하는것

		:param input_2dlist:
		:return:
		"""

		result = {}
		if type(input_2dlist[0]) != type([]) and type(input_2dlist[0]) != type(()):
			input_2dlist = [input_2dlist]
		for x in range(len(input_2dlist)):
			for y in range(len(input_2dlist[x])):
				one_value = input_2dlist[x][y]
				if one_value == "" or one_value == None:
					pass
				else:
					if one_value in list(result.keys()):
						result[one_value] = result[one_value] + 1
					else:
						result[one_value] = 1
		return result

	def count_same_data_for_data_as_dic_style(self, input_text):
		"""
		입력한 자료를 1차원자료로 간주하고, 값은 사전의 키로 만들어서 같은것이 잇으면 숫자를 증가시켜서 값을 만든다
		["1","2","2","3","4","4","4"] => {"1":1, "2":2, "3":1, "4":3}

		:param input_text:
		"""
		input_text = input_text.replace(" ", "")
		input_text = input_text.upper()
		result = {}
		for one_letter in input_text:
			if one_letter in list(result.keys()):
				result[one_letter] = result[one_letter] + 1
			else:
				result[one_letter] = 1
		return result

	def count_same_value_for_ordered_list(self, input_list):
		"""
		2개이상 반복되는것중 높은 갯수 기준으로 돌려주는것

		:param input_list:
		:return:
		"""
		result_dic = {}
		# 리스트안의 자료가 몇번나오는지 갯수를 센후에
		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in input_list:
			if one in result_dic.keys():
				result_dic[one] = result_dic[one] + 1
			else:
				result_dic[one] = 1

		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in list(result_dic.keys()):
			if result_dic[one] == 1:
				del result_dic[one]

		# 사전자료를 2차원리스트로 만든것
		new_list = []
		for key, val in result_dic.items():
			new_list.append([key, val])

		# 사전자료를 2차원리스트로 만든것을 역순으로 정렬한것
		new_list = sorted(new_list, key=lambda x: x[1], reverse=True)
		return new_list

	def count_value_nos_in_dic(self, input_dic):
		"""
		dic안의 value들의 전체 갯수를 더래서 돌려주는 것이다

		:param input_dic:
		:return:
		"""
		result = 0
		for one in input_dic.keys():
			result = result + len(input_dic[one])
		return result

	def cut_number_for_float_data_by_no_of_under_point(self, no_of_under_point=3):
		"""
		선택영역안의 모든 숫자중에서, 입력받은 소숫점아래 몇번째부터, 값을 아예 삭제하는것

		:param no_of_under_point:
		:return:
		"""
		times = 10 ** no_of_under_point
		x1, y1, x2, y2 = self.get_address_for_selection()
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = self.get_value_in_cell("", [x, y])
				try:
					one_value = math.floor(float(one_value) * times) / times
					self.write_value_in_cell("", [x, y], one_value)
				except:
					pass

	def data_jaum_xy_list(self, size=[1, 2], input_data="ㄱ"):
		"""
		자음의 xy값을 갖고온다

		:param size:
		:param input_data:
		:return:
		"""
		x, y = size
		# x, y는 글자의 크기
		ja_01 = [["ㄱ"], [1, 1, 1, y], [1, y, x, y]]
		ja_02 = [["ㄴ"], [1, 1, x, 1], [x, 1, x, y]]
		ja_03 = [["ㄷ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y]]
		ja_04 = [["ㄹ"], [1, 1, 1, y], [1, y, 0.5 * x, y], [0.5 * x, y, 0.5 * x, 1], [0.5 * x, 1, x, 1], [x, 1, x, y]]
		ja_05 = [["ㅁ"], [1, 1, 1, y], [1, y, x, y], [x, y, x, 1], [x, 1, 1, 1]]
		ja_06 = [["ㅂ"], [1, 1, x, 1], [x, 1, x, y], [x, y, 1, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_07 = [["ㅅ"], [1, 0.5 * y, 0.3 * x, 0.5 * y], [0.3 * x, 0.5 * y, x, 1], [0.3 * x, 0.5 * y, x, y]]
		ja_08 = [["ㅇ"], [0.8 * x, 0.2 * y, 0.8 * x, 0.8 * y], [0.8 * x, 0.8 * y, 0.6 * x, y, ""],
				 [0.6 * x, y, 0.2 * x, y], [0.2 * x, y, 1, 0.8 * y, "/"], [1, 0.8 * y, 1, 0.2 * y],
				 [1, 0.2 * y, 0.2 * x, 1, ""], [0.2 * x, 1, 0.6 * x, 1], [0.6 * x, 1, 0.8 * x, 0.2 * y, "/"]]
		ja_09 = [["ㅈ"], [1, 1, 1, y], [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1, "/"],
				 [0.5 * x, 0.5 * y, x, y, ""]]
		ja_10 = [["ㅊ"], [0.2 * x, 0.5 * y, 1, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.2 * x, 0.5 * y, 0.4 * x, 0.5 * y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1], [0.5 * x, 0.5 * y, x, y, ""]]
		ja_11 = [["ㅋ"], [1, 1, 1, y], [1, y, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_12 = [["ㅌ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_13 = [["ㅍ"], [1, 1, 1, y], [x, 1, x, y], [1, 0.2 * y, x, 0.2 * y], [1, 0.8 * y, x, 0.8 * y]]
		ja_14 = [["ㅎ"], [1, 0.5 * y, 0.2 * x, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.4 * x, 0.3 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, 0.6 * x, y], [0.6 * x, y, 0.8 * x, y], [0.8 * x, y, x, 0.8 * y],
				 [x, 0.8 * y, x, 0.3 * y], [x, 0.3 * y, 0.8 * x, 1], [0.8 * x, 1, 0.6 * x, 1],
				 [0.6 * x, 1, 0.4 * x, 0.3 * y]]
		ja_31 = [["ㄲ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_32 = [["ㄸ"], [1, 1, 1, 0.4 * y], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], ]
		ja_33 = [["ㅃ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_34 = [["ㅆ"], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1], [0.4 * x, 0.3 * y, x, 0.5 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_35 = [["ㅉ"], [1, 1, 1, 0.5 * y], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1],
				 [0.4 * x, 0.3 * y, x, 0.5 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_36 = [["ㄳ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_37 = [["ㄵ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_38 = [["ㄶ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y],
				 [0.2 * x, 0.6 * y, 0.2 * x, y], [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y],
				 [0.6 * x, y, x, 0.9 * y], [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y],
				 [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y], [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_39 = [["ㄺ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_40 = [["ㄻ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], [x, y, x, 0.7 * y],
				 [x, 0.7 * y, 1, 0.7 * y], ]
		ja_41 = [["ㄼ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y],
				 [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_42 = [["ㄽ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y],
				 [0.4 * x, 0.8 * y, x, y], ]
		ja_43 = [["ㄾ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, 0.7 * y, x, 0.7 * y],
				 [x, 0.7 * y, x, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_44 = [["ㄿ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [x, 0.6 * y, x, y],
				 [1, 0.7 * y, x, 0.7 * y], [1, 0.9 * y, x, 0.9 * y], ]
		ja_45 = [["ㅀ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y], [0.2 * x, 0.6 * y, 0.2 * x, y],
				 [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y], [0.6 * x, y, x, 0.9 * y],
				 [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y], [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y],
				 [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_46 = [["ㅄ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]

		jamo1_dic = {"ㄱ": ja_01, "ㄴ": ja_02, "ㄷ": ja_03, "ㄹ": ja_04, "ㅁ": ja_05,
					 "ㅂ": ja_06, "ㅅ": ja_07, "ㅇ": ja_08, "ㅈ": ja_09, "ㅊ": ja_10,
					 "ㅋ": ja_11, "ㅌ": ja_12, "ㅍ": ja_13, "ㅎ": ja_14,
					 "ㄲ": ja_31, "ㄸ": ja_32, "ㅃ": ja_33, "ㅆ": ja_34, "ㅉ": ja_35,
					 "ㄳ": ja_36, "ㄵ": ja_37, "ㄶ": ja_38, "ㄺ": ja_39, "ㄻ": ja_40,
					 "ㄼ": ja_41, "ㄽ": ja_42, "ㄾ": ja_43, "ㄿ": ja_44, "ㅀ": ja_45, "ㅄ": ja_46,
					 }

		result = jamo1_dic[input_data]
		return result

	def data_make_name_list(self, input_no=5):
		"""
		입력한 갯수만큼 이름의 갯수를 만들어 주는것

		:param input_no:
		:return:
		"""
		sung = "김이박최정강조윤장"
		name = "가나다라마바사아자차카"
		last = "진원일이삼사오구원송국한"
		if input_no > len(sung) * len(name) * len(last) / 2:
			result = []
			pass
		else:
			total_name = set()
			num = 0
			while True:
				one_sung = random.choice(sung)
				one_name = random.choice(name)
				one_last = random.choice(last)
				new_name = one_sung + one_name + one_last
				total_name.add(new_name)
				num = num + 1
				if len(total_name) == input_no:
					# print(input_no, num)
					break
			result = list(total_name)
		return result

	def data_make_sample_name(self, input_no=5):
		"""
		입력한 갯수만큼 이름의 갯수를 만들어 주는것

		:param input_no:
		:return:
		"""
		sung = "김이박최정강조윤장"
		name = "가나다라마바사아자차카"
		last = "진원일이삼사오구원송국한"
		if input_no > len(sung) * len(name) * len(last) / 2:
			result = []
			pass
		else:
			total_name = set()
			num = 0
			while True:
				one_sung = random.choice(sung)
				one_name = random.choice(name)
				one_last = random.choice(last)
				new_name = one_sung + one_name + one_last
				total_name.add(new_name)
				num = num + 1
				if len(total_name) == input_no:
					print(input_no, num)
					break
			result = list(total_name)
		return result

	def data_moum_xy_list(self, size=[1, 2], input_data="ㅏ"):
		"""
		모음을 엑셀에 나타내기 위한 좌표를 주는 것이다
		x, y는 글자의 크기

		:param size:
		:param input_data:
		:return:
		"""
		x, y = size
		mo_01 = [["ㅏ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_02 = [["ㅑ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y],
				 [0.6 * x, 0.6 * y, 0.6 * x, 0.8 * y]]
		mo_03 = [["ㅓ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_04 = [["ㅕ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]
		mo_10 = [["ㅣ"], [1, 0.6 * y, x, 0.6 * y]]
		mo_05 = [["ㅗ"], [x, 1, x, y],
				 [x, 0.5 * y, 0.8 * x, 0.5 * y]]
		mo_06 = [["ㅛ"], [x, 1, x, y],
				 [x, 0.3 * y, 0.8 * x, 0.3 * y],
				 [x, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_07 = [["ㅜ"], [1, 1, 1, y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y]]
		mo_08 = [["ㅠ"], [1, 1, 1, y],
				 [1, 0.3 * y, 0.8 * x, 0.3 * y],
				 [1, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_09 = [["ㅡ"], [0.5 * x, 1, 0.5 * x, y]]

		mo_21 = [["ㅐ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_22 = [["ㅒ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.8 * y, 0.6 * x, 0.8 * y]]
		mo_23 = [["ㅔ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_24 = [["ㅖ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]

		jamo2_dic = {
			"ㅏ": mo_01, "ㅑ": mo_02, "ㅓ": mo_03, "ㅕ": mo_04, "ㅗ": mo_05,
			"ㅛ": mo_06, "ㅜ": mo_07, "ㅠ": mo_08, "ㅡ": mo_09, "ㅣ": mo_10,
			"ㅐ": mo_21, "ㅒ": mo_22, "ㅔ": mo_23, "ㅖ": mo_24,
		}
		result = jamo2_dic[input_data]
		return result

	def data_nth_name_list(self, input_no=5):
		"""
		입력한 갯수만큼 이름의 갯수를 만들어 주는것

		:param input_no:
		:return:
		"""
		sung = "김이박최정강조윤장"
		name = "가나다라마바사아자차카"
		last = "진원일이삼사오구원송국한"
		if input_no > len(sung) * len(name) * len(last) / 2:
			result = []
			pass
		else:
			total_name = set()
			num = 0
			while True:
				one_sung = random.choice(sung)
				one_name = random.choice(name)
				one_last = random.choice(last)
				new_name = one_sung + one_name + one_last
				total_name.add(new_name)
				num = num + 1
				if len(total_name) == input_no:
					# print(input_no, num)
					break
			result = list(total_name)
		return result

	def data_random_list(self, input_list, input_limit, input_times=1):
		"""
		입력된 자료를 랜덤으로 리스트를 만드는 것

		:param input_list:
		:param input_limit:
		:param input_times:
		:return:
		"""
		result_set = []
		# if len(input_list) == 2:
		#	input_list = list(range(input_list[0], input_list[1]))
		for no in range(input_times):
			result = []
			for num in range(input_limit):
				dd = random.choice(input_list)
				result.append(dd)
				input_list.remove(dd)
			result_set.append(result)
		return result_set

	def data_serial_no(self, start_no=1, style="####"):
		"""
		1000으로 시작되는 연속된 번호를 만드는 것이다

		:param start_no:
		:param style:
		:return:
		"""
		length = len(style)
		value = 10 ** (length - 1) + start_no
		return value

	def data_several_unit_number(self, input_price):
		"""
		백만원단위, 전만원단위, 억단위로 구분

		:param input_price:
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result

	def delete_2nd_empty_lines(self, file_name):
		"""
		화일을 읽어 내려가다가 2줄이상의 띄어쓰기가 된것을 하나만 남기는것

		:param file_name:
		:return:
		"""
		f = open(file_name, 'r', encoding='UTF8')
		lines = f.readlines()
		num = 0
		result = ""
		for one_line in lines:
			if one_line == "\n":
				num = num + 1
				if num == 1:
					result = result + str(one_line)
				elif num > 1:
					# print("2줄발견")
					pass
			else:
				num = 0
				result = result + str(one_line)
		print(result)
		return result

	def delete_all_char_except_number_eng_for_value(self, input_value):
		"""
		숫자와 영어만 남기는것, 나머지것은 다 삭제하는것
		result = []

		:param input_value:
		:return:
		"""
		result = []
		for one_data in input_value:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def delete_all_explanation_for_python_file(self, input_text):
		"""
		넘어온 python화일 에서 주석으로 사용되는 것들을 지우는것

		:param input_text:
		:return:
		"""
		input_text = re.sub(re.compile(r"[\s]*#.*[\n]"), "\n", input_text)
		input_text = re.sub(re.compile(r"[\s]*''',*?'''", re.DOTALL | re.MULTILINE), "", input_text)
		input_text = re.sub(re.compile(r'[\s]*""".*?"""', re.DOTALL | re.MULTILINE), "", input_text)
		input_text = re.sub(re.compile(r"[\n][\s]*?[\n]"), "\n", input_text)
		return input_text

	def delete_continious_same_data_for_list_1d(self, input_list):
		"""
		연속된 같은 자료만 지우는 것

		:param input_list:
		:return:
		"""
		result = []
		for no in range(len(input_list) - 1):
			if input_list[no] == input_list[no + 1]:
				pass
			else:
				result.append(input_list[no])
		return result

	def delete_each_value_in_list_2d_by_index_list(self, input_list_2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		2차원자료의 각 1차원자료의 index번호에 따라서 값을 없애는것

		[2,5,7]라인을 없래라는 뜻이라면,
		[[1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8],] => [[1,2,4,5,7], [1,2,4,5,7]]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_each_value_of_list_1d_in_list_2d_by_index_list(self, input_list_2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		2차원자료의 각 1차원자료의 index번호에 따라서 값을 없애는것

		[2,5,7]라인을 없래라는 뜻이라면,
		[[1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8],] => [[1,2,4,5,7], [1,2,4,5,7]]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_empty_folder(self, old_dir):
		# 폴더삭제
		# 폴더안에 자료가 없어야 삭제
		os.rmdir(old_dir)

	def delete_empty_line_in_list_2d(self, input_list_2d):
		"""
		가로나 세로열을 기준으로 값이 없는것을 삭제하기
		입력으로 들어온 2차원의 자료중에서, 가로행이 완전히 빈것을 삭제하는 기능

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		base_no = len(input_list_2d[0])
		result = []
		for list_1d in input_list_2d:
			check_no = 0
			for value in list_1d:
				if value in [[], (), "", None]:
					check_no = check_no + 1
			if check_no != base_no:
				result.append(list_1d)
		return result

	def delete_empty_line_over2_in_file(self, file_name):
		"""
		화일을 읽어 내려가다가 2줄이상의 띄어쓰기가 된것을 하나만 남기는것
		텍스트로 저장된것을 사용하다가 필요해서 만듦
		"""
		f = open(file_name, 'r', encoding='UTF8')
		lines = f.readlines()
		num = 0
		result = ""
		for one_line in lines:
			if one_line == "\n":
				num = num + 1
				if num == 1:
					result = result + str(one_line)
				elif num > 1:
					# print("2줄발견")
					pass
			else:
				num = 0
				result = result + str(one_line)
		return result

	def delete_empty_lines(self, input_list_2d):
		"""
		2차원자료에서 전체가 빈 가로줄과 세로줄의 자료를 삭제하는 것
		"""
		temp_result = []
		for list_1d in input_list_2d:
			for value in list_1d:
				if value:
					temp_result.append(list_1d)
					break
		r_temp_result = self.change_xylist_to_yxlist(temp_result)
		temp_result_2 = []
		for list_1d in r_temp_result:
			for value in list_1d:
				if value:
					temp_result_2.append(list_1d)
					break
		result = self.change_xylist_to_yxlist(temp_result_2)
		return result

	def delete_empty_value_in_list_1d(self, input_list, condition=["", None, [], ()]):
		"""
		넘어온 리스트 형태의 자료중 조건에 맞는것이 있으면 제거하는 것
		입력형태 : ["aaa", "", None, "", "bbb"], [["aaa", "", None, "", "bbb"],"werw", 31231, [], ["aaa", "", None, "", "bbb"]]
		출력형태 : ["aaa", "bbb"], [['aaa', 'bbb'], 'werw', 31231, [], ['aaa', 'bbb']]

		:param input_list:
		:param condition:
		:return:
		"""
		for x in range(len(input_list) - 1, -1, -1):
			if input_list[x] in condition:
				del (input_list[x])
			else:
				if type(input_list[x]) == type([]):
					for y in range(len(input_list[x]) - 1, -1, -1):
						if input_list[x][y] in condition:
							del (input_list[x][y])
				else:
					if input_list[x] in condition:
						del (input_list[x])
		return input_list

	def delete_empty_xline(self, input_list_2d):
		"""
		가로나 세로열을 기준으로 값이 없는것을 삭제하기
		입력으로 들어온 2차원의 자료중에서, 가로행이 완전히 빈것을 삭제하는 기능

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		base_no = len(input_list_2d[0])
		result = []
		for list_1d in input_list_2d:
			check_no = 0
			for value in list_1d:
				if value:
					break
				else:
					check_no = base_no + 1
			if check_no != base_no:
				result.append(list_1d)
		return result

	def delete_empty_xline_and_yline(self, input_list_2d):
		"""
		2차원자료에서 전체가 빈 가로줄과 세로줄의 자료를 삭제하는 것
		"""
		temp_result = []
		for list_1d in input_list_2d:
			for value in list_1d:
				if value:
					temp_result.append(list_1d)
					break
		r_temp_result = self.change_xylist_to_yxlist(temp_result)
		temp_result_2 = []
		for list_1d in r_temp_result:
			for value in list_1d:
				if value:
					temp_result_2.append(list_1d)
					break
		result = self.change_xylist_to_yxlist(temp_result_2)
		return result

	def delete_empty_yline(self, input_list_2d):
		"""
		입력으로 들어온 2차원의 자료중에서, 세로행이 처음부터 끝까지 빈Y열을 삭제하는 기능

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		changed_list_2d = self.change_xylist_to_yxlist(input_list_2d)
		temp = self.delete_empty_line_in_list_2d(changed_list_2d)
		result = self.change_xylist_to_yxlist(temp)
		return result

	def delete_even_value_in_list_1d(self, data):
		"""
		홀수의 자료만 삭제

		:param data:
		:return:
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 1:
				result.append(data[no])
		return result

	def delete_file(self, old_path):
		"""
		화일삭제
		"""
		old_path = self.check_file(old_path)
		os.remove(old_path)

	def delete_folder(self, old_dir, empty="no"):
		"""
		폴더삭제
		폴더안에 자료가 있어도 삭제
		"""
		if empty == "no":
			shutil.rmtree(old_dir)
		else:
			os.rmdir(old_dir)

	def delete_line_in_list_2d_by_index(self, input_list_2d, no_list):
		"""
		2차원자료를 기준으로 index번호를 기준으로 삭제하는것
		입력형태 : 2차원리스트, [2,5,7]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_list_1d_by_even_no(self, data):
		"""
		홀수의 자료만 삭제

		:param data:
		:return:
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 1:
				result.append(data[no])
		return result

	def delete_list_1d_by_odd_no(self, data):
		"""
		짝수의 자료만 삭제

		:param data:
		:return:
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 0:
				result.append(data[no])
		return result

	def delete_list_1d_by_step(self, input_list, step, start=0):
		"""
		원하는 순서째의 자료를 ""으로 만드는것
		"""
		flag_no = 0
		for num in range(start, len(input_list)):
			flag_no = flag_no + 1
			if flag_no == step:
				input_list[num] = ""
				flag_no = 0
		return input_list

	def delete_list_1d_in_list_2d_by_index(self, input_list_2d, no_list):
		"""
		2차원자료를 기준으로 index번호를 기준으로 삭제하는것
		입력형태 : 2차원리스트, [2,5,7]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_list_1d_in_list_2d_by_step(self, input_list, step, start=0):
		"""
		원하는 순서째의 자료를 ""으로 만드는것
		"""
		flag_no = 0
		for num in range(start, len(input_list)):
			flag_no = flag_no + 1
			if flag_no == step:
				input_list[num] = ""
				flag_no = 0
		return input_list

	def delete_list_2d_by_index(self, input_list_2d, no_list):
		"""
		2차원 자료에서
		원하는 순서들의 자료를 삭제하는 것
		입력형태 : 2차원리스트, [2,5,7]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_list_empty_value(self, input_list, condition=["", None, [], ()]):
		"""
		넘어온 리스트 형태의 자료중 조건에 맞는것이 있으면 제거하는 것
		입력형태 : ["aaa", "", None, "", "bbb"], [["aaa", "", None, "", "bbb"],"werw", 31231, [], ["aaa", "", None, "", "bbb"]]
		출력형태 : ["aaa", "bbb"], [['aaa', 'bbb'], 'werw', 31231, [], ['aaa', 'bbb']]
		"""
		# print(condition)
		for x in range(len(input_list) - 1, -1, -1):
			if input_list[x] in condition:
				del (input_list[x])
			else:
				if type(input_list[x]) == type([]):
					for y in range(len(input_list[x]) - 1, -1, -1):
						if input_list[x][y] in condition:
							del (input_list[x][y])
				else:
					if input_list[x] in condition:
						del (input_list[x])
		return input_list

	def delete_no_meaning_words_for_list_1d(self, input_list, change_word_dic):
		"""
		의미없는 단어를 삭제하는것
		:param input_list:
		:param change_word_dic:
		:return:
		"""
		sql_1 = "[시작][숫자&특수문자:1~][끝]"  # 숫자만있는것을 삭제
		sql_2 = "[시작][숫자:1:5][영어&한글:1:1][끝]"  # 1223개 와 같은것 삭제
		sql_3 = "[시작][한글:1~][끝]"  #
		sql_4 = "[\(][문자:1~][\)]"  # 괄호안의 글자삭제

		result = []
		for one in input_list:
			one = str(one).strip()
			if self.jf.match(sql_3, one):
				if one in list(change_word_dic.keys()):
					print("발견 ==> 바꿀문자", one)
					one = change_word_dic[one]

			if self.jf.match(sql_4, one):
				print("발견 ==> (문자)  : ", one)
				one = self.jf.delete_with_jf_sql(sql_4, one)
				print("------------->", one)

			if len(one) <= 1:
				one = ""
			elif self.jf.match(sql_1, one):
				print("발견 ==> 숫자만", one)
				one = ""
			elif self.jf.match(sql_2, one):
				print("발견 ==> 숫자+1글자", one)
				one = ""

			if one != "":
				result.append(one)

			result_unique = list(set(result))
		return result_unique

	def delete_same_cell(self, input_datas):
		if len(input_datas) == 0:
			print("아무자료도 없읍니다. 확인 바랍니다")
			pass
		else:
			a = 0
			while a != len(input_datas) - 1:
				if input_datas[a] == input_datas[a + 1]: input_datas[a] = []
				a = a + 1
		return input_datas

	def delete_same_list_1d_in_list_2d_check_by_index(self, input_list_2d, base_index):
		"""
		2차원의 자료를 기준으로 각 1차원자료의 n번째 값이 같으면 제외하고 고유한것만 돌려주는 것이다

		2차원자료중에서 몇번째의 자료가 같은 것만 삭제하는것

		:param input_list_2d: 2차원 형태의 리스트
		:param base_index:
		:return:
		"""
		waste_letters = [" ", ',', '.', '"', "'", ',', '?', '-']
		result = []
		only_one = set()
		for one_list in input_list_2d:
			new_value = str(one_list[base_index])
			for one in waste_letters:
				new_value = new_value.replace(one, "")

			if new_value in only_one:
				print("같은것 찾음")
			else:
				result.append(one_list)
				only_one.add(new_value)
		return result

	def delete_same_of_mine(self, input_list):
		"""
		리스트로 받은 자료에서 순서는 지키면서 같은것을 삭제하는 것이다
		하나씩 돌리면서 나머지 자료에서

		:param input_list:
		:return:
		"""
		result = input_list
		total_no = len(input_list)
		print(total_no)
		for num_1 in range(total_no):
			base_data = input_list[num_1]
			print(base_data, total_no - num_1)
			if base_data != "":
				# 빈것은 그냥 넘어가도록 한다
				for num_2 in range(num_1 + 1, total_no):
					if base_data == input_list[num_2]:
						result[num_2] = ""
		return result

	def delete_same_value_in_list_1d(self, input_datas, status=0):
		"""
		입력자료에서 같은것만 삭제

		:param input_datas:
		:param status:
		:return:
		"""
		if status == 0:
			result = []
			# 계속해서 pop으로 하나씩 없애므로 하나도 없으면 그만 실행한다
			while len(input_datas) != 0:
				gijun = input_datas.pop()
				sjpark = 0
				result.append(gijun)
				for number in range(len(input_datas)):
					if input_datas[int(number)] == []:  # 빈자료일때는 그냥 통과한다
						pass
					if input_datas[int(number)] == gijun:  # 자료가 같은것이 있으면 []으로 변경한다
						sjpark = sjpark + 1
						input_datas[int(number)] = []
			else:
				# 중복된것중에서 아무것도없는 []마저 없애는 것이다. 위의 only_one을 이용하여 사용한다
				# 같은것중에서 하나만 남기고 나머지는 []으로 고친다
				# 이것은 연속된 자료만 기준으로 삭제를 하는 것입니다
				# 만약 연속이 되지않은 같은자료는 삭제가 되지를 않읍니다
				result = list(set(input_datas))
				for a in range(len(result) - 1, 0, -1):
					if result[a] == []:
						del result[int(a)]
		return result

	def delete_same_value_in_list_2d_by_index(self, input_list_2d, base_index):
		"""
		2차원자료중에서 몇번째의 자료가 같은 것만 삭제하는것

		:param input_list_2d: 2차원 형태의 리스트
		:param base_index:
		:return:
		"""
		waste_letters = [" ", ',', '.', '"', "'", ',', '?', '-']
		result = []
		only_one = set()
		for one_list in input_list_2d:
			new_value = str(one_list[base_index])
			for one in waste_letters:
				new_value = new_value.replace(one, "")

			if new_value in only_one:
				print("같은것 찾음")
			else:
				result.append(one_list)
				only_one.add(new_value)
		return result

	def delete_set_item_as_same_list_data(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다

		:param input_set:
		:param input_list:
		:return:
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set

	def delete_set_item_by_list(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set

	def delete_set_item_same_with_list(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set

	def delete_space(self):
		"""
		자료의 앞뒤에있는 스페이스를제거하는 함수

		:return:
		"""
		a = 111
		return a

	def delete_special_letter_for_text(self, input_text):
		"""
		특수문자를 제거하는것
		"""
		for one in input_text:
			if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
				temp = temp + str(one)
		result = temp
		return result

	def delete_special_letter_in_list(self, original_data):
		"""
		특수문자를 제거하는것
		"""
		result = []
		for one_data in original_data:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def delete_special_letter_in_text(self, input_text):
		"""
		특수문자를 제거하는것
		"""
		for one in input_text:
			if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
				temp = temp + str(one)
		result = temp
		return result

	def delete_specual_char_in_text_except_number_n_eng(self, original_data):
		"""
		숫자와 문자만 남기는것
		result = []
		입력형태 :
		출력형태 :
		"""
		result = []
		for one_data in original_data:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def delete_value_in_list_1d_by_step(self, input_list, step, start=0):
		"""
		원하는 순서째의 자료를 ""으로 만드는것
		"""
		flag_no = 0
		for num in range(start, len(input_list)):
			flag_no = flag_no + 1
			if flag_no == step:
				input_list[num] = ""
				flag_no = 0
		return input_list

	def delete_value_in_list_1d_by_step_no(self, input_list, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 ""으로 만드는것

		[1,2,3,4,5,6,7,8,9] ==> [1,2,"",4,5,"",7,8,""]

		:param input_list:
		:param step:
		:param start:
		:return:
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []
		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = ""
			result.append(temp_value)
		return result

	def delete_value_in_list_2d_when_same_until_no(self, input_list_2d, input_no=2):
		"""
		입력받은 2d자료형에서
		뒤에서 몇번째의 자료를 제외하고 같은 자료를 입력받은것엣 지우기

		:param input_list_2d:
		:param input_no:
		:return:
		"""

		is_same = []
		result = []
		for one in input_list_2d:
			if one[:-input_no] in is_same:
				pass
			# print(one)
			else:
				is_same.append(one[:-input_no])
				result.append(one)
		return result

	def delete_value_in_list_2d_when_same_until_num(self, input_list_2d, input_no=2):
		"""
		입력받은 2d자료형에서
		뒤에서 몇번째의 자료를 제외하고 같은 자료를 입력받은것엣 지우기

		:param input_list_2d:
		:param input_no:
		:return:
		"""

		is_same = []
		result = []
		for one in input_list_2d:
			if one[:-input_no] in is_same:
				pass
			# print(one)
			else:
				is_same.append(one[:-input_no])
				result.append(one)
		return result

	def delete_waste_data_in_data_except_number_eng(self, original_data):
		"""
		숫자와 영어만 남기는것, 나머지것은 다 삭제하는것
		result=[
		입력형태:
		출력형태:

		:param original_data:
		:return:
		"""
		result = []
		for one_data in original_data:
			temp = ""
			for one in one_data:
				if str(one) in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
					temp = temp + str(one)
			result.append(temp)
		return result

	def delete_word(self):
		"""
		문장내의 특정한 글자를 제거하는것

		:return:
		"""
		a = 111
		return a

	def delete_xline_in_list_2d_by_index_list(self, input_list_2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		메뉴에서 제외

		:param input_list_2d: list type 2dimension, 2차원의 리스트형
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_yline_in_list_2d_by_index_list(self, input_list_2d, no_list):
		"""
		2차원 자료에서 원하는 순서들의 자료를 삭제하는 것
		입력형태 : 2차원리스트, [2,5,7]

		:param input_list_2d: 2차원 형태의 리스트
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delta_two_list_1d(self, list_1d_a, list_1d_b):
		"""
		두개 리스트중에서，앞과 동일한것만 삭제하기 위한 것
		앞의 리스트에서 뒤에 갈은것만 삭제하는것
		예 : [1,2,3,4,5] - [3,4,5,6,7] ==> [1,2]

		:param list_1d_a:
		:param list_1d_b:
		:return:
		"""
		result = [x for x in list_1d_a if x not in list_1d_b]
		return result

	def devide_code_in_file_name(self, file_name):
		"""
		화일에서 def를 기준으로 분리하는 것
		"""
		# 텍스트 읽어오기
		file_pointer = open(file_name, 'r', encoding='utf-8')
		# 한번에 다 읽기
		result = {}
		file_list = file_pointer.readlines()
		key_value = "__aa__bb__cc__"
		temp = []
		for ori_value in file_list:
			one_value = str(ori_value).replace(" ", "")
			one_value = str(one_value).replace("\t", "")
			if one_value[0:3] == "def":
				# print(key_value)
				result[key_value] = temp
				temp = []
				key_value = "__aa__bb__cc__" + str(ori_value)
			else:
				temp.append(ori_value)
		result[key_value] = temp

		aaa = list(result.keys())
		aaa.sort()

		for one in aaa:
			update_one = one.replace("__aa__bb__cc__", "")
			update_one = update_one.replace("\n", "")
			print(update_one)
			for one_1 in result[one]:
				one_1 = one_1.replace("\n", "")
				print(one_1)

	def devide_list_1d_by_step(self, input_list_1d, step_no):
		total_no = len(input_list_1d)
		repeat_no = step_no
		group_no = divmod(len(input_list_1d), int(step_no))[0]
		namuji = total_no - repeat_no * group_no
		result = []
		print(total_no, namuji)
		for y in range(step_no):
			for x in range(group_no + 1):
				new_no = x * step_no + y
				if new_no > total_no - 1:
					break
				else:
					print(y, x, new_no)
					result.append(input_list_1d[int(new_no)])
		return result

	def diff_list1_list2(self, input_list1, input_list2):
		"""
		두개의 리스트에서 디의 자료를 삭제하는것

		:param input_list1:
		:param input_list2:
		:return:
		"""
		for one in input_list2:
			try:
				input_list1.remove(one)
			except:
				pass

		result = input_list1
		return result

	def draw_get_diagonal_xy(self, xyxy=[5, 9, 12, 21]):
		"""
		좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
		좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]
		"""
		result = []
		if xyxy[0] > xyxy[2]:
			x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
		else:
			x1, y1, x2, y2 = xyxy

		x_height = abs(x2 - x1) + 1
		y_width = abs(y2 - y1) + 1
		step = x_height / y_width
		temp = 0

		if x1 <= x2 and y1 <= y2:
			# \형태의 대각선
			for y in range(1, y_width + 1):
				x = y * step
				if int(x) >= 1:
					final_x = int(x) + x1 - 1
					final_y = int(y) + y1 - 1
					if temp != final_x:
						result.append([final_x, final_y])
						temp = final_x
		else:
			for y in range(y_width, 0, -1):
				x = x_height - y * step

				final_x = int(x) + x1
				final_y = int(y) + y1 - y_width
				temp_no = int(x)

				if temp != final_x:
					temp = final_x
					result.append([final_x, final_y])
		return result

	def draw_triangle(self, xyxy, per=100, reverse=1, size=100):
		"""
		직각삼각형
		정삼각형에서 오른쪽이나 왼쪽으로 얼마나 더 간것인지
		100이나 -100이면 직삼각형이다
		사각형은 왼쪽위에서 오른쪽 아래로 만들어 진다
		"""
		x1, y1, x2, y2 = xyxy
		width = x2 - x1
		height = y2 - y1
		lt = [x1, y1]  # left top
		lb = [x2, y1]  # left bottom
		rt = [x1, y2]  # right top
		rb = [x2, y2]  # right bottom
		tm = [x1, int(y1 + width / 2)]  # 윗쪽의 중간
		lm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		rm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		bm = [x2, int(y1 + width / 2)]  # 윗쪽의 중간
		center = [int(x1 + width / 2), int(y1 + height / 2)]

		result = [lb, rb, rt]
		return result

	def easy_format(self, input_value, big_digit="", small_digit="", comma="", fill_char="", left_right=""):
		small_digit_value = small_digit
		if left_right == "left":
			left_right_value = ""
		elif left_right == "right":
			left_right_value = ">"
		else:
			left_right_value = ""

		if small_digit != "":
			small_digit_value = "." + str(small_digit) + "f"
		format_string = left_right_value + fill_char + str(big_digit) + comma + small_digit_value
		result = format(input_value, format_string)
		return result

	def extract_list_by_index(self, input_list, position_list):
		"""
		리스트로 넘오온 자료를 원하는 열만 추출하는것
		"""
		result = []
		for one_list in input_list:
			temp = []
			for one in position_list:
				temp.append(one_list[one - 1])
			result.append(temp)
		return result

	def filter_3_list_with_3_order_no(self, i_list_2d, i_no_list):
		"""
		입력되는 2차원자료에서, 원하는 순서번째의 자료만 갖고오는 것
		bbb = pick_3_list_with_3_order_no(aaa, [5,3,2])
		:param i_list_2d:
		:param i_no_list:
		:return:
		"""
		result = []
		for no in i_no_list:
			result.append(i_list_2d[no - 1])
		return result

	def filter_category_data(self, input_list_2d, list_no):
		"""
		2차원자료의 리스트에서 y줄번호를 입력하면, 그줄의 고유한 값들만 돌려주는것
		제목이나 카테고리를 만들려고 한다

		:param input_list_2d:
		:param list_no:
		:return:
		"""
		result = []
		for no in list_no:
			temp = set([])
			for list_1d in input_list_2d:
				if list_1d[no]:
					temp.add(list_1d[no])
			result.append(list(temp))
		return result

	def filter_list_1d_for_int(self, input_list):
		"""
		입력리스트중에 정수만 골라내는 것

		:param input_list:
		"""
		result = False
		for one in input_list:
			if type(123) == type(one):
				result = one
				break
		return result

	def filter_list_1d_for_number_type(self, input_text):
		"""
		단어중에 나와있는 숫자만 분리하는기능
		"""
		re_compile = re.compile(r"([0-9]+)")
		result = re_compile.findall(input_text)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def filter_list_1d_for_str_type(self, input_list):
		"""
		문자형 자료만 추출하는것

		:param input_list:
		:return:
		"""
		result = set()
		temp_list = []
		for one_data in input_list:
			temp = self.pick_str_data_only(one_data, temp_list)
			result.update(temp)

	def filter_list_1d_for_str_type_1(self, one_value, result=[]):
		"""
		문자형 자료만 골라내는 것

		:param one_value:
		:param result:
		:return:
		"""
		if type(one_value) == type(None):
			pass
		elif type(one_value) == type([]):
			for one in one_value:
				self.pick_str_data_only(one, result)
		elif type(one_value) == type(()):
			for one in one_value:
				self.pick_str_data_only(one, result)
		elif type(one_value) == type("abc"):
			result.append(one_value)
		elif type(one_value) == type(123):
			pass
		elif type(one_value) == type(123.45):
			pass
		elif type(one_value) == type(True) or type(one_value) == type(False):
			pass
		return result

	def filter_list_1d_for_unique_data(self, input_data):
		"""
		리스트의 값중 고유한것만 골라내기
		"""
		temp = set()
		for one in input_data:
			temp.add(one)
		result = list(temp)
		return result

	def filter_list_1d_for_unique_value(self, input_datas, status=0):
		"""
		중복된 리스트의 자료를 없애는 것이다. 같은것중에서 하나만 남기고 나머지는 []으로 고친다
		"""
		if status == 0:
			result = []
			# 계속해서 pop으로 하나씩 없애므로 하나도 없으면 그만 실행한다
			while len(input_datas) != 0:
				gijun = input_datas.pop()
				sjpark = 0
				result.append(gijun)
				for number in range(len(input_datas)):
					if input_datas[int(number)] == []:  # 빈자료일때는 그냥 통과한다
						pass
					if input_datas[int(number)] == gijun:  # 자료가 같은것이 있으면 []으로 변경한다
						sjpark = sjpark + 1
						input_datas[int(number)] = []
		else:
			# 중복된것중에서 아무것도없는 []마저 없애는 것이다. 위의 only_one을 이용하여 사용한다
			# 같은것중에서 하나만 남기고 나머지는 []으로 고친다
			# 이것은 연속된 자료만 기준으로 삭제를 하는 것입니다
			# 만약 연속이 되지않은 같은자료는 삭제가 되지를 않읍니다
			result = list(self.remain_list_unique_value(input_datas))
			for a in range(len(result) - 1, 0, -1):
				if result[a] == []:
					del result[int(a)]
		return result

	def filter_list_2d_for_condition(self, input_list_2d, condition=[[2, 0]]):
		"""
		입력으로 들어온 자료에서
		condition에 있는 조건의 값들만 필터링하는것	[[2번째열, 자료있음], [(6번째열, 자료없음]...]

		:param input_list_2d:
		:param condition:
		:return:
		"""
		result = []
		count_no = len(condition)
		for list_1d in input_list_2d:
			temp = 0
			for one in condition:
				if not one[1] and not list_1d[one[0]]:
					temp = temp + 1
				elif one[1] and list_1d[one[0]]:
					temp = temp + 1
			if temp == count_no:
				result.append(list_1d)
		return result

	def filter_list_2d_for_gtlt_style(self, input_list_2d, line_no=2, condition=[[2, "<"], ["<=", 4]]):
		"""
		2차원자료에서 크고작은 조건으로 골라내는것
		:param input_list_2d:
		:param line_no:
		:param condition:
		:return:
		"""
		result = []
		if "<" in condition or "<=" in condition or ">" in condition or ">=" in condition:
			if len(condition) == 3:
				if condition[0] == "value":
					for list_1d in input_list_2d:
						exec(f"if {list_1d[line_no - 1]} {condition[1]} {condition[2]}: result.append({list_1d})")
				elif condition[2] == "value":
					for list_1d in input_list_2d:
						exec(f"if {condition[0]} {condition[1]} {list_1d[line_no - 1]}: result.append({list_1d})")
			elif len(condition) == 5:
				for list_1d in input_list_2d:
					aaa = f"if {condition[0]} {condition[1]} {list_1d[line_no - 1]} {condition[3]} {condition[4]}: result.append({list_1d})"
					# print(aaa)
					exec(aaa)
			else:
				for list_1d in input_list_2d:
					if list_1d[line_no - 1] in condition:
						result.append(list_1d)

		return result

	def filter_list_2d_for_int_n_str(self, input_list_2d):
		"""
		입력된 2차원자료를 프린트가 가능한 형태로 만든다
		숫자와 문자를 제외하고는 모드 None으로 만드는 것
		"""
		result = []
		for x, list_1d in enumerate(input_list_2d):
			t_list = []
			for y, value in enumerate(list_1d):
				temp = self.check_data_type_for_data(value)
				# print(temp, value)
				if temp in ["int", "string"]:
					t_list.append(value)
				else:
					t_list.append(None)
			result.append(t_list)
		print(result)
		return result

	def filter_list_2d_for_not_empty_value_by_index(self, input_list_2d, index_no=4):
		# index 번호의 Y열의 값이 빈것이 아닌것만 돌려주는 것
		result = []
		for index, one in enumerate(input_list_2d):
			if one[index_no]:
				result.append(one)
		return result

	def filter_list_2d_for_same_data(self, input_list_2d, input_position, input_value):
		"""
		입력으로 들어온 2차원 자료에서, 특정 위치의 특정값인것만 갖고오기

		:param input_list_2d:
		:param input_position:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			if list_1d[input_position] == input_value:
				result.append(list_1d)
		return result

	def filter_list_2d_for_same_with_first_line_and_yline(self, input_list_2d, same_line=[1, 4]):
		"""
		입력으로 들어온 자료에서
		맨처음의 자료와 같은것만 골라내기

		:param input_list_2d:
		:param same_line:
		:return:
		"""
		result = [input_list_2d[0]]
		count_no = len(same_line)
		for list_1d in input_list_2d[1:]:
			temp = 0
			for no in same_line:
				if input_list_2d[0][no - 1] == list_1d[no - 1]:
					temp = temp + 1
				else:
					break
			if temp == count_no:
				result.append(list_1d)
		return result

	def filter_list_2d_for_same_with_yline_and_value(self, input_list_2d, input_y_no, input_value):
		result = []
		for list_1d in input_list_2d:
			if list_1d[input_y_no - 1] == input.value:
				result.append(list_1d)
		return result

	def filter_list_2d_for_unique_data(self, input_2dlist):
		"""
		입력된 값중에서 고유한 값만을 골라내는것

		:param input_2dlist:
		:return:
		"""
		result = set()
		if type(input_2dlist[0]) != type([]):
			input_2dlist = [input_2dlist]
		for x in range(len(input_2dlist)):
			for y in range(len(input_2dlist[x])):
				value = input_2dlist[x][y]
				if value == "" or value == None:
					pass
				else:
					result.add(value)
		return list(result)

	def filter_list_2d_for_yline_no_and_value(self, input_list_2d, input_position, input_value):
		"""
		입력으로 들어온 2차원 자료에서, 특정 위치의 특정값인것만 갖고오기

		:param input_list_2d:
		:param input_position:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			if list_1d[input_position - 1] == input_value:
				result.append(list_1d)
		return result

	def filter_list_for_index_list(self, input_list, position_list):
		"""
		리스트로 넘오온 자료를 원하는 열만 추출하는것

		:param input_list:
		:param position_list:
		:return:
		"""
		result = []
		for one_list in input_list:
			temp = []
			for one in position_list:
				temp.append(one_list[one - 1])
			result.append(temp)
		return result

	def filter_max_data(self):
		"""
		자료중에서 가장 큰값이나 작은값을 찾아내는것

		그것을 기준으로 찾아서 자료를 넣어주는 기능

		:return:
		"""
		a = 111
		return a

	def filter_text_1d_for_eng(self, input_text):
		"""
		단어중에 나와있는 영어만 분리하는기능
		"""
		re_compile = re.compile(r"([a-zA-Z]+)")
		result = re_compile.findall(input_text)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def filter_text_for_number(self, input_text):
		"""
		단어중에 나와있는 숫자만 분리하는기능
		"""
		re_compile = re.compile(r"([0-9]+)")
		result = re_compile.findall(input_text)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def filter_two_list_1d_for_unique_data(self, list_1d_a, list_1d_b):
		"""
		두개 리스트중에서,앞과 동일한것만 삭제하기 위한 것
		앞의 리스트에서 뒤에 갈은것만 삭제하는것
		예: [1,2, 3,4,5] - [3,4,5,6,7] ==> [1,2]

		:param list_1d_a:
		:param list_1d_b:
		:return:
		"""
		result = [x for x in list_1d_a if x not in list_1d_b]
		return result

	def filter_unique_col_name_compare_table_col_name(self, table_name, data2):
		"""
		고유한 컬럼만 골라낸다

		:param table_name:
		:param data2:
		:return:
		"""
		result = []
		columns = self.get_all_file_name_in_folder(table_name)
		update_data2 = self.delete_waste_data_in_data_except_number_eng(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def filter_yline_set_at_list_2d(self, input_list_2d, list_1d):
		result = []
		for one_list in input_list_2d:
			temp = []
			for index in list_1d:
				temp.append(one_list[index])
				result.append(temp)
		return result

	def find_files_with_same_name(self, directory, target_file_name):
		matching_files = []
		for root, dirs, files in os.walk(directory):
			for file in files:
				if file == target_file_name:
					file_path = os.path.join(root, file)
					creation_time = os.path.getctime(file_path)
					creation_date = datetime.fromtimestamp(creation_time).strftime('%y%m%d')
					matching_files.append([root, creation_date, file])
		return matching_files

	def find_one_line_by_value_in_y_line(self, list_2d, check_value, y_line_no=1):
		for list_1d in list_2d:
			if list_1d[y_line_no] == check_value:
				return list_1d

	def find_same_value_in_list_2d(self, input_lisd1d_1, input_lisd1d_2):
		"""
		2차원의 자료안에서 입력값이 같은것을 찾아내기
		"""
		result = []
		for one in input_lisd1d_1:
			if one in input_lisd1d_2:
				result.append(one)
		return result

	def get_all_doc_of_each_method_for_object(self, object):
		"""
		입력 : 원하는 객체
		출력 : 모든 객체의 메소드이름을 사전형식으로 doc를 갖고오는것

		:param object:
		:return:
		"""
		bbb = ""
		result = {}
		aaa = self.get_all_method_name_with_argument_for_object(object)

		# 만들어진 자료를 정렬한다
		all_methods_name = list(aaa.keys())
		all_methods_name.sort()

		# 위에서 만들어진 자료를 기준으로 윗부분에 나타난 형식으로 만드는 것이다
		for method_name in all_methods_name:
			if not method_name.startswith("_"):
				# exec(f"bbb = {object}.{method_name}.__doc__")
				bbb = inspect.getdoc(f"{object}.{method_name}")
				result[method_name]["manual"] = str(bbb)
		return result

	def get_all_file_in_folder_with_sub_folder(self, input_path, file_name):
		"""
		입력 폴더안의 서브폴더를 포함한 곳에서 화일을 경로및 수정일자를 포함해서 돌려주는것
		"""
		import pynal
		xytime = pynal.pynal()
		result = []
		for root, sub_folder, files in os.walk(input_path):
			for item in files:
				if file_name == item:
					file_path = root + '/' + file_name
					created = os.path.getctime(file_path)
					modified = os.path.getmtime(file_path)
					dt_obj = xytime.change_any_time_to_dt_obj(modified)
					aaa = xytime.change_dt_obj_to_ymd_list(dt_obj)

					result.append([file_name, root, str(aaa[0]) + str(aaa[1]) + str(aaa[2])])
		return result

	def get_all_file_information_in_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					temp = self.get_all_file_name_in_folder_with_properties(directory + "\\" + one.name)
					result.extend(temp)
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_all_file_information_in_folder_except_sub_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					pass
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_all_file_n_folder_name_in_folder(self, directory):
		"""
		폴더 안의 화일을 읽어오는것

		:param directory:
		:return:
		"""
		result = []
		file_names = os.listdir(directory)
		for file_name in file_names:
			full_file_name = os.path.join(directory, file_name)
			result.append(file_name)
		return result

	def get_all_file_name_in_folder(self, directory="./", except_hidden=True):
		"""
		폴더안의 파일을 리스트로 만들어서 주는것
		기본적으로 hidden화일은 나타나지 않도록 한다
		"""
		result = []
		all_file_n_folder = os.scandir(directory)
		for one in all_file_n_folder:
			if not one.is_dir():
				if except_hidden:
					fa = os.stat(one).st_file_attributes
					if not bool(fa & stat.FILE_ATTRIBUTE_HIDDEN):
						result.append(one.name)

				else:
					result.append(one.name)
		return result

	def get_all_file_name_in_folder_by_first_underbar(self, input_folder):
		"""
		어떤 폴더안의 화일이름을 2단계의 메뉴로 만들어주는 코드
		화일이름을 기준으로 _로 나누어서 2단계의 메뉴을 만드는데 사용
		aaa_bbb_ccc => ["aaa", "bbb_ccc"]
		"""

		file_names = self.get_all_file_name_in_folder(input_folder)
		result = {}

		for one_file in file_names:
			splited_file_name = str(one_file).split("_")

			if len(splited_file_name) == 1:
				result[splited_file_name[0]] = ""
			else:
				result[one_file] = [splited_file_name[0]], one_file[len(splited_file_name[0]) + 1:]
		return result

	def get_all_file_name_in_folder_filter_by_extension_name(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		변경함,여러 확장자도 사용할수있도록 ["txt", "png"]
		youtil에 있음

		:param directory:
		:param filter:
		:return:
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "+" or filter == "":
			result = all_files
		else:
			for x in all_files:
				if type(filter) == type([]):
					for one in filter:
						if x.endswith("." + one):
							result.append(x)
				elif x.endswith("." + filter):
					result.append(x)
		return result

	def get_all_file_name_in_folder_with_all_properties(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					temp = self.read_file_names_in_folder_with_all_properties(directory + "\\" + one.name)
					result.extend(temp)
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_all_file_name_in_folder_with_all_properties_except_sub_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					pass
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_all_file_name_n_folder_name_in_folder(self, directory):
		"""
		폴더 안의 화일을 읽어오는것

		:param directory:
		:return:
		"""
		result = []
		file_names = os.listdir(directory)
		for file_name in file_names:
			full_file_name = os.path.join(directory, file_name)
			result.append(file_name)
		return result

	def get_all_folder_name_in_folder(self, directory="./"):
		"""
		폴더안의 파일을 리스트로 만들어서 주는것
		"""
		result = []
		all_file_n_folder = os.scandir(directory)
		for one in all_file_n_folder:
			if one.is_dir():
				result.append(one.name)
		return result

	def get_all_help_of_method_name_for_object(self, input_object):
		"""
		객체를 주면 메소드의 help를 돌려 주는것

		:param input_object:
		:return:
		"""
		result = {}
		for method_name in dir(input_object):
			temp = []
			# 이중언더 메소드는 제외시키는것
			if not method_name.startswith('__'):
				try:
					temp.append(method_name)
					temp.append(getattr(input_object, method_name).__doc__)
				except:
					pass
			result[method_name] = temp
		return result

	def get_all_method_argument_for_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = {}
		for obj_method in dir(object):
			try:
				method_data = inspect.signature(getattr(object, obj_method))
				dic_fun_var = {}
				if not obj_method.startswith("_"):
					for one in method_data.parameters:
						value_default = method_data.parameters[one].default
						value_data = str(method_data.parameters[one])
						if value_default == inspect._empty:
							dic_fun_var[value_data] = None
						else:
							value_key, value_value = value_data.split("=")
							dic_fun_var[value_key] = value_value
						result[obj_method] = dic_fun_var
			except:
				pass
		return result

	def get_all_method_code_by_method_name(self, str_method_name):
		"""
		메소드의 코드를 읽어오는것
		문자로 넣을수있도록 만든 것이다

		:param str_method_name:
		:return:
		"""
		# method_name = eval(str_method_name)
		code_text = inspect.getsource(str_method_name)
		return code_text

	def get_all_method_doc_for_object(self, obgect):
		"""
		"""
		result = {}
		for one in dir(obgect):
			temp = []
			if not one.startswith('__'):
				try:
					temp.append(one)
					# print(one)
					temp.append(getattr(obgect, one).__doc__)
				# print(getattr(obgect, one).__doc__)
				except:
					pass
			result[one] = temp
		return result

	def get_all_method_name_for_file(self, file_name):
		"""
		py로만든 화일을 읽어서 def를 기준으로 분리하는 것
		"""
		#	텍스트 읽어오기
		file_pointer = open(file_name, 'r', encoding='utf-8')
		#	한번에 다 읽기
		result = {}
		filejist = file_pointer.readlines()
		key_value = "_aa_bb_cc_"
		temp = []
		for ori_value in filejist:
			one_value = str(ori_value).replace(" ", "")
			one_value = str(one_value).replace("\t", "")
			if one_value[0:3] == "def":
				# print(key_value)
				result[key_value] = temp
				temp = []
			key_value = "_aa_bb_cc_" + str(ori_value)
		else:
			temp.append(ori_value)
		result[key_value] = temp
		aaa = list(result.keys())
		aaa.sort()
		for one in aaa:
			update_one = one.replace("_aa_bb_cc_", "")
			update_one = update_one.replace("\n", "")
			# print(update_one)
			for one_1 in result[one]:
				one_1 = one_1.replace("\n", "")

	def get_all_method_name_for_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = self.get_all_method_name_for_object_except_dunder_methods(object)
		return result

	def get_all_method_name_for_object_except_dunder_methods(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다

		:param object:
		:return:
		"""
		result = []
		for object_method in dir(object):
			if object_method.startswith("__"):
				pass
			else:
				result.append(object_method)

		return result

	def get_all_method_name_for_object_except_dunder_methods_with_prefix(self, input_object, start_text):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다

		:param object:
		:return:
		"""
		# all_method_name = self.get_all_method_name_with_argument_for_object(input_object)
		# print(all_method_name)

		all_method_name1 = self.get_all_method_name_with_argument_for_object(input_object)
		# print(all_method_name1)

		result = []
		for obj_method in all_method_name1:
			# print(obj_method)
			if obj_method.startswith("__"):
				pass
			else:
				result.append(start_text + obj_method)
		return result

	def get_all_method_name_with_argument_for_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		{"메소드이름":{"변수1":"기본값1", "변수2":"기본값2".....}......}
		:param object:
		:return:
		"""
		result = {}
		for method_name in dir(object):
			try:
				method_data = inspect.signature(getattr(object, method_name))
				# (sheet_name='', xyxy='', value='입력필요')이런형태로 결과값이 넘어온다

				one_method_data = {}
				# __로 시작되는 던더메소드를 제외하는것
				if not method_name.startswith("_"):
					for one in method_data.parameters:

						# 인자의 기본값이 있는지를 확인하는 것
						para_name = one
						para_value = method_data.parameters[one].default

						# 기본값이 없으면 None으로 하고
						if para_value == inspect._empty:
							para_value = None
						else:
							if para_value == "''" or para_value == '""':
								para_value = ''
							# 변수값중 ''가 들어간것이 없어져서, 아래의 것을 주석처리를 함
							one_method_data[para_name] = para_value

				result[method_name] = one_method_data

			except:
				pass
		return result

	def get_all_method_name_with_argument_for_object_except_dunder_methods(self, object):
		"""
		객체를 넣으면 객체의 메소드와 그 메소드의 parameter를 갖고오는 것

		:param object:
		:return:
		"""
		result = {}
		for one_method_name in dir(object):
			try:
				(sig, local_vars) = inspect.signature(getattr(object, one_method_name)), locals()
				if not one_method_name.startswith("_"):
					args = {}
					for a in sig.parameters.keys():
						args[a] = sig.parameters[a]
					result[one_method_name] = args
			except:
				pass
		return result

	def get_all_method_name_with_argument_in_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = {}
		for obj_method in dir(object):
			try:
				method_data = inspect.signature(getattr(object, obj_method))
				dic_fun_var = {}
				if not obj_method.startswith("_"):
					for one in method_data.parameters:
						value_default = method_data.parameters[one].default
						value_data = str(method_data.parameters[one])

						if value_default == inspect._empty:
							dic_fun_var[value_data] = None
						else:
							value_key, value_value = value_data.split("=")
							if "remove" in obj_method:
								print(value_key, value_value)
							if value_value == "''" or value_value == '""':
								value_value = ''
							# 변수값중 ''가 들어간것이 없어져서, 아래의 것을 주석처리를 함
							# value_value = str(value_value).replace("'", "")
							# print(value_data, "키값==>", value_key, "입력값==>", value_value)
							dic_fun_var[str(value_key)] = value_value
						result[obj_method] = dic_fun_var

			except:
				pass
		return result

	def get_all_properties_for_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다

		:param object:
		"""
		result = []
		for att in dir(object):
			result.append(att)
		return result

	def get_all_properties_for_object_except_dunder_method(self, object):
		result = []
		for i in inspect.getmembers(object):
			if not i[0].startswith('_'):
				if not inspect.ismethod(i[1]):
					result.append(i)
		return result

	def get_all_source_code_of_methods_for_object(self, input_object):
		"""
		입력객체에 대해서, 메소드를 기준으로 소스코드를 읽어오는것

		:param input_object:
		"""
		result = {}
		method_object = ""
		for object_method in dir(input_object):
			if not object_method.startswith("_"):
				try:
					exec(f"method_object = {input_object}.{object_method}")
					ddd = inspect.getsource(method_object)
					result[object_method] = ddd
				except:
					pass
		return result

	def get_arguments_for_method_name_for_object(self, object, method_name):
		result = inspect.signature(getattr(object, method_name))
		# print(result.parameters)
		return result

	def get_biff_record(self):
		height = self.height
		options = 0x00
		if self.bold:
			options |= 0x01
			self._weight = 0x02BC
		if self.italic:
			options |= 0x02
		if self.underline != self.UNDERLINE_NONE:
			options |= 0x04
		if self.struck_out:
			options |= 0x08
		if self.outline:
			options |= 0x010
		if self.shadow:
			options |= 0x020
		colour_index = self.colour_index
		weight = self._weight
		escapement = self.escapement
		underline = self.underline
		family = self.family
		charset = self.charset
		name = self.name

	def get_cho_sung_for_korea(self, input_kor):
		"""
		초성의 글자만 갖고오는것

		:param input_kor:
		:return:
		"""
		result = []
		for one in input_kor:
			try:
				aa = self.split_korea_to_jamo(one)
				result.append(aa[0][0])
			except:
				pass
		return result

	def get_code(self, file_name):
		"""
		py로 만들어진 화일을 불러온다

		:param file_name:
		:return:
		"""
		temp_list = []
		result = []

		try:
			f = open(file_name, mode='r', encoding='cp949')
			lines = f.readlines()
		finally:
			f = open(file_name, mode='r', encoding='utf-8')
			lines = f.readlines()
			print(lines)

		original = lines
		lines = list(map(lambda s: s.strip(), lines))
		start_no = 0
		for no in range(len(lines)):
			print(file_name, no)
			line = lines[no]

			changed_line = line.strip()
			changed_line = changed_line.replace("\n", "")
			if changed_line[0:3] == "def" and temp_list != []:
				print("처음은 ===> ", start_no)
				print("끝은 ===> ", no)
				temp_list.insert(0, [start_no, no])
				result.append(temp_list)
				start_no = no
				# print(temp_list)
				temp_list = []
			if changed_line != "" and changed_line[0] != "#":
				temp_list.append(changed_line)
		f.close()
		return [result, original]

	def get_code_for_python_file(self, file_name):

		temp_list = []
		result = []
		f = open(file_name, 'r', encoding='UTF8')
		lines = f.readlines()

		for line in lines:
			c_line = line.strip()
			c_line = c_line.replace("\n", "")
			if c_line and c_line[0:3] == "def" and temp_list != [] and c_line[-1] == ":":
				result.append(temp_list)
				temp_list = []
			temp_list.append(line)
		result.append(temp_list)
		f.close()
		return result

	def get_code_in_python_file(self, file_name):
		"""
		같은 코드를 찾는것
		1. 기본이 되는 코드를 읽는다
		2. def 로 시작되는 코드의 시작과 끝을 읽어온다
		py로 만들어진 화일을 불러온다

		:param file_name:
		:return:
		"""
		temp_list = []
		result = []
		f = open(file_name, 'r', encoding='UTF8')
		lines = f.readlines()
		original = lines
		lines = list(map(lambda s: s.strip(), lines))
		start_no = 0
		for no in range(len(lines)):
			line = lines[no]

			changed_line = line.strip()
			changed_line = changed_line.replace("\n", "")
			if changed_line[0:3] == "def" and temp_list != []:
				# print("처음은 ===> ", start_no)
				# print("끝은 ===> ", no)
				result.append(temp_list)
				start_no = no
				temp_list = []
			if changed_line != "" and changed_line[0] != "#":
				temp_list.append(changed_line)
		f.close()
		return [result, original]

	def get_code_in_python_file_upgrade(self, file_name):

		temp_list = []
		result = []
		f = open(file_name, 'r', encoding='UTF8')
		lines = f.readlines()

		for line in lines:
			c_line = line.strip()
			c_line = c_line.replace("\n", "")
			if c_line and c_line[0:3] == "def" and temp_list != [] and c_line[-1] == ":":
				result.append(temp_list)
				temp_list = []
			temp_list.append(line)
		result.append(temp_list)
		f.close()
		return result

	def get_computer_name_by_win32api(self):
		"""
		win32api 를 사용하는 방법

		:return:
		"""
		print(win32api.GetComputerName())
		print(win32api.GetLocalTime())
		print(win32api.GetCursorPos() )
		print(win32api.GetSystemDirectory())
		print(win32api.GetDiskFreeSpace())
		print(win32api.GetSystemFileCacheSize())
		print(win32api.GlobalMemoryStatus())
		print(win32api.GetSystemDirectory() )
		print(win32api.GetSystemDirectory()  )
		print(win32api.GetSystemDirectory()  )
		print(win32api.GetSystemDirectory()  )

	def get_current_path(self):
		"""
		현재의 경로를 돌려주는것
		"""
		result = os.getcwd()
		return result

	def get_diagonal_xy(self, xyxy=[5, 9, 12, 21]):
		"""
		좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
		좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]
		"""
		result = []
		if xyxy[0] > xyxy[2]:
			x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
		else:
			x1, y1, x2, y2 = xyxy

		x_height = abs(x2 - x1) + 1
		y_width = abs(y2 - y1) + 1
		step = x_height / y_width
		temp = 0

		if x1 <= x2 and y1 <= y2:
			# \형태의 대각선
			for y in range(1, y_width + 1):
				x = y * step
				if int(x) >= 1:
					final_x = int(x) + x1 - 1
					final_y = int(y) + y1 - 1
					if temp != final_x:
						result.append([final_x, final_y])
						temp = final_x
		else:
			for y in range(y_width, 0, -1):
				x = x_height - y * step

				final_x = int(x) + x1
				final_y = int(y) + y1 - y_width
				temp_no = int(x)

				if temp != final_x:
					temp = final_x
					result.append([final_x, final_y])
		return result

	def get_differnet_def_in_two_dic(self, mother_dic, child_dic):
		"""
		두 사전의 내용중에서 다른것을

		:param mother_dic:
		:param child_dic:
		:return:
		"""
		mother_keys_list = mother_dic.keys()
		child_keys_list = child_dic.keys0
		result_unique_key = []
		result_same_key_differ_value = []
		for one_key in mother_keys_list:
			if one_key in child_keys_list:
				if mother_dic[one_key] == child_dic[one_key]:
					pass
				else:
					result_same_key_differ_value.append(one_key)
			else:
				result_unique_key.append(one_key)
		return [result_unique_key, result_same_key_differ_value]

	def get_directory_portion_only_from_file_name(self, input_file=""):
		"""
		입력으로 들어온 화일의 총 이름에서 디렉토리 부분만 추출하는 것
		:param input_file:
		:return:
		"""
		drive, path_and_file = os.path.splitdrive(input_file)
		path, file = os.path.split(input_file)
		result = [path, file]
		return result

	def get_doc_for_method_name_with_object(self, object, method_name):

		try:
			result = getattr(object, method_name).__doc__
		except:
			result = ""

		return result

	def get_encoding_type_for_text (self, text, encoding_type):
		"""
		인코딩 상태를 확인하는 것
		text_encoding_data("Hello", "utf-8")

		:param text:
		:param encoding_type:
		:return:
		"""
		byte_data = text.encode(encoding_type)
		hex_data_as_str = "".join("(0)".format(hex(c)) for c in byte_data)
		int_data_as_str = "".join(" (0)").format(int(c) for c in byte_data)
		return int

	def get_encoding_type_in_system(self, ):
		"""
		기본적인 시스템에서의 인코딩을 읽어온다
		"""
		system_in_basic_incoding = sys.stdin.encoding
		system_out_basic_incoding = sys.stdout.encoding
		print("시스템의 기본적인 입력시의 인코딩 ====> ", system_in_basic_incoding)
		print("시스템의 기본적인 출력시의 인코딩 ====> ", system_out_basic_incoding)

	def get_file(self, file_name):
		"""
		화일 읽기

		:param file_name:
		:return:
		"""
		try:
			f = open(file_name, 'r', encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(file_name, 'r')
			result = f.readlines()
			f.close()

		return result

	def get_file_as_2_types(self, file_full_name):
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		one_file = ""
		for one in file_as_list:
			one_file = one_file + one
		return [file_as_list, one_file]

	def get_file_as_list_1d(self, file_full_name):
		"""
		화일을 리스트형태와 text형태로 2개로 돌려준다

		:param file_full_name:
		:return:
		"""
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		return file_as_list

	def get_file_as_two_types(self, file_full_name):
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		one_file = ""
		for one in file_as_list:
			one_file = one_file + one
		return [file_as_list, one_file]

	def get_file_for_file_name(self, file_name):
		"""
		화일을 읽어오는 것

		:param file_name:
		:return:
		"""
		try:
			f = open(file_name, 'r', encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(file_name, 'r')
			result = f.readlines()
			f.close()
		return result

	def get_file_in_folder(self, old_path=""):
		"""
		폴더안의 화일을 리스트로 돌려주기

		:param old_path:
		:return:
		"""
		if old_path == "": old_path = self.get_current_path()
		# 경로가 없으면 현재의 폴더를 설정한다
		result = os.listdir(old_path)
		return result

	def get_file_information_in_folder_with_sub_folder_as_dic_style(self, directory="./"):
		"""
		같은 화일일때 삭제를 하기위하여 같은 화일을 찾아내는 것이다
		플더안의 파일을 이름, 작성한날, 크기, 총경로를 사전으로 만들어 주며,
		사전의 key 는 이름_ 작성한날 _ 크기 의 형태로 만들고, 값은 [이름, 작성한날, 크기, 총경로]]으로  만든다
		만약 같은 key 를 발견하면 값에 추가를 한다

		:param directory:
		:return:
		"""
		result = {}
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					temp = self.get_file_information_in_folder_with_sub_folder_as_dic_style(directory + "/" + one.name)
					for one_key in temp.keys():
						if one_key in result.keys():
							result[one_key].append(temp[one_key])
						else:
							result[one_key] = [temp[one_key]]
				else:
					key_value = str(one.name) + "_" + str(info.st_mtime) + "" + str(info.st_size)
					one_value = [one.name, info.st_mtime, info.st_size, one.path]
					if key_value in result.keys():
						result[key_value].append(one_value)
					else:
						result[key_value] = [one_value]
			except:
				pass
		return result

	def get_file_list_from_directory(self, directory):
		"""
		입력폴더안의 화일들을 리스트형태로 돌려주는것

		:param directory:
		:return:
		"""
		result = os.listdir(directory)
		return result

	def get_file_name_in_folder_by_extension_name(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것

		:param directory:
		:param filter:
		:return:
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def get_file_name_in_folder_save_as_pickle(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def get_file_name_in_folder_with_all_properties(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					temp = self.get_file_names_in_folder_with_all_properties(directory + "\\" + one.name)
					result.extend(temp)
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_file_name_in_folder_with_all_properties_except_sub_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					pass
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_font_list_for_window(self):
		"""
		윈도우에서 설치된 font리스트를 갖고온다

		:return:
		"""
		font_names = []
		hdc = win32gui.GetDC(None)
		win32gui.EnumFontFamilies(hdc, None, self.callback, font_names)
		#print("\n".join(font_names))
		win32gui.ReleaseDC(hdc, None)
		return font_names

	def get_help_in_each_object_method_name(self, object):
		"""
		객체를 주면 메소드의 help를 돌려 주는것
		"""
		result = {}
		for one in dir(object):
			temp = []
			if not one.startswith('__'):
				try:
					temp.append(one)
					# print(one)
					temp.append(getattr(object, one).__doc__)
				# print(getattr(obgect, one).__doc__)
				except:
					pass
			result[one] = temp
		return result

	def get_help_of_method_name_for_object(self, obgect):
		"""
		read_object_method_name_help
		"""
		result = {}
		for one in dir(obgect):
			temp = []
			if not one.startswith('__'):
				try:
					temp.append(one)
					# print(one)
					temp.append(getattr(obgect, one).__doc__)
				# print(getattr(obgect, one).__doc__)
				except:
					pass
			result[one] = temp
		return result

	def get_help_of_method_name_in_object(self, object):
		"""
		객체를 주면 메소드의 help를 돌려 주는것
		"""
		result = {}
		for one in dir(object):
			temp = []
			if not one.startswith('__'):
				try:
					temp.append(one)
					# print(one)
					temp.append(getattr(object, one).__doc__)
				# print(getattr(obgect, one).__doc__)
				except:
					pass
			result[one] = temp
		return result

	def get_information_for_one_mail(self, input_object):
		"""
		어떤 객체의 모든 속성과 값을 알려주는것
		값이 없는것은 None으로 표시합니다

		:param input_mail:
		:return:
		"""

		result_dic = {}
		all_property = self.get_all_properties_for_object(input_object)
		for one in all_property:
			try:
				value = getattr(input_object, one)
				result_dic[one] = value
			except:
				result_dic[one] = None

		return result_dic

	def get_jaum_xy_list(self, size=[1, 2], input_data="ㄱ"):
		"""
		자음의 xy값을 갖고온다

		:param size:
		:param input_data:
		:return:
		"""
		x, y = size
		# x, y는 글자의 크기
		ja_01 = [["ㄱ"], [1, 1, 1, y], [1, y, x, y]]
		ja_02 = [["ㄴ"], [1, 1, x, 1], [x, 1, x, y]]
		ja_03 = [["ㄷ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y]]
		ja_04 = [["ㄹ"], [1, 1, 1, y], [1, y, 0.5 * x, y], [0.5 * x, y, 0.5 * x, 1], [0.5 * x, 1, x, 1], [x, 1, x, y]]
		ja_05 = [["ㅁ"], [1, 1, 1, y], [1, y, x, y], [x, y, x, 1], [x, 1, 1, 1]]
		ja_06 = [["ㅂ"], [1, 1, x, 1], [x, 1, x, y], [x, y, 1, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_07 = [["ㅅ"], [1, 0.5 * y, 0.3 * x, 0.5 * y], [0.3 * x, 0.5 * y, x, 1], [0.3 * x, 0.5 * y, x, y]]
		ja_08 = [["ㅇ"], [0.8 * x, 0.2 * y, 0.8 * x, 0.8 * y], [0.8 * x, 0.8 * y, 0.6 * x, y, ""],
				 [0.6 * x, y, 0.2 * x, y], [0.2 * x, y, 1, 0.8 * y, "/"], [1, 0.8 * y, 1, 0.2 * y],
				 [1, 0.2 * y, 0.2 * x, 1, ""], [0.2 * x, 1, 0.6 * x, 1], [0.6 * x, 1, 0.8 * x, 0.2 * y, "/"]]
		ja_09 = [["ㅈ"], [1, 1, 1, y], [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1, "/"],
				 [0.5 * x, 0.5 * y, x, y, ""]]
		ja_10 = [["ㅊ"], [0.2 * x, 0.5 * y, 1, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.2 * x, 0.5 * y, 0.4 * x, 0.5 * y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1], [0.5 * x, 0.5 * y, x, y, ""]]
		ja_11 = [["ㅋ"], [1, 1, 1, y], [1, y, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_12 = [["ㅌ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_13 = [["ㅍ"], [1, 1, 1, y], [x, 1, x, y], [1, 0.2 * y, x, 0.2 * y], [1, 0.8 * y, x, 0.8 * y]]
		ja_14 = [["ㅎ"], [1, 0.5 * y, 0.2 * x, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.4 * x, 0.3 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, 0.6 * x, y], [0.6 * x, y, 0.8 * x, y], [0.8 * x, y, x, 0.8 * y],
				 [x, 0.8 * y, x, 0.3 * y], [x, 0.3 * y, 0.8 * x, 1], [0.8 * x, 1, 0.6 * x, 1],
				 [0.6 * x, 1, 0.4 * x, 0.3 * y]]
		ja_31 = [["ㄲ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_32 = [["ㄸ"], [1, 1, 1, 0.4 * y], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], ]
		ja_33 = [["ㅃ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_34 = [["ㅆ"], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1], [0.4 * x, 0.3 * y, x, 0.5 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_35 = [["ㅉ"], [1, 1, 1, 0.5 * y], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1],
				 [0.4 * x, 0.3 * y, x, 0.5 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_36 = [["ㄳ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_37 = [["ㄵ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_38 = [["ㄶ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y],
				 [0.2 * x, 0.6 * y, 0.2 * x, y], [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y],
				 [0.6 * x, y, x, 0.9 * y], [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y],
				 [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y], [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_39 = [["ㄺ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_40 = [["ㄻ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], [x, y, x, 0.7 * y],
				 [x, 0.7 * y, 1, 0.7 * y], ]
		ja_41 = [["ㄼ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y],
				 [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_42 = [["ㄽ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y],
				 [0.4 * x, 0.8 * y, x, y], ]
		ja_43 = [["ㄾ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, 0.7 * y, x, 0.7 * y],
				 [x, 0.7 * y, x, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_44 = [["ㄿ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [x, 0.6 * y, x, y],
				 [1, 0.7 * y, x, 0.7 * y], [1, 0.9 * y, x, 0.9 * y], ]
		ja_45 = [["ㅀ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y], [0.2 * x, 0.6 * y, 0.2 * x, y],
				 [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y], [0.6 * x, y, x, 0.9 * y],
				 [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y], [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y],
				 [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_46 = [["ㅄ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]

		jamo1_dic = {"ㄱ": ja_01, "ㄴ": ja_02, "ㄷ": ja_03, "ㄹ": ja_04, "ㅁ": ja_05,
					 "ㅂ": ja_06, "ㅅ": ja_07, "ㅇ": ja_08, "ㅈ": ja_09, "ㅊ": ja_10,
					 "ㅋ": ja_11, "ㅌ": ja_12, "ㅍ": ja_13, "ㅎ": ja_14,
					 "ㄲ": ja_31, "ㄸ": ja_32, "ㅃ": ja_33, "ㅆ": ja_34, "ㅉ": ja_35,
					 "ㄳ": ja_36, "ㄵ": ja_37, "ㄶ": ja_38, "ㄺ": ja_39, "ㄻ": ja_40,
					 "ㄼ": ja_41, "ㄽ": ja_42, "ㄾ": ja_43, "ㄿ": ja_44, "ㅀ": ja_45, "ㅄ": ja_46,
					 }

		result = jamo1_dic[input_data]
		return result

	def get_list_1d_with_float_range(self, start, end, step):
		"""
		실수형으로 가능한 range 형태

		:param start:
		:param end:
		:param step:
		:return:
		"""
		result = []
		value = start
		while value <= end:
			yield value
			value = step + value
			result.append(value)
		return result

	def get_mail_items_in_folder_in_outlook(self, folder_object, input_no=5):
		result = []
		messages = folder_object.Items
		messages.Sort("ReceivesTime", True)
		message = messages.GetFirst()

		for no in range(input_no):
			print(message.Subject)
			message = messages.GetNext()
			result.append(message)
		return result

	def get_max_size_in_list_2d(self, list_2d_data):
		"""
		2차원 배열의 제일 큰 갯수를 확인한다
		"""
		max_length = max(len(row) for row in list_2d_data)
		return max_length

	def get_max_ylen_for_list_2d(self, list_2d_data):
		"""
		2차원 배열의 제일 큰 갯수를 확인한다
		"""
		max_length = max(len(row) for row in list_2d_data)
		return max_length

	def get_method_code(self, str_method_name):
		# 메소드의 코드를 읽어오는것
		# 문자료 넣을수있도록 만든 것이다

		method_name = eval(str_method_name)
		code_text = inspect.getsource(method_name)
		return code_text

	def get_monitors_properties(self):
		"""
		연결된 모니터들의 속성을 알려준다

		:return:
		"""
		result = {}
		sub_result = {}
		num = 0
		for m in screeninfo.get_monitors():
			num = num + 1
			# print(m)
			sub_result["x"] = m.x
			sub_result["y"] = m.y
			sub_result["height_mm"] = m.height_mm
			sub_result["width_mm"] = m.width_mm
			sub_result["height"] = m.height
			sub_result["width"] = m.width
			sub_result["primary"] = m.is_primary
			sub_result["name"] = m.name
			name = "monitor" + str(num)
			result[name] = sub_result
		return result

	def get_moum_xy_list(self, size=[1, 2], input_data="ㅏ"):
		"""
		모음을 엑셀에 나타내기 위한 좌표를 주는 것이다
		x, y는 글자의 크기

		:param size:
		:param input_data:
		:return:
		"""
		x, y = size
		mo_01 = [["ㅏ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_02 = [["ㅑ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y],
				 [0.6 * x, 0.6 * y, 0.6 * x, 0.8 * y]]
		mo_03 = [["ㅓ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_04 = [["ㅕ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]
		mo_10 = [["ㅣ"], [1, 0.6 * y, x, 0.6 * y]]
		mo_05 = [["ㅗ"], [x, 1, x, y],
				 [x, 0.5 * y, 0.8 * x, 0.5 * y]]
		mo_06 = [["ㅛ"], [x, 1, x, y],
				 [x, 0.3 * y, 0.8 * x, 0.3 * y],
				 [x, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_07 = [["ㅜ"], [1, 1, 1, y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y]]
		mo_08 = [["ㅠ"], [1, 1, 1, y],
				 [1, 0.3 * y, 0.8 * x, 0.3 * y],
				 [1, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_09 = [["ㅡ"], [0.5 * x, 1, 0.5 * x, y]]

		mo_21 = [["ㅐ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_22 = [["ㅒ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.8 * y, 0.6 * x, 0.8 * y]]
		mo_23 = [["ㅔ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_24 = [["ㅖ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]

		jamo2_dic = {
			"ㅏ": mo_01, "ㅑ": mo_02, "ㅓ": mo_03, "ㅕ": mo_04, "ㅗ": mo_05,
			"ㅛ": mo_06, "ㅜ": mo_07, "ㅠ": mo_08, "ㅡ": mo_09, "ㅣ": mo_10,
			"ㅐ": mo_21, "ㅒ": mo_22, "ㅔ": mo_23, "ㅖ": mo_24,
		}
		result = jamo2_dic[input_data]
		return result

	def get_nos_in_list_2d_by_same_xline(self, input_list_2d=""):
		"""
		2dlist의 자료의 형태로 된것중에서
		위에서 부터 같은것을 삭제 한다
		0,3,5의 3개가 같은것이라면 제일 앞의 1개는 제외하고 [3,5]를 돌려준다
		메뉴에서 제외

		:param input_list_2d: 2차원자료의 리스트
		:return:
		"""
		all_datas = input_list_2d
		total_len = len(all_datas)
		same_nos = []
		for no in range(total_len):
			if no in same_nos:
				pass
			else:
				one_list = all_datas[no]
				# print(one_list)
				for num in range(no + 1, total_len):
					if num in same_nos:
						pass
					else:
						if one_list == all_datas[num]:
							same_nos.append(num)
		return same_nos

	def get_not_empty_value_in_list_2d_by_index(self, input_list_2d, index_no=4):
		"""
		index 번호의 Y열의 값이 빈것이 아닌것만 돌려주는 것

		:param input_list_2d:
		:param index_no:
		:return:
		"""
		result = []
		for index, one in enumerate(input_list_2d):
			if one[index_no]:
				result.append(one)
		return result

	def get_one_line_as_search_word(self, file_name="python.py", input_text="menu_dic["):
		"""
		화일안에서 원하는 단어가 들어간 줄을 리스트로 만들어서 돌려주는것
		"""
		aa = open(file_name, 'r', encoding="UTF-8")
		result = []
		for one in aa.readlines():
			if input_text in str(one).strip():
				print(str(one).strip())
				result.append(str(one).strip())
		return result

	def get_one_line_as_search_word_in_file(self, file_name="python.py", input_text="menu_dic["):
		"""
		화일안에서 원하는 단어가 들어간 줄을 리스트로 만들어서 돌려주는것
		메뉴를 만들 목적으로 한것

		:param file_name:
		:param input_text:
		:return:
		"""
		aa = open(file_name, 'r', encoding="UTF-8")
		result = []
		for one in aa.readlines():
			if input_text in str(one).strip():
				# print(str(one).strip())
				result.append(str(one).strip())
		return result

	def get_one_mail_information_in_outlook(self, one_email):
		result = {}
		result["sender"] = one_email.SenderName
		result["receiver"] = one_email.To
		result["title"] = one_email.Subject
		result["time"] = one_email.ReceivedTime
		result["body"] = one_email.Body
		return result

	def get_parameter_datas_for_method_name_in_object(self, input_object, input_method_name):
		"""
		입력으로 드어오는 객체의 메소드에 대하여 파라미터들의 정보를 돌려주는 것
		출력형태 : [사전형의 기본자료형식, ==> {sheet_name:'',xyxy: [1, 1, 7, 7], xy: [3, 3])}
			       문자열의 입력변수형태,  ==> "(sheet_name='', xyxy=[1, 1, 7, 7], xy=[3, 3])"
			       사전형의 자료         ==>  {sheet_name:"sheet_name = ''",xyxy: "xyxy = [1, 1, 7, 7]", xy: "xy=[3, 3]")}
			       ]
		"""
		result = []
		dic_param_vs_default_value = {}
		meta_data = getattr(input_object, input_method_name)

		# result.append(ddd)
		basic_method_data = inspect.signature(meta_data)
		for one in basic_method_data.parameters:
			parameter_name = basic_method_data.parameters[one].name
			parameter_defalt_value = basic_method_data.parameters[one].default
			if parameter_defalt_value == inspect._empty:
				parameter_defalt_value = None
			dic_param_vs_default_value[parameter_name] = parameter_defalt_value
		result.append(dic_param_vs_default_value)
		result.append(str(basic_method_data))
		result.append(basic_method_data.parameters)
		result.append(meta_data.__doc__)

		return result

	def get_partial_list_by_index(self, input_list, position_list):
		"""
		리스트로 넘오온 자료를 원하는 열만 추출하는것

		:param input_list:
		:param position_list:
		:return:
		"""
		result = []
		for one_list in input_list:
			temp = []
			for one in position_list:
				temp.append(one_list[one - 1])
			result.append(temp)
		return result

	def get_pickle_file_in_file_path(self, path_n_name=""):
		"""
		(pickle파일 읽어오기) pickle로 자료를 만든것을 읽어오는 것이다

		:param path_n_name:
		:return:
		"""
		with open(path_n_name, "rb") as fr:
			result = pickle.load(fr)
		return result

	def get_pickle_file_name_in_folder(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def get_pickle_file_names_in_folder(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def get_pickle_list_in_folder(self, directory="./", filter="pickle"):
		"""
		객체를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def get_random_data_set_on_base_letter(self, digit=2, total_no=1, letters="가나다라마바사아자차카타파하"):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것

		:param digit:
		:param total_no:
		:param letters:
		:return:
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				number = random.choice(letters)
				temp = temp + str(number)
			result.append(temp)
		return result

	def get_random_number(self, digit=2, total_no=1):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것

		:param digit:
		:param total_no:
		:return:
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
				temp = temp + str(number)
			result.append(temp)
		return result

	def get_same_value_between_two_list_1d(self, input_list_1d_1, input_list_1d_2):
		"""
		기준값에서 1 차원의 같은 값을 찾는 것이다

		:param input_list_1d_1:
		:param input_list_1d_2:
		:return:
		"""
		result = []
		for one in input_list_1d_1:
			if one in input_list_1d_2:
				result.append(one)
		return result

	def get_same_value_for_list_2d_by_index_list(self, input_lisd2d_1, input_lisd2d_2, index_list=[1, 2]):
		"""
		2 차원의 자료들이 서로 같은것을 삭제하는 것인데,
		모두 같은것이 아니고, 일부분이 같은것을
		골라내는 기능을 만든 것이다

		:param input_lisd2d_1:
		:param input_lisd2d_2:
		:param index_list:
		:return:
		"""
		semi_result_1 = {}
		for num, value in enumerate(input_lisd2d_1):
			temp_1 = []
			for one in index_list:
				temp_1.append(value[one])
				semi_result_1[num] = [temp_1, value]
		semi_result_2 = {}
		for num, value in enumerate(input_lisd2d_2):
			temp_2 = []
			for one in index_list:
				temp_2.append(value[one])
				semi_result_2[num] = [temp_2, value]
		result = []
		for key, value in semi_result_1.items():
			for key2, value2 in semi_result_2.items():
				if value[0] == value2[0]:
					if value[1] in result:
						pass
					else:
						result.append(value[1])
		return list(result)

	def get_same_value_in_list_2d(self, input_lisd1d_1, input_lisd1d_2):
		"""
		2차원의 자료안에서 입력값이 같은것을 찾아내기

		:param input_lisd1d_1:
		:param input_lisd1d_2:
		:return:
		"""
		result = []
		for one in input_lisd1d_1:
			if one in input_lisd1d_2:
				result.append(one)
		return result

	def get_same_value_n_two_list(self, input_list_1, input_list_2):
		"""

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		checked_list_1d_1 = self.get_unique_for_list(input_list_1)
		checked_list_1d_2 = self.get_unique_for_list(input_list_2)
		#print(checked_list_1d_1)
		result = []
		for one_data in checked_list_1d_1:
			if one_data in checked_list_1d_2:
				result.append(one_data)
		return result

	def get_serial_list_for_eng(self, start_serial, count):
		"""
		입력한 영문글자를 원하는 갯수만큼 증가시킨것을 리스트로 돌려주는 것

		:param start_serial:
		:param count:
		:return:
		"""
		result =[ ]
		current_serial = start_serial
		for _ in range(count):
			result.append(current_serial)
			current_serial = self.increment_serial(current_serial)
		return result

	def get_size_for_list_2d(self, input_list_2d):
		"""
		입력값으로 온것의 크기를 돌려주는것

		:param input_list_2d:
		:return:
		"""
		len_x = len(input_list_2d)
		len_y = len(input_list_2d[0])
		return [len_x, len_y]

	def get_sub_folders_names_in_outlook(self, folder_name):
		result = []
		for no in range(self.namespace.Folders[folder_name].Folders.count):
			this_name = self.namespace.Folders[folder_name].Folders[no].name
			result.append([folder_name, no, this_name])
		return result

	def get_sum_value(self, data):
		total = 0
		for a in data:
			total = total + a
		eval = total / len(data)
		return [total, eval, len(data), max(data), min(data)]

	def get_system_encodeing_type(self, ):
		"""
		기본적인 시스템에서의 인코딩을 읽어온다
		"""
		system_in_basic_incoding = sys.stdin.encoding
		system_out_basic_incoding = sys.stdout.encoding
		print("시스템의 기본적인 입력시의 인코딩 ====> ", system_in_basic_incoding)
		print("시스템의 기본적인 출력시의 인코딩 ====> ", system_out_basic_incoding)

	def get_text_as_list(self, i_path):
		# 어떤 텍스트라도 읽어오기
		# text 자료를 읽어오기
		# 어떤 텍스트형태라도 읽어오기
		# default = ANSI
		# osv 는 utf-8 로만하면 에러가 나기도 함, uTF-8-sig
		# UTF-16
		result = []
		encoding_set = ["utf-8", "ansi", "UTE-8-sig", "utf-16", ]
		for a_coding in encoding_set:
			try:
				f = open(i_path, 'r', encoding=a_coding)
				while True:
					line = f.readline()
					if not line: break
					result.append(line)
				f.olose()
				if result != []:
					print(a_coding, result)
					return result
			except:
				pass


	def get_text_file(self, filepath):
		"""
		텍스트화일을 읽어서, 넘겨주는것

		:param file_path:
		:return:
		"""
		result = encoding_set = ["utf-8", "ansi", "UTE-8-sig", "utf-16", ]
		for a_coding in encoding_set:
			try:
				f = open(filepath, 'r', encoding = a_coding)
				for one in f.readlines():
					result = result + one
				f.close()
				return result

			except:
				pass

	def get_top_folder_names_in_outlook(self):
		result = []
		for no in range(self.namespace.Folders.count):
			this_name = self.namespace.Folders[no].Name
			result.append([no, this_name])
		return result

	def get_unique_col_name_compare_table_col_name(self, table_name, data2):
		"""
		고유한 컬럼만 골라낸다

		:param table_name:
		:param data2:
		:return:
		"""
		result = []
		columns = self.get_all_file_name_in_folder(table_name)
		update_data2 = self.delete_all_char_except_number_eng_in_value(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def get_unique_data_for_list_2d(self, input_list_2d):
		"""
		입력된 값중에서 고유한 값만을 골라내는것

		:param input_list_2d:
		:return:
		"""
		result = set()
		if type(input_list_2d[0]) != type([]):
			input_list_2d = [input_list_2d]
		for x in range(len(input_list_2d)):
			for y in range(len(input_list_2d[x])):
				value = input_list_2d[x][y]
				if value == "" or value == None:
					pass
				else:
					result.add(value)
		return list(result)

	def get_unique_data_in_list_1d(self, input_data):
		"""
		리스트의 값중 고유한것만 골라내기

		:param input_data:
		:return:
		"""
		temp = set()
		for one in input_data:
			temp.add(one)
		result = list(temp)
		return result

	def get_unique_function_between_two_python_file(self, file_a, file_b):
		"""
		두 파이썬 화일중에서 다른 함수만 갖고오는것

		:param file_a:
		:param file_b:
		:return:
		"""
		a_file = self.split_python_file_as_def(file_a)
		b_file = self.split_python_file_as_def(file_b)
		a_file_keys = a_file.keys()
		b_file_keys = b_file.keys()
		unique_a = []
		for one_key in a_file_keys:
			if not one_key in b_file_keys:
				unique_a.append([a_file_keys])
		return unique_a

	def get_window_font_list(self):
		"""
		윈도우에서 설치된 font리스트를 갖고온다

		:return:
		"""
		result = []
		hdc = win32gui.GetDC(None)
		win32gui.EnumFontFamilies(hdc, None, self.callback, result)
		win32gui.ReleaseDC(hdc, None)
		return result

	def get_xy_list_for_jaum_on_base_size(self, size=[1, 2], input_data="ㄱ"):
		"""
		일정한 크기를 기준으로 자음의 크기를 계산하는것
		자음의 xy값을 갖고온다

		:param size:
		:param input_data:
		:return:
		"""
		x, y = size
		# x, y는 글자의 크기
		ja_01 = [["ㄱ"], [1, 1, 1, y], [1, y, x, y]]
		ja_02 = [["ㄴ"], [1, 1, x, 1], [x, 1, x, y]]
		ja_03 = [["ㄷ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y]]
		ja_04 = [["ㄹ"], [1, 1, 1, y], [1, y, 0.5 * x, y], [0.5 * x, y, 0.5 * x, 1], [0.5 * x, 1, x, 1], [x, 1, x, y]]
		ja_05 = [["ㅁ"], [1, 1, 1, y], [1, y, x, y], [x, y, x, 1], [x, 1, 1, 1]]
		ja_06 = [["ㅂ"], [1, 1, x, 1], [x, 1, x, y], [x, y, 1, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_07 = [["ㅅ"], [1, 0.5 * y, 0.3 * x, 0.5 * y], [0.3 * x, 0.5 * y, x, 1], [0.3 * x, 0.5 * y, x, y]]
		ja_08 = [["ㅇ"], [0.8 * x, 0.2 * y, 0.8 * x, 0.8 * y], [0.8 * x, 0.8 * y, 0.6 * x, y, ""],
				 [0.6 * x, y, 0.2 * x, y], [0.2 * x, y, 1, 0.8 * y, "/"], [1, 0.8 * y, 1, 0.2 * y],
				 [1, 0.2 * y, 0.2 * x, 1, ""], [0.2 * x, 1, 0.6 * x, 1], [0.6 * x, 1, 0.8 * x, 0.2 * y, "/"]]
		ja_09 = [["ㅈ"], [1, 1, 1, y], [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1, "/"],
				 [0.5 * x, 0.5 * y, x, y, ""]]
		ja_10 = [["ㅊ"], [0.2 * x, 0.5 * y, 1, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.2 * x, 0.5 * y, 0.4 * x, 0.5 * y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1], [0.5 * x, 0.5 * y, x, y, ""]]
		ja_11 = [["ㅋ"], [1, 1, 1, y], [1, y, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_12 = [["ㅌ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_13 = [["ㅍ"], [1, 1, 1, y], [x, 1, x, y], [1, 0.2 * y, x, 0.2 * y], [1, 0.8 * y, x, 0.8 * y]]
		ja_14 = [["ㅎ"], [1, 0.5 * y, 0.2 * x, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.4 * x, 0.3 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, 0.6 * x, y], [0.6 * x, y, 0.8 * x, y], [0.8 * x, y, x, 0.8 * y],
				 [x, 0.8 * y, x, 0.3 * y], [x, 0.3 * y, 0.8 * x, 1], [0.8 * x, 1, 0.6 * x, 1],
				 [0.6 * x, 1, 0.4 * x, 0.3 * y]]
		ja_31 = [["ㄲ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_32 = [["ㄸ"], [1, 1, 1, 0.4 * y], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], ]
		ja_33 = [["ㅃ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_34 = [["ㅆ"], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1], [0.4 * x, 0.3 * y, x, 0.5 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_35 = [["ㅉ"], [1, 1, 1, 0.5 * y], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1],
				 [0.4 * x, 0.3 * y, x, 0.5 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_36 = [["ㄳ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_37 = [["ㄵ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_38 = [["ㄶ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y],
				 [0.2 * x, 0.6 * y, 0.2 * x, y], [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y],
				 [0.6 * x, y, x, 0.9 * y], [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y],
				 [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y], [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_39 = [["ㄺ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_40 = [["ㄻ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], [x, y, x, 0.7 * y],
				 [x, 0.7 * y, 1, 0.7 * y], ]
		ja_41 = [["ㄼ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y],
				 [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_42 = [["ㄽ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y],
				 [0.4 * x, 0.8 * y, x, y], ]
		ja_43 = [["ㄾ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, 0.7 * y, x, 0.7 * y],
				 [x, 0.7 * y, x, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_44 = [["ㄿ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [x, 0.6 * y, x, y],
				 [1, 0.7 * y, x, 0.7 * y], [1, 0.9 * y, x, 0.9 * y], ]
		ja_45 = [["ㅀ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y], [0.2 * x, 0.6 * y, 0.2 * x, y],
				 [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y], [0.6 * x, y, x, 0.9 * y],
				 [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y], [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y],
				 [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_46 = [["ㅄ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]

		jamo1_dic = {"ㄱ": ja_01, "ㄴ": ja_02, "ㄷ": ja_03, "ㄹ": ja_04, "ㅁ": ja_05,
					 "ㅂ": ja_06, "ㅅ": ja_07, "ㅇ": ja_08, "ㅈ": ja_09, "ㅊ": ja_10,
					 "ㅋ": ja_11, "ㅌ": ja_12, "ㅍ": ja_13, "ㅎ": ja_14,
					 "ㄲ": ja_31, "ㄸ": ja_32, "ㅃ": ja_33, "ㅆ": ja_34, "ㅉ": ja_35,
					 "ㄳ": ja_36, "ㄵ": ja_37, "ㄶ": ja_38, "ㄺ": ja_39, "ㄻ": ja_40,
					 "ㄼ": ja_41, "ㄽ": ja_42, "ㄾ": ja_43, "ㄿ": ja_44, "ㅀ": ja_45, "ㅄ": ja_46,
					 }

		result = jamo1_dic[input_data]
		return result

	def get_xy_list_for_moum_on_base_size(self, size=[1, 2], input_data="ㅏ"):
		"""
		모음을 엑셀에 나타내기 위한 좌표를 주는 것이다
		x, y는 글자의 크기

		:param size:
		:param input_data:
		:return:
		"""
		x, y = size
		mo_01 = [["ㅏ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_02 = [["ㅑ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y],
				 [0.6 * x, 0.6 * y, 0.6 * x, 0.8 * y]]
		mo_03 = [["ㅓ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_04 = [["ㅕ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]
		mo_10 = [["ㅣ"], [1, 0.6 * y, x, 0.6 * y]]
		mo_05 = [["ㅗ"], [x, 1, x, y],
				 [x, 0.5 * y, 0.8 * x, 0.5 * y]]
		mo_06 = [["ㅛ"], [x, 1, x, y],
				 [x, 0.3 * y, 0.8 * x, 0.3 * y],
				 [x, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_07 = [["ㅜ"], [1, 1, 1, y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y]]
		mo_08 = [["ㅠ"], [1, 1, 1, y],
				 [1, 0.3 * y, 0.8 * x, 0.3 * y],
				 [1, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_09 = [["ㅡ"], [0.5 * x, 1, 0.5 * x, y]]

		mo_21 = [["ㅐ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_22 = [["ㅒ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.8 * y, 0.6 * x, 0.8 * y]]
		mo_23 = [["ㅔ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_24 = [["ㅖ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]

		jamo2_dic = {
			"ㅏ": mo_01, "ㅑ": mo_02, "ㅓ": mo_03, "ㅕ": mo_04, "ㅗ": mo_05,
			"ㅛ": mo_06, "ㅜ": mo_07, "ㅠ": mo_08, "ㅡ": mo_09, "ㅣ": mo_10,
			"ㅐ": mo_21, "ㅒ": mo_22, "ㅔ": mo_23, "ㅖ": mo_24,
		}
		result = jamo2_dic[input_data]
		return result

	def get_xy_size_for_list_2d(self, input_list_2d):
		"""
		입력값으로 온것의 크기를 돌려주는것

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		len_x = len(input_list_2d)
		len_y = len(input_list_2d[0])
		return [len_x, len_y]

	def group_list_2d_by_index_no(self, input_list_2d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것

		:param input_list_2d:
		:param index_no:
		:return:
		"""
		result = []
		print(input_list_2d)

		sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
		print(sorted_list_2d)

		check_value = sorted_list_2d[0][index_no]
		temp = []
		for one_list in sorted_list_2d:
			if one_list[index_no] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]

				check_value = one_list[index_no]
		if temp:
			result.append(temp)
		return result

	def group_list_3d_by_index_no(self, input_list_3d, index_no=4):
		"""
		3차원의 자료를 2차원기준으로 index_no만큼씩 그룹화 하는것

		:param input_list_3d:
		:param index_no:
		:return:
		"""
		result = []
		for input_list_2d in input_list_3d:
			sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
			grouped_list_3d = self.group_list_2d_by_index_no(sorted_list_2d, index_no)
			result = result + grouped_list_3d
		return result

	def history(self):
		"""
		이화일의 변경 기록

		:return:
		"""
		result = """
			"""
		return result

	def holiday_nation(self):
		"""
		휴일기준

		:return:
		"""
		self.holiday["common"] = ["0101", "0301", "0505", "0606", "0815", "1001", "1225", 1.3]
		self.holiday["company"] = ["0708"]

	def increment_serial(self, serial):
		"""
		입력으로 들어오는 영문자를 1단계 놓은글자로 바꿔주는 것

		:param serial:
		:return:
		"""
		serial_list = list(serial)
		length = len(serial_list)
		for i in range(length -1, -1, -1):
			if serial_list[i] == 'Z':
				serial_list[i]  = 'A'
			else:
				serial_list[i] = chr(ord(serial_list[i]) + 1)
				break
		return ''.join(serial_list)

	def information_for_file_of_folder(self, directory="./"):
		"""
		폴더안의 파일을 리스트로 만들어서 주는것
		"""
		result = []
		all_file_n_folder = os.scandir(directory)
		for one in all_file_n_folder:
			if not one.is_dir():
				result.append(one.stat())
		return result

	def information_for_file_of_folder_except_sub_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_file_n_folder = os.scandir(directory)  # 현재 디렉토리의 모든 화일을 읽어온다
		for one in all_file_n_folder:
			info = one.stat()
			try:
				if one.is_dir():  # 폴더 인경우
					pass
				else:
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def insert_data_by_step_in_list(self, input_list, insert_value, step):
		"""
		기존자료에 n번째마다 자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3, 각 3번째 마다 자료를 추가한다면
		"""
		var_1, var_2 = divmod(len(input_list), int(step))
		for num in range(var_1, 0, -1):
			input_list.insert(num * int(step) - var_2 + 1, insert_value)
		return input_list

	def insert_data_for_list_1d_by_index(self, data, number=1, input_data=[]):
		"""
			리스트에 일정한 간격으로 자료삽입

		:param data:
		:param number:
		:param input_data:
		:return:
		"""
		total_number = len(data)
		dd = 0
		for a in range(len(data)):
			if a % number == 0 and a != 0:
				if total_number != a:
					data.insert(dd, input_data)
					dd = dd + 1
			dd = dd + 1
		return data

	def insert_data_in_list_1d_by_step(self, input_list, insert_value, step):
		"""
		기존자료에 n번째마다 자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3, 각 3번째 마다 자료를 추가한다면

		:param input_list:
		:param insert_value:
		:param step:
		:return:
		"""
		var_1, var_2 = divmod(len(input_list), int(step))
		for num in range(var_1, 0, -1):
			input_list.insert(num * int(step) - var_2 + 1, insert_value)
		return input_list

	def insert_line_in_list(self, data, number=1, input_data=[]):
		"""
		리스트에 일정한 간격으로 자료삽입

		:param data:
		:param number:
		:param input_data:
		:return:
		"""
		total_number = len(data)
		dd = 0
		for a in range(len(data)):
			if a % number == 0 and a != 0:
				if total_number != a:
					data.insert(dd, input_data)
					dd = dd + 1
			dd = dd + 1
		return data

	def insert_list_1d_by_step(self, input_list, insert_value, step):
		"""
		기존자료에 n번째마다 자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3, 각 3번째 마다 자료를 추가한다면
		"""
		var_1, var_2 = divmod(len(input_list), int(step))
		for num in range(var_1, 0, -1):
			input_list.insert(num * int(step) - var_2 + 1, insert_value)
		return input_list

	def insert_list_2d_blank_by_index(self, input_list_2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				input_list_2d[x].insert(int(one), "")
		return input_list_2d

	def insert_list_value_by_step(self, input_list, insert_value, step):
		"""
		기존자료에 n번째마다 자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3, 각 3번째 마다 자료를 추가한다면
		"""
		var_1, var_2 = divmod(len(input_list), int(step))
		for num in range(var_1, 0, -1):
			input_list.insert(num * int(step) - var_2 + 1, insert_value)
		return input_list

	def insert_serial_value_at_begin_for_list_2d(self, input_list_2d, start_no=1, special_char=""):
		"""
		엑셀의 제일 앞세로열에 특이한 번호를 넣고싶은 경우가 있다
		이때, 사용하기 위한 목적으로 만들었다.

		2 차원값의 값의 제일 처음값에만 순서가있는 값을 넣기
		값의 맨앞에 1), 2), 3)과같은 순서의 값을 넣고 싶을때

		:param input_list_2d: 2차원 형태의 리스트
		:param start_no:
		:param special_char:
		:return:
		"""
		for x in range(len(input_list_2d)):
			if not start_no == "":
				add_value = str(start_no + x) + special_char
			else:
				add_value = special_char
			input_list_2d[x][0] = add_value + input_list_2d[x][0]
		return input_list_2d

	def insert_value_in_list_1d_by_step(self, input_list, insert_value, step):
		"""
		기존자료에 n번째마다 자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3, 각 3번째 마다 자료를 추가한다면
		"""
		var_1, var_2 = divmod(len(input_list), int(step))
		for num in range(var_1, 0, -1):
			input_list.insert(num * int(step) - var_2 + 1, insert_value)
		return input_list

	def is_file_in_folder(self, path, file_name):
		"""
		입력폴더안의 화일인가?

		:param path: path
		:param file_name: file_name
		:return:
		"""
		result = ""
		if path == "":
			path = "C:/Users/Administrator/Documents"
		file_name_all = self.get_all_file_name_in_folder(path)
		if file_name in file_name_all:
			result = True
		return result

	def is_number(self, input_data):
		"""
		들어온 자료가 맞는지 확인하는것

		:param input_data:
		:return:
		"""
		temp = self.is_number_only(input_data)
		if temp:
			result = True
		else:
			result = False
		return result

	def is_number_only(self, input_text):
		"""
		소슷점까지는 포함한것이다

		:param input_text:
		:return:
		"""
		result = False
		temp = re.match("^[0-9.]+$", input_text)
		if temp: result = True

		return result

	def lock_sheet_with_password(self, sheet_name):
		source_letter = "1234567890"
		repeat_no = 4
		count = 0
		for a in itertools.product(source_letter, repeat=repeat_no):
			# print(a)
			count += 1
			# print(count)
			temp_pwd = ("".os.path.join(map(str, a)))
			try:
				self.set_sheet_unlock(sheet_name, temp_pwd)
			# print("확인함 == >", a)
			except:
				pass
			else:
				# print("password is == >", temp_pwd)
				break

	def make_2_digit(self, input_data):
		input_data = str(input_data)
		if len(input_data) == 1:
			result = "0" + input_data
		else:
			result = input_data
		return result

	def make_3_menu_for_folder_ver2(self, input_folder):
		"""
		어떤 폴더안의 화일이름을 3단계의 메뉴로 만들어주는 코드
		"""
		all_file_names = self.get_all_file_name_in_folder(input_folder)
		result = {}

		for one_file_name in all_file_names:
			splited_file_name = str(one_file_name).split("_")
			count_x = len(splited_file_name)
			temp = []
			len_x = 0
			if count_x == 1:
				len_x = len(splited_file_name[0])
				temp.append(splited_file_name[0])
				temp.append("")
				temp.append("")
			elif count_x == 2:
				len_x = len(splited_file_name[0]) + len(splited_file_name[1])
				temp.append(splited_file_name[0])
				temp.append(splited_file_name[1])
				temp.append("")
			elif count_x > 2:
				len_x = len(splited_file_name[0]) + len(splited_file_name[1])
				temp.append(splited_file_name[0])
				temp.append(splited_file_name[1])
				temp.append(one_file_name[len_x + 2:])

			for index, one in enumerate(temp):
				if not temp[0] in list(result.keys()):
					result[temp[0]] = {}

				if not temp[1] in list(result[temp[0]].keys()):
					result[temp[0]][temp[1]] = {}

				if not temp[2] in list(result[temp[0]][temp[1]].keys()):
					result[temp[0]][temp[1]][temp[2]] = ""
		return result

	def make_category_data(self, input_list_2d, list_no):
		# 2차원자료의 리스트에서 y줄번호를 입력하면, 그줄의 고유한 값들만 돌려주는것
		# 제목이나 카테고리를 만들려고 한다
		result = []
		for no in list_no:
			temp = set([])
			for list_1d in input_list_2d:
				if list_1d[no]:
					temp.add(list_1d[no])
			result.append(list(temp))
		return result

	def make_char_set(self, upper_eng="", lower_eng="", number="", special="", others=""):
		"""
		어떤 문자의 조합까지 넣을것인지 확인하는 것

		:param upper_eng:
		:param lower_eng:
		:param number:
		:param special:
		:param others:
		:return:
		"""
		check_char = []
		if upper_eng:    check_char.extend(list(string.ascii_uppercase))
		if lower_eng: check_char.extend(list(string.ascii_lowercase))
		if number: check_char.extend(list(string.digits))
		if special: check_char.extend("!@#$%^*_-")
		if others: check_char.extend(others)
		return check_char

	def make_dic_for_two_list(self, key_list, value_list):
		"""
		두개의 리스트를 받으면 사전으로 만들어 주는 코드

		:param key_list:
		:param value_list:
		:return:
		"""
		result = dict(zip(key_list, value_list))
		return result

	def make_dic_with_count(self, input_text):
		"""
		갯수만큼의 문자열을 사전으로 만드는 것

		:param input_text:
		:return:
		"""
		input_text = input_text.replace(" ", "")
		input_text = input_text.upper()
		result = {}
		for one_letter in input_text:
			if one_letter in list(result.keys()):
				result[one_letter] = result[one_letter] + 1
			else:
				result[one_letter] = 1
		return result

	def make_file_with_text(self, file_full_name, source_data):
		"""
		텍스트자료를 화일로 저장하는것
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one in source_data:
			new_file.write(one)

	def make_folder(self, input_folder_name):
		"""
		폴더 만들기

		:param input_folder_name:
		:return:
		"""
		try:
			os.mkdir(input_folder_name)
		except:
			pass

	def make_hangul_char(self, input_list):
		# 유니코드 한글 시작점
		base_code = 0xAC00
		# 초성, 중성, 종성 리스트
		choseong_list = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 19 글자
		jungseong_list = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]  # 21 글자
		jongseong_list = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 28 글자, 없는것 포함

		# 초성, 중성, 종성의 인덱스 찾기
		choseong_index = choseong_list.index(input_list[0])
		jungseong_index = jungseong_list.index(input_list[1])
		jongseong_index = jongseong_list.index(input_list[2])
		# 유니코드 계산
		hangul_code = base_code + (choseong_index * 21 * 28) + (jungseong_index * 28) + jongseong_index
		# 유니코드 문자로 변환
		hangul_char =chr(hangul_code)
		return hangul_char

	def make_html_as_table_for_list_2d(self, style, title_list, data_list_2d):
		"""
		2차원 자료를 html형식의 table로 마드는 것
		:param style:
		:param title_list:
		:param data_list_2d:
		:return:
		"""

		table_style_id = ""
		if style != "":
			table_style_id = " id=" + '""+style+'""
		table_html = "<table" + table_style_id + ">Wn"

		for one in title_list:
			table_html = table_html + f"<th> (one)</th>"
		for list_1d in data_list_2d:
			table_html = table_html + "<tr>"
			for value in list_1d:
				if value == None:
					value = ""
				if isinstance(value, pywintypes.TimeType):
					value = str(value)[:10]
				table_html = table_html + f"<td>(value)</td>"
			table_html = table_html + "</tr>"
		table_html = table_html + "</table>"
		return table_html

	def make_html_inline_text(self, input_text, bold, size, color):
		"""
		입력문자에 진하게, 색상, 크기를 html으로 적용하기 위하여 만든 것

		:param input_text:
		:param bold:
		:param size:
		:param color:
		:return:
		"""
		text_style: str = '<p style= "'
		aaa = ""
		if bold:
			if text_style != '<p style= "': aaa = ';'
			text_style = text_style + aaa + "font-weight: bold"
		if size:
			if text_style != '<p style= "': aaa = ';'
			text_style = text_style + aaa + "font-size: " + str(size) + "px"
		if color:
			if text_style != '<p style= "': aaa = ';'
			text_style = text_style + aaa + "color: " + str(color)
		text_style = text_style + '">' + input_text + "</p>"
		result = text_style
		return result

	def make_html_table(self, table_title_list, table_value_list):
		"""
		html용으로 사용되는 table을 만드는 것

		:param table_title_list:
		:param table_value_list:
		:return:
		"""
		body_top = """
			수고합니다<br>
			<br>
			구매 요청건에 대하여 아래와 같이 TBE요청합니다"<br>
			<br>
		"""

		body_tail = """
			<br>
			-----------------------------------------------------------------------------------<br>
			롯데정밀화학 / 구매2팀 / 박상진 수석<br>
			06181 서울 강남구 테헤란로 534 글라스타워 27층<br>
			SangJin Park / Procurement 2 Team / Senior Manager<br>
			LOTTE Fine Chemical Co., LTD<br>
			27F, Glasstower Bldg., / 534, Teheran-ro, Gangnam-gu, Seoul, 06181, Korea<br>
			Tel	 : 82-2-6974-4539			   C.P	: 010-3334-0053<br>
			e-mail : sjp@lotte.net<br>
			<br>
		"""

		table_style = """
			<html>
			<style>
			body {
				  font-family:'Malgun Gothic';
				  font-size:10pt;
				}
			table {
				width: 70%;
				padding: 11px;
				font-family:'Malgun Gothic';
				font-size:10pt;
			  }
			  tr, td {
				border-bottom: 1px solid #444444;
				padding: 3px;
				text-align: center;
			  }
			  tr, th {
				padding: 13px;
				background-color: #bbdefb;
			  }
			  td {
				background-color: #e3f2fd;
			  }
				</style>
				<body>"""

		temp = table_style + body_top + "<table>"

		temp = temp + "<tr>"
		for x in range(len(table_title_list)):
			temp = temp + "<th>" + str(table_title_list[x]) + "</th>"
		temp = temp + "</tr>"

		for x in range(len(table_value_list)):
			temp = temp + "<tr>"
			for y in range(len(table_value_list[0])):
				temp = temp + "<td>" + str(table_value_list[x][y]) + "<br></td>"
			temp = temp + "</tr>"
		temp = temp + "</table>" + body_tail + "</body></html>"
		return temp

	def make_menu_set_for_object(self, input_object,
									  except_startwith=["__", "xlapp", "xlbook", "check_", "type_", "data_"]):
		"""
		총 3가지의 결과값을 돌려준다
		1. dic["각메소드이름"] = {'1st':"", '2nd':"", '3rd':"", "method_name", "params":, "doc":"~~~" }
		어떤 객체가 오면 메소드를 3단계의 메뉴로 만들어주는 코드
		메소드이름을 나누는 기준은 _를 기준으로 한다
		만약 3단계 이하의 분리가 되면 나머지는 공백으로 만든다

		메뉴에서 1번째것을 누르면, 나머지것이 나오도록 만들기 위해 teee형식으로 만든 것이다
		"""

		menu = {}
		tree_menu = {}
		all_method_name_list = {}

		# 입력 객체에 대해서 메소드이름과 인수를 사전형으로 만드는 것
		# {"메소드이름":{"변수1":"기본값1", "변수2":"기본값2".....}......}
		self.object_dic = self.get_all_method_name_with_argument_for_object(input_object)

		# 메소드의 이름을 하나씩 넣은후에, _를 기준으로 3단계로 만드는 것
		for one_method_name in self.object_dic.keys():
			if self.check_start_with_list(one_method_name, except_startwith):

				splited_method_name = str(one_method_name).split("_")

				temp = {'1st': "", '2nd': "", '3rd': "", }
				temp['method_name'] = one_method_name
				temp['params'] = self.object_dic[one_method_name]
				temp['doc'] = self.get_doc_for_method_name_with_object(input_object, one_method_name)

				temp['1st'] = splited_method_name[0]

				if len(splited_method_name) == 2:
					temp['2nd'] = splited_method_name[1]
					temp['3rd'] = ""
				elif len(splited_method_name) > 2:
					temp['2nd'] = splited_method_name[1]
					temp['3rd'] = one_method_name[len(splited_method_name[0]) + len(splited_method_name[1]) + 2:]
				menu[one_method_name] = temp

				# tree형식으로 메뉴를 만들기 위한것
				if not temp["1st"] in tree_menu.keys():
					tree_menu[temp["1st"]] = {}

				if not temp["2nd"] in tree_menu[temp["1st"]].keys():
					tree_menu[temp["1st"]][temp["2nd"]] = {}

				if not temp["3rd"] in tree_menu[temp["1st"]][temp["2nd"]].keys():
					tree_menu[temp["1st"]][temp["2nd"]][temp["3rd"]] = ""

				all_method_name_list[temp["1st"] + temp["2nd"] + temp["3rd"]] = one_method_name
		# 제목을 기준으로 찾을수있도록 만든것
		return [menu, tree_menu, all_method_name_list]
	def make_list_for_same_repeat_no(self, input_data, line_no):
		"""
		넘어온 자료중 line_no번째의 연속된 자료가 같은 갯수를 세어서 리스트형태로 돌려주는것

		:param input_data:
		:param line_no:
		:return:
		"""
		result = []
		num = 1
		for no in range(len(input_data) - 1):
			if input_data[no][line_no] == input_data[no + 1][line_no]:
				# 위와 아래의 Item이 같은것일때
				num = num + 1
			else:
				result.append(num)
				num = 1
		# print(result)
		return result

	def make_list_on_re_compile(self, re_txt, file_name):
		"""
		텍스트화일을 읽어서 re에 맞도록 한것을 리스트로 만드는 것이다
		함수인 def를 기준으로 저장을 하며, [[공백을없앤자료, 원래자료, 시작줄번호].....]

		:param re_txt:
		:param file_name:
		:return:
		"""
		re_com = re.compile(re_txt)
		f = open(file_name, 'r', encoding='UTF8')
		lines = f.readlines()
		num = 0
		temp = ""
		temp_original = ""
		result = []
		for one_line in lines:
			aaa = re.findall(re_com, str(one_line))
			original_line = one_line
			changed_line = one_line.replace(" ", "")
			changed_line = changed_line.replace("\n", "")

			if aaa:
				result.append([temp, temp_original, num])
				temp = changed_line
				temp_original = original_line
			# print("발견", num)
			else:
				temp = temp + changed_line
				temp_original = temp_original + one_line
		return result

	def make_list_unique(self, input_data):
		"""
		리스트의 값중 고유한것만 골라내기
		"""
		temp = set()
		for one in input_data:
			temp.add(one)
		result = list(temp)
		return result

	def make_menu_for_folder_ver1(self, input_folder):
		"""
		어떤 폴더안의 화일이름을 2단계의 메뉴로 만들어주는 코드
		"""

		all_file_names = self.get_all_file_name_in_folder(input_folder)
		result = {}

		for one_file_name in all_file_names:
			splited_file_name = str(one_file_name).split("_")
			if splited_file_name[0] in result.keys():
				result[splited_file_name[0]].append(one_file_name)
			else:
				result[splited_file_name[0]] = [one_file_name]
		return result

	def make_multi_line_text_for_list_1d(self, input_l1d):
		"""
		1 차원리스트의 자료를 줄바꿈기호를 넣어서 여러줄로 되는 텍스트로 바꿔주는 것

		:param input_l1d:
		:return:
		"""
		result =  ""
		for one in input_l1d:
			result = result + str(one).strip() +chr(13)
		return result

	def make_multi_line_text_for_one_text_by_chars(self, input_text, input_chars=", "):
		"""
		한줄의 텍스트를 원하는 문자를 기준으로 나누어서, 여러줄의 텍스트로 만들어 주는것

		:param input_text:
		:param input_chars:
		:return:
		"""
		input_l1d = input_text.split(input_chars)
		result =""
		for one in input_l1d:
			result = result + str(one).strip() +chr(13)
		return result

	def make_one_text_with_special_char_for_list_1d(self, input_l1d, input_char=", "):
		"""
		1 차원리스트의 모든 자료를 원하는 글자를 붙여서 1개의 텍스트로 만들어 주는것
		각요소들의 앞뒤공백을 없애준다

		:param input_l1d:
		:param input_char:
		:return:
		"""
		result  = ""
		for one in input_l1d:
			result =result + str(one).strip() +input_char
		return result

	def make_random_list(self, input_list, input_limit, input_times=1):
		"""
		입력된 자료를 랜덤으로 리스트를 만드는 것

		:param input_list:
		:param input_limit:
		:param input_times:
		:return:
		"""
		result_set = []
		# if len(input_list) == 2:
		#	input_list = list(range(input_list[0], input_list[1]))
		for no in range(input_times):
			result = []
			for num in range(input_limit):
				dd = random.choice(input_list)
				result.append(dd)
				input_list.remove(dd)
			result_set.append(result)
		return result_set

	def make_serial_no(self, start_no=1, style="####"):
		"""
		1000으로 시작되는 연속된 번호를 만드는 것이다

		:param start_no:
		:param style:
		:return:
		"""
		length = len(style)
		value = 10 ** (length - 1) + start_no
		return value

	def make_several_unit_number(self, input_price):
		"""
		백만원단위, 전만원단위, 억단위로 구분

		:param input_price:
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result

	def make_table_sample_for_int_01(self, xlen, ylen, xtitle, ytitle, data_style=100):
		"""
		샘플을 만들어주는 것
		숫자가 들어간 2차원테이블형식의 자료를 만들어 주는 것

		:param xlen:
		:param ylen:
		:param xtitle:
		:param ytitle:
		:param data_style:
		:return:
		"""
		xtitle_list = self.make_title_with_num(xtitle, "_", xlen)
		xtitle_list.insert(0, "")
		ytitle_list = self.make_title_with_num(ytitle, "_", ylen + 1)
		result = []
		result.append(xtitle_list)
		for ix, one in enumerate(range(xlen)):
			temp = [ytitle_list[ix]]
			for two in range(ylen):
				temp.append(int(random.random() * data_style))
			result.append(temp)
		return result

	def make_team_with_condition(self, all_data, not_same_group, level, step):
		"""
		무엇인가를 하다보면, 조편성을 해야하는경우가 있는데, 이때, 여러 조건들을 만족해야만 하는
		가 생긴다
		즉, 팀장들은 분리를 해야한다던지
		부장과 과장은 같이 안들어가게 해야 한다던지
		이렇게 조건에 맞는 조를 편성하는것을 한번 만들어 보았다

		:param all_data:
		:param not_same_group:
		:param level:
		:param step:
		:return:
		"""
		# 해당하지 않는것을 제일 마지막의 자료에 넣는다
		# 전체자료중에서, leve로 묶여진것을
		changed_level = self.change_re_group_by_step(all_data, level, step)
		# print(changed_level)
		# 그룹no만큼 그룹을 만든다
		result = {}
		for no in range(step):
			result[no] = []
		# 몇번을 반복해서 계산할것인지를 나타낸다
		repeat_no, namuji = divmod(len(all_data), step)
		if namuji != 0: repeat_no = repeat_no + 1
		# 서로있으면 않되는 모든 2가지의 경우의 수를 만들어서 확인하는데 사용한다
		combi = []
		for one_group in not_same_group:
			aaa = list(itertools.permutations(one_group, 2))
			combi.extend(aaa)
			n = 0
			for list_1d in changed_level:
				randomed_list_1d = self.make_random_list(list_1d, len(list_1d))[0]
				finished = ""
				for one_value in randomed_list_1d:
					temp = []
					finished = ""
					for num in range(step):
						if finished == "ok":
							pass
						else:
							min_group_no = self.check_min_result(result, temp)
							error_found = False
							for one_item in combi:
								if (one_item[0] in result[min_group_no] or one_item[1] in result[min_group_no]) and (
										one_item[0] == one_value or one_item[1] == one_value):
									error_found = True
							if error_found:
								temp.append(min_group_no)
							else:
								result[min_group_no].append(one_value)
								finished = "ok"
		return result

	def make_text_basic(self, input_value, total_len):
		"""
		f-string처럼 문자를 변경하는것

		:param input_value:
		:param total_len:
		:return:
		"""
		result = ""
		if type(input_value) == type(123.45):
			result = self.make_text_for_float(input_value, total_len, 2, " ", "right", True)
		elif type(input_value) == type(123):
			result = self.make_text_for_integer(input_value, total_len, " ", "right", True)
		elif type(input_value) == type("123.45"):
			result = self.make_text_for_string(input_value, total_len, " ", "right")
		return result

	def make_text_file_for_text(self, file_full_name, input_text):
		"""
		텍스트자료를 화일로 저장하는것

		:param file_full_name:
		:param input_text:
		:return:
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one_line in input_text:
			new_file.write(one_line)

	def make_text_for_float(self, input_value, big_digit, small_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 실수를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param small_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""
		if comma1000:
			changed_value = f"{round(float(input_value), small_digit):,}"
		else:
			changed_value = str(round(float(input_value), small_digit))

		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def make_text_for_integer(self, input_value, big_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 숫자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""

		if comma1000:
			changed_value = f"{input_value:,}"
		else:
			changed_value = str(input_value)

		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def make_text_for_list_1d(self, input_list_2d, input_len):
		"""
		1차원리스트의 자료들을 정렬해서 텍스트로 만드는 것

		:param input_list_2d:
		:param input_len:
		:return:
		"""
		result_text = ""
		result = []
		len_list = {}
		for index, one in enumerate(input_list_2d[0]):
			len_list[index] = 0

		for list_1d in input_list_2d:
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		print(len_list)

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				temp = temp + self.make_text_basic(one, len_list[index] + input_len)

			result_text = result_text + temp + '\n'
		return result_text

	def make_text_for_string(self, input_value, big_digit, fill_empty=" ", align="right"):
		"""
		f-string처럼 문자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:return:
		"""
		changed_value = str(input_value)
		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def make_title_with_num(self, title="제목 ", connect_char="_", xlen=6):
		"""
		예제를 만들때, 제목 부분을 쉽게 만드릭 위해서 만든 것입니다

		:param title:
		:param connect_char:
		:param xlen:
		:return:
		"""
		result = []

		if title:
			title = "제목"
		for num in range(1, xlen + 1):
			result.append(title + connect_char + str(num))
		return result

	def make_two_digit(self, input_data):
		input_data = str(input_data)
		if len(input_data) == 1:
			result = "0" + input_data
		else:
			result = input_data
		return result

	def make_zip_file(self, zip_name_path, new_path_all):
		"""
		화일들을 zip으로 압축하는것
		"""
		with zipfile.ZipFile(zip_name_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
			for one in new_path_all:
				new_zip.write(one)
		new_zip.close()

	def manual(self):
		"""
		이화일의 설명

		:return:
		"""
		result = """
			여기저기 사용이 가능한것을 하나로 모아놓은 것이다
		"""
		return result

	def messagebox_for_show(self, input_text="입력필요", input_title="xython.co.kr"):
		"""
		사용하기 편하게 이름을 바꿈
		original : write_value_in_messagebox
		"""
		self.messagebox_for_show(input_text, input_title)

	def minus_two_list_1d(self, list_1d_a, list_1d_b):
		"""
		두개 리스트중에서，앞과 동일한것만 삭제하기 위한 것
		앞의 리스트에서 뒤에 갈은것만 삭제하는것
		예 : [1,2,3,4,5] - [3,4,5,6,7] ==> [1,2]
		"""
		result = [x for x in list_1d_a if x not in list_1d_b]
		return result

	def mix_two_dic_data(self, dic_1, dic_2):
		"""
		자료를 합쳐주는 기능
		입력한 자료의 테이블제목이 a, d, e라고 하고 다른 테이블의 자료가 a, b라고 할때
		1. 두개 화일의 제목을 먼저 하나로 만든다
		2. 각 테이블의 자료를 사전형식으로 바꾼다
		3. 하나씩 돌아가면서, 자료를 정렬한다

		:param dic_1:
		:param dic_2:
		:return:
		"""
		result =  []
		title_list = list(dic_1.keys())
		title_list_2 = list(dic_2.keys())
		for one in title_list_2:
			if not one in title_list:
				title_list.append(one)
		result.append(title_list)

		for index in range(len(dic_1[title_list[0]])):
			temp =  []
			for one_title in title_list:
				if one_title in dic_1.keys():
					temp.append(dic_1[one_title][index])
				else:
					temp.append(None)
				result.append(temp)

		for index in range(len(dic_2[title_list_2[0]])):
			temp =  []
		for one_title in title_list:
			if one_title in dic_2.keys():
				temp.append(dic_2[one_title][index])
			else:
				temp.append(None)
			result.append(temp)
		return result

	def mix_two_list_2d(self, input_list_1, input_list_2):
		"""
		두개의 리스트를 서로 묶어서, 새로운 리스트를 만드는 것
		[1,2,3], ["a","b","c"] ==> [[1, "a"],[2,"b"],[3,"c"]]

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result = []
		for x, y in zip(input_list_1, input_list_2):
			result.append(x + y)
		return result

	def mix_two_list_2d_by_title_name(self, input_base_list_2d, input_sub_list_2d):
		"""
		2차원의 자료에 다른 2차원의 자료를 제목을 기준으로 붙이기
		새로운것을 붙일때는 기존의 값은 빈것을 넣는다
		yx의 순서로 자료가 입력되어야 함

		:param input_base_list_2d:
		:param input_sub_list_2d:
		:return:
		"""

		blank_list = []
		for one in range(1, len(input_base_list_2d[0])):
			blank_list.append("")

		blank_list2 = []
		for one in range(1, len(input_sub_list_2d[0])):
			blank_list2.append("")

		total_len = len(input_base_list_2d[0]) + len(input_sub_list_2d[0]) - 1

		for no1, value1 in enumerate(input_sub_list_2d):
			found = False
			if value1 == None: value1 = ""

			for no2, value2 in enumerate(input_base_list_2d):
				if value2 == None: value2 = ""
				if value1[0] == value2[0]:
					input_base_list_2d[no2].extend(value1[1:])
					found = True

			if not found:
				input_base_list_2d.append(blank_list.extend(value1[1:]))

		for no, list_1d in enumerate(input_base_list_2d):
			if len(list_1d) < total_len:
				input_base_list_2d[no].extend(blank_list2)
		return input_base_list_2d

	def mix_two_list_as_beside(self, input_list_2d_1, input_list_2d_2):
		"""
		맨앞의 자료가 같다는 가정에서 하는것
		제목부분은 고유한 자료여야 한다
		자료가 없거나 값이 없을때 붙이는 빈자료를 위해 만든것

		:param input_list_2d_1:
		:param input_list_2d_2:
		:return:
		"""
		no_of_list_2d_1 = len(input_list_2d_1[0]) - 1
		no_of_list_2d_2 = len(input_list_2d_2[0]) - 1
		empty_list_2d_1 = [""] * no_of_list_2d_1
		empty_list_2d_2 = [""] * no_of_list_2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list_2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list_2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list_2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list_2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def moum_xy_list(self, size=[1, 2], input_text="ㅏ"):
		"""
		모음을 엑셀에 나타내기 위한 좌표를 주는 것이다

		:param size:
		:param input_text:
		:return:
		"""
		x, y = size
		# x, y는 글자의 크기
		mo_01 = [["ㅏ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_02 = [["ㅑ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y],
				 [0.6 * x, 0.6 * y, 0.6 * x, 0.8 * y]]
		mo_03 = [["ㅓ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_04 = [["ㅕ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]
		mo_10 = [["ㅣ"], [1, 0.6 * y, x, 0.6 * y]]
		mo_05 = [["ㅗ"], [x, 1, x, y],
				 [x, 0.5 * y, 0.8 * x, 0.5 * y]]
		mo_06 = [["ㅛ"], [x, 1, x, y],
				 [x, 0.3 * y, 0.8 * x, 0.3 * y],
				 [x, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_07 = [["ㅜ"], [1, 1, 1, y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y]]
		mo_08 = [["ㅠ"], [1, 1, 1, y],
				 [1, 0.3 * y, 0.8 * x, 0.3 * y],
				 [1, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_09 = [["ㅡ"], [0.5 * x, 1, 0.5 * x, y]]

		mo_21 = [["ㅐ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_22 = [["ㅒ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.8 * y, 0.6 * x, 0.8 * y]]
		mo_23 = [["ㅔ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_24 = [["ㅖ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]

		jamo2_dic = {
			"ㅏ": mo_01, "ㅑ": mo_02, "ㅓ": mo_03, "ㅕ": mo_04, "ㅗ": mo_05,
			"ㅛ": mo_06, "ㅜ": mo_07, "ㅠ": mo_08, "ㅡ": mo_09, "ㅣ": mo_10,
			"ㅐ": mo_21, "ㅒ": mo_22, "ㅔ": mo_23, "ㅖ": mo_24,
		}
		result = jamo2_dic[input_text]
		return result

	def move_cell_in_front_by_startwith_aaa(self, startwith="*"):
		"""
		맨앞에 특정글자가 있으면, 앞으로 옮기기

		:param startwith:
		:return:
		"""
		x, y, x2, y2 = self.read_address_for_selection()
		self.insert_yline("", y)
		for one_x in range(x, x2):
			one_value = self.read_value_in_cell("", [one_x, y + 1])
			if one_value.startswith(startwith):
				self.write_value_in_cell("", [one_x, y], one_value)
				self.write_value_in_cell("", [one_x, y + 1], None)

	def move_data_to_right_by_step(self, input_list_1d, step_no):
		"""
		1차원으로 들어온 자료를 갯수에 맞도록  분리해서 2차원의 자료로 만들어 주는것

		:param input_list_1d:
		:param step_no:
		:return:
		"""
		result = []
		for partial_list in input_list_1d[::step_no]:
			result.append(partial_list)
		return result

	def move_degree_distance(self, degree="입력필요", distance="입력필요"):
		"""
		move_degree_distance( degree="입력필요", distance="입력필요")
		현재 위치 x,y에서 30도로 20만큼 떨어진 거리의 위치를 돌려주는 것
		메뉴에서 제외

		:param degree:
		:param distance:
		:return:
		"""
		degree = degree * 3.141592 / 180
		y = distance * math.cos(degree)
		x = distance * math.sin(degree)
		return [x, y]

	def move_file(self, old_file, new_file):
		"""
		화일을 이동시키는것
		"""
		old_file = self.check_file(old_file)
		shutil.move(old_file, new_file)

	def move_folder(self, old_dir, new_dir):
		"""
		폴더를 이동시키는것
		"""
		shutil.move(old_dir, new_dir)

	def move_list_2d_by_index(self, input_list_2d, input_no_list):
		"""
		입력형태 : 2차원리스트, [[옮길것, 옮기고싶은자리].....]

		:param input_list_2d:
		:param input_no_list:
		:return:
		"""
		ori_no_dic = {}
		for one in range(len(input_list_2d[0])):
			ori_no_dic[one] = one
		for before, after in input_no_list:
			new_before = ori_no_dic[before]
			new_after = ori_no_dic[after]

			for no in range(len(input_list_2d)):
				if new_before < new_after:
					new_after = after - 1
				value = input_list_2d[no][new_before]
				del input_list_2d[no][new_before]
				input_list_2d[no].insert(int(new_after), value)
		return input_list_2d

	def mqtt_connect(self, client, userdata, flags, rc):
		"""
		"""
		if rc == 0:
			print("connected OK")
		else:
			print("Bad connection Returned code=", rc)

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

	def open_pdf_file(self, file_name):
		import os
		os.startfile(file_name)

	def overtime(self):
		# [시작시간, 끝시간, 일당몇배]
		self.ot["common"] = [["0000", "0500", 1], ["0505", "0606", 1.2]]
		self.ot["company"] = ["0708"]

	def paste_with_condition(self, range_obj, value=False, memo=False, line=False, width=False, formular=False,
							 format=False, numberformat=False, condition_format=False):
		if value: range_obj.PasteSpecial(-4163)
		if line: range_obj.PasteSpecial(7)
		if width: range_obj.PasteSpecial(8)
		if formular: range_obj.PasteSpecial(-4123)
		if format: range_obj.PasteSpecial(-4122)
		if numberformat: range_obj.PasteSpecial(12)
		if condition_format: range_obj.PasteSpecial(14)
		if memo: range_obj.PasteSpecial(-4144)
	def paste_from_clipboard(self, ):
		result = pyperclip.paste()
		return result

	def plus_two_list(self, input_list_1, input_list_2):
		"""
		두개의 리스트를 각 우치에따라서 더하기

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result = []
		for x, y in zip(input_list_1, input_list_2):
			result.append(x + y)
		return result

	def plus_two_list_with_samelen(self, input_list_2d_1, input_list_2d_2):
		"""
		선택한 영역이 2개를 서로 같은것을 기준으로 묶을려고하는것이다
		제일앞의 한즐이 같은것이다
		만약 묶을려고 할때 자료가 없을때는 그 기준자료만큼 빈자료를 넣어서 다음자료를 추가하는 것이다

		:param input_list_2d_1:
		:param input_list_2d_2:
		:return:
		"""
		no_of_list_2d_1 = len(input_list_2d_1[0]) - 1
		no_of_list_2d_2 = len(input_list_2d_2[1]) - 1
		empty_list_2d_1 = [""] * no_of_list_2d_1
		empty_list_2d_2 = [""] * no_of_list_2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list_2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list_2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list_2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list_2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def pre_treatment(self, input_list_2d):
		"""
		자료의 전처리
		자료들중에 변경을 할 자료들을 처리한다

		:param input_list_2d:
		:return:
		"""
		unique_data = collections.Counter()
		for data_1d in input_list_2d:
			value = str(data_1d[0])
			for new_word in [["(주)", ""], ["주식회사", ""], ["(유)", ""], ["유한회사", " "]]:
				value = value.replace(new_word[0], new_word[1])
				value = value.lower()
			unique_data.update([value])
			result = list(unique_data.keys())
		return result

	def print_dic_one_by_one(self, dct):
		# 사전형식의 자료를 하나씩 한줄로 사전형식으로 나타나도록 하는것
		for key, value in dct.items():
			if type(key) == type("string"): key = "'" + key + "'"
			if type(value) == type("string"): value = "'" + value + "'"

	def print_list_one_by_one(self, list_2d):
		# 2차원자료를 한줄씩 나타나도록 하는것
		if type(list_2d[0]) == type([]):
			print("[")
			for index, one in enumerate(list_2d):
				print("{}".format(one))
			print("]")

	def print_one_by_one(self, input_list):
		"""
		리스트를 하나씩 출력하는것

		:param input_list:
		:return:
		"""
		for one in input_list:
			print(one)

	def read_pickle(self, path_n_name=""):
		"""
		"""
		with open(path_n_name, "rb") as fr:
			result = pickle.load(fr)
		return result

	def read_text_file(self, file_path):
		"""
			텍스트화일을 읽어서, 넘겨주는것

		:param file_path:
		:return:
		"""
		file = open(file_path, "r")
		result = file.readlines()
		return result

	def read_text_file_as_list(self, i_path):
		"""
		어떤 텍스트라도 읽어오기
		text 자료를 읽어오기
		어떤 텍스트형태라도 읽어오기
		default = ANSI
		osv 는 utf-8 로만하면 에러가 나기도 함, uTF-8-sig
		UTF-16

		:param i_path:
		:return:
		"""
		result = []
		encoding_set = ["utf-8", "ansi", "UTE-8-sig", "utf-16", ]
		for a_coding in encoding_set:
			try:
				f = open(i_path, 'r', encoding=a_coding)
				while True:
					line = f.readline()
					if not line: break
					result.append(line)
				f.olose()
				if result != []:
					print(a_coding, result)
					return result
			except:
				pass

	def read_value_for_file_name(self, file_name):
		"""
		화일을 읽어오는 것

		:param file_name:
		:return:
		"""
		try:
			f = open(file_name, 'r', encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(file_name, 'r')
			result = f.readlines()
			f.close()
		return result

	def rename_file_name(self, old_path, new_path):
		# 화일이름 변경
		old_path = self.check_file(old_path)
		new_path = self.check_file(new_path)
		os.rename(old_path, new_path)

	def rename_folder(self, old_path, new_path):
		# 폴더이름 변경
		os.rename(old_path, new_path)

	def replace_list_1d_element_as_space_by_step(self, input_list, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 ""으로 만드는것
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []

		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = ""
			result.append(temp_value)

		return result

	def replace_text_between_a_and_b(self, input_text, start_no, end_no, replace_text):
		"""
		텍스트문장에서 번호를 기준으로 a번호에서 b번호까지의 글자를 바꾸는것으로
		번호를 기준으로 바꾸는 기능을 만든것이다
		보통 어떤 단어나 문장을 바꾸는것은 있어도, 번호를 기준으로 바꾸는것은 없어서, 만든것이며
		정규표현식에서 찾은것이 숫자로 되어있어서 그것을 이용하기 위해 만든 것이다

		:param input_text:
		:param start_no:
		:param end_no:
		:param replace_text:
		:return:
		"""
		front = input_text[:start_no]
		end = input_text[end_no:]
		result = front + replace_text + end
		return result

	def replace_word_in_text(self, input_text, before_text, after_text):
		"""
			폰트와 글자를 주면, 필셀의 크기를 돌려준다
		"""
		result = input_text.replace(before_text, after_text)
		return result

	def resize_list(self, input_list="", xy=""):
		"""
			입력으로 들어온 자료를 2차원으로 만든후
			xy로 넘어온 자료를 기준으로 만드는 것이다
			사이즈의 크기에 따라서 들어온 자료를 만든다
		"""
		result = []
		x_len, y_len = xy
		list1_max_len = len(input_list)
		list2_max_len = 0

		# 최대의 길이를 구한다
		for one_value in input_list:
			if type(one_value) == type([]):
				if list2_max_len < len(one_value):
					list2_max_len = len(one_value)

		for one_value in input_list:
			temp_list = []
			# 모든 항목을 리스트형태로 만든다
			if type(one_value) != type(one_value):
				temp_list = temp_list.append(one_value)
			else:
				temp_list = one_value

			# 최대길이에 맞도록 적은것은 ""으로 갯수를 채운다
			if list2_max_len - len(temp_list) > 0:
				for no in range(list2_max_len - len(temp_list)):
					temp_list.append("")
			result.append(temp_list)

		if xy != "":
			# x갯수를 정리한다
			if x_len < len(result):
				changed_result_2 = result[0:x_len]
			# y갯수를 정리한다
			changed_result_3 = []
			if y_len < len(changed_result_2[0]):
				for one_list in changed_result_2:
					changed_result_3.append(one_list[0:y_len])
			else:
				changed_result_3 = changed_result_2
			result = changed_result_3

		return result

	def resize_list_1d_to_list_2d_by_step(self, all_data, initial_group, step):
		"""
		기존에 그룹화되어있는것을 기준으로, 최대갯수가 step의 갯수만큼 되도록 다시 그룹화 하는것이다

		:param all_data:
		:param initial_group:
		:param step:
		:return:
		"""
		result = []
		for list_1d in initial_group:
			if len(list_1d) > step:
				repeat_no = int((len(list_1d) + step - 1) / step)
				for no in range(repeat_no - 1):
					result.append(list_1d[no * step:(no + 1) * step])
				result.append(list_1d[(repeat_no - 1) * step:])
			else:
				result.append(list_1d)
		remain_all_data = all_data
		for list_1d in initial_group:
			for one_value in list_1d:
				remain_all_data.remove(one_value)
		result.append(remain_all_data)
		return result

	def resize_list_2d(self, input_list_2d, x_start, y_start, x_len, y_len):
		"""
		2차원 리스트의 사이즈를 변경하는 것
		2차원안의 1차원자료를 몇개씩 줄여서 새롭게 2차원자료를 만드는 것이다

		:param input_list_2d:
		:param x_start:
		:param y_start:
		:param x_len:
		:param y_len:
		:return:
		"""
		result = []
		if len(input_list_2d) >= x_start + x_len and len(input_list_2d[0]) >= y_start + y_len:
			changed_list_2d = input_list_2d[x_start:x_start + x_len - 1]
			for list_1d in changed_list_2d:
				result.append(list_1d[y_start:y_start + y_len - 1])
		return result

	def resize_list_2d_by_xy_step(self, xy_list, resize=[1, 1]):
		"""
		리스트의 크기를 다시 설정하는 것
		메뉴에서 제외

		:param xy_list:
		:param resize:
		:return:
		"""
		result = []
		# 자료의 x갯수를 요청한것과 비교
		if len(xy_list) < resize[0] or resize[0] == 0:
			pass
		else:
			xy_list = xy_list[:resize[0]]
		# 자료의 y갯수를 요청한것과 비교
		for x_list in xy_list:
			if len(x_list) < resize[1] or resize[1] == 0:
				pass
			else:
				x_list = xy_list[:resize[0]]
			result.append(x_list)
		return result

	def reverse_alt_enter(self):
		# Alt+Enter로 한셀이 여러 값들이 들어있는 것들을 하나의 셀로 분리를 하는 기능
		a = 111
		return a

	def rotate_xy_by_degree(self, xy, degree):
		"""
		좌표를 각도를 넣어서 회전하는 좌표를 주는 것

		:param xy:
		:param degree:
		:return:
		"""
		rad = degree * (math.pi / 180.0)
		x2 = round(math.cos(rad) * xy[0] - math.sin(rad) * xy[1])
		y2 = round(math.sin(rad) * xy[0] + math.cos(rad) * xy[1])
		return [x2, y2]

	def run_file(self, file_full_path):
		"""
		원하는 화일을 open하는 것

		:param file_name:
		"""
		os.startfile(file_full_path)

	def run_notepad(self):
		"""
		노트패드를 실행시키고
		붙여넣기를 실행시키는 것이다
		노트패드는 com인터페이스가 없다
		"""
		shell = win32com.client.Dispatch("WScript.Shell")
		shell.Run("notepad")
		shell.AppActivate("notepad")
		shell.SendKeys("^v", 0)

	def save_file_as_pickle(self, input_data="", path_n_name=""):
		"""
		피클로 객체를 저장하는것
		"""
		if ":" in path_n_name:
			full_file_name = path_n_name
		else:
			full_file_name = "./" + path_n_name
		with open(str(full_file_name) + ".pickle", "wb") as fr:
			pickle.dump(input_data, fr)

	def save_object_as_pickle_file(self, input_object="", file_name="", path="D:\\"):
		"""
		자료를 pickle 로 저장하는것

		:param input_object:
		:param file_name:
		:param path: 경로
		:return:
		"""
		if not "." in file_name:
			file_name = file_name + ".pickle"
		with open(path + file_name, "wb") as fr:
			pickle.dump(input_object, fr)

	def set_text_format_for_float(self, input_value, big_digit, small_digit, fill_empty=" ", align="right",
								  comma1000=True):
		"""
		f-string처럼 실수를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param small_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""
		if comma1000:
			changed_value = f"{round(float(input_value), small_digit):,}"
		else:
			changed_value = str(round(float(input_value), small_digit))

		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result
	def select_list_1d_unique_y(self, data1, data2):
		"""
		고유한 컬럼만 골라낸다
		"""
		result = []
		columns = self.read_y_names(data1)
		update_data2 = self.change_waste_data(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def set_text_format_for_int(self, input_value, big_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 숫자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""

		if comma1000:
			changed_value = f"{input_value:,}"
		else:
			changed_value = str(input_value)

		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def show_dialog_for_file(self):
		"""
		화일 다이얼로그를 불러오는 것

		"""
		filter = "Picture Files \0*.jp*;*.gif;*.bmp;*.png\0Text files\0*.txt\0"
		# filter = "Picture Files (*.jp*; *.gif; *.bmp; *.png),*.xls"
		result = win32gui.GetOpenfile_nameW(InitialDir=os.environ["temp"],
										   Filter=filter,
										   Flags=win32con.OFN_ALLOWMULTISELECT | win32con.OFN_EXPLORER,
										   File="somefile_name", defExt="py",
										   Title="GetOpenfile_nameW",
										   FilterIndex=0)
		return result

	def show_file_dialog_for_image(self, file_type=""):
		"""

		:return:
		"""
		if file_type == "":
			filter = "Picture Files \*.*"
		else:
			filter = "Picture Files \0*.jp*;*.gif;*.bmp;*.png\0Text files\0*.txt\0"
		# filter = "Picture Files (*.jp*; *.gif; *.bmp; *.png),*.xls"
		result = win32gui.GetOpenfile_nameW(InitialDir=os.environ["temp"],
										   Filter=filter,
										   Flags=win32con.OFN_ALLOWMULTISELECT | win32con.OFN_EXPLORER,
										   File="somefile_name",
										   DefExt="py",
										   Title="GetOpenfile_nameW",
										   FilterIndex=0)

		# print(result)
		return result

	def show_file_dialog_general(self):
		result = win32gui.GetOpenfile_nameW(DefExt="*.*")
		return result

	def show_messagebox_with_timer(self, input_text, second, title="www.xython.co.kr"):
		"""
		몇초후에 팝업창이 자동으로 사라지는것

		:param input_text: 팝업창에 나타나는 문구
		:param second: 팝업창이 존재하는 초
		"""
		shell = win32com.client.Dispatch('WScript.Shell')
		intReturn = shell.Popup(input_text, second, title)

	def similar_test_with_two_words(self, input_list_1d, base_number=0.6):
		"""
		입력된 자료에서 유사도를 검사해서 기본설정값보다 높은 값들의 자료만 갖고옮

		:param input_list_1d:
		:param base_number:
		:return:
		"""
		result = []
		num = 0
		for one in input_list_1d:
			for two in input_list_1d[num:]:
				ratio = difflib.SequenceMatcher(None, one, two).ratio()
				if ratio >= base_number and ratio != 1.0:
					print(one, two, " : 유사도는 = = >", ratio)
					result.append([ratio, one, two, ])
		num = num + 1
		return result

	def sort(self, a, b=0):
		result_before = [(i[b], i) for i in a]
		result_before.sort()
		result = [i[1] for i in result_before]
		return result

	def sort_list_1d(self, input_list_1d):
		"""
		1차원 리스트를 정렬하는 것

		:param input_list_1d:
		:return:
		"""

		str_temp = []
		int_temp = []
		for one in input_list_1d:
			if type(one) == type("str"):
				str_temp.append(one)
			else:
				int_temp.append(one)

		result_int = sorted(int_temp)
		result_str = sorted(str_temp)
		result = result_int + result_str
		return result

	def sort_list_1d_by_element_len(self, input_list):
		"""
		일반적인 정렬이 아니고,	문자의 길이에 따라서 정렬
		:param input_list:
		:return:
		"""
		input_list.sort(key=lambda x: len(str(x)))
		return input_list

	def sort_list_1d_by_index_list(self, source, sort_index):
		"""
		sort_index는 정렬되는 순서
		[1,-2,3] ==> 1,2,3으로 정렬을 하는데, 2번째는 역순으로 정렬한다

		:param source:
		:param sort_index:
		:return:
		"""
		temp = ""
		for one in sort_index:
			if "-" in str(one):
				temp = temp + ("-x[%s], " % (abs(one)))
			else:
				temp = temp + ("x[%s], " % (one))

		lam = ("lambda x : (%s)" % temp[:-2])

		result = sorted(source, key=eval(lam))
		return result

	def sort_list_2d(self, input_list_2d):
		"""
		2차원 리스트를 정렬하는 것

		:param input_list_2d:
		:return:
		"""
		result = self.sort_list_2d_by_index(input_list_2d, 0)
		return result

	def sort_list_2d_by_index(self, input_list, index_no=0):
		"""
		입력 :  리스트자료
		리스트자료를 몇번째 순서를 기준으로 정렬하는것
		aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
		value=sort_list(리스트자료, 정렬기준번호)
		"""
		result_before = [(i[index_no], i) for i in input_list]
		result_before.sort()
		result = [i[1] for i in result_before]
		return result

	def sort_list_2d_by_yy_list(self, input_data, input_list=[0, 2, 3]):
		"""
		2차원리스트를 몇번째를 기준으로 정렬하는것
		음수를 사용하면, 역으로 되는것을 적용시킴
		"""
		text = ""
		for one in input_list:
			if one >= 0:
				text = text + "row[" + str(one * -1) + "],"
			else:
				text = text + "-row[" + str(one * -1) + "],"  # <=이부분을 변경
		text = text[:-1]
		exec("global sorted_list_2d; sorted_list_2d = sorted(input_data, key=lambda row: (%s))" % text)
		global sorted_list_2d
		return sorted_list_2d

	def sort_list_3d_by_index(self, input_list_3d, index_no=0):
		"""
			3차원자료를 정렬하는것

		:param input_list_3d:
		:param index_no:
		:return:
		"""
		result = []
		for input_list_2d in input_list_3d:
			if len(input_list_2d) == 1:
				result.append(input_list_2d)
			else:
				sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
				result.append(sorted_list_2d)
		return result

	def sort_mixed_list_1d(self, input_list_1d):
		"""
		1, 2차원의 자료가 섞여서 저장된 자료를 정렬하는 것

		:param input_list_1d:
		:return:
		"""
		int_list = sorted([i for i in input_list_1d if type(i) is float or type(i) is int])
		str_list = sorted([i for i in input_list_1d if type(i) is str])
		return int_list + str_list

	def sound_beep(self, sec=1000, hz=500):
		"""
		beep 음을 내는 것
		메뉴에서 제외

		:param sec:
		:param hz:
		:return:
		"""
		win32api.Beep(hz, sec)

	def split_all_file_name_in_folder_by_first_underbar(self, input_folder):
		"""
		어떤 폴더안의 화일이름을 2단계의 메뉴로 만들어주는 코드
		화일이름을 기준으로 _로 나누어서 2단계의 메뉴을 만드는데 사용
		aaa_bbb_ccc => ["aaa", "bbb_ccc"]
		"""

		file_names = self.get_all_file_name_in_folder(input_folder)
		result = {}

		for one_file in file_names:
			splited_file_name = str(one_file).split("_")

			if len(splited_file_name) == 1:
				result[splited_file_name[0]] = ""
			else:
				result[one_file] = [splited_file_name[0]], one_file[len(splited_file_name[0]) + 1:]
		return result

	def split_as_number_list(self, input_list_1d, num_list_1d):
		"""
		넘어온 자료를 원하는 숫자만큼씩 자르는것
		입력값 : "ㅁㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㄹ"
		분리기준 = [2,4,5]
		결과값 :["ㅁㄴ", "ㅇㄹㄴㅇ", "ㄹㄴㅇㄹㄴ", "ㅇㄹㄴㄹ"]

		:param input_list_1d:
		:param num_list_1d:
		:return:
		"""
		result = []

		for one_text in input_list_1d:
			temp = []
			text_len = len(one_text)
			remain_text = one_text
			for x in num_list_1d:
				if x <= len(remain_text):
					temp.append(remain_text[0:x])
					remain_text = remain_text[x:]
				elif len(remain_text):
					temp.append(remain_text)
					break
			result.append(temp)
		return result

	def split_code_in_file_name(self, file_name):
		"""
		화일에서 def를 기준으로 분리하는 것
		"""
		# 텍스트 읽어오기
		file_pointer = open(file_name, 'r', encoding='utf-8')
		# 한번에 다 읽기
		result = {}
		file_list = file_pointer.readlines()
		key_value = "__aa__bb__cc__"
		temp = []
		for ori_value in file_list:
			one_value = str(ori_value).replace(" ", "")
			one_value = str(one_value).replace("\t", "")
			if one_value[0:3] == "def":
				# print(key_value)
				result[key_value] = temp
				temp = []
				key_value = "__aa__bb__cc__" + str(ori_value)
			else:
				temp.append(ori_value)
		result[key_value] = temp

		aaa = list(result.keys())
		aaa.sort()

		for one in aaa:
			update_one = one.replace("__aa__bb__cc__", "")
			update_one = update_one.replace("\n", "")
			print(update_one)
			for one_1 in result[one]:
				one_1 = one_1.replace("\n", "")
				print(one_1)

	def split_data_as_number_vs_char(self, raw_data):
		"""
		문자와숫자를 분리해서 리스트로 돌려주는 것이다
		123wer -> ['123','wer']
		:param raw_data:
		:return:
		"""
		temp = ""
		int_temp = ""
		result = []
		datas = str(raw_data)
		for num in range(len(datas)):
			if num == 0:
				temp = str(datas[num])
			else:
				try:
					fore_var = int(datas[num])
					fore_var_status = "integer"
				except:
					fore_var = datas[num]
					fore_var_status = "string"
				try:
					back_var = int(datas[num - 1])
					back_var_status = "integer"
				except:
					back_var = datas[num - 1]
					back_var_status = "string"

				if fore_var_status == back_var_status:
					temp = temp + datas[num]
				else:
					result.append(temp)
					temp = datas[num]
		if len(temp) > 0:
			result.append(temp)
		return result

	def split_data_by_newline_char(self, input_text, number):
		"""
		문자열을 \n, tab으로 구분해서 분리한다

		:param input_text:
		:param number:
		:return:
		"""
		result = []
		temp_list = str(input_text).split("\n")
		for one_value_1 in temp_list:
			temp = []
			tab_list = str(one_value_1).split("\t")
			for one_value_2 in tab_list:
				temp.append(one_value_2)
			result.append(temp)

		return result

	def split_directory(self, input_file=""):
		"""
		입력으로 들어온 화일의 총 이름에서 디렉토리 부분만 추출하는 것
		:param input_file:
		:return:
		"""
		drive, path_and_file = os.path.splitdrive(input_file)
		path, file = os.path.split(input_file)
		result = [path, file]
		return result

	def split_double_moum_to_two_simple_moum(self, double_moum):
		"""
		이중모음을 단모음으로 바꿔주는것

		:param double_moum:
		:return:
		"""
		mo2_dic = {"ㅘ": ["ㅗ", "ㅏ"], "ㅙ": ["ㅗ", "ㅐ"], "ㅚ": ["ㅗ", "ㅣ"], "ㅝ": ["ㅜ", "ㅓ"], "ㅞ": ["ㅜ", "ㅔ"], "ㅟ": ["ㅜ", "ㅣ"],
				   "ㅢ": ["ㅡ", "ㅣ"], }
		result = mo2_dic[double_moum]
		return result

	def split_file_by_method_name_with_delete_empty_line(self, file_name):
		"""
		py화일을 다룰 려고 만든것이며
		화일의 메소드를 기준으로 나누면서 동시에 빈라인은 삭제하는것

		:param file_name:
		:return:
		"""
		main_def_list = []
		result = []
		total_code = ""
		total = ""
		# 화일을 읽어온다
		f = open(file_name, 'r', encoding='UTF8')
		original_lines = f.readlines()
		f.close()
		# print(len(original_lines))
		num = 1
		temp = ""
		exp_start = ""
		exp_end = ""
		exp_mid = ""
		for one_line in original_lines:
			total = total + one_line
			changed_one_line = one_line.strip()
			if changed_one_line == "":
				one_line = ""
			elif changed_one_line[0] == "#":
				one_line = ""
			elif changed_one_line[0:3] == "def":
				main_def_list.append(temp)
				temp = one_line
			elif '"""' in changed_one_line:
				if changed_one_line[0:3] == '"""':
					exp_end = "no"
					exp_start = "yes"
					one_line = ""
				elif changed_one_line[:-3] == '"""':
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_end = "yes"
						exp_start = "no"
						one_line = ""
				else:
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_mid = "yes"

				num = num + 1

			if exp_start == "yes" and exp_end == "no":
				one_line = ""

			temp = temp + one_line
			total_code = total_code + one_line
		# print(num)

		return [main_def_list, total_code, total]

	def split_file_name_as_path_n_file_name(self, file_name=""):
		"""
		화일 이름을 경로와 이름으로 구분하는 것이다
		메뉴에서 제외

		:param file_name:
		:return:
		"""
		path = ""
		changed_file_name = file_name.replace("\\", "/")
		split_list = changed_file_name.split("/")
		file_name_only = split_list[-1]
		if len(changed_file_name) == len(file_name_only):
			path = ""
		else:
			path = changed_file_name[:len(file_name_only)]

		return [path, file_name_only]

	def split_file_path_to_each_parts(self, input_value=""):
		"""
		입력값을 경로와 이름으로 분리

		:param input_value:
		:return:
		"""
		file_name = ""
		path = ""
		input_value = input_value.replace("/", "\\")
		temp_1 = input_value.split("\\")
		if "." in temp_1[-1]:
			file_name = temp_1[-1]
		if len(temp_1) > 1 and "\\" in temp_1[:len(temp_1[-1])]:
			path = input_value[:len(temp_1[-1])]
		result = [file_name, path]
		return result

	def split_list_1d_by_group_no(self, input_list_1d, step_no):
		"""
		12개의 리스트를
		입력 - [ [1,2,3,4,5,6,7,8,9,10,11,12], 4]를 받으면
				총 4개의 묶읆으로 순서를 섞어서 만들어 주는것
			   [[1,5,9],  [2,6,10],  [3,7,11],  [4,8,12]] 로 만들어 주는것

		:param input_list_1d:
		:param step_no:
		:return:
		"""
		count_no = int(len(input_list_1d) / step_no)
		group_no = divmod(len(input_list_1d), int(step_no))[0]
		namuji = len(input_list_1d) - step_no * group_no
		result = []

		for no in range(count_no):
			temp = input_list_1d[no * count_no: no * count_no + count_no]
			result.append(temp)
		if namuji > 0:
			result.append(input_list_1d[-namuji:])
		return result

	def split_list_1d_by_step(self, input_list_1d, step_no):
		"""
		1차원 리스트를 원하는 개수만 큼 자르는 것

		:param input_list_1d:
		:param step_no:
		:return:
		"""
		count_no = int(len(input_list_1d) / step_no)
		# group_no = divmod(len(input_list_1d), int(step_no))[0]
		namuji = len(input_list_1d) - step_no * count_no
		result = []

		for no in range(count_no):
			temp = input_list_1d[no * step_no: no * step_no + step_no]
			result.append(temp)
		if namuji > 0:
			result.append(input_list_1d[-namuji:])
		return result

	def split_list_1d_by_string(self, input_list, input_text):
		"""
		리스트로 들어온 자료들을 한번에 분리해서 2차원리스트로 만드는 것
		"""

		result = []
		for one_value in input_list:
			temp_result = str(one_value).split(input_text)
			result.append(temp_result)
		return result

	def split_list_1d_to_list_2d_by_step(self, input_list, input_text):
		"""
		리스트로 들어온 자료들을 한번에 분리해서 2차원리스트로 만드는 것

		:param input_list:
		:param input_text:
		:return:
		"""

		result = []
		for one_value in input_list:
			temp_result = str(one_value).split(input_text)
			result.append(temp_result)
		return result

	def split_list_2d_as_none_data(self, input_list_2d, int_flag_value_at_2d):
		"""
		2번째 자료가 같은것만 묶는다
		예 : [[1,2,3,"",5], [1,2,13,4,16], [0,0,0,4,7], [1,3,5,"",9], [1,3,5,"",10]]
		4번째것을 기준으로 한다면
		결과 : [[1,2,3,"",5], [1,3,5,"",9], [1,3,5,"",10]]
		위와같은 형태로 만들어 주는 것이다

		:param input_list_2d:
		:param int_flag_value_at_2d:
		:return:
		"""

		result = []
		for list_1d in input_list_2d:
			# print(list_1d)
			if list_1d[int_flag_value_at_2d - 1] == "" or list_1d[int_flag_value_at_2d - 1] == None:
				result.append(list_1d)
		return result

	def split_list_2d_as_same_data(self, input_list_2d, int_flag_value_at_2d):
		"""
		2번째 자료가 같은것만 묶는다
		예 : [[1,2,3,4,5], [1,2,13,4,16], [0,0,0,4,7], [1,3,5,7,9], [1,3,5,7,10]]
		4번째것을 기준으로 한다면
		결과 : [[[1,2,3,4,5], [1,2,13,4,16], [0,0,0,4,7]], [[1,3,5,7,9], [1,3,5,7,10]]]
		위와같은 형태로 만들어 주는 것이다

		:param input_list_2d:
		:param int_flag_value_at_2d:
		:return:
		"""

		result = []
		temp = []
		base_value = ""
		for list_1d in input_list_2d:
			# print(list_1d[int_flag_value_at_2d - 1])
			if base_value == "":
				base_value = list_1d[int_flag_value_at_2d - 1]

			if base_value == list_1d[int_flag_value_at_2d - 1]:
				temp.append(list_1d)
			else:
				result.append(temp)
				temp = []
				base_value = ""
		if temp:
			result.append(temp)

		return result

	def split_list_2d_by_multi_words(self, all_list_2d, split_words=["o", "3", "bc", "1", "4577"]):
		"""
		1) 분리단어들을 큰것부터 정렬해야, 작은것도 가능하기 때문에 정리하는부분이다
		2) 먼저 분리할 단어들을 빠꾸기를 이용하여, 특수한 분자로 바꾸고, 맨마지막에 분리를 하는 방식을 사용한것이다

		:param all_list_2d:
		:param split_words:
		:return:
		"""
		split_words.sort()  # 1
		split_words.reverse()
		result = []
		for list_1d in all_list_2d:
			temp_2 = []
			for one_value in list_1d:
				one_value = str(one_value)
				for one_split_word in split_words:  # 2
					one_value = one_value.replace(one_split_word, "_#_#%0_")
				temp_2.append(one_value.split("_#_#%0_"))
			result.append(temp_2)
		return result

	def split_list_as_same_data(self, input_list, empty=11, same_column=[1, 3, 5]):
		"""
		읽어온 자료에서 끝나지 않은 자료만 걸러낸후, 같은 내용의 자료를 묶는것
		다음에 다른곳에도 사용이 가능할것 같아 함수로 만듦

		:param input_list:
		:param empty:
		:param same_column:
		:return:
		"""

		result = {}
		for one_list in input_list:
			# 넘어온 자료중 11번째 자료가 비어있다면 끝나지 않은것으로 판다.
			if one_list[empty - 1] == None or one_list[empty - 1] == "":
				# 같은것의 기준인 same_column안의 리스트 자료를 다 합쳐서 같은것은 같은 항목으로 견적요청한것으로 판단한다
				basic_data = ""
				for no in same_column:
					basic_data = basic_data + str(one_list[no - 1])

				# 기존에 같은 이름의 자료가 있으면, 하나더 추가한다(2차원리스트)
				if result:
					if basic_data in result.keys():
						value = result[basic_data]
						value.append(one_list)
						result[basic_data] = value
					else:
						result[basic_data] = [one_list]
				else:
					result[basic_data] = [one_list]

		# 3차원리스트 형태로 결과값을 돌려준다
		return result.values()

	def split_method_name_with_delete_empty_line_for_file(self, file_name):
		"""
		py화일을 다룰 려고 만든것이며
		화일의 메소드를 기준으로 나누면서 동시에 빈라인은 삭제하는것

		:param file_name:
		:return:
		"""
		main_def_list = []
		result = []
		total_code = ""
		total = ""
		# 화일을 읽어온다
		f = open(file_name, 'r', encoding='UTF8')
		original_lines = f.readlines()
		f.close()
		# print(len(original_lines))
		num = 1
		temp = ""
		exp_start = ""
		exp_end = ""
		exp_mid = ""
		for one_line in original_lines:
			total = total + one_line
			changed_one_line = one_line.strip()
			if changed_one_line == "":
				one_line = ""
			elif changed_one_line[0] == "#":
				one_line = ""
			elif changed_one_line[0:3] == "def":
				main_def_list.append(temp)
				temp = one_line
			elif '"""' in changed_one_line:
				if changed_one_line[0:3] == '"""':
					exp_end = "no"
					exp_start = "yes"
					one_line = ""
				elif changed_one_line[:-3] == '"""':
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_end = "yes"
						exp_start = "no"
						one_line = ""
				else:
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_mid = "yes"

				num = num + 1

			if exp_start == "yes" and exp_end == "no":
				one_line = ""

			temp = temp + one_line
			total_code = total_code + one_line
		# print(num)

		return [main_def_list, total_code, total]

	def split_operator(self, input_value):
		result = []
		input_value = str(input_value)
		oper = ""
		short_value = ""
		for index in range(len(input_value)):
			if input_value[index] in ["<", ">", "="]:
				if oper == "":
					oper = oper + input_value[index]
					result.append(short_value)
					short_value = ""
				else:
					oper = oper + input_value[index]
			else:
				if oper != "":
					result.append(oper)
					short_value = short_value + input_value[index]
					oper = ""
				else:
					short_value = short_value + input_value[index]
		if short_value:
			result.append(short_value)
		return result

	def split_python_file_by_def_as_list(self, file_name, base_text="def"):
		"""
		화일안의 def를 기준으로 문서를 분리하는것
		같은 함수의 코드를 찾기위해 def로 나누는것
		맨앞의 시작글자에 따라서 나눌수도 있다
		"""
		temp_list = []
		result = []
		# 화일을 읽어온다
		f = open(file_name, 'r', encoding='UTF8')
		lines = f.readlines()
		original = lines
		# 빈 줄을 제거한다
		lines = list(map(lambda s: s.strip(), lines))
		start_no = 0
		for no in range(len(lines)):
			line = lines[no]

			# 각줄의 공백을 제거한다
			one_line = line.strip()
			# 혹시 잇을수있는 줄바꿈을 제거한다
			one_line = one_line.replace("\n", "")
			# 맨앞에서 def가 발견이되면 여태저장한것을 최종result리스트에 저장 하고 새로이 시작한다
			if one_line[0:(len(base_text) + 1)] == base_text and temp_list != []:
				print("처음은 ===> ", start_no)
				print("끝은 ===> ", no)
				result.append(temp_list, start_no, no)
				start_no = no
				temp_list = []
			# 빈행이나 주석으로된 열을 제외한다
			if one_line != "" and one_line[0] != "#":
				temp_list.append(one_line)
		f.close()
		return result

	def split_selection_text_to_list_1d_by_each_paragraph(self, input_text):
		"""
		워드의 선택영역을 줄바꿈을 기준으로 1차원리스트로 만들어 주는것

		:param input_text:
		:return:
		"""
		result = input_text.split(chr(13))
		return result

	def split_sentence(self, input_list_1d, base_words):
		import collections
		# 문장으로 된것을 의미있는 단어들로 분리하는 것
		aaa = collections.Counter()
		for one in input_list_1d:
			value = str(one).lower().strip()
			if len(value) == 1 or value == None or value == " ":
				pass
			else:
				for l1 in base_words:
					value = value.replace(l1[0], l1[1])
				value = value.replace(",", " ")
				value = value.replace("(", " ")
				value = value.replace(")", " ")
				value = value.replace("  ", " ")
				value = value.replace("  ", " ")
				values = value.split(" ")
				aaa.update(values)
		return aaa

	def split_text_as_eng_vs_num(self, data):
		"""
		단어중에 나와있는 숫자, 영어를 분리하는기능

		:param data:
		:return:
		"""
		re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
		result = re_compile.findall(data)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def split_text_as_name_n_title(self, input_name):
		"""
		이름과 직함이 같이 있는 입력값을 이름과 직함으로 분리하는 것

		:param input_name:
		:return:
		"""
		name = ""
		title = ""
		title_list = ["부장", "이사", "프로", "사원", "대리", "과장", "사장", "차장", "대표", "대표이사", "전무", "전무이사", "공장장"]
		input_name = input_name.strip()  # 공백을 없애는 것
		if len(input_name) > 3:
			for one in title_list:
				title_len = len(one)
				if input_name[-title_len:] == one:
					name = input_name[:-title_len]
					title = input_name[-title_len:]
					break
		return [name, title]

	def split_text_as_number_n_char(self, raw_data):
		"""
		문자와숫자를 분리해서 리스트로 돌려주는 것이다
		123wer -> ['123','wer']
		"""
		temp = ""
		int_temp = ""
		result = []
		datas = str(raw_data)
		for num in range(len(datas)):
			if num == 0:
				temp = str(datas[num])
			else:
				try:
					fore_var = int(datas[num])
					fore_var_status = "integer"
				except:
					fore_var = datas[num]
					fore_var_status = "string"
				try:
					back_var = int(datas[num - 1])
					back_var_status = "integer"
				except:
					back_var = datas[num - 1]
					back_var_status = "string"

				if fore_var_status == back_var_status:
					temp = temp + datas[num]
				else:
					result.append(temp)
					temp = datas[num]
		if len(temp) > 0:
			result.append(temp)
		return result

	def split_text_as_serial_no(self, input_data, input_list):
		"""

		:param input_data:
		:param input_list:
		:return:
		"""
		result = []
		total_len = 0
		start_no = 0
		for no in range(len(input_list)):
			if no != 0:
				start_no = total_len
			end_len = input_list[no]
			result.append(input_data[start_no:start_no + end_len])
			total_len = total_len + end_len
		return result

	def split_text_as_str_n_number(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		re_com_num = re.compile("[a-zA-Z]+|\d+")
		result = re_com_num.findall(input_text)
		return result

	def split_text_by_chars(self, input_text, input_chars=","):
		"""
		어떤 글자를 원하는 문자로 나눠서 1차원자료로 만들어 주는것

		:param input_text:
		:param input_chars:
		:return:
		"""
		result = input_text.split(input_chars)
		return result

	def split_text_by_len(self, input_text, number):
		"""
		문자열을 몇개씩 숫자만큼 분리하기
		'123456' => '12','34','56'

		:param input_text:
		:param number:
		:return:
		"""
		input_text = str(input_text)
		result = []
		for i in range(0, len(input_text), number):
			result.append(input_text[i:i + number])
		return result

	def split_text_by_newline_char(self, input_text, number):
		"""
		문자열을 \n, tab으로 구분해서 분리한다

		:param input_text:
		:param number:
		:return:
		"""
		result = []
		temp_list = str(input_text).split("\n")
		for one_value_1 in temp_list:
			temp = []
			tab_list = str(one_value_1).split("\t")
			for one_value_2 in tab_list:
				temp.append(one_value_2)
			result.append(temp)

		return result

	def split_text_by_newline_tab(self, input_text, number):
		"""
		문자열을 \n, tab으로 구분해서 분리한다
		"""
		result = []
		temp_list = str(input_text).split("\n")
		for one_value_1 in temp_list:
			temp = []
			tab_list = str(one_value_1).split("\t")
			for one_value_2 in tab_list:
				temp.append(one_value_2)
			result.append(temp)

		return result

	def split_text_by_step(self, input_text, number):
		"""
		문자열을 몇개씩 숫자만큼 분리하기
		'123456' => '12','34','56'

		:param input_text:
		:param number:
		:return:
		"""
		input_text = str(input_text)
		result = []
		for i in range(0, len(input_text), number):
			result.append(input_text[i:i + number])
		return result

	def split_text_for_csv_file(self, input_text):
		"""
		csv 형식의 자료를 읽어오는 것
		""로 들러쌓인것은 숫자나 문자이며, 아닌것은 전부 문자이다

		:param input_text:
		:return:
		"""
		result = []
		temp = ""
		num = 0
		my_type = ""
		for no in range(len(input_text)):
			one_char = input_text[no]
			if one_char == '"' and num == 0:
				my_type = "type_2"
			if one_char == '"': num = num + 1
			if one_char == ',':
				if divmod(num, 2)[1] == 0 and my_type == "type_2":
					temp = temp.replace(",", "")
					try:
						temp = int(temp[1:-1])
					except:
						temp = float(temp[1:-1])
					result.append(temp)
					temp = ""
					num = 0
					my_type = ""
				elif my_type == "":
					result.append(temp)
					temp = ""
					num = 0
				else:
					temp = temp + one_char
			else:
				temp = temp + one_char
		return result

	def split_text_to_list_1d_as_len_set(self, input_list_1d, num_list_1d):
		"""
		넘어온 자료를 원하는 숫자만큼씩 자르는것
		입력값 : "ㅁㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㄹ"
		분리기준 = [2,4,5]
		결과값 :["ㅁㄴ", "ㅇㄹㄴㅇ", "ㄹㄴㅇㄹㄴ", "ㅇㄹㄴㄹ"]

		:param input_list_1d:
		:param num_list_1d:
		:return:
		"""
		result = []

		for one_text in input_list_1d:
			temp = []
			text_len = len(one_text)
			remain_text = one_text
			for x in num_list_1d:
				if x <= len(remain_text):
					temp.append(remain_text[0:x])
					remain_text = remain_text[x:]
				elif len(remain_text):
					temp.append(remain_text)
					break
			result.append(temp)
		return result

	def split_text_to_list_1d_by_base_word(self, input_list_1d, base_words):
		"""
		문장으로 된것을 의미있는 단어들로 분리하는 것

		:param input_list_1d:
		:param base_words:
		:return:
		"""
		aaa = collections.Counter()
		for one in input_list_1d:
			value = str(one).lower().strip()
			if len(value) == 1 or value == None or value == " ":
				pass
			else:
				for l1 in base_words:
					value = value.replace(l1[0], l1[1])
				value = value.replace(",", " ")
				value = value.replace("(", " ")
				value = value.replace(")", " ")
				value = value.replace("  ", " ")
				value = value.replace("  ", " ")
				values = value.split(" ")
				aaa.update(values)
		return aaa

	def split_unique(self, raw_data, delete_or_blank=0):
		"""
		이것은 똑같은 자료가 있으면 그자료를 맨처음의 것만을 남기고 없애는 것이다
		이것을 클래스로 만들어 본다

		:param raw_data:
		:param delete_or_blank:
		:return:
		"""

		before = list(raw_data)
		blank = []
		for dd in range(len(before[0])):
			blank = blank.append('')

		for a in range(len(before) - 1):
			gijun_data = before[a]

			for b in range(a + 1, len(before)):
				cmp_data = before[b]

				result = self.cmp(gijun_data, cmp_data)
				if result == 0:
					before[b] = blank
		return before

	def split_value_as_str_part_and_number_part(self, input_text):
		"""
		문자와 숫자를 분리하는것

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		re_com_num = re.compile("[a-zA-Z]+|\d+")
		result = re_com_num.findall(input_text)
		return result

	def start_mqtt(self, broker="broker.hivemq.com", port=1883, qos=0):
		"""
		start_mqtt
		"""
		self.broker = broker
		self.port = port
		self.qos = qos

	def sum_list(self, input_list):
		"""
		넘어온 여러줄의 리스트자료를 기준으로
		각 y행마다 자료가 있는지 확인해서,
		최대한 자료가 많이 들어가도록 각 x 라인을 채워서 한줄을 만든다

		:param input_list:
		:return:
		"""
		result = []
		x_no = len(input_list)
		y_no = len(input_list[0])
		for y in range(y_no):
			temp = ""
			for x in range(x_no):
				one_value = input_list[x][y]
				if one_value != "" and one_value != None:
					temp = one_value
			result.append(temp)
		# print(result)
		return result

	def sum_two_list_2d_with_each_same_position(self, list_2d_1, list_2d_2):
		"""
		같은 사이즈의 2차원 자료를 같은 위치의 값을 더하는것
		이것은 여러 엑셀화일의 같은 형태의 자료들을 더하기 위해서 사용하는 목적이다

		:param list_2d_1:
		:param list_2d_2:
		:return:
		"""
		for x in range(len(list_2d_1)):
			for y in range(len(list_2d_1[0])):
				try:
					list_2d_1[x][y] = list_2d_1[x][y] + list_2d_2[x][y]
				except:
					list_2d_1[x][y] = str(list_2d_1[x][y]) + str(list_2d_2[x][y])
		return list_2d_1

	def swap_list_1d_for_all_data(self, input_data):
		"""
		두개의 자료들에 대해서만 자리를 바꾸는 것이다

		input_data: [a, b, c, d]
		result: [b, a, d, c]

		:param input_data:
		:return:
		"""
		result = []
		for one_data in range(int(len(input_data) / 2)):
			result.append(input_data[one_data * 2 + 1])
			result.append(input_data[one_data * 2])
		return result

	def switch_every_two_data_for_list_1d(self, input_data):
		"""
		input_data : [a, b, c, d]
		result : [b, a, d, c]
		두개의 자료들에 대해서만 자리를 바꾸는 것이다

		:param input_data:
		:return:
		"""
		result = []
		for one_data in range(int(len(input_data) / 2)):
			result.append(input_data[one_data * 2 + 1])
			result.append(input_data[one_data * 2])
		return result

	def switch_list_2d_based_on_index(self, input_list_2d, input_no_list):
		"""
		2차원의 각 1차원자료들의 index번호를 기준으로 앞뒤를 바꾸는 것
		[[1,2,3,4,5], [5,6,7,8,9]] ==> [[3,4,5, 1,2], [7,8,9, 5,6]]
		input_no_list.sort()
		input_no_list.reverse()

		:param input_list_2d: 2차원 형태의 리스트
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def switch_one_value_by_special_char(self, input_value, input_char="="):
		"""
		입력된 값에 특정한 문자가 있으면, 그것을 기준으로 앞뒤를 바꾸는 것
		"aaa=bbb" => "bbb=aaa"

		:param input_char:
		"""
		one_list = str(input_value).split(input_char)
		if len(one_list) == 2:
			result = one_list[1] + input_char + one_list[0]
		else:
			result = input_value
		return result

	def terms(self):
		"""
		용어정리 : 아래와같은 형태로 용어를 사용한다
		:return:
		"""

		result = """
			pxy : 커서의 픽셀 좌표
			pwh: 넓이, 높이의 길이를 픽셀단위로 나타낸것
			mouse_click = mouse_down + mouse_up film
			date	 : 2000-01-01
			datelist : [2000, 01, 01]
			ymdlist : [2000, 01, 01]
			time	 : 시간의 여러형태로 입력을 하면, 이에 맞도록 알아서 조정한다
			dhms	 : 2일3시간10분30초, day-hour-minute-sec
			hmslist  : [시, 분, 초]
			utc  : 1640995200.0 또는 "", 1648037614.4801838 (의미 : 2022-03-23T21:13:34.480183+09:00)
			move	 : 입력값에 더하거나 빼서 다른 값으로 바꾸는것, 입력값과 출력값이 다를때 (출력값을 입력의 형태로 바꾸면 값이 다른것)
			change   : 형태를 바꾼것
			read	 : 입력값을 원하는 형태로 변경해서 갖고오는것
			get	  : 입력값에서 원하는 형태의 값을 갖고오는것
			shift	: 현재의 값을 같은 형태에서 값을 이동시키는것
			index : 0부터 시작되는 번호들
			no : 1부터 시작되는 번호들
		"""
		return result

	def write_hangul_cjj(self, letters="박상진", canvas_size=[50, 50], stary_xy=[1, 1]):
		"""
		입력받은 한글을 크기가 50 x 50의 엑셀 시트에 글씨를 색칠하여 나타내는 것이다
		"""

		# 기본 설정부분
		size_x = canvas_size[0]
		size_y = canvas_size[1]
		# 문자 하나의 기본크기
		# 기본문자는 10을 기준으로 만들었으며, 이것을 얼마만큼 크게 만들것인지 한글자의 배수를 정하는것
		h_mm = int(canvas_size[0] / 10)
		w_mm = int(canvas_size[1] / 10)
		# 시작위치
		h_start = stary_xy[0]
		w_start = stary_xy[1]

		check_han = re.compile("[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]")
		for one_char in letters:
			# 한글을 초성, 중성, 종성으로 나누는 것이다
			if check_han.match(one_char):
				jamo123 = self.split_hangul_to_jamo(one_char)
				if jamo123[0][2] == "":
					# 가, 나, 다
					if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
						# 기본설정은 시작점은 [1,1]이며, 캔버스의 크기는 [50, 50]인것이다

						start_xy = [1, 1]
						size = [10, 5]  # 위에서 배수를 5,5를 기본으로 해서 50x50되는 것이다
						# 자음의 시작점은 1,1이며, 크기는 50 x 25의 사이즈의 자음을 만드는 것이다
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						# 모음의 시작점은 자음의 끝점에서 5를 이동한 1,30이며, 크기는 자음보다 가로의 크기를 좀 줄인
						# 50 x 20의 사이즈의 자음을 만드는 것이다

						start_xy = [1, 7]
						size = [10, 4]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

					# 구, 누, 루
					if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
						start_xy = [1, 1]
						size = [4, 10]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [6, 1]
						size = [5, 10]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

					# 와, 왜, 궈
					if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
						# lists = self.div_mo2_mo1(jamo123[0][1])

						start_xy = [1, 1]
						size = [10, 5]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 8]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 8]
						size = [6, 3]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

				if jamo123[0][2] != "":
					# 왕, 웍, 윔
					if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
						hangul_type = "23자음+1332-2중모음+24자음"
						# lists = div_mo2_mo1(jamo123[0][1])

						start_xy = [1, 1]
						size = [4, 5]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [4, 1]
						size = [3, 7]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 7]
						size = [6, 3]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 6]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

					# 앙, 양, 건
					if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
						start_xy = [1, 1]
						size = [3, 5]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 6]
						size = [5, 4]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [7, 2]
						size = [3, 6]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

					# 곡, 는
					if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
						start_xy = [1, 1]
						size = [3, 10]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [4, 1]
						size = [3, 10]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 10]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

	def xyprint(self, input_value, limit_no=20):
		#print할때 너무 많은 글자가 나오면 않되기 때문에 글자수를 줄여주면서 끝에 ~~을 넣어서 프린트해주는 기능이다
		if type(input_value) == type([]):
			result = []
			for one in input_value:
				if len(str(one)) > limit_no:
					result.append(str(one))[:limit_no] + str("~~")
		elif type(input_value) == type({}):
			result = {}
			for one in input_value.keys():
				if len(str(input_value[one])) > limit_no:
					result[one] = str(input_value[one])[:limit_no] + str("~~")
		elif type(input_value) == type("abc"):
			if len(input_value) > limit_no:
				result = input_value[:limit_no] + str("~~")
		else:
			result = input_value
		print(result)
		return result

	def make_name_list(self, input_no=5):
		"""
		샘플용 자료를 만들어 주는것
		print(sample_make_name(500))
		입력한 갯수만큼 이름의 갯수를 만들어 주는것

		:param input_no:
		:return:
		"""
		sung = "김이박최정강조윤장"
		name = "가나다라마바사아자차카"
		last = "진원일이삼사오구원송국한"
		if input_no > len(sung) * len(name) * len(last) / 2:
			result = []
			pass
		else:
			total_name = set()
			num = 0
			while True:
				one_sung = random.choice(sung)
				one_name = random.choice(name)
				one_last = random.choice(last)
				new_name = one_sung + one_name + one_last
				total_name.add(new_name)
				num = num + 1
				if len(total_name) == input_no:
					print(input_no, num)
					break
			result = list(total_name)
		return result

	def zzz_sample_pre_treatment(self, input_list_2d):
		"""
		자료의 전처리
		자료들중에 변경을 할 자료들을 처리한다

		:param input_list_2d:
		:return:
		"""
		unique_data = collections.Counter()
		for data_1d in input_list_2d:
			value = str(data_1d[0])
			for new_word in [["(주)", ""], ["주식회사", ""], ["(유)", ""], ["유한회사", " "]]:
				value = value.replace(new_word[0], new_word[1])
				value = value.lower()
			unique_data.update([value])
			result = list(unique_data.keys())
		return result

	def get_all_filename_in_folder_by_extension_name(self, directory="./", filter="pickle"):
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def make_int_list_with_option(self, start_no=1, end_no=1000, step=1, qty = 100, random_tf=False, unique_tf=True):
		"""
		make : 어디에서 기본 자료를 갖고오지 않는 경우
		정수형으로 구성된 리스트 자료를 쉽게 만들어주는 함수
		갯수가 잘못 입력되었을때를 대비 하는것

		:param start_no:
		:param end_no:
		:param step:
		:param qty: 몇개를 리스트로 만들것인지
		:param random_tf: 랜덤한 자료를 만들것인지, 끝의 tf는 true_falfe를 나타내는 뜻입니다
		:param unique_tf: 고유한것이만일지, 같은 값도 반복이 가능한지를 선택하는것, 끝의 tf는 true_falfe를 나타내는 뜻입니다
		:return:
		"""

		if qty == False or int((end_no - start_no)/step) < qty:
			qty = int((end_no -start_no)/step)
		# 고유한 자료들만 하는경우와 중복이 가능한 경우를 나눠서 적용

		if random_tf:
			if unique_tf:
				temp = list(range(start_no, end_no, step))
				random.shuffle(temp)
				result = temp[:qty]
			else:
				result =  []
				for _ in range(qty):
					result.append(random.randrange(start_no, end_no, step))
		else:
			temp = list(range(start_no, end_no, step))
			result =temp[:qty]
		return result

	def change_list_as_random_n_duplicate(self, input_l1d, qty, random_tf = True, unique_tf =True):
		"""
		입력으로 들어오는 리스트자료를 변경 => 그안에서 qty만큼 골라내는데, 랜덤하게 할것인지 중복이 가능하게 할것인지를 적선택해서 하는 것

		:param input_l1d: 입력으로 들어오는 1차원의 리스트 자료
		:param qty: 몇개를 리스트로 만들것인지
		:param random_tf:
		:param unique_tf:
		:return:
		"""
		if len(input_l1d) <qty:
			qty =len(input_l1d)
		if random_tf:
			random. shuffle(input_l1d)
		if unique_tf:
			result = input_l1d[:qty]
		else:
			result = []
			for _ in range(qty):
				result.append(random.choice(input_l1d))
		return result

	def make_text_list_from_int(self, start_no=1, end_no=1000, step=1, qty = 100, same_len = 0, start_char ="", random_tf = False, unique_tf =  False):
		"""
		make : 어디에서 기본 자료를 갖고오지 않는 경우
		뒤에 숫자가 붙은 형태의 컬럼 제목을 위한 리스트형태로 만드는 것
		예  : ["title_002","title_003","title_004","title_005"]
		Databse용 table 의 각 y열의 제목을 만들어주는 것같은 리스트를 만들어주는것
		1. 앞에 접두어를 붙일것인지
		2. 뒤에붙는 숫자의 길이를 같게 만들것인지 (100 => 0100, 12 => 0012)

		:param start_no:
		:param end_no:
		:param step:
		:param qty:
		:param same_len:
		:param start_char:
		:param random_tf:
		:param unique_tf:
		:return:
		"""

		if same_len:
			if len(str(end_no)) > same_len:
				same_len = len(str(end_no))
			if qty == False or int((end_no - start_no)/step) < qty:
				qty = int((end_no -start_no)/step)

		#고유한 자료들만 하는경우와 중복이 가능한 경우를 나눠서 적용
		result = []
		if random_tf:
			if unique_tf:
				temp = list(range(start_no, end_no, step))
				random.shuffle(temp)
				for one_value in temp[:qty]:
					result.append(start_char+(same_len-len(str(one_value)))*"0"+str(one_value))
			else:
				temp = list(range(start_no, end_no, step))
				random.shuffle(temp)
				for _ in range(qty):
					one_value = random.choice(temp)
					result.append(start_char+(same_len-len(str(one_value)))*"0"+str(one_value))
		else:
			temp = list(range(start_no, end_no, step))
			for one_value in temp[:qty]:
				result.append(start_char + (same_len - len(str(one_value))) * "0" + str(one_value))
		return result

	def print_2d(self, input_2d):
		if type(input_2d) == type([]):
			print("[")
		elif type(input_2d) == type(()):
			print("[")

		for one in input_2d:
			print(one, ",")

		if type(input_2d) == type([]):
			print("]")
		elif type(input_2d) == type(()):
			print("]")



	def find_near_list(self, rgb_list, target_rgb):
		"""
		주어진 RGB의 형태로 만든 리스트에서
		타겟 RGB와 어느 값에 가장 가까운 RGB 값인지를 찾는것
		꼭 3차원이 아닌 4차원, 5차원의 자료들도 가능하다

		:param rgb_list:
		:param target_rgb:
		:return:
		"""
		result = None
		min_distance = float('inf') #파이썬에서 양의 무한대를 나타내는 방법
		for rgb in rgb_list:
			distance = self.euclidean_distance(rgb, target_rgb)
			if distance < min_distance:
				min_distance = distance
				result = rgb
		return result

	def euclidean_distance(self, point1, point2):
		"""
		n차원 공간에서 두 점 사이의 유클리드 거리를 계산합니다

		:param point1: 첫 번째 점 (리스트 또는 튜플)
		:param point2: 두 번째 점 (리스트 또는 튜플)
		:return: 두 점 사이의 유클리드 거리
		"""
		if len(point1) != len(point2):
			raise ValueError("두 점은 같은 차원이어야 합니다.")
		distance = math.sqrt(sum((p - q) * 2 for p, q in zip(point1, point2)))
		return distance


	def find_near_value(self, sorted_list, input_no):
		"""
		정렬된 자료를 기준자료로하여, 입력된 자료에서 가장 가까운 값 기준자료를 찾아주는 코드
		양쪽이 같은 크기만큼 떨어진 경우는 작은 값을 우선으로 표현합니다

		사용할 곳 : 색에 대해서 전체를 사용하지 않고, index개념으로 사용하는 색에 대해서,  index를 rgbint값으로 바꾸던지
		decimal로 바꿔서 그중에 가까운것을 찾는 것
		RGB값에 대해서 가장 가까운 rgbint값을 찾는 것입니다

		:param sorted_list: 정렬된 2차원 자료들
		:param input_no:
		:return:
		"""
		pos = bisect.bisect_left(sorted_list, input_no)
		# 가장 가까운 값을 찾기 위해 양쪽 값을 비교합니다
		if pos ==0:
			result = sorted_list[0]
		elif pos == len(sorted_list):
			result = sorted_list[-1]
		elif abs(sorted_list[pos] - input_no) < abs(input_no - sorted_list[pos -1]):
			result = sorted_list[pos]
		else:  result = sorted_list[pos -1]
		return result

	def change_int_to_roman_num(self, num):
		"""
		로마 숫자와 그에 대응하는 정수 값의 리스트

		:param num:
		:return:
		"""
		val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
		syb = ["M", "CM", "D", "CD"  "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
		i = 0
		roman_num = ""
		while num > 0:
			for _ in range(num // val[i]):
				roman_num += syb[i]
				num -= val[i]
				i += 1
		return roman_num

	def calc_no_to_mok_list(self, input_list, my_no):
		"""
		머릿글 기호를 쉽게 사용할수있도록 만들기 위해서 필한 함수
		어떤 리스트 형태로 되어있는 자료를 숯자에 맞는 형식으로 만들어 주는것

		:param input_list:
		:param my_no:
		:return:
		"""
		final_text = ""
		base_no = len(input_list)
		result = []
		if base_no > my_no:
			result = [my_no - 1]
		else:
			while True:
				mok, namuji = divmod(my_no, base_no)
				result.insert(0, namuji - 1)
				if mok < base_no:
					result.insert(0, mok - 1)
					break
				else:
					my_no = mok

		for index in result:
			final_text = final_text + input_list[index]
		return final_text


	def find_more_elements(self, list1, list2):
		"""
		두개의 리스트에서, 작은것을 기준으로 큰것중에 어느부분이 더 있고, 위치는 어디인지를 알려주는 것
		이것의 사용목적은 워드에서 영역안의 글자를 읽어오는데, 3가지의 경우가 잇어서, 어떤것이 어떤 부분이 다른것들과 차이가 나는지를
		확인하기위해서 만든것이다

		:param list1:
		:param list2:
		:return:
		"""

		counter1 = Counter(list1)
		counter2 = Counter(list2)
		if len(counter1) < len(counter2):
			smaller_counter = counter1
			larger_counter = counter2
			smaller_list = list1
			larger_list = list2
		else:
			smaller_counter = counter2
			larger_counter = counter1
			smaller_list = list2
			larger_list = list1
		more_elements = []
		for element in larger_counter:
			if element not in smaller_counter or larger_counter[element] > smaller_counter[element]:
				more_elements.append(element)
		result=[]
		for element in more_elements:
			positions = [i for i, x in enumerate(larger_list) if x == element]
			result.append((element, positions))
		return result





