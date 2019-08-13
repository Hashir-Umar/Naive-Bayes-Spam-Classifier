#Hashir Umar
#L1F16BSCS0263
#SECTION: G

import csv
import re 
import os.path

def getStopwords():

	stopwords = ['a','about','above','across','after','again','against','all','almost','alone','along','already','also','although','always','among','an','and','another','any','anybody','anyone','anything','anywhere','are','area','areas','around','as','ask','asked','asking','asks','at','away','b','back','backed','backing','backs','be','became','because','become','becomes','been','before','began','behind','being','beings','best','better','between','big','both','but','by','c','came','can','cannot','case','cases','certain','certainly','clear','clearly','come','could','d','did','differ','different','differently','do','does','done','down','down','downed','downing','downs','during','e','each','early','either','end','ended','ending','ends','enough','even','evenly','ever','every','everybody','everyone','everything','everywhere','f','face','faces','fact','facts','far','felt','few','find','finds','first','for','four','from','full','fully','further','furthered','furthering','furthers','g','gave','general','generally','get','gets','give','given','gives','go','going','good','goods','got','great','greater','greatest','group','grouped','grouping','groups','h','had','has','have','having','he','her','here','herself','high','high','high','higher','highest','him','himself','his','how','however','i','if','important','in','interest','interested','interesting','interests','into','is','it','its','itself','j','just','k','keep','keeps','kind','knew','know','known','knows','l','large','largely','last','later','latest','least','less','let','lets','like','likely','long','longer','longest','m','made','make','making','man','many','may','me','member','members','men','might','more','most','mostly','mr','mrs','much','must','my','myself','n','necessary','need','needed','needing','needs','never','new','new','newer','newest','next','no','nobody','non','noone','not','nothing','now','nowhere','number','numbers','o','of','off','often','old','older','oldest','on','once','one','only','open','opened','opening','opens','or','order','ordered','ordering','orders','other','others','our','out','over','p','part','parted','parting','parts','per','perhaps','place','places','point','pointed','pointing','points','possible','present','presented','presenting','presents','problem','problems','put','puts','q','quite','r','rather','really','right','right','room','rooms','s','said','same','saw','say','says','second','seconds','see','seem','seemed','seeming','seems','sees','several','shall','she','should','show','showed','showing','shows','side','sides','since','small','smaller','smallest','so','some','somebody','someone','something','somewhere','state','states','still','still','such','sure','t','take','taken','than','that','the','their','them','then','there','therefore','these','they','thing','things','think','thinks','this','those','though','thought','thoughts','three','through','thus','to','today','together','too','took','toward','turn','turned','turning','turns','two','u','under','until','up','upon','us','use','used','uses','v','very','w','want','wanted','wanting','wants','was','way','ways','we','well','wells','went','were','what','when','where','whether','which','while','who','whole','whose','why','will','with','within','without','work','worked','working','works','would','x','y','year','years','yet','you','young','younger','youngest','your','yours','z']
	return stopwords

def removeStopwords(sentence):

	stopwordsArray = getStopwords()
	sentenceWithNoStopWords = []
	for word in sentence:
		flag = 0
		for stopword in stopwordsArray:
			if word == stopword:
				flag = 1
				break
		
		if flag == 0:
			sentenceWithNoStopWords.append(word)
			
	return sentenceWithNoStopWords


def splitWords(sentence):
	sentence = sentence.lower()
	sentence = re.findall(r'\w+', sentence)
	return sentence

def checkSentence(sentence, spamSentences, notSpamSentences, spamCount, notSpamCount, dictionary):

	result = ""
	
	#tokenizing and removing stopwords from my sentence 
	sentence = removeStopwords(splitWords(sentence))
	
	flag = False
	for word in sentence:
		if word in dictionary:
			flag = True
	
	if flag == False:
		result =  "Given words are not available in dataset"
	else:
		probOfSpam = spamSentences / (spamSentences + notSpamSentences)
		probOfNotSpam = notSpamSentences / (spamSentences + notSpamSentences)

		#applying naive bayes formula
		probWordGivenSpam = 1
		probWordGivenNotSpam = 1

		for word in sentence:
			if word in dictionary:
				probWordGivenSpam *= ((dictionary[word][0]+1)/(spamCount + 2))
				probWordGivenNotSpam *= ((dictionary[word][1]+1)/(notSpamCount + 2))
				
		spamRes = probWordGivenSpam * probOfSpam
		notSpamRes =  probWordGivenNotSpam * probOfNotSpam
	
		if(notSpamRes > spamRes):
			result = "Not Spam"
		else:
			result = "Spam"
			
	return result

	
def makeDictionary(file, dictionaryOutputFile, dictionary):
	
	with open(file, mode='r') as csv_file:
		
		csv_reader = csv.DictReader(csv_file)
		
		countS = 0
		countNS = 0
		countSpamSentence = 0
		countNotSpamSentence = 0
		
		for row in csv_reader:
		
			tokenizedWords = removeStopwords(splitWords(row['v2']))
			
			if row['v1'] == "spam":
				countSpamSentence += 1
			else:
				countNotSpamSentence += 1
				
			#print(tokenizedWords) #uncomment this line to print tokenized words
			
			for i in tokenizedWords:
				if row['v1'] == "spam":
					countS += 1
					if i in dictionary:
						dictionary[i][0] += 1
					else:
						dictionary[i] = [1, 0]	#spamCount, notSpamCount
				else:
					countNS += 1
					if i in dictionary:
						dictionary[i][1] += 1
					else:
						dictionary[i] = [0, 1]	#spamCount, notSpamCount
		
	return countSpamSentence, countNotSpamSentence, countS, countNS, dictionary
	
# Main Function 
if __name__ == "__main__":
	
	dictFileName = "information.txt"
	
	spamSentences = 0
	notSpamSentences = 0
	spamCount = 0
	notSpamCount = 0
	dictionary = {}
	
	print("It wall take a moment to create the dictionary file")
	spamSentences, notSpamSentences, spamCount, notSpamCount, dictionary = makeDictionary("Dataset.csv", dictFileName, dictionary)

	while 1:
		mySentence = input("\nEnter a sentence: ")
		
		print("Sentence: ", mySentence)
		print("Conclusion: ", checkSentence(mySentence, spamSentences, notSpamSentences, spamCount, notSpamCount, dictionary))
		
	