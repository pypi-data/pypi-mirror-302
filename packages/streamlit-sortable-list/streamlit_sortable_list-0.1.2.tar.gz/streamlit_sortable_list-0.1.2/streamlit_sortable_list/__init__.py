import streamlit as st
import streamlit.components.v1 as components

import os

_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "sort_selections",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component(
        "sort_selections", path=build_dir)

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.


def sort_selections(items, key=None):
    """Create a new instance of "sortable_items".
    Parameters
    ----------
    items : list[str] 
    Returns
    -------
    list[]
        Sorted version of items. 
    """
    component_value = _component_func(items=items, key=key, default=items)
    st.json(component_value)
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    st.subheader("Component with constant args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.
    sort_items = ["python", "javascript", "golang", "rust", "R", "Typescript", "VBA", "Swift", "whatiisssssssssssssssssssss"]
    sorted_items = sort_selections(sort_items)
