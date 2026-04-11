#!/usr/bin/env python3
"""Тетрис в терминале с настраиваемой задержкой падения фигур."""

from __future__ import annotations

import argparse
import curses
import random
import time
from dataclasses import dataclass

BOARD_W = 10
BOARD_H = 20
MIN_DELAY = 0.05

SHAPES = (
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
)


@dataclass
class Piece:
    shape: list[list[int]]
    x: int
    y: int


@dataclass
class GameState:
    board: list[list[int]]
    piece: Piece
    score: int = 0
    lines: int = 0
    over: bool = False
    paused: bool = False


def rotate(shape: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*shape[::-1])]


def new_piece() -> Piece:
    shape = [row[:] for row in random.choice(SHAPES)]
    x = BOARD_W // 2 - len(shape[0]) // 2
    return Piece(shape=shape, x=x, y=-1)


def collides(board: list[list[int]], piece: Piece, x: int | None = None, y: int | None = None, shape: list[list[int]] | None = None) -> bool:
    px = piece.x if x is None else x
    py = piece.y if y is None else y
    pshape = piece.shape if shape is None else shape

    for r, row in enumerate(pshape):
        for c, val in enumerate(row):
            if not val:
                continue
            nx, ny = px + c, py + r
            if nx < 0 or nx >= BOARD_W or ny >= BOARD_H:
                return True
            if ny >= 0 and board[ny][nx]:
                return True
    return False


def merge(board: list[list[int]], piece: Piece) -> None:
    for r, row in enumerate(piece.shape):
        for c, val in enumerate(row):
            if val and piece.y + r >= 0:
                board[piece.y + r][piece.x + c] = 1


def clear_lines(board: list[list[int]]) -> int:
    kept = [row for row in board if not all(row)]
    cleared = BOARD_H - len(kept)
    while len(kept) < BOARD_H:
        kept.insert(0, [0] * BOARD_W)
    board[:] = kept
    return cleared


def lock_piece(state: GameState) -> None:
    merge(state.board, state.piece)
    cleared = clear_lines(state.board)
    state.lines += cleared
    state.score += (100, 300, 700, 1500)[cleared - 1] if cleared else 0
    state.piece = new_piece()
    if collides(state.board, state.piece):
        state.over = True


def drop_distance(board: list[list[int]], piece: Piece) -> int:
    d = 0
    while not collides(board, piece, y=piece.y + d + 1):
        d += 1
    return d


def render(stdscr: curses.window, state: GameState, delay: float) -> None:
    stdscr.erase()
    stdscr.addstr(0, 0, f"Тетрис | Счёт: {state.score} | Линии: {state.lines} | Delay: {delay:.2f}s")
    stdscr.addstr(1, 0, "+" + "--" * BOARD_W + "+")

    temp = [row[:] for row in state.board]
    ghost_shift = drop_distance(state.board, state.piece)

    for r, row in enumerate(state.piece.shape):
        for c, val in enumerate(row):
            if not val:
                continue
            gy, gx = state.piece.y + r + ghost_shift, state.piece.x + c
            if 0 <= gy < BOARD_H and 0 <= gx < BOARD_W and not temp[gy][gx]:
                temp[gy][gx] = 2

    for r, row in enumerate(state.piece.shape):
        for c, val in enumerate(row):
            if val:
                ny, nx = state.piece.y + r, state.piece.x + c
                if 0 <= ny < BOARD_H and 0 <= nx < BOARD_W:
                    temp[ny][nx] = 1

    for i, row in enumerate(temp):
        line = "".join("██" if cell == 1 else "░░" if cell == 2 else "  " for cell in row)
        stdscr.addstr(i + 2, 0, f"|{line}|")

    stdscr.addstr(BOARD_H + 2, 0, "+" + "--" * BOARD_W + "+")
    stdscr.addstr(BOARD_H + 4, 0, "←/→:двигать ↑:поворот ↓:ускорить Space:сброс p:пауза +/-:delay q:выход")
    if state.paused:
        stdscr.addstr(BOARD_H + 6, 0, "ПАУЗА")
    stdscr.refresh()


def main_loop(stdscr: curses.window, start_delay: float) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(25)

    state = GameState(board=[[0] * BOARD_W for _ in range(BOARD_H)], piece=new_piece())
    delay = start_delay
    tick = time.time()

    while not state.over:
        key = stdscr.getch()

        if key == ord("q"):
            return
        if key == ord("p"):
            state.paused = not state.paused
        elif key in (ord("+"), ord("=")):
            delay = max(MIN_DELAY, delay - 0.05)
        elif key == ord("-"):
            delay += 0.05

        if not state.paused:
            if key == curses.KEY_LEFT and not collides(state.board, state.piece, x=state.piece.x - 1):
                state.piece.x -= 1
            elif key == curses.KEY_RIGHT and not collides(state.board, state.piece, x=state.piece.x + 1):
                state.piece.x += 1
            elif key == curses.KEY_UP:
                rotated = rotate(state.piece.shape)
                if not collides(state.board, state.piece, shape=rotated):
                    state.piece.shape = rotated
            elif key == curses.KEY_DOWN and not collides(state.board, state.piece, y=state.piece.y + 1):
                state.piece.y += 1
            elif key == ord(" "):
                state.piece.y += drop_distance(state.board, state.piece)
                lock_piece(state)

            now = time.time()
            if now - tick >= delay:
                tick = now
                if not collides(state.board, state.piece, y=state.piece.y + 1):
                    state.piece.y += 1
                else:
                    lock_piece(state)

        render(stdscr, state, delay)

    render(stdscr, state, delay)
    stdscr.addstr(BOARD_H + 6, 0, "Игра окончена. Нажмите любую клавишу...")
    stdscr.nodelay(False)
    stdscr.getch()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Тетрис в терминале с регулируемой задержкой")
    parser.add_argument("--delay", type=float, default=0.5, help="Задержка в секундах между шагами падения")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.delay <= 0:
        raise SystemExit("Ошибка: --delay должен быть > 0")
    curses.wrapper(main_loop, args.delay)


if __name__ == "__main__":
    main()
