from dataclasses import dataclass, field
from models.task import Task

@dataclass
class Trajectory:
    """轨迹类：记录任务执行过程中的全链路数据"""
    traj_id: str
    task: Task               # 关联任务
    skill_md_content: str    # skill.md 内容
    raw_data: str            # 模型生成的原始轨迹
    clean_data: str = ""
    is_clean_inbound: bool = False
    metadata: dict = field(default_factory=dict)
