from abc import ABC, abstractmethod
from typing import List

# ====================== 清洗策略（入库）======================
class CleanStrategy(ABC):
    """清洗策略基类"""
    @abstractmethod
    def clean(self, raw_content: str) -> str:
        pass

class InboundCleanStrategy(CleanStrategy):
    """入库清洗：minhash去重 + embedding去重"""
    def clean(self, raw_content: str) -> str:
        # TODO: 这里你可以接入真实 minhash / embedding 模型
        # 当前为示例实现
        cleaned = f"[已清洗-minhash+embedding去重] {raw_content[:50]}..."
        return cleaned

# ====================== 采样策略（出库）======================
class SamplingStrategy(ABC):
    """采样策略基类"""
    @abstractmethod
    def sample(self, item_list: List, n: int) -> List:
        pass

class ExecutableSampling(SamplingStrategy):
    """可执行物采样策略：随机采样或按权重采样"""
    def sample(self, items: List, n: int) -> List:
        if len(items) <= n:
            return items
        # 示例：取前n个，你可替换为 random.sample(items, n) 或其他逻辑
        return items[:n]

class TaskSampling(SamplingStrategy):
    """任务采样策略：按时间倒序采样（最新任务优先）"""
    def sample(self, items: List, n: int) -> List:
        if len(items) <= n:
            return items
        # 示例：取后n个（最新创建的）
        return items[-n:]

class TrajectorySampling(SamplingStrategy):
    """轨迹采样策略：步长采样（均匀分布）"""
    def sample(self, items: List, n: int) -> List:
        if len(items) <= n:
            return items
        # 示例：步长采样，均匀分布
        step = max(1, len(items) // n)
        return items[::step][:n]
