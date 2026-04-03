# 轨迹生成管理系统 (Trajectory Generation Management System)

一个用于管理可执行物、任务、环境和轨迹生成的完整系统，支持入库清洗和出库采样功能。

## 项目结构

```
project_root/
├── models/                  # 核心实体定义
│   ├── __init__.py
│   ├── executable.py        # 可执行物 (Skill/Tool/MCP)
│   ├── environment.py       # 环境接口
│   ├── task.py              # 任务类
│   └── trajectory.py        # 轨迹类
├── manager/
│   ├── __init__.py
│   ├── strategies.py        # 清洗和采样策略
│   └── trajectory_manager.py # 核心管理器
├── main.py                  # 入口示例
└── README.md                # 本文件
```

## 核心功能

### 1. 可执行物 (Executable)
- **类型**: Skill / Tool / MCP
- **来源**: skill.md 文件 + 自带材料文件
- **处理**: 入库清洗 (MinHash 去重 + Embedding 去重)
- **出库**: 专属采样方法

### 2. 环境 (Environment)
- **职责**: 为任务提供数据读写的上下文隔离
- **设计**: 抽象接口，由外部实现具体逻辑
- **场景**: hospital, finance 等

### 3. 任务 (Task)
- **生成**: 大模型根据多个同类可执行物自动生成
- **关联**: 1 个任务 ↔ 1 个环境
- **处理**: 入库清洗 (去重)
- **出库**: 专属采样

### 4. 轨迹 (Trajectory)
- **生成**: 大模型根据 Task + Skill.md + 材料文件生成
- **内容**: 记录任务执行过程中的全链路数据
- **处理**: 入库清洗 (去重)
- **出库**: 专属采样

## 快速开始

### 安装依赖
```bash
# 本项目使用 Python 标准库，无需额外依赖
python --version  # 建议 Python 3.8+
```

### 运行示例
```bash
python main.py
```

### 代码示例

```python
from models.executable import SkillExecutable
from models.environment import SimpleEnvironment
from models.task import Task
from models.trajectory import Trajectory
from manager.trajectory_manager import TrajectoryManager

# 创建管理器
manager = TrajectoryManager()

# 创建 Skill
skill = SkillExecutable(
    exe_id="skill_001",
    name="问诊技能",
    file_path="skills/medical.md",
    material_files=["materials/data.txt"],
    raw_content="医生问诊流程..."
)

# 存储并自动清洗
manager.store_executable(skill)

# 创建环境和任务
env = SimpleEnvironment(env_id="env_001", scene="hospital")
task = Task(
    task_id="task_001",
    name="问诊任务",
    executables=[skill],
    environment=env,
    raw_content="任务内容..."
)
manager.store_task(task)

# 生成轨迹
trajectory = Trajectory(
    traj_id="traj_001",
    task=task,
    skill_md_content=skill.raw_content,
    raw_data="轨迹数据..."
)
manager.store_trajectory(trajectory)

# 出库采样
sampled_skills = manager.sample_executables(1)
sampled_tasks = manager.sample_tasks(1)
sampled_trajectories = manager.sample_trajectories(1)
```

## 策略模式

### 入库清洗策略
- `InboundCleanStrategy`: MinHash 去重 + Embedding 去重
- 可扩展其他清洗策略

### 出库采样策略
- `ExecutableSampling`: 可执行物采样（默认取前 N 个）
- `TaskSampling`: 任务采样（默认取最新 N 个）
- `TrajectorySampling`: 轨迹采样（默认步长均匀采样）

## 扩展开发

### 添加新的可执行物类型
```python
class NewExecutable(Executable):
    def __init__(self, exe_id, name, file_path, material_files, raw_content):
        super().__init__(
            exe_id=exe_id, name=name, exe_type="new_type",
            file_path=file_path, material_files=material_files,
            raw_content=raw_content
        )
```

### 实现自定义清洗策略
```python
from manager.strategies import CleanStrategy

class CustomCleanStrategy(CleanStrategy):
    def clean(self, raw_content: str) -> str:
        # 实现你的清洗逻辑
        return cleaned_content
```

### 实现自定义环境
```python
from models.environment import BaseEnvironment

class CustomEnvironment(BaseEnvironment):
    def __init__(self, env_id, scene, db_connection):
        self.env_id = env_id
        self.scene = scene
        self.db_conn = db_connection
    
    def get_readonly_access(self):
        return self.db_conn.readonly()
    
    def get_readwrite_access(self):
        return self.db_conn.readwrite()
```

## TODO

- [ ] 集成真实的 MinHash 去重算法
- [ ] 集成 Embedding 模型进行语义去重
- [ ] 连接真实数据库存储
- [ ] 添加异步处理支持
- [ ] 添加日志记录
- [ ] 添加单元测试

## License

MIT
