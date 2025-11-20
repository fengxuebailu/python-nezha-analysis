# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
import os

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_wordcloud(word_freq, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    wordcloud = WordCloud(
        font_path='simhei.ttf',
        width=800,
        height=600,
        background_color='white'
    ).generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('哪吒评论词云图', fontsize=20)

    output_file = os.path.join(output_dir, 'wordcloud.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"词云图已保存到 {output_file}")

def create_sentiment_pie(sentiment_dist, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    labels = list(sentiment_dist.keys())
    sizes = list(sentiment_dist.values())
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.1, 0, 0)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('评论情感分布', fontsize=16)

    output_file = os.path.join(output_dir, 'sentiment_pie.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"情感饼图已保存到 {output_file}")

def create_trend_line(trend_data, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dates = list(trend_data.keys())
    counts = list(trend_data.values())

    plt.figure(figsize=(12, 6))
    plt.plot(dates, counts, marker='o', linestyle='-', linewidth=2, markersize=6)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('评论数量', fontsize=12)
    plt.title('评论热度趋势', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(output_dir, 'trend_line.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"趋势折线图已保存到 {output_file}")

def visualize_data(input_file='data/analysis_results.json'):
    print("开始数据可视化...")

    with open(input_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    word_freq = results['word_frequency']
    sentiment_dist = results['sentiment_distribution']
    trend_data = results['trend_data']

    create_wordcloud(word_freq)
    create_sentiment_pie(sentiment_dist)
    create_trend_line(trend_data)

    print("数据可视化完成")

def main():
    visualize_data()

if __name__ == '__main__':
    main()
