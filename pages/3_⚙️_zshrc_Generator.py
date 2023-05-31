import streamlit as st
import requests
import random
from github import Github
from jinja2 import Template

def get_plugins():
    """
    Get the list of plugins from the ohmyzsh repository
    
    Returns:
        The list of plugins.
    """

    g = Github()
    repo = g.get_repo("ohmyzsh/ohmyzsh")
    contents = repo.get_contents("plugins")
    plugins = []
    for content in contents:
        plugins.append(content.name)
    return plugins

st.set_page_config(page_title="Zshrc Generator", page_icon="⚙️")
st.title("Zshrc Generator")

# Initialize session state

if "plugins" not in st.session_state:
    st.session_state.plugins = get_plugins()

if "selected_plugins" not in st.session_state:
    st.session_state.selected_plugins = []

if "theme" not in st.session_state:
    st.session_state.theme = "random"

# Input fields
st.session_state["selected_plugins"] = st.multiselect(
        "Plugins",
        options=st.session_state.plugins,
        default=st.session_state.get("selected_plugins", []),
    )

st.session_state["theme"] = st.selectbox(
        "Theme",
        options=["random", "robbyrussell", "agnoster", "bira", "steeef"],
        index=0
    )

# Generate zshrc

if st.button("Generate"):
    if st.session_state.theme == "random":
        st.session_state.theme = random.choice(["robbyrussell", "agnoster", "bira", "steeef"])
    template = Template("""\
        # ~/.zshrc

        ZSH_THEME="{{ theme }}"

        plugins=(
            {%- for plugin in plugins %}
            "{{ plugin }}"
            {%- endfor %}
        )

        source $ZSH/oh-my-zsh.sh
        source ~/.config/env.sh

        # Aliases

        alias zshconfig="vim ~/.zshrc"
        alias ohmyzsh="vim ~/.oh-my-zsh"
        alias envconfig="vim ~/.config/env.sh"
        alis ymlsrt="yq sort -i"
        alias ymlval="yq eval"
        """)
    zshrc_content = template.render(plugins=st.session_state.selected_plugins, theme=st.session_state.theme)
    st.code(zshrc_content)

    st.download_button(
        label="Download .zshrc",
        data=zshrc_content.encode("utf-8"),
        file_name=".zshrc",
        mime="text/plain"
    )