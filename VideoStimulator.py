from moviepy import *
import streamlit as st
import ffmpeg
def combine_videos(input_file):
    top_clip = VideoFileClip(input_file)
    bottom_clip = VideoFileClip("Subway.mp4")
    final_clip = VideoFileClip("input_file")
    new_height = top_clip.size[1] // 2
    scale_factor = new_height / float(top_clip.size[1])
    top_clip_resized = top_clip.resized(scale_factor)

    if top_clip.duration > bottom_clip.duration:
        num_repeats = int(bottom_clip.duration / top_clip.duration) + 1

        # Create a list of repeated video clips
        repeated_clips = [bottom_clip] * num_repeats

        # Concatenate the repeated clips to create the final video
        final_clip = concatenate_videoclips(repeated_clips, method="compose")

        # Trim the final concatenated clip to the desired duration
        final_clip = final_clip.subclipped(0, top_clip.duration)
    elif bottom_clip.duration >top_clip.duration:
        bottom_clip = bottom_clip.subclipped(0,top_clip.duration)
    bottom_clip_resized =final_clip.resized(width=top_clip_resized.w)

    final = clips_array([[top_clip_resized], [bottom_clip_resized]])
    final.write_videofile("output.mp4", codec="libx264")

def main():
    st.title("Subway Surfer It!")
    st.subheader("Lecture videos too boring? Need a way to make videos more engaging? SubwaySurferIt!\n\nThis app serves as a byproduct of ongoing work building agentic AI for short form video automation.")
    uploaded_file = st.file_uploader("Upload your video")
    st.text("Made with love by Cyrus Correll")
    if not uploaded_file:
        st.button("Upload Media To Begin", disabled=True)
    else:
        st.markdown(
            """
            <style>
            .gradient-button {
                background: linear-gradient(45deg, #ff7e5f, #feb47b);
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                cursor: pointer;
                font-size: 1rem;
                border-radius: 0.25rem;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        if st.button("Subway Surfer It!"):
            with open("temp_input.mp4", "wb") as f:
                f.write(uploaded_file.read())
            combine_videos("temp_input.mp4")
            progress_bar=st.progress(0)
            for i in range(101):
                time.sleep(0.01)
                progress_bar.progress(i)
            st.video("output.mp4")
            with open("output.mp4", "rb") as vid_file:
                st.download_button("Download Video", vid_file, file_name="output.mp4", mime="video/mp4")

if __name__ == "__main__":
    main()