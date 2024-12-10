import streamlit as st
from process import Process
import app_fragments

# This is the main page of the app.
# Content to this page has been mainly been implemetned using fragments properly manage execution flow and to avoid unecessary reruns of the whole page/app.

# Title
st.markdown("""# Montecarlo Simulation""")

st.markdown("""
## Instructions:
1. **Choose Distribution Type**: Select from Exponential, Normal, or Uniform.
2. **Add Process Steps**: Define the parameters for the selected distribution.
   - **Exponential**: Enter a rate (λ).
   - **Normal**: Enter mean and standard deviation.
   - **Uniform**: Enter lower and upper bounds.
3. **Adjust Process Steps**: After adding steps, you can update the parameters or delete steps as needed.
4. **Simulate Process**: Specify the number of simulations and click "Simulate" to generate results.
5. **Visualize Results**: Adjust the bin count for the histogram and view the simulation outcomes.
6. **Download Data**: Download the simulation results as a CSV file.
            """)

st.divider()

# Initialize a Process intance if not exists
if "process" not in st.session_state:
    st.session_state.process = Process()

# Selectbox for distribution types
st.markdown("## Add steps")
process_type = st.selectbox("Select Distribution", ("Exponential", "Normal", "Uniform"))

# Adds form
app_fragments.process_step_form(process_type)

st.divider()

# Section for process steps
# Heading
st.markdown("""## Process Steps""")

# Lists process steps
app_fragments.show_process_steps()

st.divider()

# heading
st.markdown("## Simulate")


if st.session_state.process.get_steps() is None:
    st.write("No process steps to simulate...")

    if "simulation_results" in st.session_state:
        del st.session_state.simulation_results
else:
    n_simulations = st.number_input(
        "Number of simulations", min_value=100, value=1000, step=1
    )
    simulate_button = st.button("Simulate")

    if simulate_button:
        results = st.session_state.process.simulate_process(n_simulations=n_simulations)
        st.session_state.simulation_results = results

    if "simulation_results" in st.session_state:
        st.write("## Simulation results")

        st.write("### Statistics")
        stats = st.session_state.simulation_results.describe()
        st.dataframe(stats, use_container_width=True)

        st.write("### Visualization")

        app_fragments.histogram()

        st.write("### Download results")
        app_fragments.download_results()
