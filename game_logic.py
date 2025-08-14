from typing import List, Optional, Tuple

class JogoDaVelha:
    def __init__(self):
        self.tabuleiro: List[List[str]] = [[" " for _ in range(3)] for _ in range(3)]
        self.jogador_atual: str = "X"
        self.vencedor: Optional[str] = None
        self.empate: bool = False

    def fazer_jogada(self, linha: int, coluna: int) -> bool:
        if self.tabuleiro[linha][coluna] != " " or self.vencedor is not None:
            return False

        self.tabuleiro[linha][coluna] = self.jogador_atual
        self.verificar_vitoria(linha, coluna)
        self.verificar_empate()

        if not self.vencedor and not self.empate:
            self.jogador_atual = "O" if self.jogador_atual == "X" else "X"
        
        return True

    def verificar_vitoria(self, linha: int, coluna: int):
       
        if all(cell == self.jogador_atual for cell in self.tabuleiro[linha]):
            self.vencedor = self.jogador_atual
            return

        
        if all(self.tabuleiro[i][coluna] == self.jogador_atual for i in range(3)):
            self.vencedor = self.jogador_atual
            return

        
        if linha == coluna and all(self.tabuleiro[i][i] == self.jogador_atual for i in range(3)):
            self.vencedor = self.jogador_atual
            return

        if linha + coluna == 2 and all(self.tabuleiro[i][2-i] == self.jogador_atual for i in range(3)):
            self.vencedor = self.jogador_atual
            return

    def verificar_empate(self):
        if all(cell != " " for row in self.tabuleiro for cell in row) and self.vencedor is None:
            self.empate = True

    def reiniciar(self):
        self.tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
        self.jogador_atual = "X"
        self.vencedor = None
        self.empate = False

    def obter_estado(self) -> Tuple[List[List[str]], Optional[str], bool]:
        return self.tabuleiro, self.vencedor, self.empate