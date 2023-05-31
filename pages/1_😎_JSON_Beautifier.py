import streamlit as st
import json
import jmespath

def filter_json(json_object, queryfilter):
    """
    Filters a JSON object using a JMESPath query filter.

    Args:
        json_object (dict): The JSON object to filter.
        queryfilter (str): The JMESPath query filter to apply.

    Returns:
        The filtered JSON object.
    """
    if queryfilter:
        expression = jmespath.compile(queryfilter)
        return expression.search(json_object)
    else:
        return json_object

# Session State also supports attribute based syntax
if 'json' not in st.session_state:
    st.session_state.json = ''

if 'queryfilter' not in st.session_state:
    st.session_state.queryfilter = ''

st.set_page_config(page_title="Json Beautifier", page_icon="😎")
st.title("JSON Beautifier")


st.session_state["json"] = st.text_area(
        "Paste your json here",
        height=400,
        value=st.session_state["json"]
    )  

st.session_state["queryfilter"] = st.sidebar.text_input(
        "Filter", 
        value=st.session_state["queryfilter"]
    )


st.sidebar.markdown(
    """ 
    # Filter
    You can use the [JMESPath](https://jmespath.org/) syntax to filter the json.
    For example, if you want to filter the following json:
    ```
    {
        "people": [
            {
                "name": "John",
                "age": 30
            },
            {
                "name": "Jane",
                "age": 25
            }
        ]
    }
    ```
    You can use the following filters:
    - `people[*].name` to get the names of all people
    - `people[?age > 25].name` to get the names of people older than 25
    - `people[?name == 'Jane'].age` to get the age of Jane
    """
)

if st.button("Beautify"):
    try:
        json_object = json.loads(st.session_state.json)
        filtered_json = filter_json(json_object, st.session_state.queryfilter)
        if isinstance(filtered_json, list) or isinstance(filtered_json, dict):
            st.json(filtered_json)
        else:
            st.markdown(f'The Filter **{st.session_state.queryfilter}** resulted in a single object **{filtered_json}**')

    except json.decoder.JSONDecodeError:
        st.error("Invalid JSON")

