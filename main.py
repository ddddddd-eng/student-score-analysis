import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
def load_and_clean_data(filename):
    df = pd.read_csv(filename)
    df['score']=pd.to_numeric(df['score'], errors='coerce')
    df.loc[(df['score'] < 0) | (df['score'] > 100), 'score'] = pd.NA
    df['name'] = df['name'].str.strip()
    df['gender'] = df['gender'].str.strip()
    df['class'] = df['class'].str.strip()
    df['gender']=df['gender'].replace({'男生':'男','女生':'女'})
    df['class'] = df['class'].replace({
        '1班': '一班',
        '二 班': '二班'
    })
    return df
def prepare_final_data(df):
    df['level']=df['score'].apply(get_level)
    df['passed']=df['score']>=60
    final_df=(
        df[['name','score','level','gender','class','passed']]
        .dropna(subset=['name','score'])
        .drop_duplicates()
        .reset_index(drop=True)
    )
    return final_df
def find_outliers_iqr(data):
    q1=data.quantile(0.25)
    q3=data.quantile(0.75)
    iqr=q3-q1
    lower_bound=q1-1.5*iqr
    upper_bound=q3+1.5*iqr
    outliers=data[(data<lower_bound)|(data>upper_bound)]
    return outliers
def get_level(score):
    if pd.isna(score):
        return '缺失'
    elif score>=90:
        return '优秀'
    elif score>=80:
        return '良好'
    elif score>=60:
        return '及格'
    else:
        return '不及格'
def analyse_classes(final_df):
    class_mean=final_df.groupby('class')['score'].mean().round(2)
    class_count=final_df.groupby('class')['name'].count()
    class_passed_rate=final_df.groupby('class')['passed'].mean()*100
    class_summary=pd.DataFrame({
        '人数':class_count,
        '平均分':class_mean,
        '及格率':class_passed_rate.round(2)
    })
    class_order=['一班','二班','三班']
    class_summary=class_summary.reindex(class_order)
    best_class=class_mean.idxmax()
    best_score=class_mean.max().round(2)
    return class_summary,best_class,best_score
def analyse_gender(final_df):
    gender_mean=final_df.groupby('gender')['score'].mean()
    gender_count=final_df.groupby('gender')['name'].count()
    gender_median=final_df.groupby('gender')['score'].median()
    return gender_mean,gender_count,gender_median
def analyse_levels(final_df):
    level_counts=final_df['level'].value_counts()
    level_rate=(final_df['level'].value_counts(normalize=True)*100).round(2)
    group_mean=final_df.groupby('level')['score'].mean().round(2)
    passed_count=final_df['passed'].sum()
    passed_rate=final_df['passed'].mean()*100
    return level_counts,level_rate,group_mean,passed_count,passed_rate
def print_outlier_summary(df):
    valid_score=df['score'].dropna()
    outliers=find_outliers_iqr(valid_score)
    if outliers.empty:
        print('无异常数据')
    else:
        print('异常数据为:',outliers)
def print_basic_summary(df,final_df):
    print('原始数据行数:',len(df))
    print('清洗后的行数:',len(final_df))
    print('清洗掉的行数:',len(df)-len(final_df))
    retention_rate=len(final_df)/len(df)*100
    print('数据保留率为:',round(retention_rate,2),'%')
    print('清洗后平均分：', final_df['score'].mean().round(2))
    print('清洗后最高分：', final_df['score'].max())
    print('清洗后最低分：', final_df['score'].min())
def print_ranking(final_df):
    sorted_df=final_df.sort_values(by='score',ascending=False)
    print('从高到低排列:')
    print(sorted_df)
    top3=sorted_df[['name','score','gender','class']].head(3).reset_index(drop=True)
    top3.index=top3.index+1
    top3.index.name='排名'
    print('前三名:',top3)
def print_score_statistics(final_df):
    print(final_df['score'].describe().round(2))
    print('平均分:',final_df['score'].mean().round(2))
    print('中位数:',final_df['score'].median())
def print_level_summary(final_df):
    level_counts,level_rate,group_mean,passed_count,passed_rate=analyse_levels(final_df)
    disply_level_counts=level_counts.rename({
        '及格':'及格档'
    })
    print('各等级人数:')
    print(disply_level_counts)
    display_level_rate = level_rate.rename({
        '及格': '及格档'
    })
    print('各等级比例:')
    print(display_level_rate)
    display_group_mean = group_mean.rename({
        '及格': '及格档'
    })
    print('各等级平均分:')
    print(display_group_mean)
    print('总及格人数:',passed_count)
    print('总及格率:',round(passed_rate,2),'%')
def print_class_summary(final_df):
    class_summary,best_class,best_score=analyse_classes(final_df)
    print('班级汇总表：')
    print(class_summary)
    print('平均分最高的班：', best_class)
    print('此班平均分为：', best_score)
    return class_summary
def print_gender_summary(final_df):
    gender_mean,gender_count,gender_median=analyse_gender(final_df)
    print('男女平均成绩为:',gender_mean.round(2))
    print('男女各自人数为:',gender_count)
    print('男女中位数为:',gender_median)
def plot_class_average(final_df):
    class_order=['一班','二班','三班']
    class_mean=final_df.groupby('class')['score'].mean().reindex(class_order)
    class_mean.plot(kind='bar', rot=0)
    plt.title('各班平均成绩')
    plt.xlabel('班级')
    plt.ylabel('平均成绩')
    plt.savefig(
        'figures/class_average.png',
        dpi=300,
        bbox_inches='tight'
    )
    plt.show()
def plot_score_distribution(final_df):
    plt.hist(final_df['score'], bins=5, edgecolor='black')
    plt.title('学生成绩分布')
    plt.xlabel('成绩')
    plt.ylabel('人数')
    mean_score=final_df['score'].mean()
    median_score=final_df['score'].median()
    plt.axvline(mean_score, linestyle='--', label='平均分')
    plt.axvline(median_score, linestyle=':', label='中位数')
    plt.legend()
    plt.savefig(
        'figures/score_distribution.png',
        dpi=300,
        bbox_inches='tight'
    )
    plt.show()
def plot_score_boxplot(final_df):
    plt.boxplot(final_df['score'], showmeans=True)
    plt.title('学生成绩箱线图')
    plt.ylabel('成绩')
    plt.savefig(
        'figures/score_boxplot.png',
        dpi=300,
        bbox_inches='tight'
    )
    plt.show()
def save_results(final_df,class_summary):
    final_df.to_csv(
        'students_clean.csv',index=False,encoding='utf-8-sig'
        )
    class_summary.to_csv(
        'class_summary.csv',encoding='utf-8-sig'
        )
    print('分析结果已保存')
def main():
    df = load_and_clean_data('students.csv')
    print_outlier_summary(df)
    final_df=prepare_final_data(df)
    print_basic_summary(df,final_df)
    print_ranking(final_df)
    print_score_statistics(final_df)
    print_level_summary(final_df)
    class_summary=print_class_summary(final_df)   
    print_gender_summary(final_df)
    plot_class_average(final_df)
    plot_score_distribution(final_df)
    plot_score_boxplot(final_df)
    save_results(final_df,class_summary)
if __name__=="__main__":
    main()

