import re
import nltk
import heapq  
import scipy
import urllib.request
from bs4 import BeautifulSoup
from googlesearch import search 
# import speech_synthesis as SS

def get_websites(query, num=5):
	return search(query, tld="co.in", num=10, stop=1, pause=2)


def get_text(url):
	try:
		print(url)
		scraped_data = urllib.request.urlopen(url)  
		article = scraped_data.read()

		parsed_article = BeautifulSoup(article,'lxml')

		paragraphs = parsed_article.find_all('p')

		article_text = ""

		for p in paragraphs:  
			article_text += p.text

		formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
		formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  

		return article_text, formatted_article_text
	except: 
		return "", ""


def get_summary(text, formated_text):
	sentence_list = nltk.sent_tokenize(text)  
	stopwords = nltk.corpus.stopwords.words('english')

	word_frequencies = {}  
	for word in nltk.word_tokenize(formated_text):  
		if word not in stopwords:
			if word not in word_frequencies.keys():
				word_frequencies[word] = 1
			else:
				word_frequencies[word] += 1

	maximum_frequncy = max(word_frequencies.values())

	for word in word_frequencies.keys():  
		word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


	sentence_scores = {}  
	for sent in sentence_list:  
		for word in nltk.word_tokenize(sent.lower()):
			if word in word_frequencies.keys():
				if len(sent.split(' ')) < 30:
					if sent not in sentence_scores.keys():
						sentence_scores[sent] = word_frequencies[word]
					else:
						sentence_scores[sent] += word_frequencies[word]

	summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

	summary = ' '.join(summary_sentences)  

	return summary


def get_videos(text):

	query = urllib.parse.quote('mit ' + text)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib.request.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	links = []
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		links.append('https://www.youtube.com' + vid['href'])
	return links



if __name__ == '__main__':
	url = 'https://en.wikipedia.org/wiki/Computer_science'

	text, formated_text = get_text(url)

	summary = get_summary(text, formated_text)
	print(summary)
	# model = SS.load_model()
	# SS.synthesize_parapgraph(model, summary)
