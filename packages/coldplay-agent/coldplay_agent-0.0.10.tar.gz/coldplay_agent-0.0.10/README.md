```1.1 本地代码运行
下载代码包
export PYTHONPATH=$(pwd)
python app/main.py --queue mytest

```1.2 pip安装包运行（建议）
1.2.1安装coldplay_agent
安装默认版本：pip install coldplay_agent
安装指定版本：pip install coldplay_agent=0.0.3

1.2.2查看coldplay_agent版本
运行指令：pip show coldplay_agent

1.2.3初始化coldplay_agent数据
运行指令：coldplayagent-init 
程序会提示用户输入Enter your userinfo: example:{"apiserver_host":"http://172.16.10.24"}
在输入栏下输入：{"apiserver_host":"http://172.16.10.24"}
http://172.16.10.24这个是样例，实际输入以API server地址为准
运行成功进入下一步

1.2.4运行coldplay_agent
运行指令：coldplayagent --queue mytest
其中--queue是队列名称，用于跟APIserver的通信

2.查看训练进程是否启动
cd 训练项目目录下
ps aux | grep 'python legged_gym/scripts/train.py --task=pointfoot_rough'

3.pip打包
如果存在旧版本，使用以下命令卸载：
pip uninstall my_package
重新生成.tar.gz和.whl文件：
python setup.py sdist bdist_wheel

安装新的版本
pip install dist/my_package-0.0.1-py3-none-any.whl

上传到PyPI（可选）
pip install twine
twine upload dist/*

