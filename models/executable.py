from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Executable:
    """可执行物基类：Skill / Tool / MCP"""
    exe_id: str
    name: str
    exe_type: str  # skill / tool / mcp
    file_path: str  # skill.md 路径
    material_files: List[str]  # 自带材料文件
    raw_content: str  # md原文内容
    clean_content: str = ""  # 清洗后内容
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 入库清洗标记
    is_clean_inbound: bool = False

class SkillExecutable(Executable):
    """Skill 类型可执行物"""
    def __init__(self, exe_id, name, file_path, material_files, raw_content):
        super().__init__(
            exe_id=exe_id,
            name=name,
            exe_type="skill",
            file_path=file_path,
            material_files=material_files,
            raw_content=raw_content
        )

# Tool、MCP 子类可以同样扩展
class ToolExecutable(Executable):
    def __init__(self, exe_id, name, file_path, material_files, raw_content):
        super().__init__(
            exe_id=exe_id, name=name, exe_type="tool",
            file_path=file_path, material_files=material_files,
            raw_content=raw_content
        )

class MCPExecutable(Executable):
    def __init__(self, exe_id, name, file_path, material_files, raw_content):
        super().__init__(
            exe_id=exe_id, name=name, exe_type="mcp",
            file_path=file_path, material_files=material_files,
            raw_content=raw_content
        )
