import streamlit as st
from process import Process, NormalStep, ExponentialStep, UniformStep
import altair as alt
import pandas as pd
import app_fragments

# Title
st.write("""# Montecarlo Simulation
This is a very simple application to simulate.
         """)
# Initialize a Process intance if not exists
if 'process' not in st.session_state:
    st.session_state.process = Process()

# Selectbox for distribution types
process_type = st.selectbox("Select Distribution", ("Exponential", "Normal", "Uniform"))

# Add step form
app_fragments.process_step_form(process_type)

st.divider()

# Heading
st.write("""## Process Steps""")

# Show process stps
app_fragments.show_process_steps()

st.session_state.process.display_steps()

st.divider()

#heading
st.write("## Simulate")



if st.session_state.process.get_steps() is None:
    st.write("No process steps to simulate...")

    if 'simulation_results' in st.session_state:
        del st.session_state.simulation_results
else:
    n_simulations = st.number_input("Number of simulations", min_value= 100, value=1000, step=1)
    simulate_button = st.button("Simulate")

    if simulate_button:
        results = st.session_state.process.simulate_process(n_simulations= n_simulations)
        st.session_state.simulation_results = results

    if 'simulation_results' in st.session_state:
        st.write("## Simulation results")

        st.write("### Statistics")
        stats = st.session_state.simulation_results.describe()
        #st.write(stats)
        st.dataframe(stats, use_container_width=True)
        
        st.write("### Visualization")

        app_fragments.histogram()

        st.write("### Download results")
        app_fragments.download_results()