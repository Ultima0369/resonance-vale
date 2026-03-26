@echo off
REM 对话整理定时任务
REM 每天自动整理新的对话记录

echo ========================================
echo 璇玑-星尘对话整理定时任务
echo 开始时间: %date% %time%
echo ========================================

REM 切换到脚本目录
cd /d "C:\Users\lgdln\.openclaw\workspace\tools"

REM 运行对话整理工作流
python conversation_workflow.py

echo ========================================
echo 任务完成时间: %date% %time%
echo ========================================

REM 暂停查看结果（调试时使用）
REM pause