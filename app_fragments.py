import streamlit as st
import altair as alt
from process_steps import ExponentialStep, NormalStep, UniformStep

alt.theme.enable("quartz")


def process_step_form(process_type: str):
    """
    Adds form components based on users selection.

    Args:
        process_type (str): value of selebox in app.py -file.  

    """

    with st.form("add_process_step", clear_on_submit=True):
        st.write("Add process step:")

        if process_type == "Exponential":
            name = st.text_input("add name")
            rate = st.number_input("Rate (lambda)", min_value=0.01, step=0.1)

        elif process_type == "Normal":
            name = st.text_input("add name")
            mean = st.number_input("Mean", min_value=0.0, step=0.1)
            std_dev = st.number_input("Standard Deviation", min_value=0.0, step=0.1)

        elif process_type == "Uniform":
            name = st.text_input("add name")
            lower_bound = st.number_input("Lower Bound", min_value=0.0, step=0.1)
            upper_bound = st.number_input("Upper Bound", min_value=0.0, step=0.1)

        # A button to add step
        add_step = st.form_submit_button("Add Step")

        # Logic for handling inputs when add_step button is pressed
        if add_step:
            try:
                if not name:
                    st.error("Name cannot be empty.")

                elif name in st.session_state.process.get_names():
                    st.error("Name already exists")

                else:
                    if process_type == "Exponential":
                            st.session_state.process.insertAtEnd(
                                ExponentialStep(name, rate)
                            )

                    elif process_type == "Normal":
                            st.session_state.process.insertAtEnd(
                                NormalStep(name, mean, std_dev)
                            )

                    elif process_type == "Uniform":
                            try:
                                st.session_state.process.insertAtEnd(
                                    UniformStep(name, lower_bound, upper_bound)
                                )
                            except AssertionError as e:
                                st.error(f"Validation error: {e}")
                            except Exception as e:
                                 st.error(f"Unexpected error: {e}")

            except Exception as e:
                st.exception(e)


@st.fragment
def show_process_steps():
    """
    Displays a list of all process steps in the session state. 
    Each step includes inputs for adjusting its parameters and buttons for updating or deleting the step.
    
    """

    if st.session_state.process.get_steps() is None:
        st.write("No process steps to display here...")
    else:
        for i, step in enumerate(st.session_state.process.get_steps()):
            with st.popover(f"{step.name}", use_container_width=True):
                if isinstance(step, ExponentialStep):
                    st.write(step.name)

                    new_rate = st.number_input(
                        "rate (lambda)",
                        min_value=0.01,
                        value=step.rate,
                        step=0.1,
                        key=f"rate_{i}",
                    )
                    update_step = st.button("Update", key=f"update_{i}")

                    if update_step:
                        st.session_state.process.update_step(step.name, rate=new_rate)
                        st.success("Step updated.")
                        st.success(f"{step.name} successfully updated.")
                        st.rerun(scope="fragment")

                elif isinstance(step, NormalStep):
                    st.write(step.name)

                    new_mean = st.number_input(
                        "Mean",
                        min_value=0.0,
                        value=step.mean,
                        step=0.1,
                        key=f"mean_{i}",
                    )
                    new_std_dev = st.number_input(
                        "Standard Deviation",
                        min_value=0.0,
                        value=step.stdev,
                        step=0.1,
                        key=f"std_dev{i}",
                    )
                    update_step = st.button("Update", key=f"update_{i}")

                    if update_step:
                        st.session_state.process.update_step(
                            step.name, mean=new_mean, stdev=new_std_dev
                        )
                        st.success("Step updated.")
                        st.success(f"{step.name} successfully updated.")
                        st.rerun(scope="fragment")

                elif isinstance(step, UniformStep):
                    st.write(step.name)
                    new_lower_bound = st.number_input(
                        "Lower Bound",
                        min_value=0.0,
                        value=step.low,
                        step=0.1,
                        key=f"low_{i}",
                    )
                    new_upper_bound = st.number_input(
                        "Upper Bound",
                        min_value=0.0,
                        value=step.high,
                        step=0.1,
                        key=f"high_{i}",
                    )
                    update_step = st.button("Update", key=f"update_{i}")

                    if update_step:
                            if new_lower_bound <= new_upper_bound:                            
                                st.session_state.process.update_step(
                                    step.name, low=new_lower_bound, high=new_upper_bound
                                )
                                st.success("Step updated.")
                                st.success(f"{step.name} successfully updated.")
                                st.rerun(scope="fragment")
                            else:
                                 st.error("Lower bound must be  less than or equal to upper bound")

                if st.button("Delete step", key=f"delete_{i}"):
                    st.session_state.process.deleteStep(step.name)
                    st.success(f"Step '{step.name}' deleted.")
                    st.rerun(scope="fragment")


@st.fragment
def histogram():
    """
        Displays a slider to adjust the number of bins and a histogram to visualize simulation results.
    """

    bins = st.slider("Number of bins", min_value=2, max_value=200, value=20)

    histogram = (
        alt.Chart(st.session_state.simulation_results)
        .mark_bar()
        .encode(alt.X("Total:Q", bin=alt.Bin(maxbins=bins)), y="count()")
        .interactive()
    )
    st.altair_chart(histogram, use_container_width=True)


@st.fragment
def download_results():
    """
    Checks if simulation results exist in session state and provides a button to download the results as a CSV file.
    """

    if "simulation_results" in st.session_state:
        st.download_button(
            label="Download Simulation Data",
            data=st.session_state.simulation_results.to_csv(index=False),
            file_name="simulation_results.csv",
            mime="text/csv",
        )
