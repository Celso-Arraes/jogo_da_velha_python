import sqlite3
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name: str = "jogo_da_velha.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pais TEXT,
            vitorias INTEGER DEFAULT 0,
            derrotas INTEGER DEFAULT 0,
            empates INTEGER DEFAULT 0
        )
        """)
        self.conn.commit()

    def adicionar_jogador(self, nome: str, pais: str = "Desconhecido") -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO jogadores (nome, pais) VALUES (?, ?)
        """, (nome, pais))
        self.conn.commit()
        return cursor.lastrowid

    def buscar_jogador(self, nome: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT id, nome, pais, vitorias, derrotas, empates 
        FROM jogadores 
        WHERE nome = ?
        """, (nome,))
        result = cursor.fetchone()
        if result:
            return {
                "id": result[0],
                "nome": result[1],
                "pais": result[2],
                "vitorias": result[3],
                "derrotas": result[4],
                "empates": result[5]
            }
        return None

    def atualizar_estatisticas(self, jogador_id: int, vitoria: bool = False, derrota: bool = False, empate: bool = False):
        cursor = self.conn.cursor()
        if vitoria:
            cursor.execute("""
            UPDATE jogadores SET vitorias = vitorias + 1 WHERE id = ?
            """, (jogador_id,))
        elif derrota:
            cursor.execute("""
            UPDATE jogadores SET derrotas = derrotas + 1 WHERE id = ?
            """, (jogador_id,))
        elif empate:
            cursor.execute("""
            UPDATE jogadores SET empates = empates + 1 WHERE id = ?
            """, (jogador_id,))
        self.conn.commit()

    def obter_ranking(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT nome, pais, vitorias, derrotas, empates 
        FROM jogadores 
        ORDER BY vitorias DESC, empates DESC
        """)
        ranking = []
        for row in cursor.fetchall():
            ranking.append({
                "nome": row[0],
                "pais": row[1],
                "vitorias": row[2],
                "derrotas": row[3],
                "empates": row[4]
            })
        return ranking

    def close(self):
        self.conn.close()