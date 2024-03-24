import gradio as gr
from services.Solver import find_optimal_journey, extract_station_names, display_train, display_gares


csv_file_gares = 'data/SNCF_gares.csv'
choices = extract_station_names(csv_file_gares)

dataset_train = [
                "10 trains synthéthiques",
                "50 trains synthéthiques",
                "API SNCF 25 trains",
                "API SNCF 100 trains",
                "API SNCF 1000 trains",
                "API SNCF 10000 trains",
                ]


def interface_calculateur():
    inputs = [
            gr.components.Dropdown(choices=choices, label="Gare de départ", value='Frankfurt am Main - Hauptbahnhof'),
            gr.components.Dropdown(choices=choices, label="Gare d'arrivée", value='Paris Est'),
            gr.components.Slider(minimum=0, maximum=24, step=1, label="Heure de départ", value=0),
            gr.components.Radio(choices=[
                "Depth First Search",
                "A star",
                "Breadth First Search",
                ], value="Depth First Search", label="Algorithme"),
            gr.components.Radio(choices=dataset_train, value="API SNCF 100 trains", label="Données"),
            gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance de la durée pour le voyageur", value=1),
            gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance du prix pour le voyageur", value=0),
            gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance des émissions CO2 pour le voyageur", value=0)
            ]
    outputs = [
            gr.components.Textbox(label='Chemin Optimal'),
            gr.components.Image(label='Parcours suggéré'),
            gr.components.Image(label='Graph des chemins potentiels'),
            ]

    return gr.Interface(
        find_optimal_journey,
        inputs=inputs,
        outputs=outputs,
        css="footer {visibility: hidden}",
        allow_flagging="never",
        submit_btn="Calculer",
        clear_btn="Effacer"
        )


def interface_trains():
    inputs = [
        gr.components.Radio(choices=dataset_train, value="API SNCF 25 trains", label="Données"),
            ]
    outputs = [
        gr.components.DataFrame()
            ]

    return gr.Interface(
        display_train,
        inputs=inputs,
        outputs=outputs,
        css="footer {visibility: hidden}",
        allow_flagging="never",
        submit_btn="Afficher",
        clear_btn="Effacer"
        )


def interface_gares():
    inputs = []
    outputs = [
        gr.components.DataFrame(),
        gr.components.Image(label='Carte de la répartition des gares')
            ]

    return gr.Interface(
        display_gares,
        inputs=inputs,
        outputs=outputs,
        css="footer {visibility: hidden}",
        allow_flagging="never",
        submit_btn="Afficher",
        clear_btn="Effacer"
        )


interfaces = [
    interface_calculateur(),
    interface_trains(),
    interface_gares(),
]


demo = gr.TabbedInterface(
    interface_list=interfaces,
    tab_names=["Calculateur", "Trains", "Gares"],
    css="footer {visibility: hidden}",
    title="Rail Aventure",
    theme=gr.themes.Base()
    )

# demo.launch(favicon_path="./data/favicon.ico")
demo.launch(favicon_path="./data/favicon.ico", share=True)
