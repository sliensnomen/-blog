import os
import shutil
from fastapi import APIRouter, Request

router = APIRouter()

# 动态定位 Manager 根目录
CURRENT_API_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_API_DIR, "..", ".."))

# 1️⃣ 文章数据目录 (先清空目标，再全量复制 —— 文章数据以 Manager 为准)
SYNC_DIRS = ["posts", "chatters", "moments"]

# 2️⃣ 共享页面目录 (只覆盖 Manager 有的文件，保留目标独有的文件)
SYNC_APP_DIRS = [
    "about", "chatter", "friends", "moments", "music",
    "photowall", "posts", "projects", "timeline", "tree",
    "api/test", "api/weather"
]

# 3️⃣ app/ 根级文件
SYNC_APP_FILES = ["page.tsx", "layout.tsx", "globals.css"]

# 4️⃣ components/ 排除列表 (管理后台组件不同步)
# Navbar.tsx 在两个项目中功能不同（XHBlogs 纯博客 vs Manager 带后台入口），也不同步
EXCLUDE_COMPONENTS = ["editor", "settings"]
EXCLUDE_COMPONENT_FILES = ["Navbar.tsx"]

# 5️⃣ 其他根级文件
SYNC_ROOT_FILES = [
    "data/albums.ts",
    "data/friends.ts",
    "data/projects.ts",
    "siteConfig.ts"
]

# 6️⃣ 说说/关于我等特殊内容文件
SYNC_CONTENT_FILES = [
    "app/about/about.md"
]


def is_safe_blog_dir(target_path):
    """防呆检测：只有包含 package.json 的才被认为是安全的博客目录"""
    return os.path.exists(os.path.join(target_path, "package.json"))


def sync_directory_contents(src_dir, dst_dir, exclude_subdirs=None, exclude_files=None):
    """
    同步目录内容：复制源目录的所有文件到目标目录，
    保留目标目录中独有的文件（不删除）。
    """
    if not os.path.exists(src_dir):
        return

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    exclude_files = exclude_files or []

    for root, dirs, files in os.walk(src_dir):
        # 排除指定子目录
        if exclude_subdirs:
            dirs[:] = [d for d in dirs if d not in exclude_subdirs]

        rel_path = os.path.relpath(root, src_dir)

        for file in files:
            if file in exclude_files:
                continue

            src_file = os.path.join(root, file)
            if rel_path == '.':
                dst_file = os.path.join(dst_dir, file)
            else:
                dst_file = os.path.join(dst_dir, rel_path, file)

            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)


@router.post("/check")
async def check_blog_path(request: Request):
    """检测目标路径是否合法且具备基本结构"""
    try:
        payload = await request.json()
        target_path = payload.get("blogPath", "").strip()

        if not target_path or not os.path.exists(target_path):
            return {"success": False, "message": "🚫 目标物理路径不存在，请检查输入！"}

        if not is_safe_blog_dir(target_path):
            return {"success": False,
                    "message": "⚠️ 危险！目标路径未检测到 package.json，似乎不是一个有效的前端项目，已拦截操作。"}

        missing = []
        for d in ["posts", "data", "app"]:
            if not os.path.exists(os.path.join(target_path, d)):
                missing.append(d)

        if missing:
            return {"success": True,
                    "message": f"✅ 路径安全。但目标缺失以下文件夹：{', '.join(missing)}。同步时将自动创建。"}

        return {"success": True, "message": "✅ 路径校验通过，目录结构完美！"}
    except Exception as e:
        return {"success": False, "message": f"校验异常: {str(e)}"}


@router.post("/execute")
async def execute_sync(request: Request):
    """执行物理覆盖同步"""
    try:
        payload = await request.json()
        target_path = payload.get("blogPath", "").strip()

        if not is_safe_blog_dir(target_path):
            return {"success": False, "message": "安全拦截：目标路径不合法！"}

        # 1️⃣ 同步文章数据 (先彻底删除目标文件夹，再把 Manager 的复制过去)
        for d in SYNC_DIRS:
            src_dir = os.path.join(PROJECT_ROOT, d)
            dst_dir = os.path.join(target_path, d)

            if os.path.exists(src_dir):
                if os.path.exists(dst_dir):
                    shutil.rmtree(dst_dir)
                shutil.copytree(src_dir, dst_dir)

        # 2️⃣ 同步共享页面目录 (保留目标独有的文件)
        for d in SYNC_APP_DIRS:
            src_dir = os.path.join(PROJECT_ROOT, "app", d)
            dst_dir = os.path.join(target_path, "app", d)
            sync_directory_contents(src_dir, dst_dir)

        # 3️⃣ 同步 app/ 根级文件
        for f in SYNC_APP_FILES:
            src_file = os.path.join(PROJECT_ROOT, "app", f)
            dst_file = os.path.join(target_path, "app", f)
            if os.path.exists(src_file):
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)

        # 4️⃣ 同步 components/ (排除管理后台组件和 Navbar.tsx)
        src_components = os.path.join(PROJECT_ROOT, "components")
        dst_components = os.path.join(target_path, "components")
        sync_directory_contents(src_components, dst_components, exclude_subdirs=EXCLUDE_COMPONENTS, exclude_files=EXCLUDE_COMPONENT_FILES)

        # 5️⃣ 同步其他根级文件
        for f in SYNC_ROOT_FILES:
            src_file = os.path.join(PROJECT_ROOT, f.replace("/", os.sep))
            dst_file = os.path.join(target_path, f.replace("/", os.sep))

            if os.path.exists(src_file):
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)

                # 🌟 核心过滤逻辑：如果是 siteConfig.ts，拦截并剔除敏感信息
                if os.path.basename(f) == "siteConfig.ts":
                    with open(src_file, "r", encoding="utf-8") as file_in:
                        lines = file_in.readlines()

                    with open(dst_file, "w", encoding="utf-8") as file_out:
                        for line in lines:
                            if "picBedName:" in line or "picBedUrl:" in line or "picBedToken:" in line or "图床核心配置" in line:
                                continue
                            file_out.write(line)
                else:
                    shutil.copy2(src_file, dst_file)

        # 6️⃣ 同步特殊内容文件（关于我、图库配置等）
        for f in SYNC_CONTENT_FILES:
            src_file = os.path.join(PROJECT_ROOT, f.replace("/", os.sep))
            dst_file = os.path.join(target_path, f.replace("/", os.sep))
            if os.path.exists(src_file):
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)

        return {"success": True, "message": "🎉 完美撒花！所有文章、页面代码与配置已同步至目标博客。"}
    except Exception as e:
        return {"success": False, "message": f"同步过程中发生致命错误: {str(e)}"}
