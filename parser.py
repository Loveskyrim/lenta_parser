import requests
from bs4 import BeautifulSoup
import argparse
import sys
import os
import pickle5 as pickle

class Parser:

	def appending(self, lst, _ref, _time, _text, _title=False):
		"""
		appending(lst, _ref, _time, _text, _title=False)
		Appends args to the list 'lst' to store in file
		"""
		if _title:
			lst.append("https://lenta.ru/" + _ref)
			lst.append(_time)
			lst.append(_title.text)
			lst.append(_text.text)
		else:
			lst.append("https://lenta.ru/" + _ref)
			lst.append(_time)
			lst.append(_text.text)

		return lst


	def dump_list(self, file, *args):
		"""
		dump_list(file, *args)
		Dumps lists to the file
		"""
		for lists in args:
			pickle.dump(lists, file, 2)


	def news_7_parse(self, news, date=''):
		"""
		news_7_parse(news, date='')
		Processes top 7 news from lenta.ru
		Get arguments for 2 types of news
		Date (_time) gets from the news URL
		"""
		tops = []
		for index in news:
			try:
				_ref = index.h2.a["href"]
				temp = _ref.split("/")
				_time = temp[2] + '.' + temp[3] + '.' + temp[4]
				_text = index.h2.a
			except AttributeError:
				_ref = index.a["href"]
				temp = _ref.split("/")
				_time = temp[2] + '.' + temp[3] + '.' + temp[4]
				_text = index.a

			# print(_ref)
			# print(_text.text)
			# print(_time)

			if date != '' and date == _time:
				tops = self.appending(tops, "https://lenta.ru/" + _ref, _time, _text)

			elif date == '':
				tops = self.appending(tops, "https://lenta.ru/" + _ref, _time, _text)
		
		# print(tops)
		return tops


	def news_parse(self, news, date=''):
		"""
		news_parse(news, date='')
		Processes not top 7 news from lenta.ru
		Get arguments for 2 types of news
		Date (_time) gets from the news URL
		"""
		parsed_news = []
		for index in news:

			try:
				_ref = index.find("div", {"class": "titles"}).h3.a["href"]
				temp = _ref.split("/")
				_time = temp[2] + '.' + temp[3] + '.' + temp[4]
				_text = index.find("div", {"class": "titles"}).h3.a.span
			except AttributeError:
				_ref = index.a["href"]
				temp = _ref.split("/")
				_text = index.a
				
				if temp[0] == '':
					_time = temp[2] + '.' + temp[3] + '.' + temp[4]
				else:
					temp = temp[4].split("-")
					len_temp = len(temp)
					_time = temp[len_temp-1][:4] + '.' + temp[len_temp-2] + '.' + temp[len_temp-3]

			# print(_ref)
			# print(_text.text)
			# print(_time)

			if date != '' and date == _time:
				parsed_news = self.appending(
					parsed_news, "https://lenta.ru/" + _ref, _time, _text)

			elif date == '':
				parsed_news = self.appending(
					parsed_news, "https://lenta.ru/" + _ref, _time, _text)
		
		# print(parsed_news)
		return parsed_news

	def article_parse(self, articles, date=''):
		"""
		article_parse(articles, date='')
		Processes articles from lenta.ru
		Gets arguments for 2 types of articles
		Date (_time) gets from the article URL
		"""
		parsed_arts = []
		for index in articles:

			try:
				_ref = articles.find("div", {"class": "titles"}).h3.a["href"]
				temp = _ref.split("/")
				_time = temp[2] + '.' + temp[3] + '.' + temp[4]
				_title = index.find("div", {"class": "titles"}).h3.a.span
				_text = index.find("div", {"class": "titles"}).div
			except AttributeError:
				_ref = index.a["href"]
				temp = _ref.split("/")
				_time = ''
				_title = index.a.span
				_text = index.a.div
				if _title != None and temp[0] == '':
					_time = temp[2] + '.' + temp[3] + '.' + temp[4]
			finally:
				if _title != None and temp[0] == '':

					# print(_ref)	
					# print(_title.text)
					# print(_text.text)
					# print(_time)

					if date != '' and date == _time:
						parsed_arts = self.appending(
							parsed_arts,
							"https://lenta.ru/" + _ref,
							_time, _text, _title)

					elif date == '':
						parsed_arts = self.appending(
							parsed_arts,
							"https://lenta.ru/" + _ref,
							_time, _text, _title)
		# print(parsed_arts)
		return parsed_arts

	def top_article_parse(self, articles, date=''):
		"""
		top_article_parse(articles, date='')
		Processes top article from lenta.ru
		"""
		parsed_arts = []
		# _class = articles.find("div", {"class": "g-date"}).a.text
		_ref = articles.find("div", {"class": "b-feature__header"}).a["href"]
		temp = _ref.split("/")
		_time = temp[2] + '.' + temp[3] + '.' + temp[4]
		_title = articles.find("div", {"class": "b-feature__header"}).a
		_text = articles.find("div", {"class": "rightcol"}).a

		# print(_ref)	
		# print(_title.text)
		# print(_text.text)
		# print(_time)

		if date != '' and date == _time:
			parsed_arts = self.appending(
				parsed_arts, 
				"https://lenta.ru/" + _ref, 
				_time, _text, _title)

		elif date == '':
			parsed_arts = self.appending(
				parsed_arts,
				"https://lenta.ru/" + _ref,
				_time, _text, _title)

		# print(parsed_arts)
		return parsed_arts

	def arts_parse(self, soup, date=''):
		"""
		arts_parse(soup, date='')
		Processes articles from lenta.ru
		"""
		top_article = soup.find("div", {"class": "b-feature__wrap"})
		articles = soup.find_all("div", {"class": "article"})

		articles1 = self.top_article_parse(top_article, date)
		articles2 = self.article_parse(articles, date)

		return articles1, articles2


	def n_parse(self, soup, date=''):
		"""
		n_parse(soup, date='')
		Processes 3 types of news from lenta.ru
		"""
		top_7_section = soup.find("section", {"class": "js-top-seven"})
		top_7_news = top_7_section.find_all(
			"div",
			{"class": ["first-item", "item"]})

		news_all = soup.find_all("div", {"class": "news"})

		yellow_box = soup.find(
			"section",
			{"class": "js-yellow-box"}).div.find_all("div", {"class": "item"})

		news1 = self.news_7_parse(top_7_news, date)
		news2 = self.news_parse(news_all, date)
		news3 = self.news_parse(yellow_box, date)

		return news1, news2, news3


	def processing(self, rubric='', date=''):
		"""
		processing(rubric='', date='')
		Gets data from lenta.ru depending on the conditions
		"""
		r = requests.get("https://lenta.ru/")    # Get Response method
		r.encoding = 'utf8'
		a1, a2, n1, n2, n3 = [0]*5
		soup = BeautifulSoup(r.content, 'lxml') #  Create an object

		if rubric == 'articles':
			a1, a2 = self.arts_parse(soup, date)
		elif rubric == 'news':
			n1, n2, n3 = self.n_parse(soup, date)
		else:
			n1, n2, n3 = self.n_parse(soup, date)
			a1, a2 = self.arts_parse(soup, date)

		return a1, a2, n1, n2, n3


	def collect(self, params):
		"""
		collect(params)
		Collects data from lenta.ru and dumps them into given 
		file in binary format
		"""
		_date = ''
		try:
			path = os.path.dirname(params.file)
			if not os.path.exists(path):
				os.makedirs(path)
			with open(params.file, 'wb') as f:
				if params.date:
					_date = params.date

				a1, a2, n1, n2, n3 = self.processing(params.rubric, _date)

				self.dump_list(f, a1, a2, n1, n2, n3)

		except:
			raise



def parse_args(args):
	"""
	parse_args(args)
	Parses given arguments.
	Example: 
	--file=”/home/Ivanov/crawler/data/lenta_ru.pkl” 
	--rubric=news 
	--date=2020.01.28
	"""
	parser = argparse.ArgumentParser(
		description='This is a Lenta.ru main page parser; parses data to file in binary format')
	requiredNamed = parser.add_argument_group('required arguments')
	file = requiredNamed.add_argument(
		"--file", 
		help="print in file to store info", 
		type=str)
	file.required = True

	parser.add_argument(
		"--rubric",
		default=False,
		choices=['articles', 'news'],
		help='Get articles or news',
		type=str)
	parser.add_argument(
		'--date',
		default=False,
		help='Get info of this date',
		type=str)

	return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    parser_1 = Parser()
    parser_1.collect(params)


if __name__ == '__main__':
    main()
