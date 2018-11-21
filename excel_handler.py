import xlwings as xw
import lazy_object_proxy


class ExcelHandler():
    def __init__(self):
        self.application = lazy_object_proxy.Proxy(self.initial_application)
        self.book = self.application.books.active
        self.sheet = self.book.sheets.active
        self.save_current_features()

    def initial_application(self):
        return xw.App(visible=False)

    def save_workbook(self, file_path):
        self.book.save(file_path)

    def toggle_unnecessary_features(self, switch):
        if (switch is False):
            self.save_current_features()
            self.application.calculation = 'manual'
            self.application.display_alerts = False
            self.application.screen_updating = False
            self.application.api.EnableEvents = False
            self.application.api.EnableAnimations = False
            self.sheet.api.DisplayPagebreaks = False
        else:
            self.application.calculation = self.current_calculation
            self.application.display_alerts = self.current_display_alerts
            self.application.screen_updating = self.current_screen_updating
            self.application.api.EnableEvents = self.current_enable_events
            self.application.api.EnableAnimations = self.current_enable_animations
            self.sheet.api.DisplayPagebreaks = self.current_display_pagebreaks

    def save_current_features(self):
        self.current_calculation = self.application.calculation
        self.current_display_alerts = self.application.display_alerts
        self.current_screen_updating = self.application.screen_updating
        self.current_enable_events = self.application.api.EnableEvents
        self.current_enable_animations = self.application.api.EnableAnimations
        self.current_display_pagebreaks = self.sheet.api.DisplayPagebreaks

    def exit(self):
        self.application.kill()
