from dataclasses import dataclass
from abc import ABC, abstractmethod

class BaseEnvironment(ABC):
    """环境基类（接口），别人负责实现"""
    env_id: str
    scene: str  # 场景：hospital / finance 等

    @abstractmethod
    def get_readonly_access(self):
        """只读接口"""
        pass

    @abstractmethod
    def get_readwrite_access(self):
        """读写接口"""
        pass

@dataclass
class SimpleEnvironment(BaseEnvironment):
    """示例环境，仅占位"""
    env_id: str
    scene: str

    def get_readonly_access(self):
        return f"readonly_{self.env_id}"

    def get_readwrite_access(self):
        return f"readwrite_{self.env_id}"
