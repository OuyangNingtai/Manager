from typing import List, Optional
from models.executable import Executable
from models.task import Task
from models.trajectory import Trajectory
from manager.strategies import (
    InboundCleanStrategy,
    ExecutableSampling,
    TaskSampling,
    TrajectorySampling
)

class TrajectoryManager:
    """轨迹生成管理器：核心中控，负责串联生产 -> 清洗 -> 存储 -> 出库全流程"""
    
    def __init__(self):
        # 存储区（模拟数据库）
        self.executables: List[Executable] = []
        self.tasks: List[Task] = []
        self.trajectories: List[Trajectory] = []

        # 策略初始化
        self.inbound_clean = InboundCleanStrategy()
        self.samplers = {
            "executable": ExecutableSampling(),
            "task": TaskSampling(),
            "trajectory": TrajectorySampling()
        }

    # ====================== 入库清洗（统一方法）======================
    def clean_inbound_executable(self, exe: Executable) -> None:
        """对可执行物进行入库清洗"""
        exe.clean_content = self.inbound_clean.clean(exe.raw_content)
        exe.is_clean_inbound = True

    def clean_inbound_task(self, task: Task) -> None:
        """对任务进行入库清洗"""
        task.clean_content = self.inbound_clean.clean(task.raw_content)
        task.is_clean_inbound = True

    def clean_inbound_trajectory(self, traj: Trajectory) -> None:
        """对轨迹进行入库清洗"""
        traj.clean_data = self.inbound_clean.clean(traj.raw_data)
        traj.is_clean_inbound = True

    # ====================== 存储 ======================
    def store_executable(self, exe: Executable) -> None:
        """存储可执行物并自动进行入库清洗"""
        self.clean_inbound_executable(exe)
        self.executables.append(exe)

    def store_task(self, task: Task) -> None:
        """存储任务并自动进行入库清洗"""
        self.clean_inbound_task(task)
        self.tasks.append(task)

    def store_trajectory(self, traj: Trajectory) -> None:
        """存储轨迹并自动进行入库清洗"""
        self.clean_inbound_trajectory(traj)
        self.trajectories.append(traj)

    # ====================== 出库采样 ======================
    def sample_executables(self, n: int) -> List[Executable]:
        """采样可执行物"""
        return self.samplers["executable"].sample(self.executables, n)

    def sample_tasks(self, n: int) -> List[Task]:
        """采样任务"""
        return self.samplers["task"].sample(self.tasks, n)

    def sample_trajectories(self, n: int) -> List[Trajectory]:
        """采样轨迹"""
        return self.samplers["trajectory"].sample(self.trajectories, n)

    # ====================== 查询方法 ======================
    def get_executable_by_id(self, exe_id: str) -> Optional[Executable]:
        """根据 ID 查询可执行物"""
        for exe in self.executables:
            if exe.exe_id == exe_id:
                return exe
        return None

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """根据 ID 查询任务"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_trajectory_by_id(self, traj_id: str) -> Optional[Trajectory]:
        """根据 ID 查询轨迹"""
        for traj in self.trajectories:
            if traj.traj_id == traj_id:
                return traj
        return None

    # ====================== 统计信息 ======================
    def get_stats(self) -> dict:
        """获取当前存储统计信息"""
        return {
            "executables_count": len(self.executables),
            "tasks_count": len(self.tasks),
            "trajectories_count": len(self.trajectories)
        }
