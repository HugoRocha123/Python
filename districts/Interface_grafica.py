import sys
from datetime import datetime
from collections import Counter
from GestorDistritos import GestorDistritos
from GestorMunicipios import GestorMunicipios
from GestorContratos import GestorContratos

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QComboBox, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QListWidget, QFrame, QAbstractItemView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor


def format_currency(value):
    try:
        return f"{float(value):,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "0,00 €"


def format_date(date_str):
    try:
        if not date_str:
            return ""
        dt = datetime.fromisoformat(str(date_str).replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return str(date_str)


class KPICard(QFrame):
    def __init__(self, title, value, subtitle=""):
        super().__init__()
        self.setObjectName("KPICard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(6)

        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("color: #a1a1aa; font-size: 12px; font-weight: bold;")

        self.lbl_value = QLabel(str(value))
        self.lbl_value.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: bold;")

        self.lbl_subtitle = QLabel(subtitle)
        self.lbl_subtitle.setStyleSheet("color: #71717a; font-size: 11px;")

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)
        layout.addWidget(self.lbl_subtitle)

        self.setStyleSheet("""
            QFrame#KPICard {
                background-color: #18181c;
                border: 1px solid #252529;
                border-radius: 10px;
            }
        """)

    def setValue(self, value):
        self.lbl_value.setText(str(value))

    def setTitle(self, title):
        self.lbl_title.setText(str(title))

    def setSubtitle(self, subtitle):
        self.lbl_subtitle.setText(str(subtitle))


class CityContractFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("City Contract Finder")
        self.resize(1100, 650)
        self.setMinimumSize(950, 580)

        self.gestor_distritos = GestorDistritos()
        self.gestor_municipios = GestorMunicipios()

        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        workspace_layout = QVBoxLayout(central_widget)
        workspace_layout.setContentsMargins(30, 25, 30, 30)
        workspace_layout.setSpacing(18)

        self.setStyleSheet("""
            QWidget#CentralWidget {
                background-color: #121214;
            }
            QLabel#AppBranding {
                color: #38bdf8;
                font-size: 20px;
                font-weight: bold;
            }
            QLabel#SectionTitle {
                color: #ffffff;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QComboBox {
                background-color: #1e1e24;
                border: 1px solid #2d2d34;
                border-radius: 6px;
                padding: 6px 12px;
                color: #ffffff;
            }
            QPushButton#UpdateBtn {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 7px 16px;
                font-weight: bold;
            }
            QPushButton#UpdateBtn:hover { background-color: #059669; }

            QTableWidget {
                background-color: #18181c;
                border: 1px solid #252529;
                border-radius: 8px;
                gridline-color: #252529;
                color: #e4e4e7;
            }
            QHeaderView::section {
                background-color: #1e1e24;
                color: #a1a1aa;
                padding: 8px;
                border: none;
                font-weight: bold;
                border-bottom: 1px solid #252529;
            }
            QListWidget {
                background-color: #18181c;
                border: 1px solid #252529;
                border-radius: 8px;
                color: #e4e4e7;
                padding: 8px;
            }
        """)

        top_bar = QHBoxLayout()

        app_logo = QLabel("🏢 City Contract Finder")
        app_logo.setObjectName("AppBranding")
        top_bar.addWidget(app_logo)
        top_bar.addStretch()

        lbl_district = QLabel("District:")
        lbl_district.setStyleSheet("color: #a1a1aa;")
        self.combo_district = QComboBox()
        self.combo_district.setFixedWidth(160)
        self.combo_district.currentTextChanged.connect(self.update_city)

        lbl_city = QLabel("City:")
        lbl_city.setStyleSheet("color: #a1a1aa;")
        self.combo_city = QComboBox()
        self.combo_city.setFixedWidth(140)

        btn_update = QPushButton("UPDATE LOCATION")
        btn_update.setObjectName("UpdateBtn")
        btn_update.clicked.connect(self.update_contracts)

        top_bar.addWidget(lbl_district)
        top_bar.addWidget(self.combo_district)
        top_bar.addWidget(lbl_city)
        top_bar.addWidget(self.combo_city)
        top_bar.addWidget(btn_update)
        workspace_layout.addLayout(top_bar)

        self.lbl_table_header = QLabel("ACTIVE CONTRACTS")
        self.lbl_table_header.setObjectName("SectionTitle")
        workspace_layout.addWidget(self.lbl_table_header)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ["Contract ID", "Object", "Procedure Type", "Value (€)", "Publication Date", "District Code", "Municipality Code"]
        )
        self.table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        workspace_layout.addWidget(self.table_widget)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        kpi_grid_layout = QVBoxLayout()
        kpi_grid_layout.setSpacing(12)

        row_kpi_1 = QHBoxLayout()
        self.card_total = KPICard("Total Active Contracts", "0", "Loaded from data")
        self.card_value = KPICard("Total Contract Value", "0,00 €", "Loaded from data")
        row_kpi_1.addWidget(self.card_total)
        row_kpi_1.addWidget(self.card_value)

        row_kpi_2 = QHBoxLayout()
        self.card_largest = KPICard("Largest Active Contract", "0,00 €", "Loaded from data")
        self.card_avg = KPICard("Avg Contract Value", "0,00 €", "Loaded from data")
        row_kpi_2.addWidget(self.card_largest)
        row_kpi_2.addWidget(self.card_avg)

        kpi_grid_layout.addLayout(row_kpi_1)
        kpi_grid_layout.addLayout(row_kpi_2)
        bottom_row.addLayout(kpi_grid_layout, stretch=4)

        dept_container = QVBoxLayout()
        lbl_dept_title = QLabel("PROCEDURE TYPE DISTRIBUTION")
        lbl_dept_title.setObjectName("SectionTitle")

        self.dept_feed = QListWidget()
        self.dept_feed.addItem("Loading data...")

        dept_container.addWidget(lbl_dept_title)
        dept_container.addWidget(self.dept_feed)
        bottom_row.addLayout(dept_container, stretch=3)

        recent_container = QVBoxLayout()
        lbl_recent_title = QLabel("RECENTLY AWARDED CONTRACTS")
        lbl_recent_title.setObjectName("SectionTitle")

        self.recent_feed = QListWidget()
        self.recent_feed.addItem("Loading data...")

        recent_container.addWidget(lbl_recent_title)
        recent_container.addWidget(self.recent_feed)
        bottom_row.addLayout(recent_container, stretch=3)

        workspace_layout.addLayout(bottom_row)

        self.load_districts()
        self.update_city()
        self.combo_city.currentTextChanged.connect(self.update_contracts)
        self.update_contracts()

    def load_districts(self):
        self.combo_district.blockSignals(True)
        self.combo_district.clear()

        self.combo_district.addItem("All Districts", None)

        if hasattr(self.gestor_distritos, "obter_distritos"):
            distritos = self.gestor_distritos.obter_distritos()
            for d in distritos:
                if isinstance(d, dict):
                    self.combo_district.addItem(d.get("nome", ""), d.get("id"))
                else:
                    self.combo_district.addItem(str(d), str(d))
        elif hasattr(self.gestor_distritos, "get_listadistritos"):
            distritos = self.gestor_distritos.get_listadistritos()
            for d in distritos:
                self.combo_district.addItem(str(d), str(d))

        self.combo_district.blockSignals(False)

    def update_city(self):
        
        district_name = self.combo_district.currentText()
        district_code = self.gestor_distritos.get_iddistrito(district_name)
        if hasattr(self.gestor_distritos, "get_iddistrito"):
            district_code = self.gestor_distritos.get_iddistrito(district_name) or district_code

        self.combo_city.blockSignals(True)
        self.combo_city.clear()
        self.combo_city.addItem("All Cities", None)

        municipios = []
        if district_code:
            if hasattr(self.gestor_municipios, "obter_municipios"):
                municipios = self.gestor_municipios.obter_municipios(district_code)
            elif hasattr(self.gestor_municipios, "get_listamunicipios"):
                municipios = self.gestor_municipios.get_listamunicipios(district_code)

        if municipios:
            for m in municipios:
                if isinstance(m, dict):
                    self.combo_city.addItem(m.get("nome", ""), m.get("id"))
                else:
                    self.combo_city.addItem(str(m), str(m))

        self.combo_city.blockSignals(False)

        if self.combo_city.count() > 0:
            self.combo_city.setCurrentIndex(0)

    def update_contracts(self):
        district_name = self.combo_district.currentText()
        city_name = self.combo_city.currentText()

        district_code = self.gestor_distritos.get_iddistrito(district_name)
        municipality_code =  self.gestor_municipios.get_idmmunicipios(city_name)

        print("=== DEBUG ===")
        print("district_name:", district_name)
        print("city_name:", city_name)
        print("district_code:", district_code)
        print("municipality_code:", municipality_code)

        contratos = GestorContratos(municipality_code)
        lista_contratos = contratos.obter_contratos(20)

        print("contratos recebidos da API:", len(lista_contratos))

        self.table_widget.setRowCount(len(lista_contratos))

        total_value = 0.0
        largest_value = 0.0

        for row_idx, contrato in enumerate(lista_contratos):
            contract_id = str(contrato.get("id", ""))
            obj = str(contrato.get("object", ""))
            procedure_type = str(contrato.get("procedure_type", ""))
            contract_price = contrato.get("contract_price", 0)
            publication_date = format_date(contrato.get("publication_date", ""))
            district_code_txt = str(contrato.get("district_code", ""))
            municipality_code_txt = str(contrato.get("municipality_code", ""))

            try:
                price_value = float(contract_price or 0)
            except (TypeError, ValueError):
                price_value = 0.0

            total_value += price_value
            largest_value = max(largest_value, price_value)

            dados = (
                contract_id,
                obj,
                procedure_type,
                format_currency(contract_price),
                publication_date,
                district_code_txt,
                municipality_code_txt,
            )

            for col_idx, text in enumerate(dados):
                item = QTableWidgetItem(text)
                if col_idx == 3:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    item.setForeground(QColor("#34d399"))
                self.table_widget.setItem(row_idx, col_idx, item)

        total_contracts = len(lista_contratos)
        avg_value = total_value / total_contracts if total_contracts else 0.0

        self.card_total.setValue(str(total_contracts))
        self.card_value.setValue(format_currency(total_value))
        self.card_largest.setValue(format_currency(largest_value))
        self.card_avg.setValue(format_currency(avg_value))

        if city_name and city_name != "All Cities":
            self.lbl_table_header.setText(
                f"ACTIVE CONTRACTS IN {city_name.upper()} ({district_name.upper()} DISTRICT)"
            )
        elif district_name and district_name != "All Districts":
            self.lbl_table_header.setText(
                f"ACTIVE CONTRACTS IN {district_name.upper()} DISTRICT"
            )
        else:
            self.lbl_table_header.setText("ACTIVE CONTRACTS")

        self.dept_feed.clear()
        if total_contracts:
            counts = Counter(str(c.get("procedure_type", "Unknown")) for c in lista_contratos)
            for procedure_type, count in counts.most_common():
                percent = (count / total_contracts) * 100
                self.dept_feed.addItem(f"📄 {procedure_type} ────────── {percent:.0f}%")
        else:
            self.dept_feed.addItem("No data available")

        self.recent_feed.clear()
        if lista_contratos:
            recentes = sorted(
                lista_contratos,
                key=lambda x: str(x.get("publication_date", "")),
                reverse=True
            )[:5]

            for contrato in recentes:
                date_txt = format_date(contrato.get("publication_date", ""))
                obj_txt = str(contrato.get("object", ""))
                if len(obj_txt) > 60:
                    obj_txt = obj_txt[:57] + "..."
                self.recent_feed.addItem(f"✨ [{date_txt}] {obj_txt}")
        else:
            self.recent_feed.addItem("No recent contracts")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = CityContractFinderApp()
    window.show()
    sys.exit(app.exec())
