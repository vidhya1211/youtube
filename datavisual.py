import googleapiclient.discovery
import streamlit as st
import pandas as pd
import datetime
import isodate
import json
import sqlite3

# API connection
def Api_connect():
    Api_Id="AIzaSyAiaHRP1_jvLvsczmw75yDEUUpcnfN44sc"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=Api_Id)
    return youtube
youtube=Api_connect()

# Find the channel details
def channel_info(channel_id):
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=channel_id
    )
    response = request.execute()
    
    for i in response['items']:
        data= dict(channel_name=i['snippet']['title'],
                   Channel_Id=i['id'],
                   Subscribers=i['statistics']['subscriberCount'],
                   Views=i['statistics']['viewCount'],
                   Total_Videos=i['statistics']['videoCount'],
                   Channel_description=i['snippet']['description'],
                   Playlist_Id=i['contentDetails']['relatedPlaylists']['uploads'])
    return data

# create the dataframe of playlist
def find_playlists(channel_id):
    playlist_info=[]

    response=youtube.channels().list(id=channel_id,
                                    part='contentDetails'
                                    ).execute()
    Playlist_Id= response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token=None

    while True:
        response1=youtube.playlistItems().list(
                                            part='snippet',
                                            playlistId=Playlist_Id,
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
        for i in (response1['items']):
            my_dict=dict(channel_id=i['snippet']['channelId'],
                        playlist_id=i['snippet']['playlistId'],
                        video_id=i['snippet']['resourceId']['videoId'])
            playlist_info.append(my_dict)
            next_page_token=response1.get('nextPageToken')
        if next_page_token is None:
                break
    df=pd.DataFrame(playlist_info)
    
    return df

# Find the video_ids
def find_videos_id(channel_id):
    video_info=[]
    response=youtube.channels().list(id=channel_id,
                                     part='contentDetails'
                                     ).execute()
    Playlist_Id= response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token=None

    while True:
        response1=youtube.playlistItems().list(
                                            part='snippet',
                                            playlistId=Playlist_Id,
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
        for i in range(len(response1['items'])):
            video_info.append(response1['items'][i]['snippet']['resourceId']['videoId'])
            next_page_token=response1.get('nextPageToken')
        if next_page_token is None:
                break
    return video_info

#create the dataframe of video_details
def find_video_table(video_ids):
     video_data=[]
     for video_details in video_ids:
          request = youtube.videos().list(
                                   part='snippet,contentDetails,statistics',
                                   id=video_details
          )
          response=request.execute()
          
          for i in response["items"]:
               publish_date_str = i['snippet']['publishedAt']
               publish_date = datetime.datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%SZ')
               formatted_publish_date = publish_date.strftime('%Y-%m-%d %H:%M:%S')
               dur = isodate.parse_duration(i['contentDetails']['duration'])
               duration_seconds = dur.total_seconds()
               duration_hms = str(datetime.timedelta(seconds=duration_seconds))
               my_data=dict(Channel_Name=i['snippet']['channelTitle'],
                         channel_id=i['snippet']['channelId'],
                         Video_Id=i['id'],
                         Title=i['snippet']['title'],
                         Tags=i['snippet'].get('tags'),
                         Thumbnail=i['snippet']['thumbnails']['default']['url'],
                         Description=i['snippet'].get('description'),
                         PPublished_At= formatted_publish_date,
                         Duration_HMS= duration_hms,
                         Duration= duration_seconds,
                         Views=int(i['statistics'].get('viewCount')),
                         Likes=int(i['statistics'].get('likeCount')),
                         Comments=int(i['statistics'].get('commentCount')),
                         Favorite_count=int(i['statistics']['favoriteCount']),
                         Definition=i['contentDetails']['definition'],
                         Caption_Status=i['contentDetails']['caption']
                         )
               video_data.append(my_data)
     df1=pd.DataFrame(video_data)
     video_data['views'] = pd.to_numeric(video_data['views'], errors='coerce') 
     return df1


# Find the video_details
def find_video_info(video_ids):
     video_data=[]
     for video_details in video_ids:
          request = youtube.videos().list(
                                   part='snippet,contentDetails,statistics',
                                   id=video_details
          )
          response=request.execute()
          for i in response["items"]:
               duration = i['contentDetails']['duration']
               duration_seconds = isodate.parse_duration(duration).total_seconds()
               data=dict(Channel_Name=i['snippet']['channelTitle'],
                         channel_id=i['snippet']['channelId'],
                         Video_Id=i['id'],
                         Title=i['snippet']['title'],
                         Tags=i['snippet'].get('tags'),
                         Thumbnail=i['snippet']['thumbnails']['default']['url'],
                         Description=i['snippet'].get('description'),
                         Published_At=i['snippet']['publishedAt'],
                         Duration=duration_seconds,
                         Views=i['statistics'].get('viewCount'),
                         Likes=i['statistics'].get('likeCount'),
                         Comments=i['statistics'].get('commentCount'),
                         Favorite_count=i['statistics']['favoriteCount'],
                         Definition=i['contentDetails']['definition'],
                         Caption_Status=i['contentDetails']['caption']
                         )
               video_data.append(data)
     return video_data

# Create the dataframe of comment_details
def find_comment_table(Comment_detail):
    Comment_data=[]
    try:
        for video_id in Comment_detail:
            request=youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50
            )
            response = request.execute()

            for i in response['items']:
                data1=dict(Comment_Id=i['snippet']['topLevelComment']['id'],
                          Video_Id=i['snippet']['topLevelComment']['snippet']['videoId'],
                          Comment_Text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
                          Comment_Author=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                          Comment_Published=i['snippet']['topLevelComment']['snippet']['publishedAt'])
                Comment_data.append(data1)
        df2=pd.DataFrame(Comment_data)    
        return df2
    except:
        pass
    return Comment_data

#find the comment_details
def find_comment_info(Comment_detail):
    Comment_data=[]
    try:
        for video_id in Comment_detail:
            request=youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50
            )
            response = request.execute()

            for i in response['items']:
                data=dict(Comment_Id=i['snippet']['topLevelComment']['id'],
                          Video_Id=i['snippet']['topLevelComment']['snippet']['videoId'],
                          Comment_Text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
                          Comment_Author=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                          Comment_Published=i['snippet']['topLevelComment']['snippet']['publishedAt'])
                Comment_data.append(data)

    except:
        pass
    return Comment_data

# Function to get Channel_details
def main():
    st.title(":red[YOUTUBE HARVESTING AND WAREHOUSING]")
    st.header("DATA COLLECTION")
    st.write("This Data collection zone can collect data by using channel id  and gives all the channel details,playlist details,comment details and video details")

                       
    youtube = Api_connect()

    channel_id_input_placeholder = 'channel_id_input'
    channel_id = st.text_input('Enter the Channel ID', key=channel_id_input_placeholder)

    if st.button("GET DETAILS"):
        playlist = find_videos_id(channel_id)
        video_data= find_video_info(playlist)
        comment_data= find_comment_info(playlist)
        channel_data = channel_info(channel_id)
    

        if isinstance(channel_data, dict):
                channel_data = {key: [value] for key, value in channel_data.items()}

        st.subheader("Channel Details")
        st.write(pd.DataFrame(channel_data))

        st.subheader("Video Details")
        st.write(pd.DataFrame(video_data))

        st.subheader("Comment Details")
        st.write(pd.DataFrame(comment_data))

        st.subheader("Playlist Details")
        st.write(pd.DataFrame(playlist))
if __name__ == "__main__":
    main()

#SQLITE3 connection configuration
def create_table(connection):
        cursor = connection.cursor()
        channel_table_query='''create table if not exists channels(channel_name varchar(100),
                                                        Channel_Id varchar(80) primary key,
                                                        Subscribers bigint,
                                                        Views bigint,
                                                        Total_Videos bigint,
                                                        Channel_description text,
                                                        playlist_id varchar(80))'''
        cursor.execute(channel_table_query)
        connection.commit()
        playlist_table_query='''create table if not exists vd(Channel_Id varchar(100),
                                                    Playlist_Id varchar(100),
                                                    Video_id varchar(80) primary key)'''
        cursor.execute(playlist_table_query)
        connection.commit()

        video_table_query='''create table if not exists videos(Channel_Name varchar(100),
                                                        channel_id varchar(100),
                                                        Video_Id varchar(30) primary key,
                                                        Title varchar(150),
                                                        Tags text,
                                                        Thumbnail varchar(200),
                                                        Description text,
                                                        Published_At datetime,
                                                        Duration_HMS Varchar(20),
                                                        Duration int,
                                                        Views bigint,
                                                        Likes bigint,
                                                        Comments int,
                                                        Favorite_count int,
                                                        Definition varchar(10),
                                                        Caption_Status varchar(50))'''
        cursor.execute(video_table_query)
        connection.commit()
        comment_table_query='''create table if not exists comments(Comment_Id varchar(255),
                                                                Video_Id varchar(255),
                                                                Comment_Text text primary key,
                                                                Comment_Author varchar(150),
                                                                Comment_Published datetime)'''
        cursor.execute(comment_table_query)
        connection.commit()
        try:
               cursor.execute(channel_table_query)
               cursor.execute(video_table_query)
               cursor.execute(comment_table_query)
               cursor.execute(playlist_table_query)
               connection.commit()
               print("Tables created successfully in sqlite3")
        except sqlite3.Error as e:
                print("Error creating tables in sqlite3:", e)
                connection.rollback()
        finally:
                cursor.close()

# Insert the table details
def insert_channel_info(connection,channel_data):
    cursor = connection.cursor()
    try:
        insert_query= '''INSERT OR IGNORE INTO channels(channel_name,Channel_Id,Subscribers,Views,Total_Videos,Channel_description,Playlist_Id) VALUES(?,?,?,?,?,?,?)'''
        values = (channel_data['channel_name'], channel_data['Channel_Id'], channel_data['Subscribers'], channel_data['Views'], channel_data['Total_Videos'], channel_data['Channel_description'], channel_data['Playlist_Id'])
        cursor.execute(insert_query,values)
        connection.commit()
        print("Channel table inserted into sqlite3 successfully!")
    except sqlite3.Error as e:
        print("Error inserting channel info into sqlite3:", e)
        connection.rollback()
    finally:
        cursor.close()



def insert_video_data(connection, video_data):
    cursor = connection.cursor()
    try:
        if isinstance(video_data, pd.DataFrame):
            insert_query= '''INSERT OR IGNORE INTO videos(Channel_Name,channel_id,Video_Id,Title,Tags,Thumbnail,Description, Published_At,Duration_HMS, Duration,Views,Likes, Comments,Favorite_count,Definition,Caption_Status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            for __,row in video_data.iterrows():
                row['Tags'] = json.dumps(row['Tags'])
                values=(row['Channel_Name'],row['channel_id'], row['Video_Id'],row['Title'],row['Tags'], row['Thumbnail'],row['Description'],row['Published_At'],row.get('Duration_HMS',None), row['Duration'],row['Views'],row['Likes'], row['Comments'],row['Favorite_count'],row['Definition'], row['Caption_Status'])
                cursor.execute(insert_query,values)
            connection.commit()
            print("videos table inserted into sqlite3 successfully!")
        else:
             print("video_data is not a DataFrame!")       
    except sqlite3.Error as e:
        print("Error inserting video data into sqlite3:", e)
        connection.rollback()
        
    finally:       
            cursor.close()

def insert_comment_data(connection, comment_data):
    cursor = connection.cursor()
    try:
        if isinstance(comment_data, pd.DataFrame):
            insert_query= '''INSERT OR IGNORE INTO comments(Comment_Id,Video_Id,Comment_Text,Comment_Author,Comment_Published) VALUES(?,?,?,?,?)'''
            for __,row in comment_data.iterrows():
                values=(row['Comment_Id'],row['Video_Id'], row['Comment_Text'],row['Comment_Author'],row['Comment_Published'])
                cursor.execute(insert_query,values)
            connection.commit()
            print("Comments table inserted into sqlite3 successfully!")
        else:
             print("comment_data is not a DataFrame!") 
    except sqlite3.Error as e:
        print("Error inserting comment data into sqlite3:", e)
        connection.rollback()
    finally:
        cursor.close()

#Function to insert channel details into SQLITE3 database
def main():
    st.title(":red[MIGRATION TO SQLITE3]")

    youtube = Api_connect()

    channel_id = st.text_input('Enter the Channel ID')

    if st.button("Migrate Data"):
        playlist_data =find_videos_id(channel_id)
        video_data=pd.DataFrame(find_video_info( playlist_data))
        comment_data= pd.DataFrame(find_comment_info( playlist_data))
        channel_data = channel_info(channel_id)
        connection = sqlite3.connect("mydatabase.db")
        if connection is not None:
            create_table(connection)
            insert_channel_info(connection, channel_data)
            insert_video_data(connection, video_data)
            insert_comment_data(connection, comment_data)
            

            connection.close()

            st.success("Data migrated to SQLITE3 successfully!")

if __name__ == "__main__":
    main()

with st.sidebar:
    st.header("*Domain*")
    st.markdown("- Social Media\n")
    st.header("*Skills From This Project*")
    st.markdown("- Python scripting\n- Data Collection\n- Streamlit\n- API Intergration\n- Sqlite3 ")
    st.header("*About Project*") 
    st.markdown("- Building a simple UI with streamlit, retrieving data from youtube API,migrating to a Sqlite3 data warehouse, querying the data warehouse with Sqlite3, and displaying the data in streamlit app")

#Queries and results
def execute_query(query):
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data

st.title(":red[QUERIES AND RESULTS]")
question = st.selectbox("Select Your Question To Display The Query",
                        ("1.What are the names of all the videos and their corresponding channels?",
                        "2.Which channels have the most number of videos, and how many videos do they have?",
                        "3.What are the top 10 most viewed videos and their respective channels?",
                        "4.How many comments were made on each video, and what are their corresponding video names?",
                        "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
                        "6.What is the total number of likes for each video, and what are their corresponding video names?",
                        "7.What is the total number of views for each channel, and what are their corresponding channel names?",
                        "8.What are the names of all the channels that have published videos in the year 2022?",
                        "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                        "10.Which videos have the highest number of comments, and what are their corresponding channel names?"),
                        )

if question=="1.What are the names of all the videos and their corresponding channels?":
    query1='''select Title as videos, channel_name as channelname from videos'''
    data = execute_query(query1)
    df=pd.DataFrame(data,columns=["video title", "channel name"])
    st.write(df)
    
elif question=="2.Which channels have the most number of videos, and how many videos do they have?":
    query2='''select channel_name as channelname, total_videos as No_videos from channels
                order by total_videos desc '''
    data = execute_query(query2)
    df1=pd.DataFrame(data,columns=["channelname", "No of videos"])
    st.write(df1)

elif question=="3.What are the top 10 most viewed videos and their respective channels?":
    query3='''select Views as view, channel_name as channelname, title as videotitle from videos 
                where views is not null order by views desc limit 10'''
    data = execute_query(query3)
    df2=pd.DataFrame(data,columns=["view", "channelname", "videotitle"])
    st.write(df2)

elif question=="4.How many comments were made on each video, and what are their corresponding video names?":
    query4='''select comments as no_comments, title as videotitle from videos where comments is not null'''
    data = execute_query(query4)
    df3=pd.DataFrame(data,columns=["no of comments", "videotitle"])
    st.write(df3)

elif question=="5.Which videos have the highest number of likes, and what are their corresponding channel names?":
    query5='''select title as videotitle, channel_name as channelname, likes as likescount from videos
                where likes is not null order by likes desc'''
    data = execute_query(query5)
    df4=pd.DataFrame(data,columns=["videotitle", "channelname", "likescount"])
    st.write(df4)

elif question=="6.What is the total number of likes for each video, and what are their corresponding video names?":
    query6='''select likes as likescount, title as videotitle from videos'''
    data = execute_query(query6)
    df5=pd.DataFrame(data,columns=["likescount", "videotitle"])
    st.write(df5)

elif question=="7.What is the total number of views for each channel, and what are their corresponding channel names?":
    query7='''select channel_name as channelname, views as totalviews from channels'''
    data = execute_query(query7)
    df6=pd.DataFrame(data,columns=["channelname", "totalviews"])
    st.write(df6)

elif question=="8.What are the names of all the channels that have published videos in the year 2022?":
    query8='''SELECT DISTINCT channel_name as channelname 
                FROM videos 
                WHERE strftime('%Y', Published_At) = '2022' '''
    data = execute_query(query8)
    df7=pd.DataFrame(data,columns=[ "channelname"])
    st.write(df7)

elif question=="9.What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    query9='''select channel_name as channelname, avg(Duration) as average_duration from videos group by channel_name'''
    data = execute_query(query9)
    df8=pd.DataFrame(data,columns=["channelname", "average_duration"])
    df8['average_duration'] = pd.to_timedelta(df8['average_duration'], unit='s')
    st.write(df8)

elif question=="10.Which videos have the highest number of comments, and what are their corresponding channel names?":
    query10='''select title as video_title, channel_name as channelname, comments as comments from videos 
                    where comments is not null order by comments desc'''
    data = execute_query(query10)
    df9=pd.DataFrame(data,columns=["video_title", "channelname","comments" ])
    st.write(df9)