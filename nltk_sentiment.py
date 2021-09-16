from nltk import sent_tokenize
import nltk

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
except :
    print('Downloading... vader module')
    nltk.download('vader_lexicon')

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

if __name__ == '__main__':
    example_text = r'Gogogo AirAsia. We Trust you tony, you can make it. Q3 revenue increase'
    example_text2 = r'AirAsia Q3 revenue is negative, dont give them a trust. it might fall into PN17 group'
    score = text_analysis(example_text)
    # vader = SentimentIntensityAnalyzer()
    # score = vader.polarity_scores(example_text)
    print(f'final score: {score}')

