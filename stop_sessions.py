from pyrogram.client import Client

# Function to stop a Pyrogram session
def stop_session(session_name):
    try:
        app = Client(session_name)
        app.stop()
        print(f"Session '{session_name}' stopped successfully.")
    except Exception as e:
        print(f"Error stopping session '{session_name}': {e}")

# Loop over session files in the "sessions/" directory
def stop_all_sessions():
    import os

    sessions_directory = "old_sessions/"
    for session_file in os.listdir(sessions_directory):
        if session_file.endswith(".session"):
            session_name = session_file[:-8]  # Remove the ".session" extension
            stop_session(session_name)

# Example usage
stop_all_sessions()
