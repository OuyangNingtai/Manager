#!/usr/bin/env python3
"""
轨迹生成管理系统 - 主入口示例

运行此文件将演示完整的流程：
1. 创建可执行物（Skill）
2. 入库清洗并存储
3. 创建环境和任务
4. 生成轨迹并存储
5. 出库采样
"""

from models.executable import SkillExecutable
from models.environment import SimpleEnvironment
from models.task import Task
from models.trajectory import Trajectory
from manager.trajectory_manager import TrajectoryManager


def main():
    # 1. 创建管理器
    print("=" * 60)
    print("🚀 轨迹生成管理系统启动")
    print("=" * 60)
    
    manager = TrajectoryManager()

    # 2. 创建 Skill（模拟从 skill.md 读取）
    print("\n📝 创建可执行物 (Skill)...")
    skill1 = SkillExecutable(
        exe_id="skill_001",
        name="问诊技能",
        file_path="skills/medical_consultation.md",
        material_files=["materials/patient_history.txt", "materials/symptoms.pdf"],
        raw_content="这是从 skill.md 读取的内容：医生问诊流程，包括初步询问、症状分析、诊断建议..."
    )
    
    skill2 = SkillExecutable(
        exe_id="skill_002",
        name="处方技能",
        file_path="skills/prescription.md",
        material_files=["materials/drug_database.txt"],
        raw_content="这是从 skill.md 读取的内容：根据诊断结果开具处方，包括药物选择、剂量计算..."
    )

    # 3. 存储并自动入库清洗
    print("🧹 对可执行物进行入库清洗...")
    manager.store_executable(skill1)
    manager.store_executable(skill2)
    print(f"✅ 已存储 {len(manager.executables)} 个可执行物")

    # 4. 创建环境（医院场景）
    print("\n🏥 创建环境 (Hospital Scene)...")
    env = SimpleEnvironment(env_id="env_hospital_001", scene="hospital")
    print(f"✅ 环境创建完成：{env.env_id}, 场景：{env.scene}")

    # 5. 创建任务（模型根据多个 skill 生成）
    print("\n📋 创建任务 (Task)...")
    task = Task(
        task_id="task_001",
        name="医院完整问诊任务",
        executables=[skill1, skill2],
        environment=env,
        raw_content="模型生成的任务：患者主诉头痛发热，需要进行完整问诊流程并开具处方..."
    )
    manager.store_task(task)
    print(f"✅ 任务已存储并清洗：{task.name}")

    # 6. 生成轨迹（模型根据 Task + Skill.md + 材料文件生成）
    print("\n📊 生成轨迹 (Trajectory)...")
    trajectory = Trajectory(
        traj_id="traj_001",
        task=task,
        skill_md_content=skill1.raw_content + "\n" + skill2.raw_content,
        raw_data="""
        轨迹步骤记录：
        Step 1: 接收患者主诉 - 头痛、发热 38.5°C
        Step 2: 询问病史 - 无过敏史，近期有接触感冒患者
        Step 3: 症状分析 - 上呼吸道感染可能性大
        Step 4: 诊断建议 - 血常规检查
        Step 5: 开具处方 - 退烧药 + 抗生素
        Step 6: 医嘱 - 多休息，多喝水，3 天后复诊
        """
    )
    manager.store_trajectory(trajectory)
    print(f"✅ 轨迹已存储并清洗：{trajectory.traj_id}")

    # 7. 查看统计信息
    print("\n📈 当前存储统计:")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"   - {key}: {value}")

    # 8. 出库采样（不同实体使用不同策略）
    print("\n🎯 出库采样演示:")
    
    sampled_exec = manager.sample_executables(1)
    print(f"   - 可执行物采样 (取 1 个): {sampled_exec[0].name if sampled_exec else '无'}")
    
    sampled_task = manager.sample_tasks(1)
    print(f"   - 任务采样 (取 1 个): {sampled_task[0].name if sampled_task else '无'}")
    
    sampled_traj = manager.sample_trajectories(1)
    print(f"   - 轨迹采样 (取 1 个): {sampled_traj[0].traj_id if sampled_traj else '无'}")

    # 9. 查询演示
    print("\n🔍 查询演示:")
    found_skill = manager.get_executable_by_id("skill_001")
    if found_skill:
        print(f"   - 找到可执行物：{found_skill.name}, 清洗状态：{found_skill.is_clean_inbound}")
    
    found_task = manager.get_task_by_id("task_001")
    if found_task:
        print(f"   - 找到任务：{found_task.name}, 清洗状态：{found_task.is_clean_inbound}")

    print("\n" + "=" * 60)
    print("✅ 所有操作完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
