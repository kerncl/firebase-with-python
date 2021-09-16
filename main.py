from firebase import firebase
from datetime import datetime
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import nltk

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except :
    print('Downloading... vader module')
    nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

try:
    nltk.data.find('/corpora/stopwords')
except:
    print('Downloading... stopwords module')
    nltk.download('stopwords')
from nltk.corpus import stopwords

firebase = firebase.FirebaseApplication("https://bursa-60b86.firebaseio.com/", None)


def text_analysis(message):
    """
    Text processing by using nltk vader library
    Args:
        message (str): message input for text processing

    Returns:
        (dict): returns dictionary with 'neg' & 'pos' key
    """
    vader = SentimentIntensityAnalyzer()
    score_data = vader.polarity_scores(message)
    score =score_data['compound']
    print(score_data)
    # Processing by sentences
    # score = {'neg': 0, 'pos': 0}
    # for i,sentences in enumerate(sent_tokenize(message)):
    #     score_data =vader.polarity_scores(sentences)
    #     score['neg'] += score_data['neg']
    #     score['pos'] += score_data['pos']
    #     print(score)
    # score['neg'] = score['neg'] / (i + 1)
    # score['pos'] = score['pos'] / (i + 1)
    # print(score)
    return score


def get_score(threshold_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)):
    """
    Get the score of the user comment
    Returns:
        (dict): score of the comment
    """
    list_data = firebase.get('/comments', '')
    for id, data in list_data.items():
        date, time = data['date'].split(' ')
        yyyy,mm,dd = date.split('-')
        h, m, s = time.split(':')
        data_datetime = datetime.now().replace(year=int(yyyy), month=int(mm), day=int(dd), hour=int(h), minute=int(m))
        if threshold_datetime < data_datetime:
            comment = data['comment']
            score = text_analysis(comment)
            firebase.put('/comments/'+id, 'score', score)


def get_keyword(video_id):
    """
    Get keyword from the comment and upload to firebase
    Args:
        video_id (str): video_id

    Returns:
        None
    """
    comments = [data['comment'] for data in firebase.get('/'+video_id,'').values()]
    # comments = ['I love earth, mars, jupiter and earth .', 'fk you', 'your mum asshole', 'earth', 'fuck you',
    #             'fk fk fk fk']
    stopWords= set(stopwords.words('english'))
    stopWords |= {'.', 'All', 'is', ' ', ',', 'I'}
    wordsFiltered = []
    # topkeywords = []
    newStrings = [', '.join(word) for word in [word_tokenize(comment) for comment in comments]]

    for newString in newStrings:
        newString = word_tokenize(newString)
        for keyword in newString:
            if keyword not in stopWords:
                wordsFiltered.append(keyword)
                fdist = FreqDist(wordsFiltered)
                topkeywords = fdist.most_common(5)

    print('Top Keywords : ', topkeywords)
    firebase.delete('/coment_keyword/'+video_id, '')
    for topkeyword in topkeywords:
        keyword = topkeyword[0]
        count = topkeyword[1]
        firebase.put('/comment_keyword/'+ video_id, keyword, count)
        print(keyword)
        print(count)
    print()
    pass


if __name__ == '__main__':
    current_date_time = datetime.now()
    timer_lunch = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    timer_close = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
    timer_day = datetime.now().replace(hour=23, minute=00, second=0, microsecond=59)
    M_update = False
    A_update = False
    N_update = False
    # get_score()
    get_keyword('comments')
    while True:
        if current_date_time > timer_lunch:
            if not M_update:
                score = get_score()
                M_update = True
                N_update = False
            # firebasepy.post_data(, score)
        elif current_date_time > timer_close:
            if not A_update:
                score = get_score(timer_lunch)
                A_update = True
                M_update = False
        elif current_date_time > timer_day:
            if not N_update:
                score = get_score(timer_close)
                N_update = True
                A_update = False