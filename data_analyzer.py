# -*- coding: utf-8 -*-
import pandas as pd
import jieba
from snownlp import SnowNLP
from collections import Counter
import json
import os

def load_stopwords():
    stopwords = set([
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你',
        '会', '着', '没有', '看', '好', '自己', '这', '我们', '他', '来', '那', '她', '之', '吗', '啊', '呢', '吧', '这个', '什么'
    ])
    return stopwords

def text_analysis(df):
    stopwords = load_stopwords()
    all_words = []

    for text in df['评论内容']:
        words = jieba.cut(text)
        filtered_words = [w for w in words if len(w) > 1 and w not in stopwords]
        all_words.extend(filtered_words)

    word_freq = Counter(all_words).most_common(30)
    print(f"提取词数: {len(all_words)} 个")

    return dict(word_freq)

def sentiment_analysis(df):
    sentiments = []

    for text in df['评论内容']:
        s = SnowNLP(text)
        score = s.sentiments
        sentiments.append(score)

    df['情感分数'] = sentiments

    positive = sum(1 for s in sentiments if s > 0.6)
    negative = sum(1 for s in sentiments if s < 0.4)
    neutral = len(sentiments) - positive - negative

    sentiment_dist = {
        '积极': positive,
        '消极': negative,
        '中性': neutral
    }

    print(f"情感分析: 积极 {positive} 消极 {negative} 中性 {neutral}")

    return df, sentiment_dist

def trend_analysis(df):
    df['评论时间'] = pd.to_datetime(df['评论时间'])
    df['日期'] = df['评论时间'].dt.date

    daily_counts = df.groupby('日期').size()
    trend_data = {str(date): int(count) for date, count in daily_counts.items()}

    print(f"趋势分析完成 {len(trend_data)} 天")

    return trend_data

def save_analysis_results(word_freq, sentiment_dist, trend_data, output_dir='data'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    results = {
        'word_frequency': word_freq,
        'sentiment_distribution': sentiment_dist,
        'trend_data': trend_data
    }

    output_file = os.path.join(output_dir, 'analysis_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"分析结果已保存到 {output_file}")

def analyze_data(input_file='data/cleaned_data.csv'):
    print("开始数据分析...")

    df = pd.read_csv(input_file, encoding='utf-8-sig')
    print(f"读取到 {len(df)} 条清洗后的数据")

    word_freq = text_analysis(df)
    df, sentiment_dist = sentiment_analysis(df)
    trend_data = trend_analysis(df)

    save_analysis_results(word_freq, sentiment_dist, trend_data)

    df.to_csv('data/analyzed_data.csv', index=False, encoding='utf-8-sig')

    return word_freq, sentiment_dist, trend_data

def main():
    analyze_data()
    print("数据分析完成")

if __name__ == '__main__':
    main()
