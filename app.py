import gradio as gr
from services.Solver import find_optimal_journey, lister_gares, trains
import pandas as pd

choices = lister_gares(trains)
dataframe_trains = pd.DataFrame(trains)


def interface_calculateur():
    inputs = [
            gr.components.Dropdown(choices=choices, label="Gare de départ", value='Paris'),
            gr.components.Dropdown(choices=choices, label="Gare d'arrivée", value='Bordeaux'),
            gr.components.Slider(minimum=0, maximum=24, step=1, label="Heure de départ", value=0),
            gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance de la durée pour le voyageur", value=1),
            gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance du prix pour le voyageur", value=1),
            gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance des émissions CO2 pour le voyageur", value=1)
            ]
    outputs = [
            gr.components.Textbox(label='Chemin Optimal'),
            gr.components.Image(label='Graph des chemins potentiels')
            ]

    return gr.Interface(
        find_optimal_journey,
        inputs=inputs,
        outputs=outputs,
        css="footer {visibility: hidden}",
        allow_flagging="never",
        )


def interface_trains():
    return gr.components.Dataframe(
        dataframe_trains,
        label='Trains en circulation'
        )


interfaces = [
    interface_calculateur(),
    interface_trains()
]


demo = gr.TabbedInterface(
    interface_list=interfaces,
    tab_names=["Calculateur", "Trains"],
    css="footer {visibility: hidden}",
    title="Rail Aventure",
    theme=gr.themes.Base()
    )

demo.launch(favicon_path="./data/favicon.ico")
# demo.launch(favicon_path="./data/favicon.ico", share=True)
