from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import OWAction

from oasys.widgets import widget
import oasys.widgets.gui as oasysgui
from oasys.widgets.gui import ConfirmDialog

class MyFirstWidget(widget.OWWidget):
    name = "My 1st Widget"
    description = "My 1st Widget"
    icon = "icons/n1.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "<my email>"
    priority = 1
    category = "Tools"
    keywords = ["data", "file", "load", "read"]

    want_main_area = 1

    inputs = [("my_input_data", object, "set_input"),]

    outputs = [{"name": "my_output_data",
                "type": object,
                "doc": "my_output_data",
                "id": "my_output_data"}, ]

    want_main_area=1

    MAX_WIDTH = 1320
    MAX_HEIGHT = 700

    CONTROL_AREA_WIDTH = 405
    TABS_AREA_HEIGHT = 560

    field_1 = Setting(1.0)
    field_2 = Setting("this is a string")
    field_3 = Setting(1)
    field_4 = Setting(2)
    field_5 = Setting(0)
    file = "select me!"
    notes = Setting("this is a text area")

    def __init__(self):
        super().__init__()

        geom = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(round(geom.width()*0.05),
                               round(geom.height()*0.05),
                               round(min(geom.width()*0.98, self.MAX_WIDTH)),
                               round(min(geom.height()*0.95, self.MAX_HEIGHT))))

        self.setMaximumHeight(self.geometry().height())
        self.setMaximumWidth(self.geometry().width())


        self.runaction = OWAction("Run Action", self)
        self.runaction.triggered.connect(self.run_action)
        self.addAction(self.runaction)


        # CONTROL AREA
        self.controlArea.setFixedWidth(self.CONTROL_AREA_WIDTH)

        general_options_box = oasysgui.widgetBox(self.controlArea, "General Options", addSpace=True, orientation="vertical", width=400)

        oasysgui.lineEdit(general_options_box, self, "field_1", label="Field 1", labelWidth=250, addSpace=False, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(general_options_box, self, "field_2", label="Field 2", labelWidth=250, addSpace=False, valueType=str, orientation="horizontal")

        gui.comboBox(general_options_box, self, "field_3", label="Field 3",
                     items=["Option 1", "Option 2", "Option 3", "Option 4"],
                     sendSelectedValue=False, orientation="horizontal",
                     callback=self.set_field_3)

        gui.radioButtons(general_options_box, self, "field_4",
                         ["Option 1", "Option 2", "Option 3", "Option 4"],
                         callback=self.set_field_4)

        gui.checkBox(general_options_box, self, 'field_5', 'Field 5')


        file_box = oasysgui.widgetBox(general_options_box, "", addSpace=False, orientation="horizontal", height=25)

        self.le_file = oasysgui.lineEdit(file_box, self, "file", label="some file", addSpace=False, orientation="horizontal")

        gui.button(file_box, self, "...", callback=self.select_file)

        text_area_box = oasysgui.widgetBox(general_options_box, "", addSpace=False, orientation="vertical", width=390, height=330)

        self.text_area = oasysgui.textArea(height=320, width=380, readOnly=False)
        self.text_area.setText(self.notes)
        self.text_area.textChanged.connect(self.set_text_area)

        text_area_box.layout().addWidget(self.text_area)

        gui.separator(general_options_box)

        gui.button(general_options_box, self, "Run Action", callback=self.run_action, height=45)

        self.call_callbacks()

        # MAIN AREA
        self.main_tabs = oasysgui.tabWidget(self.mainArea)

        plot_tab = oasysgui.createTabPage(self.main_tabs, "Plots")
        out_tab = oasysgui.createTabPage(self.main_tabs, "Output")

    def call_callbacks(self):
        self.set_field_3()
        self.set_field_4()

    def set_text_area(self):
        self.notes = self.text_area.toPlainText()

    def select_file(self):
        self.le_file.setText(oasysgui.selectFileFromDialog(self, self.file, "Open File", file_extension_filter="*.txt"))

    def run_action(self):
        if ConfirmDialog.confirmed(self):
            self.send("my_output_data", "HI! I am a newborn widget!")

    def set_field_3(self):
        self.field_1 = 1.0*(self.field_3 + 1)

    def set_field_4(self):
        self.field_2 = "Option " + str(self.field_4 + 1)

    def set_input(self, input_data):
        pass

import sys

if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = MyFirstWidget()
    ow.show()
    a.exec_()
    ow.saveSettings()
