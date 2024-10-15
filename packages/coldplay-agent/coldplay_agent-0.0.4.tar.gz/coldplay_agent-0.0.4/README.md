```1.运行
export PYTHONPATH=$(pwd)
python app/main.py --queue default

2.查看训练进程是否启动
cd 训练项目目录下
ps aux | grep 'python legged_gym/scripts/train.py --task=pointfoot_rough'
