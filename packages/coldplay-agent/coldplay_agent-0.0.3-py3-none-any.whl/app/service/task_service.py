# app/service/task_service.py

import json
import shlex
import subprocess
from app.service.util_service import UtilService

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
        project_url = f"{apiserver_host}/dev-api/{data['code_url'].strip('/')}"
        script_run_url = data['script_run_url']
        script_name = data['script_name']
        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
        print(f"project_url:{project_url} script_run_url_new:{script_run_url_new}")
        project_url = shlex.quote(project_url)
        script_run_url_new = shlex.quote(script_run_url_new)

        process = subprocess.Popen(["bash", "/home/yons/work/www/coldplay_agent/app/run_task.sh", project_url, script_run_url_new])
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
        subprocess.Popen(["bash", "/home/yons/work/www/coldplay_agent/app/stop_task.sh"])
        print(f"执行成功")

        return True