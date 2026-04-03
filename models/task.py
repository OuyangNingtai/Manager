from dataclasses import dataclass, field
from typing import List
from models.executable import Executable
from models.environment import BaseEnvironment

@dataclass
class Task:
    """任务类：由多个同类可执行物组成，绑定一个环境"""
    task_id: str
    name: str
    executables: List[Executable]  # 多个同类可执行物
    environment: BaseEnvironment   # 绑定一个环境
    raw_content: str               # 模型生成的原始任务
    clean_content: str = ""
    is_clean_inbound: bool = False
    metadata: dict = field(default_factory=dict)
