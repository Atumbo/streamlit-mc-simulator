from streamlit.testing.v1 import AppTest


def test_base_elements():
    at = AppTest.from_file("app.py").run()

    # print(at.markdown)

    assert at.markdown[0].value == """# Montecarlo Simulation"""

    at.selectbox[0].select("Normal").run()
    assert at.selectbox[0].value == "Normal"

    at.text_input[0].input("streamlit").run()
    at.number_input[0].set_value(120).run()
    at.number_input[1].set_value(12).run()
    at.button[0].click().run()

    assert at.session_state.process.get_names() == ["streamlit"]

    at.button[3].click().run()

    # print(list(at.session_state['simulation_results'].columns))

    assert list(at.session_state["simulation_results"].columns) == [
        "streamlit",
        "Total",
    ]
    assert at.session_state["simulation_results"].shape == (1000, 2)
