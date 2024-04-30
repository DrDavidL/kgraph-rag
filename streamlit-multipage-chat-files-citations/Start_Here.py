import streamlit as st
from components import header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit import Graphlit

st.set_page_config(
    page_title="Graphlit Demo Application",
    page_icon="💡",
    layout="wide"
)

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.write("*Please contact David Liebovitz, MD if you need an updated password for access.*")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

# col1, col2 = st.columns(2)
if check_password():
# with col1:
    with st.form("credentials_form"):
        st.markdown("### 💡 Start here:")
        st.info("This tool leverages Graphlit to extract data from your content, build a knowledge graph, create a vectorstore then enabling comprehensive search and chat with your content.")
        # st.info("Locate connection information for your project in the [Graphlit Developer Portal](https://portal.graphlit.dev/)")
        if st.secrets["organization_id"] is None:
            st.text_input("Organization ID", value=st.session_state['organization_id'], key="organization_id", type="password")
        if st.secrets["environment_id"] is None:
            st.text_input("Preview Environment ID", value=st.session_state['environment_id'], key="environment_id", type="password")
        if st.secrets["jwt_secret"] is None:
            st.text_input("Secret", value=st.session_state['jwt_secret'], key="jwt_secret", type="password")
            
        if st.secrets["organization_id"] and st.secrets["environment_id"] and st.secrets["jwt_secret"]:
            st.session_state['jwt_secret'] = st.secrets["jwt_secret"]
            st.session_state['environment_id'] = st.secrets["environment_id"]
            st.session_state['organization_id'] = st.secrets["organization_id"]
            st.write("Credentials found.  Click Generate Token to continue.")

            submit_credentials = st.form_submit_button("Generate Token")

            if submit_credentials:
                if st.session_state['jwt_secret'] and st.session_state['environment_id'] and st.session_state['organization_id']:
                    # Initialize Graphlit client
                    graphlit = Graphlit(organization_id=st.session_state['organization_id'], environment_id=st.session_state['environment_id'], jwt_secret=st.session_state['jwt_secret'])

                    st.session_state['graphlit'] = graphlit
                    st.session_state['token'] = graphlit.token

                    st.switch_page("pages/1_Upload_Files.py")
                else:
                    st.error("Please fill in all the connection information.")

                st.markdown("**Python SDK code example:**")

# with col2:        
#     st.markdown("**Python SDK code example:**")

#     with stylable_container(
#         "codeblock",
#         """
#         code {
#             white-space: pre-wrap !important;
#         }
#         """,
#     ):
#         st.code(language="python", body="""
#                 from graphlit import Graphlit

#                 graphlit = Graphlit(
#                     organization_id="{organization-id}", 
#                     environment_id="{environment-id}", 
#                     jwt_secret="{jwt-secret}"
#                 )

#                 """)
