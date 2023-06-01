import os
import streamlit as st
import markdown as md
import jinja2

st.set_page_config(page_title="Markdown Converter", page_icon="🔃")

if "markdown" not in st.session_state:
    st.session_state.markdown = ""

if "style" not in st.session_state:
    st.session_state.style = "default"

if "customstyle" not in st.session_state:  
    st.session_state.customstyle = ""

if "title" not in st.session_state:
    st.session_state.title = "Markdown Website"


st.title("Markdown Converter")

col1 =st.columns(2)
with col1[0]:
    st.session_state["markdown"] = st.text_area(
            "Markdown",
            placeholder= "# Hello World",
            height=400,
            value=st.session_state.get("markdown", "")
        )
with col1[1]:
    st.markdown( st.session_state.markdown)

convertbtn = st.button("Convert")

with st.expander("Additional Options"):
    st.session_state["title"] = st.text_input("Title", value=st.session_state.get("title", ""))
    st.session_state["style"] = st.selectbox( "Style", ["default", "github", "simple", "bootstrap", "material", "custom"])
    if st.session_state.style == "custom":
        st.session_state["customstyle"] = st.text_area(
            "Custom Style",
            height=200,
            value=st.session_state.get("customstyle", "")
        )

if convertbtn:
    html= ""
    try:
        html = md.markdown(st.session_state.markdown, extensions=['extra'])
    except Exception as e:
        st.error(e)

    stylesheet = f"{st.session_state.style}.css"
    template = "html-template.j2"
    if os.path.exists(f"templates/md_converter/styles/{stylesheet}"):
        with open(f"templates/md_converter/styles/{stylesheet}") as f:
            css = f.read()
    elif st.session_state.style == "custom":
        css = st.session_state.customstyle
    else:
        st.warning(f"Stylesheet {stylesheet} not found. Using default instead.")
        with open(f"templates/md_converter/styles/default.css") as f:
            css = f.read()

    with open(f"templates/md_converter/{template}") as f:
        template = f.read()
    html = jinja2.Template(template).render(content=html, css=css, title=st.session_state.title)
    st.download_button(
        label="Download HTML",
        data=html,
        file_name="markdown.html",
        mime="text/html"
    )
    st.code(html, language="html")


