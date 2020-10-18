from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import re
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# nltk.download('punkt')
# nltk.download('stopwords')

# Выгружаем информация по нужнм статьям с GoogleNews (лимит - 10 статей)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
googlenews = GoogleNews(start='09/18/2020',end='10/18/2020')
googlenews.search('Russia')
result = googlenews.result()
df = pd.DataFrame(result)

# Выгружаем информация по нужным статьям с GoogleNews (ещё 10 статей)
for i in range(2, 20):
    googlenews.getpage(i)
    result = googlenews.result()
    df = pd.DataFrame(result)

# проходимся по ссылкам на новости и вгружаем текст новостей, слова сохраняем в text
text = []
for ind in df.index:
    article = Article(df['link'][ind], config=config)
    try:
        article.download()
    except Exception: # некотые ссылки возвращают 403, их пропускаем
        continue
    article.parse()
    article.nlp()
    sentence = article.text.lower()
    match_pattern = re.findall(r'\b[a-z]{3,15}\b', sentence) # из текста берем только слова
    text.extend(match_pattern)

# переводим получившийся список слов в строку
text = ' '.join(text)

# Create and generate a word cloud image:
other = {'russia', 'russian', 'one', 'two'}
STOPWORDS.update(other)
wordcloud = WordCloud(max_font_size=50, max_words=20, stopwords=STOPWORDS, background_color="white").generate(text)
wordcloud.to_file("first_review.png")
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

