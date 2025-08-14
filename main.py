import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from database import Database
from game_logic import JogoDaVelha
from ui import JogoDaVelhaUI

class JogoDaVelhaApp(JogoDaVelhaUI):
    def __init__(self, db):
        super().__init__(db)
        self.jogo = JogoDaVelha()
        self.jogador_x = None
        self.jogador_o = None
        self.pais_x = None
        self.pais_o = None
        
       
        self.btn_reiniciar.clicked.connect(self.reiniciar_jogo)
        

        self.atualizar_ui()

    def realizar_jogada(self, linha, coluna):
        if not self.jogador_x or not self.jogador_o:
            QMessageBox.warning(self, "Aviso", "Por favor, registre os jogadores primeiro.")
            return
            
        if self.jogo.fazer_jogada(linha, coluna):
            self.atualizar_ui()
            
            tabuleiro, vencedor, empate = self.jogo.obter_estado()
            
            if vencedor or empate:
                self.atualizar_estatisticas(vencedor, empate)
                
                msg = QMessageBox()
                msg.setWindowTitle("Fim de jogo")
                
                if vencedor:
                    nome_vencedor = self.jogador_x if vencedor == "X" else self.jogador_o
                    msg.setText(f"{nome_vencedor} ({vencedor}) venceu!\nDeseja jogar novamente?")
                else:
                    msg.setText("Empate!\nDeseja jogar novamente?")
                
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                resposta = msg.exec()
                
                if resposta == QMessageBox.StandardButton.Yes:
                    self.reiniciar_jogo()

    def atualizar_ui(self):
        tabuleiro, vencedor, empate = self.jogo.obter_estado()
        self.atualizar_tabuleiro_ui(tabuleiro)
        self.atualizar_status_jogo(vencedor, empate)

    def reiniciar_jogo(self):
        self.jogo.reiniciar()
        self.atualizar_ui()
        
      
        for btn in self.botoes_tabuleiro:
            btn.setEnabled(True)

    def atualizar_estatisticas(self, vencedor, empate):
        if not hasattr(self, 'jogador_x') or not hasattr(self, 'jogador_o'):
            return
            
        jogador_x_db = self.db.buscar_jogador(self.jogador_x)
        jogador_o_db = self.db.buscar_jogador(self.jogador_o)
        
        if vencedor == "X":
            self.db.atualizar_estatisticas(jogador_x_db["id"], vitoria=True)
            self.db.atualizar_estatisticas(jogador_o_db["id"], derrota=True)
        elif vencedor == "O":
            self.db.atualizar_estatisticas(jogador_o_db["id"], vitoria=True)
            self.db.atualizar_estatisticas(jogador_x_db["id"], derrota=True)
        elif empate:
            self.db.atualizar_estatisticas(jogador_x_db["id"], empate=True)
            self.db.atualizar_estatisticas(jogador_o_db["id"], empate=True)
        
        self.atualizar_ranking()

def main():
    app = QApplication(sys.argv)
    
    
    app.setStyle("Fusion")
    
    
    db = Database()

    
    janela = JogoDaVelhaApp(db)
    janela.show()
    
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()