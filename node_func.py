import textblob
from textblob import TextBlob
    
def korean_node(text):

    try:
        import korean_romanizer
        from korean_romanizer.romanizer import Romanizer
        translated_text = TextBlob(text).translate(to='ko')
        r = Romanizer(str(translated_text))
        r2 = r.romanize()
        return r2

    except ImportError:
        print('error while importing the package for the {x}'.format(x=korean_node.__name__))   
        return 0

def chinese_node(text):
    
    try:
        import pinyin 
        translated_text = TextBlob(text).translate(to='zh')
        r = pinyin.get(str(translated_text),format='strip')
        return r

    except ImportError:
        print('error while importing the package for the {x}'.format(x=chinese_node.__name__))   
        return 0

def japanese_node(text):

    try:
        import romaji 
        translated_text = TextBlob(text).translate(to='ja')
        r =  romaji.transliterate(str(translated_text))
        return r[0]
        
    except ImportError:
        print('error while importing the package for the {x}'.format(x=japanese_node.__name__))   
        return 0

