import streamlit as st
import moviepy.editor as mp
import tempfile
import os

st.title("?? AI Video Editor Prototype")

st.write("Upload a video (20–30 mins) and AI will remove silent parts + add text overlay.")

# Upload video
video_file = st.file_uploader("Upload your video", type=["mp4", "mov", "avi", "mkv"])

if video_file:
    # Save upload temporarily
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    st.video(tfile.name)

    if st.button("? Edit Video"):
        with st.spinner("Processing video... this may take a while ?"):
            # Load video
            clip = mp.VideoFileClip(tfile.name)

            # Simple: trim first 60 seconds (demo) instead of AI silence removal
            # (You can replace with AI-based silence detection later)
            edited = clip.subclip(0, min(60, clip.duration))

            # Add text overlay
            txt = mp.TextClip("? Edited by AI ?", fontsize=50, color="white")
            txt = txt.set_duration(edited.duration).set_position(("center", "bottom"))

            final = mp.CompositeVideoClip([edited, txt])

            # Export final
            out_path = os.path.join(tempfile.gettempdir(), "edited_video.mp4")
            final.write_videofile(out_path, codec="libx264")

            st.success("? Video Edited Successfully!")
            st.video(out_path)
