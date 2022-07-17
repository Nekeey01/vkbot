import requests, sys, re, random, datetime
from bs4 import BeautifulSoup

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

TOKEN = 'a91599fcf74bf2cf32074f0049265d2ed31256f676bf3c0349f0783c01a5d4330dc37b5e9dd958836467f'

group_list=[
    "Э-1-15, Э-11-16.1",
    "Э-1-16",
    "Э-1-17",
    "Э-2-15, Э-11-16.2",
    "Э-2-16, Э-11-17",
    "Э-2-17, Э-11-18",
    "КС-1-15",
    "КС-1-16",
    "КС-1-17",
    "КС-2-15",
    "КС-2-16",
    "КС-2-17",
    "КС-3-15, КС-11-16",
    "КС-3-16, КС-11-17",
    "КС-3-17, КС-11-18",
    "П-1-15",
    "П-1-16",
    "П-1-17",
    "П-2-15, П-11-16",
    "П-2-16",
    "П-2-17",
    "П-3-16",
    "П-3-17, П-11-18",
    "П-4-16, П-11-17",
    "ИС-1-15",
    "ИС-1-16",
    "ИС-1-17",
    "ИС-2-15",
    "ИС-2-16",
    "ИС-2-17",
    "ИС-3-15",
    "ИС-3-16, ИС-11-17",
    "ИС-3-17, ИС-11-18",
    "И-1-15",
    "И-1-16",
    "И-1-17",
    "И-2-15, И-11-16",
    "И-2-16",
    "И-2-17",
    "И-3-16",
    "И-3-17, И-11-18",
    "И-4-16",
    "И-5-16, И-11-17",
    "СА50-1-17, СА50-11-18",
    "БД50-1-17, БД50-11-18",
    "ВД50-1-17, ВД50-11-18",
    "ИС50-1-17, ИС50-1-18",
    "Т50-1-17, Т50-11-18",
    "БИ-1-16",
    "БИ-1-17",
    "БИ-2-16, БИ-11-17",
    "БИ50-1-17",
    "БИ50-2-17, БИ50-11-18",
    "Ю-1-16",
    "Ю-1-17",
    "Ю-1-18",
    "Ю-2-16, Ю-11-17",
    "Ю-2-17, Ю-11-18",
    "БИ50-1-18",
    "БИ50-2-18",
    "ИСИП-1-18",
    "ИСИП-10-18",
    "ИСИП-11-18",
    "ИСИП-12-18",
    "ИСИП-13-18",
    "ИСИП-14-18",
    "ИСИП-15-18",
    "ИСИП-2-18",
    "ИСИП-3-18",
    "ИСИП-4-18",
    "ИСИП-5-18",
    "ИСИП-6-18",
    "ИСИП-7-18",
    "ИСИП-8-18",
    "ИСИП-9-18",
    "КС-1-18",
    "П-1-18",
    "СА50-1-18",
    "СА50-2-18",
    "Э-1-18",
    "Э-2-18",
]


class Main:
	def __init__(self, token, group_id, list_group):
		self.vk = vk_api.VkApi(token=token)	
		self.longpoll = VkBotLongPoll(vk=self.vk, group_id=group_id)
		self.vk_get_api=self.vk.get_api()

		self.groups=[]
		self.vivod=[]

		self.group_list=list_group

		self.zam_check=0
		self.numb_group=""

	def start(self):
		# Основной цикл
		self.zamena(grups=True)
		for event in self.longpoll.listen():
			# Если пришло новое сообщение
			if event.type == VkBotEventType.MESSAGE_NEW:

				# Сообщение от пользователя
				self.request=event.obj.text
				print('Текст:', event.obj.text)	

				# Каменная логика ответа
				if self.request.title()=="Привет":
					self.vk_get_api.messages.send(chat_id=event.chat_id, random_id=random.randint(1,23523533), message="Дарова гнида подъеботная")
				
				elif self.request.title()=="Замены":
					self.vk_get_api.messages.send(chat_id=event.chat_id, random_id=random.randint(1,23523533), message="Группы, имеющие изменения: \n{}".format("\n".join(self.groups)))
					self.zam_check=1
				
				elif self.zam_check==1 and self.request in self.group_list:
					self.write_msg(event.chat_id, self.request)
				
				elif (self.request[:11]=="Замены для ") and (self.request[11:].upper() in self.group_list):
					if self.request[11:].upper() in self.groups: self.write_msg(event.chat_id, self.request[11:].upper())
					else: self.vk_get_api.messages.send(chat_id=event.chat_id, random_id=random.randint(1,23523533), message="Увы, но изменений для этой группы нет")
				
				elif self.request.title()=="Выход" or self.request=="Иди нахуй": return
				
				elif self.request.title()=="Извини" or self.request.title()=="Прости":
					self.vk_get_api.messages.send(chat_id=event.chat_id, random_id=random.randint(1,23523533), message="Так то лучше, кожаный ублюдок")
		
				else:
					self.vk_get_api.messages.send(chat_id=event.chat_id, random_id=random.randint(1,23523533), message="Нема") 
	def write_msg(self, user_id, group):
		self.zamena(group)
		self.vk_get_api.messages.send(chat_id=user_id, random_id=random.randint(1,23523533), message="{}".format(str(self.numb_group))) # Номер группы
		for g in range(len(self.vivod)): self.vk_get_api.messages.send(chat_id=user_id, random_id=random.randint(1,23523533), message=self.vivod[g]) # Пары

	def zamena(self, gruppa="ИСИП-4-18", grups=False):
		# Подключение
		url = "https://mpt.ru/studentu/izmeneniya-v-raspisanii/"
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')

		group = soup.find_all("caption") # Для вычесления кол-ва групп.
		for i in range(len(group)):
			# Очищение списков
			para_=[]
			para_r_from_=[]
			para_r_to_=[]
			para_r_from=[]
			para_r_to=[]

			group_ = soup.find_all("caption")[i].get_text() # Название Группы
			para =  soup.find_all('th', class_='lesson-number')[i].get_text() # Надпись "пара". Заменить обычным словом.
			all_ =  str(soup.find_all("table", class_='table table-striped')[i]) # Группа и вся инфа про нее
			para_.append(re.findall(r'<td class="lesson-number">(\d)', all_)) # Номер пары у данной группы
			para_r_from_.append(re.findall(r'<td class="replace-from">(.*?)<', all_)) # Что заменяют
			para_r_to_.append(re.findall(r'<td class="replace-to">(.*?)<', all_)) # На что заменяют

			for j in range(len(para_[0])):
				para_r_to=re.sub(" +", " ", para_r_to_[0][j]) # Убираем пробелы 
				para_r_from=re.sub(" +", " ", para_r_from_[0][j]) # Убираем пробелы

				#Проверка на группу и режим
				if group_[8:] == gruppa and grups==False: 
					fin= str(para) + " - " + str(para_[0][j]) + "\n" + str(para_r_from) + " заменяется на " + str(para_r_to)
					self.vivod.append(fin)
			if group_[8:] == gruppa and grups==False: 
				self.numb_group=group_
			if grups: 
				self.groups.append(str(group_[8:]))



	def wake_up():
		RED_WEEK = "Числитель"
		BLUE_WEEK = "Знаменатель" 

		url = "https://mpt.ru/studentu/raspisanie-zanyatiy/"
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')

		week = soup.find_all('div', class_='col-xs-12 col-sm-12 col-md-7 col-md-pull-5').get_text()[8:]


		DAY_NOW = datetime.datetime.today().strftime("%A")


		VTORNIK= {
			"Первый будильник в :":"7:45",
			"Встать в :":"8:20",
			"Последний будильник в :":"9:00",
			"Выйти в :":"9:20",
			"Пары":{2:"История", 3:"Математика", 4:"ОБЖ", 5:"Информатика"},
			"Корпус :":"Нахим.",
			"Дома в ":"18:00-18:30",
		}



		SREDA_RED= {
			"Первый будильник в :":"6:45",
			"Встать в :":"7:20",
			"Последний будильник в :":"8:00",
			"Выйти в :":"8:20",
			"Пары":{2:"Физика", 3:"Иностранный язык", 4:"Русский язык", 5:"Иностранный язык"},
			"Корпус :":"Нежинская",
			"Дома в ":"19:00-19:30",
		}

		SREDA_BLUE= {
			"Первый будильник в :":"6:45",
			"Встать в :":"7:20",
			"Последний будильник в :":"8:00",
			"Выйти в :":"8:20",
			"Пары":{2:"Физика", 3:"Иностранный язык", 4:"Русский язык"},
			"Корпус :":"Нежинская",
			"Дома в ":"17:30-18:00",
		}




		CHETVERG_RED= {
			"Первый будильник в :":"6:00",
			"Встать в :":"6:40",
			"Последний будильник в :":"7:20",
			"Выйти в :":"7.40",
			"Пары":{1:"Введение в специальность", 2:"Обществознание", 3:"Физическая культура", 4:"Обществознание"},
			"Корпус :":"Нахим.",
			"Дома в ":"16:30-17:00",
		}

		CHETVERG_BLUE= {
			"Первый будильник в :":"6:00",
			"Встать в :":"6:40",
			"Последний будильник в :":"7:20",
			"Выйти в :":"7.40",
			"Пары":{1:"Введение в специальность", 2:"История", 3:"Физическая культура", 4:"Обществознание"},
			"Корпус :":"Нахим.",
			"Дома в ":"16:30-17:00",
		}




		FRIDAY_RED= {
			"Первый будильник в :":"6:45",
			"Встать в :":"7:20",
			"Последний будильник в :":"8:00",
			"Выйти в :":"8:20",
			"Пары":{2:"Астрономия", 3:"Физика", 4:"Литература", 5:"Математика"},
			"Корпус :":"Нежинская",
			"Дома в ":"19:00-19:30",
		}

		FRIDAY_BLUE= {
			"Первый будильник в :":"6:45",
			"Встать в :":"7:20",
			"Последний будильник в :":"8:00",
			"Выйти в :":"8:20",
			"Пары":{2:"Астрономия", 3:"Иностранный язык", 4:"Физическая культура", 5:"Математика"},
			"Корпус :":"Нежинская",
			"Дома в ":"19:00-19:30",
		}



		SUBOTA_RED= {
			"Первый будильник в :":"6:45",
			"Встать в :":"7:20",
			"Последний будильник в :":"8:00",
			"Выйти в :":"8:20",
			"Пары":{2:"Математика", 3:"Литература"},
			"Корпус :":"Нежинская",
			"Дома в ":"15:30-16:00",
		}

		SUBOTA_BLUE= {
			"Первый будильник в :":"6:45",
			"Встать в :":"7:20",
			"Последний будильник в :":"8:00",
			"Выйти в :":"8:20",
			"Пары":{2:"Математика", 3:"Литература", 4:"Введение в специальность"},
			"Корпус :":"Нежинская",
			"Дома в ":"17:30-18:00",
		}
		


		self.vk_get_api.messages.send(chat_id=user_id, random_id=random.randint(1,23523533), message=)


# Запуск
Server1=Main(TOKEN, 180553756, group_list)
Server1.start()




def wr(j):
	with open('D:\\_python\\4.txt', 'w') as ouf:
	    print(j, file=ouf)
def pr(item, test=1):
	if test == 1:
		print ("\n", "_TEST - ", item, "\n")
	else:
		print ("\n", item, "\n")















def raspisanie():
	url = "https://mpt.ru/studentu/raspisanie-zanyatiy/"
	page = self.requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	group = soup.find_all("caption")

	all_ =  str(soup.find_all("div", class_='tab-pane')) # Группа и вся инфа про нее

	grup = re.findall(r'<h3>(.*?)</h3>', all_)

	if grup == "Группа ИСиП-4-18":

		text = re.findall(r'<div role="tabpanel" class="tab-pane" id="specRasp79ac36708fcb7ded9e3c42c0972dddd4">"(.*)<div role="tabpanel" class="tab-pane" id="specRaspd1d81fb3ed78ac1d030189cb8f52f540">', all_)
		for x in range(7):
			days.append(re.findall(r'<h4>(.*?)<span', text))
			para.append(re.findall(r'<td>(\d)</td>', text))
			# para.append(re.findall(r'<tr>(\d)</tr>', all_))
			# para.append(re.findall(r'</thead>(\d)<thead>', all_))


	# print(all_)

	para_.append(re.findall(r'<td class="lesson-number">(\d)', all_)) # Номер пары у данной группы

	para_r_from_.append(re.findall(r'<td class="replace-from">(.*?)<', all_)) # Что заменяют
	
	para_r_to_.append(re.findall(r'<td class="replace-to">(.*?)<', all_)) # На что заменяют




