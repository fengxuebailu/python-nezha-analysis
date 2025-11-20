# -*- coding: utf-8 -*-
import pandas as pd
import re
import os

def remove_duplicates(df):
    before_count = len(df)
    df = df.drop_duplicates(subset=['评论内容'], keep='first')
    after_count = len(df)
    print(f"去除重复评论: {before_count - after_count} 条")
    return df

def clean_text(text):
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、；：""''（）\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_data(input_file='data/raw_data.csv', output_file='data/cleaned_data.csv'):
    print("开始处理数据...")

    df = pd.read_csv(input_file, encoding='utf-8-sig')
    print(f"读取到 {len(df)} 条原始数据")

    df = remove_duplicates(df)

    df['评论内容'] = df['评论内容'].apply(clean_text)

    df = df[df['评论内容'].str.len() > 0]

    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"清洗后数据保存到 {output_file}")
    print(f"最终保留 {len(df)} 条数据")

    return output_file

def main():
    process_data()
    print("数据清洗完成")

if __name__ == '__main__':
    main()
