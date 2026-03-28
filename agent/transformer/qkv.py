import numpy as np

# ===== 1️⃣ 输入（3个词，每个词4维向量）=====
# shape: (3, 4)
# 3 = 词的数量（序列长度）
# 4 = embedding 维度
X = np.array([
    [1.0, 0.0, 1.0, 0.0],  # 猫
    [0.0, 1.0, 0.0, 1.0],  # 吃
    [1.0, 1.0, 0.0, 0.0]   # 鱼
])

# ===== 2️⃣ 初始化权重（模型参数）=====
# 实际中这些是训练学出来的，这里用随机数模拟

np.random.seed(42)  # 固定随机种子，保证每次结果一样

# W_Q: 用来生成 Query 的权重矩阵
# shape: (4, 4) → 输入维度4 → 输出维度4
W_Q = np.random.rand(4, 4)

# W_K: 用来生成 Key 的权重矩阵
W_K = np.random.rand(4, 4)

# W_V: 用来生成 Value 的权重矩阵
W_V = np.random.rand(4, 4)


# ===== 3️⃣ 计算 Q K V =====
# Q: Query（我想找什么）
# K: Key（我有什么特征）
# V: Value（我提供什么信息）

# X @ W_Q → (3,4) @ (4,4) = (3,4)
Q = X @ W_Q

# 每个词都会生成一个 Q 向量
K = X @ W_K
V = X @ W_V


# ===== 4️⃣ 计算 Attention 分数 =====
# scores[i][j] 表示：
# 第 i 个词（Query） 对 第 j 个词（Key）的关注程度

# Q @ K.T → (3,4) @ (4,3) = (3,3)
scores = Q @ K.T


# ===== 5️⃣ 缩放（Scaling）=====
# dk = Key 向量的维度（这里是 4）
dk = K.shape[1]

# 防止数值过大（Transformer 标准做法）
scores = scores / np.sqrt(dk)


# ===== 6️⃣ softmax（转概率）=====
def softmax(x):
    # x: (3,3) 的分数矩阵

    # 防止指数爆炸（数值稳定技巧）
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))

    # 每一行归一化（每个词对所有词的关注权重）
    return exp_x / exp_x.sum(axis=1, keepdims=True)

# weights: Attention 权重
# shape: (3,3)
weights = softmax(scores)

# 含义：
# weights[i][j] = 第 i 个词对第 j 个词的关注比例


# ===== 7️⃣ 加权求和（核心输出）=====
# output[i] = 所有 V 的加权平均
# shape: (3,4)
output = weights @ V

# (3,3) @ (3,4) = (3,4)

# 含义：
# 每个词的新表示 = 按 attention 权重融合所有词的信息


# ===== 打印结果 =====
print("Q（Query）:\n", Q)
print("\nK（Key）:\n", K)
print("\nV（Value）:\n", V)

print("\nAttention 分数（未归一化）:\n", scores)
print("\nAttention 权重（softmax后）:\n", weights)
print("\n最终输出（融合后的向量）:\n", output)