import pandas as pd
import json
import uuid
import time

# Step 1: 加载数据集
df = pd.read_json("hf://datasets/AdaptLLM/finance-tasks/ConviFinQA/test.json")

# 提取问题和答案对
def extract_qa_pairs(df):
    results = []
    for _, row in df.iterrows():
        question = row['input']
        answer = row['label']
        # 生成唯一标识符
        unique_id = str(uuid.uuid4())
        # 保存为结构化的 JSON 格式
        result = {
            "id": unique_id,
            "Question": question.strip(),
            "Answer": answer.strip(),
        }
        results.append(result)
    return results

# 开始计时
start_time = time.time()

# 提取问题-答案对
results = extract_qa_pairs(df)

# 结束计时
end_time = time.time()

# 计算提取到的问题-答案对数量
total_pairs = len(results)

# 将结果保存为 JSON 文件
with open('reformatted_dataset.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)

# 输出统计信息
print(f"Total question-answer pairs extracted: {total_pairs}")
print(f"Time taken: {end_time - start_time} seconds")
