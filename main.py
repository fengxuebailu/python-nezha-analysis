# -*- coding: utf-8 -*-
import data_collector
import data_processor
import data_analyzer
import data_visualizer
import os

def print_banner():
    print("=" * 50)
    print("      哪吒电影评论分析系统")
    print("=" * 50)
    print()

def main():
    print_banner()

    print("[1/4] 数据采集阶段")
    print("-" * 50)
    data_collector.main()
    print()

    print("[2/4] 数据清洗阶段")
    print("-" * 50)
    data_processor.main()
    print()

    print("[3/4] 数据分析阶段")
    print("-" * 50)
    data_analyzer.main()
    print()

    print("[4/4] 数据可视化阶段")
    print("-" * 50)
    data_visualizer.main()
    print()

    print("=" * 50)
    print("所有任务已完成")
    print("=" * 50)
    print("\n结果文件位置:")
    print(f"  - 原始数据: data/raw_data.csv")
    print(f"  - 清洗数据: data/cleaned_data.csv")
    print(f"  - 分析结果: data/analysis_results.json")
    print(f"  - 词云图: output/wordcloud.png")
    print(f"  - 情感饼图: output/sentiment_pie.png")
    print(f"  - 趋势折线图: output/trend_line.png")
    print()

if __name__ == '__main__':
    main()
