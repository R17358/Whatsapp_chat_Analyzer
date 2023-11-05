import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s'
    matches = re.findall(pattern, data)
    message = re.split(pattern, data)[1:]

    dates = [match.split(', ')[0] for match in matches]
    times = [match.split(', ')[1].split('\u202f')[0] for match in matches]

    df = pd.DataFrame({
        'user_msg': message,
        'date': dates,
        'time': times
    })
    #print(df)
    user = []
    msg = []
    for i in df['user_msg']:
        x = re.split("([\w\W]+?):\s", i)
        if x[1:]:
            user.append(x[1])
            msg.append(x[2])
        else:
            user.append("Group Notification")
            msg.append(x[0])

    df['user'] = user
    df['msg'] = msg
    df.drop(columns=['user_msg'], inplace=True)

    # Specify the date format as 'd%m%Y' to avoid parsing issues
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df['year'] = df['date'].dt.year.astype(str)
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format the date as %d%m%Y

    return df
