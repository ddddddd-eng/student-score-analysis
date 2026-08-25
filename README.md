# Student Score Analysis

一个使用 Python 和 pandas 完成的学生成绩数据清洗与分析项目。
## 项目功能
- 读取学生成绩 CSV 数据
- 清洗缺失值、异常成绩和重复数据
- 自动生成成绩等级和是否及格字段
- 统计平均分、中位数、最高分和最低分
- 生成成绩排行榜和 Top 3
- 按班级分析人数、平均分和及格率
- 按性别分析人数、平均分和中位数
- 使用 IQR 方法检测异常成绩
- 导出清洗后的数据和班级汇总结果
## 数据文件
- `students.csv`：原始学生成绩数据，包含姓名、成绩、性别和班级等字段。
- `students_clean.csv`：清洗后的学生数据。
- `class_summary.csv`：各班人数、平均分和及格率的汇总结果。
## 如何运行
1. 安装 Python 3.10 或以上版本。

2. 安装 pandas：

```bash
pip install pandas
```

3. 进入项目文件夹：

```powershell
cd student_score_analysis
```

4. 运行程序：

```powershell
python main.py
```

程序运行后，会在项目文件夹中生成：

- `students_clean.csv`
- `class_summary.csv`