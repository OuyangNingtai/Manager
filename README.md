# 轨迹生成管理系统 (Trajectory Generation Management System) 示例

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



