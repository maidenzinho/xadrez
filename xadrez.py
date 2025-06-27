import sys
import random
import chess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout,
    QMessageBox, QComboBox, QVBoxLayout, QLabel, QInputDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt

PIECE_EMOJIS = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟︎', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

class ChessGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xadrez♟️")
        self.board = chess.Board()
        self.buttons = {}
        self.selected_square = None
        self.possible_moves = []
        self.player_color = chess.WHITE  # Default, can be changed
        self.scores = {'player': 0, 'cpu': 0, 'draw': 0}

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Placar
        self.score_label = QLabel(self.score_text())
        self.layout.addWidget(self.score_label)

        # Informação
        self.info_label = QLabel("Sua vez")
        self.layout.addWidget(self.info_label)

        # Escolha de dificuldade
        difficulty_layout = QHBoxLayout()
        self.difficulty_box = QComboBox()
        self.difficulty_box.addItems(["Fácil", "Médio", "Difícil"])
        difficulty_layout.addWidget(QLabel("Dificuldade:"))
        difficulty_layout.addWidget(self.difficulty_box)
        self.layout.addLayout(difficulty_layout)

        # Grade do tabuleiro
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

        self.ask_player_color()

    def score_text(self):
        return f"Você: {self.scores['player']} | CPU: {self.scores['cpu']} | Empates: {self.scores['draw']}"

    def ask_player_color(self):
        color, ok = QInputDialog.getItem(self, "Escolha a cor", "Com qual cor deseja jogar?", ["Brancas", "Pretas"], 0, False)
        if ok:
            self.player_color = chess.WHITE if color == "Brancas" else chess.BLACK
            self.ask_difficulty()
            if self.player_color == chess.BLACK:
                self.cpu_move()
        else:
            self.close()

    def ask_difficulty(self):
        difficulties = ["Fácil", "Médio", "Difícil"]
        difficulty, ok = QInputDialog.getItem(self, "Escolha a dificuldade", "Dificuldade:", difficulties, 0, False)
        if ok:
            index = difficulties.index(difficulty)
            self.difficulty_box.setCurrentIndex(index)
        self.draw_board()

    def draw_board(self):
        # Limpar grid e botões
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.buttons.clear()

        # Montar tabuleiro visual (mostra sempre do ponto de vista do jogador)
        for row in range(8):
            for col in range(8):
                board_row = 7 - row if self.player_color == chess.WHITE else row
                board_col = col if self.player_color == chess.WHITE else 7 - col
                square = chess.square(board_col, board_row)
                piece = self.board.piece_at(square)
                btn = QPushButton()
                btn.setFixedSize(60, 60)
                btn.setStyleSheet(
                    f"font-size:28px;background-color:{'#F0D9B5' if (row + col) % 2 == 0 else '#B58863'};"
                )
                if piece:
                    btn.setText(PIECE_EMOJIS.get(piece.symbol(), ''))
                btn.clicked.connect(lambda _, sq=square: self.handle_click(sq))
                self.grid.addWidget(btn, row, col)
                self.buttons[square] = btn

        self.clear_highlights()
        self.score_label.setText(self.score_text())
        if self.board.is_check():
            if self.board.turn == self.player_color:
                self.info_label.setStyleSheet("color: #cc0000; font-weight: bold")
                self.info_label.setText("Você está em xeque!")
            else:
                self.info_label.setStyleSheet("color: #cc0000; font-weight: bold")
                self.info_label.setText("CPU está em xeque!")
        else:
            self.info_label.setStyleSheet("")
            if self.board.turn == self.player_color:
                self.info_label.setText("Sua vez")
            else:
                self.info_label.setText("Vez da CPU...")

    def handle_click(self, square):
        if self.board.turn != self.player_color or self.board.is_game_over():
            return

        piece = self.board.piece_at(square)
        if self.selected_square is None:
            # Selecionar peça do jogador
            if piece and piece.color == self.player_color:
                self.selected_square = square
                self.highlight_square(square, "red")
                self.highlight_possible_moves(square)
            else:
                self.selected_square = None
                self.clear_highlights()
        else:
            # Tentar movimento
            move = chess.Move(self.selected_square, square)
            if (self.board.piece_at(self.selected_square) and
                self.board.piece_at(self.selected_square).piece_type == chess.PAWN and
                chess.square_rank(square) in [0, 7]):
                move = self.ask_promotion(self.selected_square, square)

            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.clear_highlights()
                self.draw_board()
                if self.board.is_game_over():
                    self.show_game_over()
                else:
                    QApplication.processEvents()
                    self.cpu_move()
            else:
                QMessageBox.warning(self, "Movimento inválido", "Esse movimento não é permitido.")
                self.selected_square = None
                self.clear_highlights()

    def highlight_square(self, square, color):
        btn = self.buttons.get(square)
        if btn:
            btn.setStyleSheet(btn.styleSheet() + f"border: 2px solid {color};")

    def highlight_possible_moves(self, square):
        self.clear_highlights()
        self.highlight_square(square, "red")
        piece = self.board.piece_at(square)
        if not piece:
            return
        for move in self.board.legal_moves:
            if move.from_square == square:
                self.highlight_square(move.to_square, "green")

    def clear_highlights(self):
        for btn in self.buttons.values():
            # Remove bordas coloridas
            style = btn.styleSheet()
            for cor in ["red", "green"]:
                style = style.replace(f"border: 2px solid {cor};", "")
            btn.setStyleSheet(style)

    def ask_promotion(self, from_square, to_square):
        options = ["Rainha", "Torre", "Bispo", "Cavalo"]
        piece_map = {"Rainha": chess.QUEEN, "Torre": chess.ROOK, "Bispo": chess.BISHOP, "Cavalo": chess.KNIGHT}
        choice, ok = QInputDialog.getItem(self, "Promoção", "Escolha a peça para promoção:", options, 0, False)
        if ok:
            return chess.Move(from_square, to_square, promotion=piece_map[choice])
        return chess.Move(from_square, to_square, promotion=chess.QUEEN)

    def cpu_move(self):
        if self.board.is_game_over():
            return
        difficulty = self.difficulty_box.currentText()
        move = None
        if difficulty == "Fácil":
            move = self.blunder_move()
        elif difficulty == "Médio":
            move = self.medium_move()
        elif difficulty == "Difícil":
            move = self.smart_move()
        else:
            move = self.random_move()

        if move:
            # Promoção automática para rainha
            if (self.board.piece_at(move.from_square) and
                self.board.piece_at(move.from_square).piece_type == chess.PAWN and
                chess.square_rank(move.to_square) in [0, 7]):
                move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
            self.board.push(move)
            self.clear_highlights()
            self.draw_board()
            if self.board.is_game_over():
                self.show_game_over()

    def blunder_move(self):
        moves = list(self.board.legal_moves)
        if random.random() < 0.7:
            return random.choice(moves)
        else:
            scored_moves = []
            for move in moves:
                self.board.push(move)
                score = self.evaluate_board()
                self.board.pop()
                scored_moves.append((score, move))
            scored_moves.sort()  # do pior para o melhor
            return scored_moves[0][1] if scored_moves else random.choice(moves)

    def medium_move(self):
        captures = [m for m in self.board.legal_moves if self.board.is_capture(m)]
        if captures and random.random() < 0.8:
            return random.choice(captures)
        scored_moves = []
        for move in self.board.legal_moves:
            self.board.push(move)
            score = self.evaluate_board() + random.uniform(-1, 1)
            self.board.pop()
            scored_moves.append((score, move))
        scored_moves.sort(reverse=True)
        return scored_moves[0][1]

    def smart_move(self):
        best_move = None
        best_score = -float('inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = self.evaluate_board() + 0.1 * len(list(self.board.legal_moves))
            self.board.pop()
            if score > best_score or (score == best_score and random.random() < 0.3):
                best_score = score
                best_move = move
        return best_move if best_move else self.random_move()

    def evaluate_board(self):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3.2,
            chess.BISHOP: 3.3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        score = 0
        for piece_type in piece_values:
            score += len(self.board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
            score -= len(self.board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        # Score do ponto de vista da CPU
        return score if self.player_color == chess.WHITE else -score

    def random_move(self):
        return random.choice(list(self.board.legal_moves))

    def show_game_over(self):
        if self.board.is_checkmate():
            if self.board.turn == self.player_color:
                result = "CPU venceu! Xeque-mate."
                self.scores['cpu'] += 1
            else:
                result = "Você venceu! Xeque-mate."
                self.scores['player'] += 1
        elif self.board.is_stalemate():
            result = "Empate por afogamento."
            self.scores['draw'] += 1
        elif self.board.is_insufficient_material():
            result = "Empate por material insuficiente."
            self.scores['draw'] += 1
        elif self.board.is_seventyfive_moves() or self.board.is_fivefold_repetition():
            result = "Empate por regras."
            self.scores['draw'] += 1
        else:
            result = "Empate."
            self.scores['draw'] += 1
        QMessageBox.information(self, "Fim de jogo", result)
        self.board.reset()
        self.selected_square = None
        self.clear_highlights()
        self.draw_board()
        # Se o usuário está com as pretas, a CPU começa
        if self.player_color == chess.BLACK:
            self.cpu_move()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessGame()
    window.show()
    sys.exit(app.exec_())
