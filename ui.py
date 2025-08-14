from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QComboBox, QMessageBox, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor
from typing import Optional

class JogoDaVelhaUI(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Jogo da Velha")
        self.setMinimumSize(1000, 700)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        self.setup_ui()

    def setup_ui(self):
        self.jogo_panel = QWidget()
        self.jogo_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.jogo_layout = QVBoxLayout()
        self.jogo_panel.setLayout(self.jogo_layout)
        
        self.titulo_jogo = QLabel("JOGO DA VELHA")
        self.titulo_jogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo_jogo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.titulo_jogo.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        self.jogo_layout.addWidget(self.titulo_jogo)
        
        self.tabuleiro_widget = QWidget()
        self.tabuleiro_layout = QGridLayout()
        self.tabuleiro_widget.setLayout(self.tabuleiro_layout)
        self.tabuleiro_layout.setSpacing(5)
        
        self.botoes_tabuleiro = []
        for i in range(3):
            for j in range(3):
                btn = QPushButton("")
                btn.setFixedSize(120, 120)
                btn.setFont(QFont("Arial", 40, QFont.Weight.Bold))
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ecf0f1;
                        border: 2px solid #bdc3c7;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #d6dbdf;
                    }
                """)
                btn.clicked.connect(self.criar_manipulador_jogada(i, j))
                self.tabuleiro_layout.addWidget(btn, i, j)
                self.botoes_tabuleiro.append(btn)
        
        self.jogo_layout.addWidget(self.tabuleiro_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.status_jogo = QLabel("Aguardando início do jogo")
        self.status_jogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_jogo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.status_jogo.setStyleSheet("color: #2c3e50; margin: 20px 0;")
        self.jogo_layout.addWidget(self.status_jogo)
        
        self.btn_reiniciar = QPushButton("REINICIAR JOGO")
        self.btn_reiniciar.setFixedHeight(50)
        self.btn_reiniciar.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.btn_reiniciar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_reiniciar.clicked.connect(self.reiniciar_jogo)
        self.jogo_layout.addWidget(self.btn_reiniciar)
        

        self.info_panel = QWidget()
        self.info_panel.setMinimumWidth(400)
        self.info_layout = QVBoxLayout()
        self.info_panel.setLayout(self.info_layout)
        
     
        self.formulario_jogadores = QWidget()
        self.form_layout = QVBoxLayout()
        self.formulario_jogadores.setLayout(self.form_layout)
        
    
        input_style = """
            QLineEdit, QComboBox {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                margin-top: 10px;
            }
        """
        
        
        self.label_jogador_x = QLabel("Jogador X:")
        self.input_jogador_x = QLineEdit()
        self.input_jogador_x.setPlaceholderText("Nome do jogador X")
        self.input_pais_x = QComboBox()
        self.input_pais_x.addItems(["Brasil", "Argentina", "Portugal", "EUA", "Outro"])
        
        
        self.label_jogador_o = QLabel("Jogador O:")
        self.input_jogador_o = QLineEdit()
        self.input_jogador_o.setPlaceholderText("Nome do jogador O")
        self.input_pais_o = QComboBox()
        self.input_pais_o.addItems(["Brasil", "Argentina", "Portugal", "EUA", "Outro"])
        
        
        for widget in [self.label_jogador_x, self.input_jogador_x, self.input_pais_x,
                     self.label_jogador_o, self.input_jogador_o, self.input_pais_o]:
            widget.setStyleSheet(input_style)
        
        self.btn_registrar = QPushButton("REGISTRAR")
        self.btn_registrar.setFixedHeight(45)
        self.btn_registrar.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.btn_registrar.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.btn_registrar.clicked.connect(self.registrar_jogadores)
        
        
        self.form_layout.addWidget(self.label_jogador_x)
        self.form_layout.addWidget(self.input_jogador_x)
        self.form_layout.addWidget(QLabel("País:"))
        self.form_layout.addWidget(self.input_pais_x)
        self.form_layout.addSpacing(15)
        self.form_layout.addWidget(self.label_jogador_o)
        self.form_layout.addWidget(self.input_jogador_o)
        self.form_layout.addWidget(QLabel("País:"))
        self.form_layout.addWidget(self.input_pais_o)
        self.form_layout.addSpacing(20)
        self.form_layout.addWidget(self.btn_registrar)
        
        self.info_layout.addWidget(self.formulario_jogadores)
        
        
        self.ranking_label = QLabel("RANKING DE JOGADORES")
        self.ranking_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ranking_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.ranking_label.setStyleSheet("color: #2c3e50; margin: 20px 0 10px 0;")
        self.info_layout.addWidget(self.ranking_label)
        
        self.tabela_ranking = QTableWidget()
        self.tabela_ranking.setColumnCount(5)
        self.tabela_ranking.setHorizontalHeaderLabels(["#", "Nome", "País", "Vitórias", "Empates"])
        self.tabela_ranking.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.tabela_ranking.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f2f2f2;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.tabela_ranking.verticalHeader().setVisible(False)
        self.tabela_ranking.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_ranking.setAlternatingRowColors(True)
        
        header = self.tabela_ranking.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.info_layout.addWidget(self.tabela_ranking)
        
        self.main_layout.addWidget(self.jogo_panel, stretch=2)
        self.main_layout.addWidget(self.info_panel, stretch=1)

    def criar_manipulador_jogada(self, linha, coluna):
        def manipulador():
            self.realizar_jogada(linha, coluna)
        return manipulador

    def realizar_jogada(self, linha, coluna):
        pass

    def atualizar_tabuleiro_ui(self, tabuleiro):
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                self.botoes_tabuleiro[index].setText(tabuleiro[i][j])
                self.botoes_tabuleiro[index].setEnabled(tabuleiro[i][j] == " ")

    def atualizar_status_jogo(self, vencedor, empate):
        if vencedor:
            nome_vencedor = self.jogador_x if vencedor == "X" else self.jogador_o
            self.status_jogo.setText(f"VENCEDOR: {nome_vencedor} ({vencedor})")
            self.status_jogo.setStyleSheet("color: #27ae60; font-weight: bold;")
        elif empate:
            self.status_jogo.setText("EMPATE!")
            self.status_jogo.setStyleSheet("color: #f39c12; font-weight: bold;")
        else:
            jogador_atual_nome = self.jogador_x if self.jogo.jogador_atual == "X" else self.jogador_o
            self.status_jogo.setText(f"Vez de: {jogador_atual_nome} ({self.jogo.jogador_atual})")
            self.status_jogo.setStyleSheet("color: #2c3e50; font-weight: bold;")

    def reiniciar_jogo(self):
        pass

    def registrar_jogadores(self):
        nome_x = self.input_jogador_x.text().strip()
        nome_o = self.input_jogador_o.text().strip()
        
        if not nome_x or not nome_o:
            QMessageBox.warning(self, "Aviso", "Por favor, insira os nomes de ambos os jogadores.")
            return
        
        if nome_x == nome_o:
            QMessageBox.warning(self, "Aviso", "Os nomes dos jogadores devem ser diferentes.")
            return
        
        pais_x = self.input_pais_x.currentText()
        pais_o = self.input_pais_o.currentText()
        
        
        jogador_x = self.db.buscar_jogador(nome_x)
        if not jogador_x:
            self.db.adicionar_jogador(nome_x, pais_x)
        
        jogador_o = self.db.buscar_jogador(nome_o)
        if not jogador_o:
            self.db.adicionar_jogador(nome_o, pais_o)
        
        self.jogador_x = nome_x
        self.jogador_o = nome_o
        self.pais_x = pais_x
        self.pais_o = pais_o
        
        self.status_jogo.setText(f"Vez de: {self.jogador_x} (X)")
        self.status_jogo.setStyleSheet("color: #2c3e50; font-weight: bold;")
        
        QMessageBox.information(self, "Sucesso", "Jogadores registrados com sucesso!")
        self.atualizar_ranking()

    def atualizar_ranking(self):
        ranking = self.db.obter_ranking()
        self.tabela_ranking.setRowCount(len(ranking))
        
        for i, jogador in enumerate(ranking):
            self.tabela_ranking.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.tabela_ranking.setItem(i, 1, QTableWidgetItem(jogador["nome"]))
            self.tabela_ranking.setItem(i, 2, QTableWidgetItem(jogador["pais"]))
            self.tabela_ranking.setItem(i, 3, QTableWidgetItem(str(jogador["vitorias"])))
            self.tabela_ranking.setItem(i, 4, QTableWidgetItem(str(jogador["empates"])))
            
            
            if hasattr(self, 'jogador_x') and jogador["nome"] in [self.jogador_x, self.jogador_o]:
                for col in range(5):
                    self.tabela_ranking.item(i, col).setBackground(QColor(200, 230, 255))
                    self.tabela_ranking.item(i, col).setFont(QFont("Arial", 12, QFont.Weight.Bold))