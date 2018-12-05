import xlwings as xw
import lazy_object_proxy


class AppExcelHandler():
    def __init__(self):
        self.application = lazy_object_proxy.Proxy(self.__initial_application)
        self.__features_switch = True

    def __initial_application(self):
        return xw.App(visible=False, add_book=False)

    def __toggle_features(self, switch):
        if (switch is False):
            self.__save_current_features()
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

    def turnon_features(self):
        if self.__features_switch is False:
            self.__toggle_features(True)
            self.__features_switch = True

    def turnoff_features(self):
        if self.__features_switch is True:
            self.__toggle_features(False)
            self.__features_switch = False

    def __save_current_features(self):
        self.current_calculation = self.application.calculation
        self.current_display_alerts = self.application.display_alerts
        self.current_screen_updating = self.application.screen_updating
        self.current_enable_events = self.application.api.EnableEvents
        self.current_enable_animations = self.application.api.EnableAnimations
        self.current_display_pagebreaks = self.sheet.api.DisplayPagebreaks

    def exit(self):
        self.application.quit()

    def add_book(self):
        book = self.application.books.add()
        self.book = book
        self.sheet = self.book.sheets.active
        self.turnoff_features()

    def save_book(self, excel_path):
        self.book.save(excel_path)

    def close_book(self):
        self.turnon_features()
        self.book.close()
