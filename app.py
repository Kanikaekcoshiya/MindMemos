import streamlit as st
from file_utils import process_file, export_to_pdf
from db import get_history, save_history, save_feedback
from auth import add_user, login_user
from datetime import datetime

#APP UI 
st.set_page_config(page_title="MindMemos", page_icon="📝", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_history" not in st.session_state:
    st.session_state.show_history = False

# LOGIN/SIGNUP 
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #1e1e96;'>📝 MindMemos</h1>", unsafe_allow_html=True)
    menu = st.radio("Select Option", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Signup":
        if st.button("Create Account"):
            if add_user(username, password):
                st.success("✅ Account created! Please login.")
            else:
                st.error("⚠️ Username already exists.")

    elif menu == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

else:
    # SIDEBAR 
    st.sidebar.markdown(f"### 👋 Welcome {st.session_state.username}!")
    if st.sidebar.button("📜 Show History"):
        st.session_state.show_history = not st.session_state.show_history

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.show_history = False
        st.rerun()

    # HISTORY 
    if st.session_state.show_history:
        st.sidebar.markdown("### 📜 Your History")
        user_history = get_history(st.session_state.username)
        if user_history:
            for h in user_history:
                with st.sidebar.expander(f"📄 {h['filename']} - {h['note_type']}"):
                    st.markdown(f"**Language:** {h['language']}")
                    st.markdown(f"**Date:** {h['timestamp'].strftime('%d-%m-%Y %H:%M')}")
                    st.markdown("**Notes:**")
                    st.write(h['output'])
        else:
            st.sidebar.info("No history found yet.")

    # MAIN UPLOAD 
    st.markdown("<h1 style='text-align: center; color: #1e1e96;'>📝 MindMemos</h1>", unsafe_allow_html=True)
    st.write("Upload a PDF or DOCX to generate smart notes!")

    uploaded_file = st.file_uploader("📂 Upload a PDF or DOCX", type=["pdf", "docx"])

    if uploaded_file:
        st.success("✅ File uploaded successfully!")

        language = st.selectbox("Choose the language for your notes:", ["English", "French", "Spanish", "German"])
        prompt_type = st.radio("Choose your preferred note style:", ["Summary Notes", "Detailed Notes", "Q&A Format"])

        if st.button("Generate Notes"):
            with st.spinner("⏳ Generating notes, please wait..."):
                notes = process_file(uploaded_file, prompt_type, language)
                st.session_state.generated_notes = notes
                st.session_state.filename = uploaded_file.name

                # Save to history
                save_history(
                    st.session_state.username,
                    uploaded_file.name,
                    prompt_type,
                    language,
                    notes
                )

    # GENERATED NOTES 
    if "generated_notes" in st.session_state:
        st.markdown("### 📝 Generated Notes:")
        if st.session_state.generated_notes.strip():
            st.write(st.session_state.generated_notes)
        else:
            st.warning("⚠️ No notes generated. Please try again with another file or style.")

        pdf_buffer = export_to_pdf(st.session_state.generated_notes)
        st.download_button("⬇️ Download Notes as PDF", data=pdf_buffer,
                           file_name="MindMemos_Notes.pdf", mime="application/pdf")

        # FEEDBACK 
        st.markdown("---")
        st.subheader("💬 Share your feedback")
        
        feedback = st.text_area("Additional feedback (optional):")

        if st.button("Submit Feedback"):
            save_feedback(
                st.session_state.username,
                st.session_state.filename,
                feedback
            )
            st.success("✅ Thank you for your feedback!")
