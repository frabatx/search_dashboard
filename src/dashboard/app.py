from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Input
from textual.containers import Vertical
from textual.reactive import var
from textual.events import Key


from load import load_documents


class DashboardApp(App):
    CSS_PATH = "app.tcss"

    search_term: var[str] = var("")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Cerca titolo, sottotitolo o anno...", id="search-input")
        yield Vertical(
            DataTable(id="document-table")
        )
        yield Footer()

    def on_mount(self) -> None:
        self.documents = load_documents()
        self.refresh_table(self.documents)
        self.query_one(Input).focus()  # autofocus sulla barra di ricerca

    def refresh_table(self, docs: list[dict]) -> None:
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "Titolo", "Sottotitolo", "Anno")

        for doc in docs:
            meta = doc["metadata"]
            table.add_row(
                doc["sourceDocumentId"],
                meta["titolo"],
                meta["sottotitolo"],
                str(meta["anno"]),
            )

    def on_input_changed(self, event: Input.Changed) -> None:
        raw_query = event.value.strip()
        self.search_term = raw_query.lower()

        if not raw_query:
            self.refresh_table(self.documents)
            return

        # Comando speciale: keyboard <termine>
        if raw_query.lower().startswith("keyboard "):
            _, _, keyword = raw_query.partition(" ")
            keyword = keyword.strip().lower()
            if not keyword:
                self.refresh_table(self.documents)
                return
        else:
            keyword = self.search_term

        # Filtro principale
        filtered = [
            doc for doc in self.documents
            if keyword in doc["sourceDocumentId"].lower()
            or keyword in doc["metadata"]["titolo"].lower()
            or keyword in doc["metadata"]["sottotitolo"].lower()
            or keyword in str(doc["metadata"]["anno"])
        ]
        self.refresh_table(filtered)

    def on_key(self, event: Key) -> None:
        focused = self.focused
        table = self.query_one(DataTable)
        search_input = self.query_one(Input)

        if focused is table:
            if event.key == "j":
                table.action_cursor_down()
            elif event.key == "k":
                table.action_cursor_up()
        elif focused is search_input and event.key == "tab":
            table.focus()
        elif focused is table and event.key == "tab":
            search_input.focus()

# def run():
#     DashboardApp().run()

# if __name__ == "__main__":
#     run()

# class DashboardApp(App):
#     CSS_PATH = "app.tcss" # Stiamo usando il CSS diagnostico modificato

#     # Variabile reattiva per il termine di ricerca
#     search_term: var[str] = var("")

#     def compose(self) -> ComposeResult:
#         yield Header()
#         # Puoi ripristinare il placeholder originale se vuoi
#         yield Input(placeholder="🔍 Cerca titolo, sottotitolo o anno...", id="search-input")
#         yield Vertical(
#             DataTable(id="document-table")
#             # La DataTable è ancora vuota, la popoleremo tra poco
#         )
#         yield Footer()

#     def on_mount(self) -> None:
#         self.query_one(Input).focus()
#         # Per ora, non carichiamo/popoliamo la tabella, lo faremo come passo successivo
#         # self.documents = [] # Inizializza se necessario
#         # self.documents = load_documents()
#         # self.refresh_table(self.documents)
#         pass

#     # Metodo per aggiornare la tabella (lo definiremo/scommenteremo tra poco)
#     def refresh_table(self, docs: list[dict]) -> None:
#         table = self.query_one(DataTable)
#         table.clear(columns=True) # Pulisce anche le colonne esistenti
        
#         # Aggiungi le colonne (solo se non sono già state aggiunte o se clear(columns=True) le rimuove)
#         # Questo è un buon posto per assicurarsi che le colonne esistano.
#         # Textual potrebbe dare errori se si aggiungono righe senza prima definire le colonne.
#         if not table.columns: # Controlla se le colonne sono già definite
#              table.add_columns("ID", "Titolo", "Sottotitolo", "Anno")
#         # Oppure, se clear(columns=True) rimuove sempre le colonne, aggiungile sempre qui:
#         # table.add_columns("ID", "Titolo", "Sottotitolo", "Anno")


#         for doc in docs:
#             meta = doc.get("metadata", {}) # Usa .get() per sicurezza
#             table.add_row(
#                 doc.get("sourceDocumentId", ""),
#                 meta.get("titolo", ""),
#                 meta.get("sottotitolo", ""),
#                 str(meta.get("anno", "")), # Converti in stringa per sicurezza
#             )

#     # Metodo per gestire il cambio dell'input (lo definiremo/scommenteremo tra poco)
#     def on_input_changed(self, event: Input.Changed) -> None:
#         raw_query = event.value.strip()
#         self.search_term = raw_query.lower() # search_term è già una var, si aggiornerà

#         # Logica di filtro (da scommentare/implementare)
#         # if not raw_query:
#         #     self.refresh_table(self.documents) # Mostra tutti i documenti
#         #     return
#         #
#         # # Qui la logica di filtro basata su self.search_term
#         # # filtered_docs = [doc for doc in self.documents if ...]
#         # # self.refresh_table(filtered_docs)
#         pass # Per ora non fa nulla

#     # Metodo per gestire gli eventi da tastiera (lo definiremo/scommenteremo tra poco)
#     def on_key(self, event: Key) -> None:
#         # focused = self.focused
#         # table = self.query_one(DataTable)
#         # search_input = self.query_one(Input)
#         #
#         # if focused is table:
#         #     if event.key == "j":
#         #         table.action_cursor_down()
#         #     elif event.key == "k":
#         #         table.action_cursor_up()
#         # elif focused is search_input and event.key == "tab":
#         #     event.prevent_default() # Importante per sovrascrivere il comportamento di default del Tab
#         #     table.focus()
#         # elif focused is table and event.key == "tab":
#         #     event.prevent_default() # Importante
#         #     search_input.focus()
#         pass # Per ora non fa nulla

def run():
    app = DashboardApp()
    app.run()

if __name__ == "__main__":
    run()