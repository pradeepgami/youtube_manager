import sqlite3
import streamlit as st
import pandas as pd

# Database connection
conn = sqlite3.connect("youtube_videos.db", check_same_thread=False)
cursor = conn.cursor()

# Table creation
cursor.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time TEXT NOT NULL,
    UNIQUE(name, time)
)
""")
conn.commit()

# Functions
def list_videos():
    cursor.execute("SELECT * FROM videos")
    return cursor.fetchall()

def add_video(name, time):
    try:
        cursor.execute("INSERT INTO videos (name, time) VALUES (?, ?)", (name, time))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def update_video(video_id, new_name, new_time):
    cursor.execute("UPDATE videos SET name = ?, time = ? WHERE id = ?", (new_name, new_time, video_id))
    conn.commit()
    return cursor.rowcount

def delete_video(video_id):
    cursor.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    return cursor.rowcount

# Streamlit UI
st.title("🎬 YouTube Video Manager")

menu = ["List Videos", "Add Video", "Update Video", "Delete Video"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "List Videos":
    st.subheader("All Videos")
    videos = list_videos()
    if videos:
        # Row numbers + data
        data = []
        for i, (vid_id, name, time) in enumerate(videos, start=1):
            data.append((i, name, time))
        df = pd.DataFrame(data, columns=["S.No", "Video Name", "Video Time"])
        st.table(df)
    else:
        st.info("No videos found.")


elif choice == "Add Video":
    st.subheader("Add New Video")
    name = st.text_input("Video Name")
    time = st.text_input("Video Time")
    if st.button("Add"):
        if name and time:
            if add_video(name, time):
                st.success("✅ Video Added Successfully!")
            else:
                st.warning("⚠️ This video already exists.")
        else:
            st.warning("⚠️ Please enter both Name and Time.")

elif choice == "Update Video":
    st.subheader("Update Video")
    video_id = st.number_input("Video ID", step=1)
    new_name = st.text_input("New Name")
    new_time = st.text_input("New Time")
    if st.button("Update"):
        if new_name and new_time:
            rows = update_video(video_id, new_name, new_time)
            if rows > 0:
                st.success("✅ Video Updated Successfully!")
            else:
                st.warning("⚠️ No video found with that ID.")
        else:
            st.warning("⚠️ Please enter both New Name and New Time.")

elif choice == "Delete Video":
    st.subheader("Delete Video")
    video_id = st.number_input("Video ID to Delete", step=1)
    if st.button("Delete"):
        rows = delete_video(video_id)
        if rows > 0:
            st.error("🗑️ Video Deleted Successfully!")
        else:
            st.warning("⚠️ No video found with that ID.")
