# app/service/task_service.py

import json
import shlex
import subprocess
from app.service.util_service import UtilService
from pathlib import Path

class TaskService:
    
    @staticmethod
    def task_run(data):
        """
        处理任务运行逻辑
        """
        print(f"data: {data}")
        # 执行脚本文件
        # 使用 subprocess.Popen 让命令在后台执行
        coldplay_config = UtilService.load_coldplay_config()
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')
        project_url = f"{apiserver_host}/{data['code_url'].strip('/')}"
        script_run_url = data['script_run_url']
        script_name = data['script_name']
        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
        print(f"project_url:{project_url} script_run_url_new:{script_run_url_new}")
        project_url = shlex.quote(project_url)
        script_run_url_new = shlex.quote(script_run_url_new)

        # 获取当前文件所在路径
        current_file = Path(__file__).resolve()
        # 获取项目根目录app目录
        project_app_root = current_file.parent.parent # 假设项目目录在上级
        process = subprocess.Popen(["bash", f"{project_app_root}/scripts/run_task.sh", project_url, script_run_url_new])
        print(f"执行成功")

        return True
    
    @staticmethod
    def task_stop():
        """
        处理任务终止逻辑
        """
        print(f"stop run")
        # 执行脚本文件
        # 使用 subprocess.Popen 让命令在后台执行
        # 获取当前文件所在路径
        current_file = Path(__file__).resolve()
        # 获取项目根目录app目录
        project_app_root = current_file.parent.parent  # 假设项目目录在上级
        subprocess.Popen(["bash", f"{project_app_root}/scripts/stop_task.sh"])
        print(f"执行成功")

        return True