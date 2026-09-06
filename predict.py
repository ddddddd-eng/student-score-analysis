import pandas as pd
import joblib
pipeline=joblib.load('student_score_pipeline.pkl')
def predict_score(study_hours,sleep_hours,attendance):
    new_student = pd.DataFrame({
        'study_hours': [study_hours],
        'sleep_hours': [sleep_hours],
        'attendance': [attendance]
    })

    predicted_score = pipeline.predict(new_student)
    return round(predicted_score[0],2)
def get_user_input():
    while True:
        try:
            study_hours=float(input('请输入学习时长:'))
            sleep_hours=float(input('请输入睡眠时长:'))
            attendance=float(input('请输入出勤率:'))
            if study_hours<0 or study_hours>24:
                print('学习时长应在0-24小时之间')
                continue
            if sleep_hours<0 or sleep_hours>24:
                print('睡眠时长应在0-24小时之间')
                continue
            if attendance<0 or attendance>100:
                print('出勤率应在0-100之间')
                continue
            return study_hours,sleep_hours,attendance
        except ValueError:
            print('输入错误，请输入数字')
def main():
    study_hours,sleep_hours,attendance=get_user_input()
    score=predict_score(
        study_hours,
        sleep_hours,
        attendance
    )
    print('预测分数为:',score)
if __name__ == "__main__":
    main()
