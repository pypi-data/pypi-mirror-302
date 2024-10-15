```1.1 本地代码运行
下载代码包
export PYTHONPATH=$(pwd)
python app/main.py --queue default

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
