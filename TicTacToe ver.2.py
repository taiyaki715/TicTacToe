import tkinter as tk
from tkinter import messagebox
import functools


class Game:
    # 初期化、インスタンス生成
    def __init__(self):
        self.turn = 0
        self.board = Board()
        self.computer = Computer(self.board)
        self.window = Window(self)
        self.window.root.mainloop()

    # ゲーム終了処理
    def end_game(self, result):
        if result == 'win':
            text = "あなたの勝ちです。"
        elif result == 'lose':
            text = "あなたの負けです。"
        elif result == 'draw':
            text = "引き分けです。"

        messagebox.showinfo("ゲーム終了", text)

        self.window.root.destroy()

    # メイン処理
    def main(self, position):
        if self.board.set_player(position):
            self.turn += 1
            self.window.window_refresh(self.board.data)
            if self.board.judge():
                self.end_game(self.board.judge())
            elif self.turn == 9:
                self.end_game('draw')
            self.board.set_computer(self.computer.computer_guess())
            self.window.window_refresh(self.board.data)
            self.turn += 1
            if self.board.judge():
                self.end_game(self.board.judge())
            elif self.turn == 9:
                self.end_game('draw')


class Computer:
    def __init__(self, board):
        self.board = board

    def computer_guess(self):
        # コンピュータ思考用関数Ver.2
        self.board.weight = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for y in range(3):
            for x in range(3):
                if self.board.data[y][x] != 0:
                    self.board.weight[y][x] -= 10
                else:
                    # 横方向
                    number_of_player = 0
                    number_of_computer = 0
                    for counter in range(3):
                        if self.board.data[y][counter] == 1:
                            self.board.weight[y][x] -= 1
                            number_of_player += 1
                        elif self.board.data[y][counter] == 2:
                            self.board.weight[y][x] += 1
                            number_of_computer += 1
                    if number_of_player == 2:
                        self.board.weight[y][x] += 5
                    elif number_of_player == 2:
                        self.board.weight[y][x] += 5
                    # 縦方向
                    number_of_player = 0
                    number_of_computer = 0
                    for counter in range(3):
                        if self.board.data[counter][x] == 1:
                            self.board.weight[y][x] -= 1
                            number_of_player += 1
                        elif self.board.data[counter][x] == 2:
                            self.board.weight[y][x] += 1
                            number_of_computer += 1
                    if number_of_player == 2:
                        self.board.weight[y][x] += 5
                    elif number_of_player == 2:
                        self.board.weight[y][x] += 5

                    if (y == 0 and x == 0) or (y == 2 and x == 0):
                        number_of_player = 0
                        number_of_computer = 0
                        for counter in range(3):
                            if self.board.data[counter][counter] == 1:
                                self.board.weight[y][x] -= 1
                                number_of_player += 1
                            elif self.board.data[counter][counter] == 2:
                                self.board.weight[y][x] += 1
                                number_of_computer += 1
                        if number_of_player == 2:
                            self.board.weight[y][x] += 5
                        elif number_of_player == 2:
                            self.board.weight[y][x] += 5
                    elif (y == 2 and x == 0) or (y == 0 and x == 2):
                        number_of_player = 0
                        number_of_computer = 0
                        for counter in range(3):
                            if self.board.data[counter][2 - counter] == 1:
                                self.board.weight[y][x] -= 1
                                number_of_player += 1
                            elif self.board.data[counter][2 - counter] == 2:
                                self.board.weight[y][x] += 1
                                number_of_computer += 1
                        if number_of_player == 2:
                            self.board.weight[y][x] += 5
                        elif number_of_player == 2:
                            self.board.weight[y][x] += 5

        # 最大インデックス選択
        self.max_index = sum(self.board.weight, []).index(
            max(list((sum(self.board.weight, [])))))

        # 選択インデックス二次元化
        counter = 0
        for y in range(3):
            for x in range(3):
                counter += 1
                if counter - 1 == self.max_index:
                    self.max_index_2d = (y, x)

        return self.max_index_2d


class Board:
    def __init__(self):
        self.data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.weight = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # 重複判定
    def is_duplication(self, position):
        if self.data[position[0]][position[1]] == 0:
            return False
        else:
            return True

    # プレーヤのコマを置く
    def set_player(self, position):
        if not self.is_duplication(position):
            self.data[position[0]][position[1]] = 1
            return True
        else:
            return False

    def set_computer(self, position):
        if not self.is_duplication(position):
            self.data[position[0]][position[1]] = 2
            return True
        else:
            return False

    # 3つのコマが並んでいるか判定
    def judge(self):
        # 横方向
        for i in range(3):
            if self.data[i][0] == self.data[i][1] == self.data[i][2] == 1:
                return 'win'
            elif self.data[i][0] == self.data[i][1] == self.data[i][2] == 2:
                return 'lose'

        # 縦方向
        for i in range(3):
            if self.data[0][i] == self.data[1][i] == self.data[2][i] == 1:
                return 'win'
            elif self.data[0][i] == self.data[1][i] == self.data[2][i] == 2:
                return 'lose'

        # 斜め方向
        if self.data[0][0] == self.data[1][1] == self.data[2][2] == 1:
            return 'win'
        elif self.data[2][0] == self.data[1][1] == self.data[0][2] == 1:
            return 'win'
        elif self.data[0][0] == self.data[1][1] == self.data[2][2] == 2:
            return 'lose'
        elif self.data[2][0] == self.data[1][1] == self.data[0][2] == 2:
            return 'lose'


class Window:

    WINDOW_WIDTH = '155'  # ウィンドウ幅
    WINDOW_HEIGHT = '167'  # ウィンドウ高
    BUTTON_WIDTH = 6  # ボタン幅
    BUTTON_HEIGHT = 3  # ボタン高
    USER_SYMBOL = "○"  # ユーザーアイコン
    COMPUTER_SYMBOL = "×"  # コンピュータアイコン

    def __init__(self, game):

        self.game = game

        # メインウィンドウ描画
        self.root = tk.Tk()

        # ウィンドウサイズ設定
        self.root.geometry(self.WINDOW_WIDTH + "x" + self.WINDOW_HEIGHT)
        self.root.resizable(False, False)

        # ボタン描画
        self.label_0_0 = tk.StringVar()
        self.button_0_0 = tk.Button(textvariable=self.label_0_0,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (0, 0)))
        self.button_0_0.grid(row=0, column=0)

        self.label_0_1 = tk.StringVar()
        self.button_0_1 = tk.Button(textvariable=self.label_0_1,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (0, 1)))
        self.button_0_1.grid(row=0, column=1)

        self.label_0_2 = tk.StringVar()
        self.button_0_2 = tk.Button(textvariable=self.label_0_2,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (0, 2)))
        self.button_0_2.grid(row=0, column=2)

        self.label_1_0 = tk.StringVar()
        self.button_1_0 = tk.Button(textvariable=self.label_1_0,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (1, 0)))
        self.button_1_0.grid(row=1, column=0)

        self.label_1_1 = tk.StringVar()
        self.button_1_1 = tk.Button(textvariable=self.label_1_1,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (1, 1)))
        self.button_1_1.grid(row=1, column=1)

        self.label_1_2 = tk.StringVar()
        self.button_1_2 = tk.Button(textvariable=self.label_1_2,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (1, 2)))
        self.button_1_2.grid(row=1, column=2)

        self.label_2_0 = tk.StringVar()
        self.button_2_0 = tk.Button(textvariable=self.label_2_0,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (2, 0)))
        self.button_2_0.grid(row=2, column=0)

        self.label_2_1 = tk.StringVar()
        self.button_2_1 = tk.Button(textvariable=self.label_2_1,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (2, 1)))
        self.button_2_1.grid(row=2, column=1)

        self.label_2_2 = tk.StringVar()
        self.button_2_2 = tk.Button(textvariable=self.label_2_2,
                                    width=self.BUTTON_WIDTH,
                                    height=self.BUTTON_HEIGHT,
                                    command=functools.partial(
                                        self.button_clicked, (2, 2)))
        self.button_2_2.grid(row=2, column=2)

    # ボタンイベント呼び出し
    def button_clicked(self, position):
        self.game.main(position)

    # 画面更新用関数
    def window_refresh(self, data):
        for y in range(3):
            for x in range(3):
                if data[y][x] == 0:
                    char = ''
                elif data[y][x] == 1:
                    char = '○'
                else:
                    char = '×'

                if y == 0 and x == 0:
                    self.label_0_0.set(char)
                if y == 0 and x == 1:
                    self.label_0_1.set(char)
                if y == 0 and x == 2:
                    self.label_0_2.set(char)
                if y == 1 and x == 0:
                    self.label_1_0.set(char)
                if y == 1 and x == 1:
                    self.label_1_1.set(char)
                if y == 1 and x == 2:
                    self.label_1_2.set(char)
                if y == 2 and x == 0:
                    self.label_2_0.set(char)
                if y == 2 and x == 1:
                    self.label_2_1.set(char)
                if y == 2 and x == 2:
                    self.label_2_2.set(char)


if __name__ == '__main__':
    game = Game()
