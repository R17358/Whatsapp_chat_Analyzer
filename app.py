import re
import pandas as pd
import streamlit as st
import preprocessor
import functions
import matplotlib.pyplot as plt

# Define the Streamlit app title
st.sidebar.title('WhatsApp Chat Analyzer')

# File upload widget
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp Chat Export File")

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the uploaded file as a string
    data = uploaded_file.read().decode('utf-8')

    # Preprocess the chat data
    df = preprocessor.preprocess(data)
    print(df)
    # Get unique users for analysis
    user_details = df['user'].unique().tolist()

    # Remove 'Group Notification' from user list
    user_details = [user for user in user_details if user != 'Group Notification']
        # Sort user list and add 'Overall' option
    user_details.sort()
    user_details.insert(0, 'Overall')
    print(user_details)

    # Select user for analysis
    selected_user = st.sidebar.selectbox('Show Analysis as:', user_details)

    # Analyze button
    if st.sidebar.button('Analyse'):
        # Fetch statistics for the selected user
        num_msgs, words, num_med, link = functions.fetch_stats(selected_user, df)

        # Display basic statistics
        st.title('OverAll Basic Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.subheader(num_msgs)
        with col2:
            st.header('Total Words')
            st.subheader(words)
        with col3:
            st.header('Media Shared')
            st.subheader(num_med)
        with col4:
            st.header('Link Shares')
            st.subheader(link)

        # Display monthly timeline
        timeline = functions.monthly_timeline(selected_user, df)
        print(timeline)
        st.title('Monthly Timeline')
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['msg'], color='maroon')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Display daily timeline
        timeline = functions.daily_timeline(selected_user, df)
        st.title('Daily Timeline')
        fig, ax = plt.subplots()
        ax.plot(timeline['date'], timeline['msg'], color='purple')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Display activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        
        # Analyze and display most active month and day
        active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list = functions.activity_map(selected_user, df)
        
        with col1:
            st.header('Most Active Month')
            fig, ax = plt.subplots()
            ax.bar(active_month_df['month'], active_month_df['msg'])
            ax.bar(month_list[month_msg_list.index(max(month_msg_list))], max(month_msg_list), color='green', label='Highest')
            ax.bar(month_list[month_msg_list.index(min(month_msg_list))], min(month_msg_list), color='red', label='Lowest')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header('Most Active Day')
            fig, ax = plt.subplots()
            ax.bar(active_day_df['day'], active_day_df['msg'])
            ax.bar(day_list[day_msg_list.index(max(day_msg_list))], max(day_msg_list), color='green', label='Highest')
            ax.bar(day_list[day_msg_list.index(min(day_msg_list))], min(day_msg_list), color='red', label='Lowest')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # Analyze and display most active users if 'Overall' is selected
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, percent = functions.most_chaty(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x, color='cyan')
                st.pyplot(fig)
            with col2:
                st.dataframe(percent)

        # Create and display word cloud
        df_wc = functions.create_wordcloud(selected_user, df)
        st.title('Most Common Words')
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
