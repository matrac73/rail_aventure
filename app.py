import gradio as gr
from services.Solver import find_optimal_journey, lister_gares, trains

choices = lister_gares(trains)

demo = gr.Interface(
    find_optimal_journey,
    inputs=[
        gr.components.Dropdown(choices=choices, label="Gare de départ", value='Paris'),
        gr.components.Dropdown(choices=choices, label="Gare d'arrivée", value='Bordeaux'),
        gr.components.Slider(minimum=0, maximum=24, step=1, label="Heure de départ", value=0),
        gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance de la durée pour le voyageur", value=1),
        gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance du prix pour le voyageur", value=1),
        gr.components.Slider(minimum=0, maximum=5, step=1, label="Importance des émissions CO2 pour le voyageur", value=1)
        ],
    outputs=[
        gr.components.Textbox(label='Chemin Optimal'),
        gr.components.Image(label='Graph des chemins potentiels'),
        gr.components.Dataframe(label='Trains en circulation')
        ],
    css="footer {visibility: hidden}",
    title="Rail aventure",
    description="Pour une fois qu'on peut allier écologie et économie, pourquoi se priver ?",
    theme=gr.themes.Base(),
    allow_flagging="never",
    )

demo.launch(favicon_path="./data/favicon.ico")
# demo.launch(share=True, favicon_path="favicon.ico")
