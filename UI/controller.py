import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._y_min = None
        self._y_max = None

    def handleBuildGraph(self, e):
        self._y_min = self._view._ddYear1.value
        self._y_max = self._view._ddYear2.value
        if self._y_min is None or self._y_max is None:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text(f"Seleziona y_min e y_max", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(int(self._y_min), int(self._y_max))
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text(f"{self._model.printGraph()}"))
        self._view._btnPrintDetails.disabled = False
        self._view._btnCalcolaSoluzione.disabled = False
        self._view.update_page()



    def handlePrintDetails(self, e):
        lista = self._model.get_info_comp()
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text(f"Stampa dettagli:"))
        for item in lista:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{item[1]} --> {item[0]}"))
        self._view.update_page()

    def handleCercaTeamSfortunati(self, e):
        k_input = self._view._txtInSoglia.value
        m_input = self._view._txtInNumDiEdizioni.value
        if k_input is None or m_input is None:
            self._view._txt_result.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text(f"Un numeri di k piloti ed m edizioni.", color="red"))
            self._view.update_page()
            return
        try:
            k = int(k_input)
            m = int(m_input)
            tasso, team = self._model.get_opt_set(k,m,self._y_min,self._y_max)
            print(tasso)
            if len(team) == 0:
                self._view._txt_result.controls.clear()
                self._view._txt_result.controls.append(
                    ft.Text(f"Ci sono meno di k piloti validi,", color="red"))
                self._view.update_page()
                return
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Team più sfortunati:"))
            for item in team:
                self._view._txt_result.controls.append(ft.Text(f"{item}"))
            self._view.update_page()
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text(f"Un numeri di k piloti ed m edizioni (numerici).", color="red"))
            self._view.update_page()
            return



    def fillDDYears(self):
        anni = self._model.get_years()
        for year in anni:
            self._view._ddYear1.options.append(ft.dropdown.Option(year))
            self._view._ddYear2.options.append(ft.dropdown.Option(year))

