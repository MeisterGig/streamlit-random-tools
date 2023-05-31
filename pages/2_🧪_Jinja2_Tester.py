import streamlit as st
import jinja2
import yaml

st.set_page_config(page_title="Jinja2 Tester", page_icon="🧪")
st.title("Jinja2 Tester")

st.session_state["variables"] = st.text_area(
        "Variables",
        placeholder= "foo: bar",
        height=200,
        value=st.session_state.get("variables", "")
    )

st.session_state["template"] = st.text_area(
        "Template",
        placeholder="{{ foo }}",
        height=200,
        value=st.session_state.get("template", "")
    )

if st.button("Render"):
    try:
        template = jinja2.Template(st.session_state.template)
        variables = yaml.safe_load(st.session_state.variables)
        st.code(template.render(variables))
    except Exception as e:
        st.error(e)
