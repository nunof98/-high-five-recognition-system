from dotenv import load_dotenv
import streamlit as st
from sharepoint_client import SharePointClient

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="High Five Recognition",
    page_icon="✋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for brand colors and styling
st.markdown(
    """
<style>
    .main {
        background: linear-gradient(135deg, #FF9900 0%, #FFE79B 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #FF9900 0%, #FFE79B 100%);
    }
    div[data-testid="stForm"] {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .success-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    .color-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        text-transform: uppercase;
        border: 3px solid currentColor;
        margin: 1rem 0;
    }
    h1 {
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF9900 0%, #FFE79B 100%);
        color: #333;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        width: 100%;
    }
    .stTextArea textarea, .stTextInput input {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #FF9900;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Color mapping
COLORS = {
    "red": "#e74c3c",
    "blue": "#3498db",
    "green": "#2ecc71",
    "yellow": "#f39c12",
    "purple": "#9b59b6",
    "orange": "#FF9900",
}


def get_query_params():
    """Get token and color from URL query parameters"""
    try:
        query_params = st.query_params
        token = query_params.get("token", None)
        color = query_params.get("color", None)
        return token, color
    except Exception:
        return None, None


def display_existing_message(data):
    """Display an existing High Five message"""
    st.markdown("# 🎉 High Five Already Given!")

    color_hex = COLORS.get(data["Color"].lower(), "#333")

    st.markdown(
        f"""
    <div class="success-card">
        <div style="border-left: 4px solid {color_hex}; padding-left: 15px;">
            <div class="color-badge" style="color: {color_hex};">
                {data["Color"].upper()} Token
            </div>
            <p style="font-size: 1.2em; margin: 15px 0;"><strong>"{data["Message"]}"</strong></p>
            <p style="color: #666; font-size: 0.9em;">- {data["SubmittedBy"]}</p>
            <p style="color: #999; font-size: 0.8em; margin-top: 10px;">
                {data["Timestamp"]}
            </p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def show_new_token_form(token, color):
    """Display form for new High Five submission"""
    st.markdown("# ✋ Give Your High Five!")

    with st.form("highfive_form", clear_on_submit=True):
        # Display token color
        color_hex = COLORS.get(color.lower(), "#333")
        st.markdown(
            f"""
        <div>
            <label style="font-weight: 600; color: #555;">Token Color:</label>
            <div class="color-badge" style="color: {color_hex};">
                {color.upper()}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Message input
        message = st.text_area(
            "Your Recognition Message",
            placeholder="Write why this person deserves a High Five...",
            height=120,
            help="Share your appreciation and recognition",
        )

        # Name input
        submitted_by = st.text_input(
            "Your Name",
            placeholder="Enter your name",
            help="Who is giving this High Five?",
        )

        # Submit button
        submit_button = st.form_submit_button("Send High Five 🎉")

        if submit_button:
            if not message or not submitted_by:
                st.error("⚠️ Please fill in all fields")
                return False

            # Submit to SharePoint
            try:
                with st.spinner("Sending your High Five..."):
                    sp_client = SharePointClient()
                    success = sp_client.add_token(
                        token=token,
                        color=color,
                        message=message,
                        submitted_by=submitted_by,
                    )

                if success:
                    st.session_state["submitted"] = True
                    st.rerun()
                else:
                    st.error("❌ This token has already been used!")
                    return False
            except Exception as e:
                st.error(f"❌ Error submitting: {str(e)}")
                return False

    return True


def show_success_message():
    """Display success message after submission"""
    st.markdown("# ✅ High Five Sent!")
    st.markdown(
        """
    <div class="success-card">
        <p style="text-align: center; font-size: 1.1em; color: #666;">
            Your recognition has been recorded. Thank you! 🎉
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def show_error_message(error_text):
    """Display error message"""
    st.markdown("# ❌ Oops!")
    st.markdown(
        f"""
    <div class="success-card">
        <p style="text-align: center; font-size: 1.1em; color: #666;">
            {error_text}
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def main():
    """Main application logic"""

    # Get query parameters
    token, color = get_query_params()

    # Validate parameters
    if not token or not color:
        show_error_message("Invalid QR code. Missing token or color parameter.")
        st.stop()

    # Check if form was just submitted
    if st.session_state.get("submitted", False):
        show_success_message()
        st.stop()

    # Initialize SharePoint client and check token
    try:
        with st.spinner("Checking your High Five token..."):
            sp_client = SharePointClient()
            existing_data = sp_client.check_token(token)

        if existing_data:
            # Token exists - display the message
            display_existing_message(existing_data)
        else:
            # New token - show form
            show_new_token_form(token, color)

    except Exception as e:
        show_error_message(
            f"Unable to connect to the server. Please try again later.<br><small>Error: {str(e)}</small>"
        )


if __name__ == "__main__":
    main()
