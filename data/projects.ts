// 🛡️ 本文件由控制台自动生成，请勿手动修改

export type Project = {
  id: string;
  name: string;
  description: string;
  icon: string;
  githubUrl: string;
  tags: string[];
};

export const projectsData: Project[] = [
  {
    "id": "proj_1775049332705",
    "name": "Computational Chemistry Tool",
    "githubUrl": "https://github.com/heiehiehi/Computational_Chemistry_Tool",
    "description": "整合 GROMACS 分析流程的小工具集，包含 RMSF、RMSD、氢键分析等常用脚本，个人在 WSL2 + Ubuntu 22 环境下使用。",
    "icon": "🧪",
    "tags": [
      "Gromacs",
      "RMSF",
      "Python"
    ]
  },
  {
    "id": "proj_1779210456123",
    "name": "DungeonDice",
    "githubUrl": "",
    "description": "一个正在开发中的 Godot 地牢探险小品，回合制战斗 + 随机房间生成，目前进度：能跑能跳的小方块。",
    "icon": "🎲",
    "tags": [
      "Godot",
      "GDScript",
      "独立游戏"
    ]
  },
  {
    "id": "proj_1779210678901",
    "name": "AI NPC Engine",
    "githubUrl": "",
    "description": "为跑团场景设计的 AI NPC 对话引擎，接入 Gemini API，支持带上下文和人格限制的即兴对话。",
    "icon": "🎭",
    "tags": [
      "AI",
      "D&D",
      "FastAPI"
    ]
  },
  {
    "id": "proj_1779210892345",
    "name": "XHBlogs 部署脚本",
    "githubUrl": "",
    "description": "为 XHBlogs 写的 systemd 开机自启方案和一键启动脚本，让本地博客可以稳定运行在 3000/39998 端口。",
    "icon": "🚀",
    "tags": [
      "Next.js",
      "systemd",
      "Shell"
    ]
  },
];