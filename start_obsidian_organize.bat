@echo off
echo 璇玑 - Obsidian 仓库整理启动工具
echo ========================================

echo.
echo 步骤1: 查看当前状况
echo ----------------------------------------
echo 已创建的分析报告:
echo   1. obsidian_analysis_report.md - 详细分析报告
echo   2. obsidian_manual_organize_guide.md - 手动整理指南
echo.

echo 步骤2: 新文件夹结构
echo ----------------------------------------
echo 已创建以下文件夹结构:
echo   00-索引/     - 导航和索引文件
echo   01-日记/     - 个人日记和时间记录
echo   02-项目/     - 项目和任务管理
echo   03-知识/     - 知识库和概念定义
echo   04-对话/     - 对话记录和交流
echo   05-创作/     - 创作内容和作品
echo   06-资源/     - 参考资料和素材
echo   07-人物/     - 人物档案和联系
echo   08-模板/     - 模板和格式文件
echo   99-归档/     - 归档和旧文件
echo.

echo 步骤3: 选择整理方式
echo ----------------------------------------
echo 请选择整理方式:
echo   1. 手动整理 (推荐) - 按照指南逐步整理
echo   2. 查看分析报告 - 了解详细状况
echo   3. 打开仓库文件夹 - 开始手动整理
echo   4. 打开整理指南 - 查看详细说明
echo.

set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 手动整理建议:
    echo   1. 先整理日期格式文件 (YYYY-MM-DD.md)
    echo   2. 再整理对话文件 (*对话*.md)
    echo   3. 然后整理概念文件 (*概念*.md)
    echo   4. 最后整理其他文件
    echo.
    echo 详细步骤请查看: obsidian_manual_organize_guide.md
    echo.
    set /p open="是否打开整理指南? (y/n): "
    if /i "%open%"=="y" (
        start obsidian_manual_organize_guide.md
    )
) else if "%choice%"=="2" (
    echo.
    echo 打开分析报告...
    start obsidian_analysis_report.md
) else if "%choice%"=="3" (
    echo.
    echo 打开仓库文件夹...
    explorer "D:\LDD\璇玑台"
) else if "%choice%"=="4" (
    echo.
    echo 打开整理指南...
    start obsidian_manual_organize_guide.md
) else (
    echo 无效选项
)

echo.
echo 提示:
echo   1. 整理前建议先备份重要文件
echo   2. 可以分多次整理，不要一次性整理所有文件
echo   3. 整理后记得更新内部链接
echo   4. 创建索引页面方便导航
echo.

pause