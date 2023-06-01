import streamlit as st
import graphviz
import openai

st.set_page_config(page_title="Graph Generator", page_icon="🖊️")
st.title("Graph Generator")

if "graph" not in st.session_state:
    st.session_state.graph = ""

if "prompt" not in st.session_state:
    st.session_state.prompt = ""


useai = st.sidebar.checkbox("Use OpenAI API")
with st.sidebar:
    if useai:
        st.session_state.openaikey = st.sidebar.text_input("OPENAI_API_KEY", type="password")
        st.markdown("You can get your API key from [here](https://platform.openai.com/account/api-keys)")
        st.session_state.prompt = st.text_area(
            "Past your prompt here",
            height=200,
            value=st.session_state.get("prompt", ""),
        )
        if st.button("Get Graphviz Code"):
            openai.api_key = st.session_state.openaikey
            
            st.session_state.graph = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[
                    {"role": "system", "content": "Only generate Graphviz code nothing else!\n If you can generate any graphviz code just answer with an empty string!\nExample:\ndigraph {\n    a -> b -> c;\n    b -> d;\n}"},
                    {"role": "user", "content": st.session_state.prompt}
                ]
            )["choices"][0]["message"]["content"]



st.session_state.graph = st.text_area(
        "Paste your graph here",
        height=400,
        value=st.session_state.get("graph", "")
    )

# add an example of how to use graphviz in the sidebar
with st.expander("Examples"):
    st.markdown(
        """
        # Graphviz
        You can use the [Graphviz](https://graphviz.org/) syntax to generate graphs.
        For example, if you want to generate the following graph:
        ```
        digraph {
            a -> b -> c;
            b -> d;
        }
        ```
        Another example:
        ```
        digraph {
            a -> b -> c;
            b -> d;
            b -> a;
            f -> a;
            f -> b;
            f -> c;
            f -> d;
            a -> e;
            b -> e;
            c -> e;
            d -> e;
            subgraph cluster_0 {
                style=filled;
                color=lightgrey;
                node [style=filled,color=white];
                a0 -> a1 -> a2 -> a3;
            }
        }
        
        """
    )


if st.button("Render"):
    try:
        st.graphviz_chart(st.session_state.graph)
    except Exception as e:
        st.error(e)
    try:
        st.download_button(
            label="Download Image",
            data=graphviz.Source(st.session_state.graph).pipe(format="png"),
            file_name="graph.png",
            mime="image/png"
        )
    except Exception as e:
        print(e)