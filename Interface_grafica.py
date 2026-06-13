import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QComboBox, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QListWidget, QFrame, QAbstractItemView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from GestorDistritos import GestorDistritos
from GestorMunicipios import GestorMunicipios
from GestorContratos import GestorContratos

class KPICard(QFrame):
    """Custom dashboard metric layout card for financial KPI statistics."""

    def __init__(self, title, value, footer=""):
        super().__init__()
        self.setObjectName("KPICard")

        self.setStyleSheet("""
            QFrame#KPICard {
                background-color: #1e1e24;
                border: 1px solid #2d2d34;
                border-radius: 8px;
                padding: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(2)

        lbl_title = QLabel(title.upper())
        lbl_title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #a1a1aa;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_val = QLabel(str(value))
        lbl_val.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        lbl_val.setStyleSheet("color: #ffffff; margin: 2px 0px;")
        lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)

        if footer:
            lbl_foot = QLabel(footer)
            lbl_foot.setFont(QFont("Segoe UI", 9, QFont.Weight.Medium))
            lbl_foot.setStyleSheet("color: #38bdf8;")  # Highlighted cyan text
            lbl_foot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_foot)


class CityContractFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("City Contract Finder")
        self.resize(1100, 650)
        self.setMinimumSize(950, 580)

        # Central Window Widget Setup
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        # Main Layout Setup
        workspace_layout = QVBoxLayout(central_widget)
        workspace_layout.setContentsMargins(30, 25, 30, 30)
        workspace_layout.setSpacing(18)

        # Global Application Stylesheet (Dark Enterprise Palette)
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

            /* Table Custom Styles */
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

            /* Bottom Cards / Lists styling */
            QListWidget {
                background-color: #18181c;
                border: 1px solid #252529;
                border-radius: 8px;
                color: #e4e4e7;
                padding: 8px;
            }
        """)

        # --- TOP HEADER BAR ---
        top_bar = QHBoxLayout()

        app_logo = QLabel("🏢 City Contract Finder")
        app_logo.setObjectName("AppBranding")
        top_bar.addWidget(app_logo)
        top_bar.addStretch()

        lbl_district = QLabel("District:")
        lbl_district.setStyleSheet("color: #a1a1aa;")
        self.combo_district = QComboBox()
        dist = GestorDistritos()
        self.combo_district.addItems(dist.get_listadistritos()) # TODO : adicionar distritos
        self.combo_district.setFixedWidth(160)
        self.combo_district.currentTextChanged.connect(self.update_city)

        lbl_city = QLabel("City:")
        lbl_city.setStyleSheet("color: #a1a1aa;")
        self.combo_city = QComboBox()
        
        self.combo_city.setFixedWidth(140)
        self.update_city()
        btn_update = QPushButton("UPDATE LOCATION")
        btn_update.setObjectName("UpdateBtn")
        btn_update.clicked.connect(self.update_contracts)

        top_bar.addWidget(lbl_district)
        top_bar.addWidget(self.combo_district)
        top_bar.addWidget(lbl_city)
        top_bar.addWidget(self.combo_city)
        top_bar.addWidget(btn_update)
        workspace_layout.addLayout(top_bar)

        # Table Header Section Label
        lbl_table_header = QLabel("ACTIVE CONTRACTS IN LISBON (LISBON DISTRICT)") # TODO : texto depende do distrito seleccionado
        lbl_table_header.setObjectName("SectionTitle")
        workspace_layout.addWidget(lbl_table_header)

        # --- CONTRACT DATA GRID (QTableWidget) ---
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(
            ["Contract ID", "Vendor", "Status", "Description", "Value (€)", "End Date"])
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Fit header sizes dynamically
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        workspace_layout.addWidget(self.table_widget)

        # --- BOTTOM OVERVIEW REGION ---
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        # Column Layout 1: KPI Block Matrix Cards
        kpi_grid_layout = QVBoxLayout()
        kpi_grid_layout.setSpacing(12)

        # TODO : actualizar kpi
        row_kpi_1 = QHBoxLayout()
        self.card_total = KPICard("Total Active Contracts", "156", "Active Tenders")
        self.card_value = KPICard("Total Contract Value", "45,800,000 €", "Allocated Budget")
        row_kpi_1.addWidget(self.card_total)
        row_kpi_1.addWidget(self.card_value)

        # TODO : actualizar KPI
        row_kpi_2 = QHBoxLayout()
        self.card_largest = KPICard("Largest Active Contract", "5,200,000 €", "Public Works Dept")
        self.card_avg = KPICard("Avg Contract Value", "293,589 €", "Standard Distribution")
        row_kpi_2.addWidget(self.card_largest)
        row_kpi_2.addWidget(self.card_avg)

        kpi_grid_layout.addLayout(row_kpi_1)
        kpi_grid_layout.addLayout(row_kpi_2)
        bottom_row.addLayout(kpi_grid_layout, stretch=4)

        # Column Layout 2: Department Breakdown Breakdown Display
        dept_container = QVBoxLayout()
        lbl_dept_title = QLabel("DEPARTMENT ALLOCATION")
        lbl_dept_title.setObjectName("SectionTitle")

        self.dept_feed = QListWidget()
        # TODO : actualizar as percentagens
        self.dept_feed.addItems([
            "🏗️ Public Works & Infrastructure ────────── 40%",
            "🚌 Transportation & Transit ─────────────── 20%",
            "🧹 Sanitation & Waste Management ────────── 20%",
            "🌳 Parks & Green Spaces ────────────────── 10%",
            "🛡️ Public Safety & Security ───────────────── 6%",
            "📁 Administration & Tech Support ──────────── 4%"
        ])
        dept_container.addWidget(lbl_dept_title)
        dept_container.addWidget(self.dept_feed)
        bottom_row.addLayout(dept_container, stretch=3)

        # Column Layout 3: Recent Awards Ticker Timeline Feed
        recent_container = QVBoxLayout()
        lbl_recent_title = QLabel("RECENTLY AWARDED CONTRACTS")
        lbl_recent_title.setObjectName("SectionTitle")

        self.recent_feed = QListWidget()
        # TODO :
        self.recent_feed.addItems([
            "✨ [12/01/2026] Acme Paving ─ Resurfacing project",
            "✨ [08/01/2026] Vertex Tech ─ Network upgrade",
            "✨ [03/01/2026] GreenScape ─ Public square garden",
            "✨ [22/12/2025] SafeRoute Inc ─ Smart light grid"
        ])
        recent_container.addWidget(lbl_recent_title)
        recent_container.addWidget(self.recent_feed)
        bottom_row.addLayout(recent_container, stretch=3)

        workspace_layout.addLayout(bottom_row)

        # Initialize Sample Mock Data rows
        self.update_contracts()

    def update_contracts(self):
        mun = GestorMunicipios()
        id_municipio = mun.get_listamunicipios(self.combo_city.currentText())
        contratos = GestorContratos(id_municipio)

        
        lista_contratos = contratos.obter_contratos()
        """Loads mockup row indices inside the dataset tables frame."""
        print("Update Contracts")
        # TODO:
        
        """mock_contracts = [(
            ("0015", "Acme Paving Ltd.", "In Progress", "Avenida da Liberdade Road Resurfacing", "1,250,000",
             "11/30/2026"),
            ("0013", "Sintra Builders S.A.", "In Progress", "Structural Retrofitting Civic Center", "650,000",
             "08/15/2026"),
            ("0022", "Vertex Systems", "Under Review", "Municipal Cloud Infrastructure Migrations", "2,100,000",
             "03/01/2027"),
            ("0023", "EcoClean Solutions", "In Progress", "District Fleet Maintenance & Waste Logistics", "1,450,000",
             "12/31/2026"),
            ("0014", "Logilux Security", "Completed", "CCTV Monitoring System Expansion Phase II", "420,000",
             "05/01/2026"))
        ]"""

        self.table_widget.setRowCount(len(lista_contratos))

        for row_idx, contrato in enumerate(lista_contratos):
            dados = (
                str(contrato.get("id", "")),
                str(contrato.get("object", "")),
                str(contrato.get("procedure_type", "")),
                str(contrato.get("contract_price", "")),
                str(contrato.get("publication_date", "")),
                str(contrato.get("district_code", "")),
            )

            for col_idx, text in enumerate(dados):
                item = QTableWidgetItem(text)

                if col_idx == 2:
                    if "In Progress" in text:
                        item.setForeground(QColor("#34d399"))
                    elif "Under Review" in text:
                        item.setForeground(QColor("#fbbf24"))
                    else:
                        item.setForeground(QColor("#a1a1aa"))

                elif col_idx == 3:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                self.table_widget.setItem(row_idx, col_idx, item)

    def update_city(self):
        mun = GestorMunicipios()
        dist = GestorDistritos()
        codigo_distrito = dist.get_iddistrito(self.combo_district.currentText())
        print("Update Cities")
        self.combo_city.clear()
        self.combo_city.addItems(mun.get_listamunicipios(codigo_distrito)) # TODO : seleccionar cidade correcta
        pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = CityContractFinderApp()
    window.show()
    sys.exit(app.exec())