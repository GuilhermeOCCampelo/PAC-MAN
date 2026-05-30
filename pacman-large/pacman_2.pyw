#! /usr/bin/python

# pacman.pyw
# By David Reilly
# Code conversion and improvement by https://github.com/Wollala/pacman-python
# Modified with Quiz System

import os
import random
import sys

import pygame
from pygame.locals import *

# ============================================
# SISTEMA DE QUIZ
# ============================================
class QuizSystem:
    def __init__(self):
        # === PERGUNTAS DA AULA DE INGLES ===
        # Para adicionar/editar: copie um bloco { ... }.
        # "correct" deve ser a LETRA (A, B, C ou D) da opcao certa.
        self.questions = [
            {
                "question": "What is a screenplay?",
                "options": ["A) The script for a film", "B) The trailer of a movie", "C) The opening credits", "D) The cover of the DVD"],
                "correct": "A"
            },
            {
                "question": "What do we call a group of actors in a movie?",
                "options": ["A) Crew", "B) Cast", "C) Team", "D) Staff"],
                "correct": "B"
            },
            {
                "question": "What is a 'set' in filmmaking?",
                "options": ["A) The opening scene of a film", "B) The place where the scenes are filmed", "C) A pair of matching films", "D) A type of camera lens"],
                "correct": "B"
            },
            {
                "question": "What do we call the place where movie tickets are sold?",
                "options": ["A) Lobby", "B) Counter", "C) Box Office", "D) Reception"],
                "correct": "C"
            },
            {
                "question": "What do we call the music soundtrack of a film?",
                "options": ["A) Beat", "B) Score", "C) Tune", "D) Theme"],
                "correct": "B"
            },
            {
                "question": "Where are movie sets usually located?",
                "options": ["A) Cinema", "B) Theater", "C) Studio", "D) Gallery"],
                "correct": "C"
            },
            {
                "question": "International regulations must be checked _____ filmmaking.",
                "options": ["A) Before", "B) During", "C) After", "D) Never"],
                "correct": "A"
            },
            {
                "question": "Visual Effects are part of which stage of filmmaking?",
                "options": ["A) Pre-production", "B) Production", "C) Post-production", "D) Marketing"],
                "correct": "C"
            },
            {
                "question": "Which is the passive voice of: 'The director filmed the scene at night.'?",
                "options": ["A) The scene is filmed at night by the director", "B) The scene was filmed at night by the director", "C) The scene filmed at night by the director", "D) The director was filmed at night by the scene"],
                "correct": "B"
            },
            {
                "question": "Find the corrected version of: 'The movie was direct by a famous Brazilian director.'",
                "options": ["A) The movie was directing by a famous Brazilian director", "B) The movie were directed by a famous Brazilian director", "C) The movie was directed by a famous Brazilian director", "D) The movie has direct by a famous Brazilian director"],
                "correct": "C"
            }
        ]

        self.current_question = None
        self.active = False            # True = mostrando a pergunta
        self.showing_feedback = False  # True = mostrando Correct / Wrong
        self.last_answer_correct = False
        self.font_large = None
        self.font_small = None

    def initialize_fonts(self):
        try:
            self.font_large = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 26)
        except:
            self.font_large = pygame.font.SysFont('arial', 36)
            self.font_small = pygame.font.SysFont('arial', 26)

    def start_quiz(self):
        # Sorteia uma pergunta aleatoria, evitando repetir a ultima
        # (se houver mais de uma pergunta cadastrada).
        if len(self.questions) > 1:
            escolhas = [q for q in self.questions if q is not self.current_question]
        else:
            escolhas = self.questions
        self.current_question = random.choice(escolhas)
        self.active = True
        self.showing_feedback = False
        return True

    def check_answer(self, answer):
        correct = bool(self.current_question) and answer.upper() == self.current_question["correct"]
        self.last_answer_correct = correct
        self.active = False
        self.showing_feedback = True
        return correct

    def end_feedback(self):
        self.showing_feedback = False
        self.current_question = None

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current = ''
        for word in words:
            test = word if current == '' else current + ' ' + word
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def draw(self, screen, screen_size):
        if not (self.active or self.showing_feedback) or not self.current_question:
            return

        # Fundo escurecido
        overlay = pygame.Surface(screen_size)
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Caixa central: maior que antes, p/ acomodar perguntas/opcoes longas.
        box_width = min(screen_size[0] - 40, 720)
        box_height = min(screen_size[1] - 40, 450)
        box_x = (screen_size[0] - box_width) // 2
        box_y = (screen_size[1] - box_height) // 2

        pygame.draw.rect(screen, (30, 30, 80), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, (255, 255, 0), (box_x, box_y, box_width, box_height), 4)

        if self.active:
            # --- Mostra a pergunta e as opcoes ---
            title = self.font_large.render("ENGLISH QUESTION!", True, (255, 255, 0))
            title_rect = title.get_rect(center=(screen_size[0] // 2, box_y + 35))
            screen.blit(title, title_rect)

            # Pergunta (centralizada, com quebra de linha automatica)
            q_lines = self._wrap_text(self.current_question["question"],
                                      self.font_small, box_width - 60)
            y = box_y + 75
            for line in q_lines:
                line_surf = self.font_small.render(line, True, (255, 255, 255))
                line_rect = line_surf.get_rect(center=(screen_size[0] // 2, y))
                screen.blit(line_surf, line_rect)
                y += 28

            # Opcoes (alinhadas a esquerda, com quebra de linha se for longa)
            y += 12
            opt_x = box_x + 30
            opt_w = box_width - 60
            for option in self.current_question["options"]:
                opt_lines = self._wrap_text(option, self.font_small, opt_w)
                for i, ln in enumerate(opt_lines):
                    # continuacao recua para alinhar visualmente com o texto apos "X) "
                    x = opt_x if i == 0 else opt_x + 28
                    opt_surf = self.font_small.render(ln, True, (200, 200, 255))
                    screen.blit(opt_surf, (x, y))
                    y += 26
                y += 4   # pequeno respiro entre opcoes

            instruction = self.font_small.render(
                "Press A, B, C or D to answer", True, (255, 255, 0))
            inst_rect = instruction.get_rect(
                center=(screen_size[0] // 2, box_y + box_height - 28))
            screen.blit(instruction, inst_rect)
        else:
            # --- Mostra o feedback (Correct / Wrong) ---
            if self.last_answer_correct:
                msg = "CORRECT!"
                color = (0, 255, 0)
                sub = "You got the power-up!"
            else:
                msg = "WRONG!"
                color = (255, 60, 60)
                # mostra qual era a resposta certa (bom para aprender)
                correct_letter = self.current_question["correct"]
                correct_option = ""
                for option in self.current_question["options"]:
                    if option.strip().upper().startswith(correct_letter):
                        correct_option = option
                        break
                sub = "Correct answer: " + correct_option

            msg_surf = self.font_large.render(msg, True, color)
            msg_rect = msg_surf.get_rect(center=(screen_size[0] // 2, box_y + box_height // 2 - 20))
            screen.blit(msg_surf, msg_rect)

            sub_surf = self.font_small.render(sub, True, (255, 255, 255))
            sub_rect = sub_surf.get_rect(center=(screen_size[0] // 2, box_y + box_height // 2 + 25))
            screen.blit(sub_surf, sub_rect)

if os.name == "nt":
    SCRIPT_PATH = os.getcwd()
else:
    SCRIPT_PATH = sys.path[0]    

SCREEN_TILE_SIZE_HEIGHT = 23
SCREEN_TILE_SIZE_WIDTH = 30

TILE_WIDTH = TILE_HEIGHT = 24

HS_FONT_SIZE = 16
HS_LINE_HEIGHT = 16
HS_WIDTH = 408
HS_HEIGHT = 120
HS_XOFFSET = 180
HS_YOFFSET = 400
HS_ALPHA = 200

SCORE_XOFFSET = 50
SCORE_YOFFSET = 34
SCORE_COLWIDTH = 13

IMG_EDGE_LIGHT_COLOR = (255, 206, 255, 255)
IMG_FILL_COLOR = (132, 0, 132, 255)
IMG_EDGE_SHADOW_COLOR = (255, 0, 255, 255)
IMG_PELLET_COLOR = (128, 0, 128, 255)

# --- Dificuldade dos fantasmas -------------------------------------------
# Velocidade dos fantasmas em pixels/frame. Cada vez que voce limpa o mapa,
# eles sobem um degrau desta lista (e depois ficam no ultimo valor).
# IMPORTANTE: so use numeros que dividem 24 (1,2,3,4,6,8,12) senao os
# fantasmas saem do alinhamento do labirinto. O Pac-Man anda a 3.
GHOST_SPEED_LEVELS = [2, 3, 4]
# Velocidade dos "olhos" do fantasma comido voltando pra caixa (bem rapido).
GHOST_EYES_SPEED = 6

NO_GIF_TILES = [23]
NO_WX = 0
USER_NAME = "User"

# === Ranking de jogadores (nome + pontuacao), salvo em res/ranking.txt ===
RANKING_FILE = os.path.join(SCRIPT_PATH, "res", "ranking.txt")
current_player_name = ""    # nome do jogador atual
name_input_buffer = ""      # o que esta sendo digitado na tela de nome

def get_ranking():
    entries = []
    try:
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ", 1)
                if len(parts) == 2 and parts[0].isdigit():
                    entries.append((int(parts[0]), parts[1]))
    except IOError:
        pass
    entries.sort(key=lambda e: e[0], reverse=True)
    return entries

def add_score_to_ranking(name, score):
    if not name:
        name = "Player"
    entries = get_ranking()
    entries.append((int(score), name))
    entries.sort(key=lambda e: e[0], reverse=True)
    entries = entries[:10]   # guarda os 10 melhores
    try:
        with open(RANKING_FILE, "w", encoding="utf-8") as f:
            for sc, nm in entries:
                f.write("%d %s\n" % (sc, nm))
    except IOError:
        pass
    return entries

JS_DEVNUM = 0
JS_XAXIS = 0
JS_YAXIS = 1
JS_STARTBUTTON = 0

def get_image_surface(file_path):
    image = pygame.image.load(file_path).convert()
    return image

pygame.mixer.pre_init(22050, -16, 1, 1024)
pygame.mixer.init()
pygame.mixer.set_num_channels(7)
channel_backgound = pygame.mixer.Channel(6)

clock = pygame.time.Clock()
pygame.init()

window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Pacman Quiz")

screen = pygame.display.get_surface()
pygame.mouse.set_visible(False)

img_Background = get_image_surface(os.path.join(SCRIPT_PATH, "res", "backgrounds", "1.gif"))

snd_pellet = {
    0: pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "pellet1.wav")),
    1: pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "pellet2.wav"))}
snd_levelintro = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "levelintro.wav"))
snd_default = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "default.wav"))
snd_extrapac = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "extrapac.wav"))
snd_gh2gohome = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "gh2gohome.wav"))
snd_death = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "death.wav"))
snd_powerpellet = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "powerpellet.wav"))
snd_eatgh = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "eatgh2.wav"))
snd_fruitbounce = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "fruitbounce.wav"))
snd_eatfruit = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "eatfruit.wav"))
snd_extralife = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "extralife.wav"))

ghostcolor = {
    0: (255, 0, 0, 255),
    1: (255, 128, 255, 255),
    2: (128, 255, 255, 255),
    3: (255, 128, 0, 255),
    4: (50, 50, 255, 255),
    5: (255, 255, 255, 255)}

rect_list = []

class game:
    def __init__(self):
        self.levelNum = 0
        self.score = 0
        self.lives = 3

        self.mode = 0
        self.modeTimer = 0
        self.ghostTimer = 0
        self.ghostValue = 0
        self.ghostSpeed = GHOST_SPEED_LEVELS[0]  # sobe a cada mapa limpo
        self.fruitTimer = 0
        self.fruitScoreTimer = 0
        self.fruitScorePos = (0, 0)

        self.SetMode(3)

        self.screenTileSize = (SCREEN_TILE_SIZE_HEIGHT, SCREEN_TILE_SIZE_WIDTH)
        self.screenSize = (self.screenTileSize[1] * TILE_WIDTH, self.screenTileSize[0] * TILE_HEIGHT)

        self.screenPixelPos = (0, 0)
        self.screenNearestTilePos = (0, 0)
        self.screenPixelOffset = (0, 0)

        self.digit = {}
        for i in range(0, 10, 1):
            self.digit[i] = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", str(i) + ".gif"))
        self.imLife = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "life.gif"))
        self.imGameOver = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "gameover.gif"))
        self.imReady = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "ready.gif"))
        self.imLogo = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "logo.gif"))
        self.imHiscores = self.makehiscorelist()

    @staticmethod
    def defaulthiscorelist():
        return [(100000, "David"), (80000, "Andy"), (60000, "Count Pacula"), (40000, "Cleopacra"),
                (20000, "Brett Favre"), (10000, "Sergei Pachmaninoff")]

    @staticmethod
    def writehiscores(hs):
        fname = os.path.join(SCRIPT_PATH, "res", "hiscore.txt")
        f = open(fname, "w")
        for line in hs:
            f.write(str(line[0]) + " " + line[1] + "\n")
        f.close()

    @staticmethod
    def getplayername():
        if NO_WX:
            return USER_NAME
        try:
            import wx
        except:
            print("Erro ao importar wx")
            return USER_NAME
        app = wx.App(None)
        dlog = wx.TextEntryDialog(None, "Você entrou no ranking! Nome:")
        dlog.ShowModal()
        name = dlog.GetValue()
        dlog.Destroy()
        app.Destroy()
        return name

    @staticmethod
    def PlayBackgoundSound(snd):
        channel_backgound.stop()
        channel_backgound.play(snd, loops=-1)

    def gethiscores(self):
        try:
            f = open(os.path.join(SCRIPT_PATH, "res", "hiscore.txt"))
            hs = []
            for line in f:
                while len(line) > 0 and (line[0] == "\n" or line[0] == "\r"):
                    line = line[1:]
                while len(line) > 0 and (line[-1] == "\n" or line[-1] == "\r"):
                    line = line[:-1]
                score = int(line.split(" ")[0])
                name = line.partition(" ")[2]
                if score > 99999999: score = 99999999
                if len(name) > 22: name = name[:22]
                hs.append((score, name))
            f.close()
            if len(hs) > 6: hs = hs[:6]
            while len(hs) < 6: hs.append((0, ""))
            return hs
        except IOError:
            return self.defaulthiscorelist()

    def updatehiscores(self, newscore):
        hs = self.gethiscores()
        for line in hs:
            if newscore >= line[0]:
                hs.insert(hs.index(line), (newscore, self.getplayername()))
                hs.pop(-1)
                break
        self.writehiscores(hs)

    def makehiscorelist(self):
        global rect_list
        f = pygame.font.Font(os.path.join(SCRIPT_PATH, "res", "zig_____.ttf"), HS_FONT_SIZE)
        scoresurf = pygame.Surface((HS_WIDTH, HS_HEIGHT), pygame.SRCALPHA)
        scoresurf.set_alpha(HS_ALPHA)
        linesurf = f.render("HIGH SCORES".center(28), 1, (255, 255, 0))
        scoresurf.blit(linesurf, (0, 0))
        hs = self.gethiscores()
        vpos = 0
        for line in hs:
            vpos += HS_LINE_HEIGHT
            linesurf = f.render(line[1].ljust(18) + str(line[0]).rjust(10), 1, (255, 255, 255))
            scoresurf.blit(linesurf, (0, vpos))
        return scoresurf

    def drawmidgamehiscores(self):
        self.imHiscores = self.makehiscorelist()

    def StartNewGame(self):
        self.levelNum = 1
        self.score = 0
        self.lives = 3
        self.ghostSpeed = GHOST_SPEED_LEVELS[0]  # reseta a dificuldade

        self.SetMode(0)
        thisLevel.LoadLevel(thisGame.GetLevelNum())

    def AddToScore(self, amount):
        extraLifeSet = [25000, 50000, 100000, 150000]

        for specialScore in extraLifeSet:
            if self.score < specialScore <= self.score + amount:
                snd_extralife.play()
                thisGame.lives += 1

        self.score += amount

    def DrawScore(self):
        global rect_list
        self.DrawNumber(self.score, (SCORE_XOFFSET, self.screenSize[1] - SCORE_YOFFSET))

        for i in range(0, self.lives, 1):
            screen.blit(self.imLife, (34 + i * 10 + 16, self.screenSize[1] - 18))

        screen.blit(thisFruit.imFruit[thisFruit.fruitType], (4 + 16, self.screenSize[1] - 28))

        if self.mode == 3:
            screen.blit(self.imGameOver, (self.screenSize[0] / 2 - (self.imGameOver.get_width() / 2),
                                          self.screenSize[1] / 2 - (self.imGameOver.get_height() / 2)))
        elif self.mode == 0 or self.mode == 4:
            screen.blit(self.imReady, (self.screenSize[0] / 2 - 20, self.screenSize[1] / 2 + 12))

        self.DrawNumber(self.levelNum, (0, self.screenSize[1] - 20))

    def DrawNumber(self, number, x_y):
        global rect_list
        (x, y) = x_y

        strNumber = str(number)

        for i in range(0, len(str(number)), 1):
            if strNumber[i] == '.':
                break
            iDigit = int(strNumber[i])
            screen.blit(self.digit[iDigit], (x + i * SCORE_COLWIDTH, y))

    def SmartMoveScreen(self):
        possibleScreenX = player.x - self.screenTileSize[1] / 2 * TILE_WIDTH
        possibleScreenY = player.y - self.screenTileSize[0] / 2 * TILE_HEIGHT

        if self.screenSize[0] >= thisLevel.lvlWidth * TILE_WIDTH:
            possibleScreenX = -(self.screenSize[0] - thisLevel.lvlWidth * TILE_WIDTH) / 2
        elif possibleScreenX < 0:
            possibleScreenX = 0
        elif possibleScreenX > thisLevel.lvlWidth * TILE_WIDTH - self.screenSize[0]:
            possibleScreenX = thisLevel.lvlWidth * TILE_WIDTH - self.screenSize[0]

        if self.screenSize[1] >= thisLevel.lvlHeight * TILE_HEIGHT:
            possibleScreenY = -(self.screenSize[1] - thisLevel.lvlHeight * TILE_HEIGHT) / 2
        elif possibleScreenY < 0:
            possibleScreenY = 0
        elif possibleScreenY > thisLevel.lvlHeight * TILE_HEIGHT - self.screenSize[1]:
            possibleScreenY = thisLevel.lvlHeight * TILE_HEIGHT - self.screenSize[1]

        thisGame.MoveScreen((possibleScreenX, possibleScreenY))

    def MoveScreen(self, newX_newY):
        (newX, newY) = newX_newY
        self.screenPixelPos = (newX, newY)
        self.screenNearestTilePos = (
            int(newY / TILE_HEIGHT), int(newX / TILE_WIDTH))
        self.screenPixelOffset = (
            newX - self.screenNearestTilePos[1] * TILE_WIDTH, newY - self.screenNearestTilePos[0] * TILE_HEIGHT)

    def GetScreenPos(self):
        return self.screenPixelPos

    def GetLevelNum(self):
        return self.levelNum

    def SetNextLevel(self):
        self.levelNum += 1

        self.SetMode(0)
        thisLevel.LoadLevel(thisGame.GetLevelNum())

        player.velX = 0
        player.velY = 0
        player.anim_pacmanCurrent = player.anim_pacmanS

    def RestartSameLevel(self):
        # Limpou o mapa: recomeca o MESMO mapa, com fantasmas um pouco mais
        # rapidos (sobe um degrau na lista GHOST_SPEED_LEVELS, ate o maximo).
        if self.ghostSpeed in GHOST_SPEED_LEVELS:
            i = GHOST_SPEED_LEVELS.index(self.ghostSpeed)
            if i < len(GHOST_SPEED_LEVELS) - 1:
                self.ghostSpeed = GHOST_SPEED_LEVELS[i + 1]
        else:
            self.ghostSpeed = GHOST_SPEED_LEVELS[-1]

        self.SetMode(0)
        thisLevel.LoadLevel(thisGame.GetLevelNum())  # mesmo numero de nivel

        player.velX = 0
        player.velY = 0
        player.reqDirX = 0
        player.reqDirY = 0
        player.anim_pacmanCurrent = player.anim_pacmanS

    def SetMode(self, newMode):
        self.mode = newMode
        self.modeTimer = 0

        if newMode == 0:
            self.PlayBackgoundSound(snd_levelintro)
        elif newMode == 1:
            self.PlayBackgoundSound(snd_default)
        elif newMode == 2:
            self.PlayBackgoundSound(snd_death)
        elif newMode == 8:
            self.PlayBackgoundSound(snd_gh2gohome)
        elif newMode == 9:
            self.PlayBackgoundSound(snd_extrapac)
        else:
            channel_backgound.stop()


class node:
    def __init__(self):
        self.g = -1
        self.h = -1
        self.f = -1
        self.parent = (-1, -1)
        self.type = -1


class path_finder:
    def __init__(self):
        self.map = {}
        self.size = (-1, -1)

        self.pathChainRev = ""
        self.pathChain = ""

        self.start = (-1, -1)
        self.end = (-1, -1)

        self.current = (-1, -1)

        self.openList = []
        self.closedList = []

        self.neighborSet = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def ResizeMap(self, numRows_numCols):
        (numRows, numCols) = numRows_numCols
        self.map = {}
        self.size = (numRows, numCols)

        for row in range(0, self.size[0], 1):
            for col in range(0, self.size[1], 1):
                self.Set((row, col), node())
                self.SetType((row, col), 0)

    def CleanUpTemp(self):
        self.pathChainRev = ""
        self.pathChain = ""
        self.current = (-1, -1)
        self.openList = []
        self.closedList = []

    def FindPath(self, startPos, endPos):
        self.CleanUpTemp()
        self.start = startPos
        self.end = endPos

        self.AddToOpenList(self.start)
        self.SetG(self.start, 0)
        self.SetH(self.start, 0)
        self.SetF(self.start, 0)

        thisLowestFNode = None
        doContinue = True
        while doContinue:

            thisLowestFNode = self.GetLowestFNode()

            if thisLowestFNode != self.end and thisLowestFNode != False:
                self.current = thisLowestFNode
                self.RemoveFromOpenList(self.current)
                self.AddToClosedList(self.current)

                for offset in self.neighborSet:
                    thisNeighbor = (self.current[0] + offset[0], self.current[1] + offset[1])

                    if not thisNeighbor[0] < 0 and not thisNeighbor[1] < 0 and not thisNeighbor[0] > self.size[
                        0] - 1 and not thisNeighbor[1] > self.size[1] - 1 and not self.GetType(thisNeighbor) == 1:
                        cost = self.GetG(self.current) + 10

                        if self.IsInOpenList(thisNeighbor) and cost < self.GetG(thisNeighbor):
                            self.RemoveFromOpenList(thisNeighbor)

                        if not self.IsInOpenList(thisNeighbor) and not self.IsInClosedList(thisNeighbor):
                            self.AddToOpenList(thisNeighbor)
                            self.SetG(thisNeighbor, cost)
                            self.CalcH(thisNeighbor)
                            self.CalcF(thisNeighbor)
                            self.SetParent(thisNeighbor, self.current)
            else:
                doContinue = False

        if not thisLowestFNode:
            return False

        self.current = self.end
        while not self.current == self.start:
            if self.current[1] > self.GetParent(self.current)[1]:
                self.pathChainRev += 'R'
            elif self.current[1] < self.GetParent(self.current)[1]:
                self.pathChainRev += 'L'
            elif self.current[0] > self.GetParent(self.current)[0]:
                self.pathChainRev += 'D'
            elif self.current[0] < self.GetParent(self.current)[0]:
                self.pathChainRev += 'U'
            self.current = self.GetParent(self.current)
            self.SetType(self.current, 4)

        for i in range(len(self.pathChainRev) - 1, -1, -1):
            self.pathChain += self.pathChainRev[i]

        self.SetType(self.start, 2)
        self.SetType(self.end, 3)

        return self.pathChain

    def Unfold(self, row_col):
        (row, col) = row_col
        return (row * self.size[1]) + col

    def Set(self, row_col, newNode):
        (row, col) = row_col
        self.map[self.Unfold((row, col))] = newNode

    def GetType(self, row_col):
        (row, col) = row_col
        return self.map[self.Unfold((row, col))].type

    def SetType(self, row_col, newValue):
        (row, col) = row_col
        self.map[self.Unfold((row, col))].type = newValue

    def GetF(self, row_col):
        (row, col) = row_col
        return self.map[self.Unfold((row, col))].f

    def GetG(self, row_col):
        (row, col) = row_col
        return self.map[self.Unfold((row, col))].g

    def GetH(self, row_col):
        (row, col) = row_col
        return self.map[self.Unfold((row, col))].h

    def SetG(self, row_col, newValue):
        (row, col) = row_col
        self.map[self.Unfold((row, col))].g = newValue

    def SetH(self, row_col, newValue):
        (row, col) = row_col
        self.map[self.Unfold((row, col))].h = newValue

    def SetF(self, row_col, newValue):
        (row, col) = row_col
        self.map[self.Unfold((row, col))].f = newValue

    def CalcH(self, row_col):
        (row, col) = row_col
        self.map[self.Unfold((row, col))].h = abs(row - self.end[0]) + abs(col - self.end[0])

    def CalcF(self, row_col):
        (row, col) = row_col
        unfoldIndex = self.Unfold((row, col))
        self.map[unfoldIndex].f = self.map[unfoldIndex].g + self.map[unfoldIndex].h

    def AddToOpenList(self, row_col):
        (row, col) = row_col
        self.openList.append((row, col))

    def RemoveFromOpenList(self, row_col):
        (row, col) = row_col
        self.openList.remove((row, col))

    def IsInOpenList(self, row_col):
        (row, col) = row_col
        if self.openList.count((row, col)) > 0:
            return True
        else:
            return False

    def GetLowestFNode(self):
        lowestValue = 1000
        lowestPair = (-1, -1)

        for iOrderedPair in self.openList:
            if self.GetF(iOrderedPair) < lowestValue:
                lowestValue = self.GetF(iOrderedPair)
                lowestPair = iOrderedPair

        if not lowestPair == (-1, -1):
            return lowestPair
        else:
            return False

    def AddToClosedList(self, row_col):
        (row, col) = row_col
        self.closedList.append((row, col))

    def IsInClosedList(self, row_col):
        (row, col) = row_col
        if self.closedList.count((row, col)) > 0:
            return True
        else:
            return False

    def SetParent(self, row_col, parentRow_parentCol):
        (row, col) = row_col
        (parentRow, parentCol) = parentRow_parentCol
        self.map[self.Unfold((row, col))].parent = (parentRow, parentCol)

    def GetParent(self, row_col):
        (row, col) = row_col
        return self.map[self.Unfold((row, col))].parent


class ghost:
    def __init__(self, ghostID):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 2

        self.nearestRow = 0
        self.nearestCol = 0

        self.id = ghostID

        self.state = 1

        self.homeX = 0
        self.homeY = 0

        self.currentPath = ""

        self.anim = {}
        for i in range(1, 7, 1):
            self.anim[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "ghost " + str(i) + ".gif"))

            for y in range(0, TILE_HEIGHT, 1):
                for x in range(0, TILE_WIDTH, 1):

                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        self.anim[i].set_at((x, y), ghostcolor[self.id])

        self.animFrame = 1
        self.animDelay = 0

    def Draw(self):
        global rect_list
        pupilSet = None

        if thisGame.mode == 3:
            return False

        for y in range(6, 12, 1):
            for x in [5, 6, 8, 9]:
                self.anim[self.animFrame].set_at((x, y), (248, 248, 248, 255))
                self.anim[self.animFrame].set_at((x + 9, y), (248, 248, 248, 255))

                if player.x > self.x and player.y > self.y:
                    pupilSet = (8, 9)
                elif player.x < self.x and player.y > self.y:
                    pupilSet = (5, 9)
                elif player.x > self.x and player.y < self.y:
                    pupilSet = (8, 6)
                elif player.x < self.x and player.y < self.y:
                    pupilSet = (5, 6)
                else:
                    pupilSet = (5, 9)

        for y in range(pupilSet[1], pupilSet[1] + 3, 1):
            for x in range(pupilSet[0], pupilSet[0] + 2, 1):
                self.anim[self.animFrame].set_at((x, y), (0, 0, 255, 255))
                self.anim[self.animFrame].set_at((x + 9, y), (0, 0, 255, 255))

        if self.state == 1:
            screen.blit(self.anim[self.animFrame],
                        (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))
        elif self.state == 2:
            if thisGame.ghostTimer > 100:
                screen.blit(ghosts[4].anim[self.animFrame],
                            (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))
            else:
                tempTimerI = int(thisGame.ghostTimer / 10)
                if tempTimerI == 1 or tempTimerI == 3 or tempTimerI == 5 or tempTimerI == 7 or tempTimerI == 9:
                    screen.blit(ghosts[5].anim[self.animFrame],
                                (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))
                else:
                    screen.blit(ghosts[4].anim[self.animFrame],
                                (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))

        elif self.state == 3:
            screen.blit(tileIDImage[tileID['glasses']],
                        (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))

        if thisGame.mode == 6 or thisGame.mode == 7:
            return False

        self.animDelay += 1

        if self.animDelay == 2:
            self.animFrame += 1

            if self.animFrame == 7:
                self.animFrame = 1

            self.animDelay = 0

    def Move(self):
        self.x += self.velX
        self.y += self.velY

        self.nearestRow = int(((self.y + (TILE_HEIGHT / 2)) / TILE_HEIGHT))
        self.nearestCol = int(((self.x + (TILE_HEIGHT / 2)) / TILE_WIDTH))

        if (self.x % TILE_WIDTH) == 0 and (self.y % TILE_HEIGHT) == 0:
            if self.currentPath is not False and (len(self.currentPath) > 0):
                self.currentPath = self.currentPath[1:]
                self.FollowNextPathWay()

            else:
                self.x = self.nearestCol * TILE_WIDTH
                self.y = self.nearestRow * TILE_HEIGHT

                self.currentPath = path.FindPath((self.nearestRow, self.nearestCol),
                                                   (player.nearestRow, player.nearestCol))
                self.FollowNextPathWay()

    def FollowNextPathWay(self):
        # Reescrito para NUNCA recorrer infinitamente. O bug antigo: quando o
        # fantasma chegava em cima do Pac-Man, FindPath devolvia uma rota vazia
        # e a funcao se chamava pra sempre (RecursionError -> jogo fechava).
        # Agora, se nao houver rota, o fantasma simplesmente para neste frame.
        if self.currentPath is False:
            self.velX = 0
            self.velY = 0
            return

        if len(self.currentPath) > 0:
            if self.currentPath[0] == "L":
                (self.velX, self.velY) = (-self.speed, 0)
            elif self.currentPath[0] == "R":
                (self.velX, self.velY) = (self.speed, 0)
            elif self.currentPath[0] == "U":
                (self.velX, self.velY) = (0, -self.speed)
            elif self.currentPath[0] == "D":
                (self.velX, self.velY) = (0, self.speed)
            return

        # ---- currentPath esta vazio: precisamos de uma rota nova ----
        if self.state == 3:
            # "olhos" chegaram em casa: volta a ser fantasma normal
            self.state = 1
            self.speed = thisGame.ghostSpeed

            (randRow, randCol) = (0, 0)
            tries = 0
            while (not thisLevel.GetMapTile((randRow, randCol)) == tileID['pellet']
                   or (randRow, randCol) == (0, 0)):
                randRow = random.randint(1, thisLevel.lvlHeight - 2)
                randCol = random.randint(1, thisLevel.lvlWidth - 2)
                tries += 1
                if tries > 200:   # mapa sem pellets (ja limpo): desiste sem travar
                    break
            self.currentPath = path.FindPath((self.nearestRow, self.nearestCol), (randRow, randCol))
        else:
            # fantasma normal: persegue o Pac-Man
            self.currentPath = path.FindPath((self.nearestRow, self.nearestCol),
                                             (player.nearestRow, player.nearestCol))

        # So segue se realmente conseguiu uma rota nova; senao, para por agora.
        if self.currentPath is not False and len(self.currentPath) > 0:
            self.FollowNextPathWay()
        else:
            self.velX = 0
            self.velY = 0


class fruit:
    def __init__(self):
        self.slowTimer = 0
        self.x = -TILE_WIDTH
        self.y = -TILE_HEIGHT
        self.velX = 0
        self.velY = 0
        self.speed = 2
        self.active = False

        self.bouncei = 0
        self.bounceY = 0

        self.nearestRow = (-1, -1)
        self.nearestCol = (-1, -1)

        self.imFruit = {}
        for i in range(0, 5, 1):
            self.imFruit[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "fruit " + str(i) + ".gif"))

        self.currentPath = ""
        self.fruitType = 1

    def Draw(self):
        global rect_list
        if thisGame.mode == 3 or self.active == False:
            return False

        screen.blit(self.imFruit[self.fruitType],
                    (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1] - self.bounceY))

    def Move(self):
        if not self.active:
            return False

        self.bouncei += 1
        if self.bouncei == 1:
            self.bounceY = 2
        elif self.bouncei == 2:
            self.bounceY = 4
        elif self.bouncei == 3:
            self.bounceY = 5
        elif self.bouncei == 4:
            self.bounceY = 5
        elif self.bouncei == 5:
            self.bounceY = 6
        elif self.bouncei == 6:
            self.bounceY = 6
        elif self.bouncei == 9:
            self.bounceY = 6
        elif self.bouncei == 10:
            self.bounceY = 5
        elif self.bouncei == 11:
            self.bounceY = 5
        elif self.bouncei == 12:
            self.bounceY = 4
        elif self.bouncei == 13:
            self.bounceY = 3
        elif self.bouncei == 14:
            self.bounceY = 2
        elif self.bouncei == 15:
            self.bounceY = 1
        elif self.bouncei == 16:
            self.bounceY = 0
            self.bouncei = 0
            snd_fruitbounce.play()

        self.slowTimer += 1
        if self.slowTimer == 2:
            self.slowTimer = 0

            self.x += self.velX
            self.y += self.velY

            self.nearestRow = int(((self.y + (TILE_WIDTH / 2)) / TILE_WIDTH))
            self.nearestCol = int(((self.x + (TILE_HEIGHT / 2)) / TILE_HEIGHT))

            if (self.x % TILE_WIDTH) == 0 and (self.y % TILE_HEIGHT) == 0:
                if len(self.currentPath) > 0:
                    self.currentPath = self.currentPath[1:]
                    self.FollowNextPathWay()

                else:
                    self.x = self.nearestCol * TILE_WIDTH
                    self.y = self.nearestRow * TILE_HEIGHT

                    self.active = False
                    thisGame.fruitTimer = 0

    def FollowNextPathWay(self):
        if not self.currentPath == False:

            if len(self.currentPath) > 0:
                if self.currentPath[0] == "L":
                    (self.velX, self.velY) = (-self.speed, 0)
                elif self.currentPath[0] == "R":
                    (self.velX, self.velY) = (self.speed, 0)
                elif self.currentPath[0] == "U":
                    (self.velX, self.velY) = (0, -self.speed)
                elif self.currentPath[0] == "D":
                    (self.velX, self.velY) = (0, self.speed)


class pacman:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 3

        # Direcao que o jogador PEDIU (buffer). Fica em espera ate dar pra virar.
        # Valores: -1, 0 ou 1 em cada eixo.
        self.reqDirX = 0
        self.reqDirY = 0

        self.nearestRow = 0
        self.nearestCol = 0

        self.homeX = 0
        self.homeY = 0

        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        self.anim_pacmanCurrent = {}

        self.animFrame = 1

        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-l " + str(i) + ".gif"))
            self.anim_pacmanR[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-r " + str(i) + ".gif"))
            self.anim_pacmanU[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-u " + str(i) + ".gif"))
            self.anim_pacmanD[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-d " + str(i) + ".gif"))
            self.anim_pacmanS[i] = get_image_surface(os.path.join(SCRIPT_PATH, "res", "sprite", "pacman.gif"))

        self.pelletSndNum = 0

    def Move(self):
        self.nearestRow = int(((self.y + (TILE_WIDTH / 2)) / TILE_WIDTH))
        self.nearestCol = int(((self.x + (TILE_HEIGHT / 2)) / TILE_HEIGHT))

        # ---- Buffer de direcao ----------------------------------------
        # O jogador so pode VIRAR (mudar de eixo) quando esta alinhado ao
        # centro de um tile; inverter o sentido (180) pode a qualquer momento.
        # Enquanto a virada pedida nao for possivel, ela fica em espera.
        aligned = (self.x % TILE_WIDTH == 0) and (self.y % TILE_HEIGHT == 0)

        if self.reqDirX != 0 or self.reqDirY != 0:
            reqVelX = self.reqDirX * self.speed
            reqVelY = self.reqDirY * self.speed
            isReversal = (reqVelX == -self.velX and reqVelY == -self.velY
                          and (self.velX != 0 or self.velY != 0))
            if isReversal or aligned:
                if not thisLevel.CheckIfHitWall((self.x + reqVelX, self.y + reqVelY),
                                                (self.nearestRow, self.nearestCol)):
                    self.velX = reqVelX
                    self.velY = reqVelY

        # ---- Movimento na direcao atual -------------------------------
        moving = (self.velX != 0 or self.velY != 0)
        if moving and not thisLevel.CheckIfHitWall((self.x + self.velX, self.y + self.velY),
                                                   (self.nearestRow, self.nearestCol)):
            self.x += self.velX
            self.y += self.velY
            thisLevel.CheckIfHitSomething((self.x, self.y), (self.nearestRow, self.nearestCol))
        else:
            # Bateu na parede: para, MAS mantem a direcao pedida em espera.
            self.velX = 0
            self.velY = 0

        # ---- Colisoes verificadas TODO frame (mesmo parado) -----------
        # Assim um fantasma nao atravessa o Pac-Man parado sem encosta-lo.
        for i in range(0, 4, 1):
            if thisLevel.CheckIfHit((self.x, self.y), (ghosts[i].x, ghosts[i].y), TILE_WIDTH / 2):
                if ghosts[i].state == 1:
                    thisGame.SetMode(2)

                elif ghosts[i].state == 2:
                    thisGame.AddToScore(thisGame.ghostValue)
                    thisGame.ghostValue = thisGame.ghostValue * 2
                    snd_eatgh.play()

                    ghosts[i].state = 3
                    ghosts[i].speed = GHOST_EYES_SPEED
                    ghosts[i].x = ghosts[i].nearestCol * TILE_WIDTH
                    ghosts[i].y = ghosts[i].nearestRow * TILE_HEIGHT
                    ghosts[i].currentPath = path.FindPath((ghosts[i].nearestRow, ghosts[i].nearestCol), (
                        thisLevel.GetGhostBoxPos()[0] + 1, thisLevel.GetGhostBoxPos()[1]))
                    ghosts[i].FollowNextPathWay()

                    thisGame.SetMode(5)

        if thisFruit.active:
            if thisLevel.CheckIfHit((self.x, self.y), (thisFruit.x, thisFruit.y), TILE_WIDTH / 2):
                thisGame.AddToScore(2500)
                thisFruit.active = False
                thisGame.fruitTimer = 0
                thisGame.fruitScoreTimer = 80
                snd_eatfruit.play()

        if thisGame.ghostTimer > 0:
            thisGame.ghostTimer -= 1

            if thisGame.ghostTimer == 0:
                thisGame.PlayBackgoundSound(snd_default)
                for i in range(0, 4, 1):
                    if ghosts[i].state == 2:
                        ghosts[i].state = 1
                thisGame.ghostValue = 0

        thisGame.fruitTimer += 1
        if thisGame.fruitTimer == 380:
            pathwayPair = thisLevel.GetPathwayPairPos()

            if not pathwayPair == False:
                pathwayEntrance = pathwayPair[0]
                pathwayExit = pathwayPair[1]

                thisFruit.active = True

                thisFruit.nearestRow = pathwayEntrance[0]
                thisFruit.nearestCol = pathwayEntrance[1]

                thisFruit.x = thisFruit.nearestCol * TILE_WIDTH
                thisFruit.y = thisFruit.nearestRow * TILE_HEIGHT

                thisFruit.currentPath = path.FindPath((thisFruit.nearestRow, thisFruit.nearestCol), pathwayExit)
                thisFruit.FollowNextPathWay()

        if thisGame.fruitScoreTimer > 0:
            thisGame.fruitScoreTimer -= 1

    def Draw(self):
        global rect_list
        if thisGame.mode == 3:
            return False

        if self.velX > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velX < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.velY > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.velY < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU

        screen.blit(self.anim_pacmanCurrent[self.animFrame],
                    (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))

        if thisGame.mode == 1 or thisGame.mode == 8 or thisGame.mode == 9:
            if self.velX != 0 or self.velY != 0:
                self.animFrame += 1

            if self.animFrame == 9:
                self.animFrame = 1


class level:
    def __init__(self):
        self.lvlWidth = 0
        self.lvlHeight = 0
        self.edgeLightColor = (255, 255, 0, 255)
        self.edgeShadowColor = (255, 150, 0, 255)
        self.fillColor = (0, 255, 255, 255)
        self.pelletColor = (255, 255, 255, 255)

        self.map = {}

        self.pellets = 0
        self.powerPelletBlinkTimer = 0

    def SetMapTile(self, row_col, newValue):
        (row, col) = row_col
        self.map[(row * self.lvlWidth) + col] = newValue

    def GetMapTile(self, row_col):
        (row, col) = row_col
        if 0 <= row < self.lvlHeight and 0 <= col < self.lvlWidth:
            return self.map[(row * self.lvlWidth) + col]
        else:
            return 0

    @staticmethod
    def IsWall(row_col):
        (row, col) = row_col
        if row > thisLevel.lvlHeight - 1 or row < 0:
            return True

        if col > thisLevel.lvlWidth - 1 or col < 0:
            return True

        result = thisLevel.GetMapTile((row, col))

        if 100 <= result <= 199:
            return True
        else:
            return False

    def CheckIfHitWall(self, possiblePlayerX_possiblePlayerY, row_col):
        (possiblePlayerX, possiblePlayerY) = possiblePlayerX_possiblePlayerY
        (row, col) = row_col
        numCollisions = 0

        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (possiblePlayerX - (iCol * TILE_WIDTH) < TILE_WIDTH) and (
                        possiblePlayerX - (iCol * TILE_WIDTH) > -TILE_WIDTH) and (
                        possiblePlayerY - (iRow * TILE_HEIGHT) < TILE_HEIGHT) and (
                        possiblePlayerY - (iRow * TILE_HEIGHT) > -TILE_HEIGHT):

                    if self.IsWall((iRow, iCol)):
                        numCollisions += 1

        if numCollisions > 0:
            return True
        else:
            return False

    @staticmethod
    def CheckIfHit(playerX_playerY, x_y, cushion):
        (playerX, playerY) = playerX_playerY
        (x, y) = x_y
        if (playerX - x < cushion) and (playerX - x > -cushion) and (playerY - y < cushion) and (
                playerY - y > -cushion):
            return True
        else:
            return False

    @staticmethod
    def CheckIfHitSomething(playerX_playerY, row_col):
        (playerX, playerY) = playerX_playerY
        (row, col) = row_col
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (playerX - (iCol * TILE_WIDTH) < TILE_WIDTH) and (
                        playerX - (iCol * TILE_WIDTH) > -TILE_WIDTH) and (
                        playerY - (iRow * TILE_HEIGHT) < TILE_HEIGHT) and (
                        playerY - (iRow * TILE_HEIGHT) > -TILE_HEIGHT):
                    result = thisLevel.GetMapTile((iRow, iCol))

                    if result == tileID['pellet']:
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        snd_pellet[player.pelletSndNum].play()
                        player.pelletSndNum = 1 - player.pelletSndNum

                        thisLevel.pellets -= 1

                        thisGame.AddToScore(10)

                        if thisLevel.pellets == 0:
                            thisGame.SetMode(6)

                    elif result == tileID['pellet-power']:
                        # ATIVA O QUIZ
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        quiz_system.start_quiz()
                        thisGame.SetMode(12) # Modo 12 = Quiz Ativo

                    elif result == tileID['door-h']:
                        for i in range(0, thisLevel.lvlWidth, 1):
                            if not i == iCol:
                                if thisLevel.GetMapTile((iRow, i)) == tileID['door-h']:
                                    player.x = i * TILE_WIDTH

                                    if player.velX > 0:
                                        player.x += TILE_WIDTH
                                    else:
                                        player.x -= TILE_WIDTH

                    elif result == tileID['door-v']:
                        for i in range(0, thisLevel.lvlHeight, 1):
                            if not i == iRow:
                                if thisLevel.GetMapTile((i, iCol)) == tileID['door-v']:
                                    player.y = i * TILE_HEIGHT

                                    if player.velY > 0:
                                        player.y += TILE_HEIGHT
                                    else:
                                        player.y -= TILE_HEIGHT

    def GetGhostBoxPos(self):
        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile((row, col)) == tileID['ghost-door']:
                    return row, col

        return False

    def GetPathwayPairPos(self):
        doorArray = []

        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile((row, col)) == tileID['door-h']:
                    doorArray.append((row, col))
                elif self.GetMapTile((row, col)) == tileID['door-v']:
                    doorArray.append((row, col))

        if len(doorArray) == 0:
            return False

        chosenDoor = random.randint(0, len(doorArray) - 1)

        if self.GetMapTile(doorArray[chosenDoor]) == tileID['door-h']:
            for i in range(0, thisLevel.lvlWidth, 1):
                if not i == doorArray[chosenDoor][1]:
                    if thisLevel.GetMapTile((doorArray[chosenDoor][0], i)) == tileID['door-h']:
                        return doorArray[chosenDoor], (doorArray[chosenDoor][0], i)
        else:
            for i in range(0, thisLevel.lvlHeight, 1):
                if not i == doorArray[chosenDoor][0]:
                    if thisLevel.GetMapTile((i, doorArray[chosenDoor][1])) == tileID['door-v']:
                        return doorArray[chosenDoor], (i, doorArray[chosenDoor][1])

        return False

    def DrawMap(self):
        global rect_list
        self.powerPelletBlinkTimer += 1
        if self.powerPelletBlinkTimer == 40:
            self.powerPelletBlinkTimer = 0

        for row in range(-1, thisGame.screenTileSize[0] + 1, 1):
            for col in range(-1, thisGame.screenTileSize[1] + 1, 1):

                actualRow = thisGame.screenNearestTilePos[0] + row
                actualCol = thisGame.screenNearestTilePos[1] + col

                useTile = self.GetMapTile((actualRow, actualCol))
                if useTile != 0 and useTile != tileID['door-h'] and useTile != tileID['door-v']:
                    px = col * TILE_WIDTH - thisGame.screenPixelOffset[0]
                    py = row * TILE_HEIGHT - thisGame.screenPixelOffset[1]
                    center = (int(px + TILE_WIDTH / 2), int(py + TILE_HEIGHT / 2))
                    pelletRGB = self.pelletColor[:3]

                    if useTile == tileID['pellet']:
                        # bolinha normal: pontinho pequeno
                        pygame.draw.circle(screen, pelletRGB, center, max(2, TILE_WIDTH // 8))

                    elif useTile == tileID['pellet-power']:
                        # bolinha grande (power-up): pisca
                        if self.powerPelletBlinkTimer < 20:
                            pygame.draw.circle(screen, pelletRGB, center, max(4, TILE_WIDTH // 4))

                    elif useTile == tileID['showlogo']:
                        screen.blit(thisGame.imLogo, (px, py))

                    elif useTile == tileID['hiscores']:
                        screen.blit(thisGame.imHiscores, (px, py))

                    else:
                        screen.blit(tileIDImage[useTile], (px, py))

    def LoadLevel(self, levelNum):
        self.map = {}
        self.pellets = 0

        f = open(os.path.join(SCRIPT_PATH, "res", "levels", str(levelNum) + ".txt"), 'r')
        lineNum = -1
        rowNum = 0
        isReadingLevelData = False

        for line in f:

            lineNum += 1

            while len(line) > 0 and (line[-1] == "\n" or line[-1] == "\r"): line = line[:-1]
            while len(line) > 0 and (line[0] == "\n" or line[0] == "\r"): line = line[1:]
            str_splitBySpace = line.split(' ')

            j = str_splitBySpace[0]

            if j == "'" or j == "":
                useLine = False
            elif j == "#":
                useLine = False

                firstWord = str_splitBySpace[1]

                if firstWord == "lvlwidth":
                    self.lvlWidth = int(str_splitBySpace[2])

                elif firstWord == "lvlheight":
                    self.lvlHeight = int(str_splitBySpace[2])

                elif firstWord == "edgecolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "edgelightcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)

                elif firstWord == "edgeshadowcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "fillcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.fillColor = (red, green, blue, 255)

                elif firstWord == "pelletcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.pelletColor = (red, green, blue, 255)

                elif firstWord == "fruittype":
                    thisFruit.fruitType = int(str_splitBySpace[2])

                elif firstWord == "startleveldata":
                    isReadingLevelData = True
                    rowNum = 0

                elif firstWord == "endleveldata":
                    isReadingLevelData = False

            else:
                useLine = True

            if useLine:

                if isReadingLevelData:

                    for k in range(0, self.lvlWidth, 1):
                        self.SetMapTile((rowNum, k), int(str_splitBySpace[k]))

                        thisID = int(str_splitBySpace[k])
                        if thisID == 4:
                            player.homeX = k * TILE_WIDTH
                            player.homeY = rowNum * TILE_HEIGHT
                            self.SetMapTile((rowNum, k), 0)

                        elif 10 <= thisID <= 13:
                            ghosts[thisID - 10].homeX = k * TILE_WIDTH
                            ghosts[thisID - 10].homeY = rowNum * TILE_HEIGHT
                            self.SetMapTile((rowNum, k), 0)

                        elif thisID == 2:
                            self.pellets += 1

                    rowNum += 1
        f.close()
        GetCrossRef()

        path.ResizeMap((self.lvlHeight, self.lvlWidth))

        for row in range(0, path.size[0], 1):
            for col in range(0, path.size[1], 1):
                if self.IsWall((row, col)):
                    path.SetType((row, col), 1)
                else:
                    path.SetType((row, col), 0)

        self.Restart()

    def Restart(self):
        for i in range(0, 4, 1):
            ghosts[i].x = ghosts[i].homeX
            ghosts[i].y = ghosts[i].homeY
            ghosts[i].velX = 0
            ghosts[i].velY = 0
            ghosts[i].state = 1
            ghosts[i].speed = thisGame.ghostSpeed
            ghosts[i].Move()

            (randRow, randCol) = (0, 0)

            while not self.GetMapTile((randRow, randCol)) == tileID['pellet'] or (randRow, randCol) == (0, 0):
                randRow = random.randint(1, self.lvlHeight - 2)
                randCol = random.randint(1, self.lvlWidth - 2)

            ghosts[i].currentPath = path.FindPath((ghosts[i].nearestRow, ghosts[i].nearestCol), (randRow, randCol))
            ghosts[i].FollowNextPathWay()

        thisFruit.active = False

        thisGame.fruitTimer = 0

        player.x = player.homeX
        player.y = player.homeY
        player.velX = 0
        player.velY = 0
        player.reqDirX = 0
        player.reqDirY = 0

        player.anim_pacmanCurrent = player.anim_pacmanS
        player.animFrame = 1


# ============================================
# DEFINIÇÕES DE TILES (Estava faltando)
# ============================================
tileID = {}
tileIDImage = {}


def GetCrossRef():
    global tileID, tileIDImage
    # Le o crossref.txt, que associa o NOME de cada peca ao seu NUMERO.
    # Aceita o formato do editor VB6 ("<numero> <nome> <descricao>"),
    # ignora comentarios (linhas que comecam com ') e comandos (com #),
    # e tolera espacos extras entre as colunas.
    f = open(os.path.join(SCRIPT_PATH, "res", "crossref.txt"), 'r')
    for line in f:
        line = line.strip()
        if line == "" or line[0] == "'" or line[0] == "#":
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        # formato do editor: "<numero> <nome> ..."
        if parts[0].lstrip('-').isdigit():
            tileID[parts[1]] = int(parts[0])
        # formato antigo do port Python: "<nome> <numero> ..."
        elif parts[1].lstrip('-').isdigit():
            tileID[parts[0]] = int(parts[1])
    f.close()

    # Pre-preenche todas as posicoes 0..199 com um tile vazio, para que a
    # recoloracao das paredes (mais abaixo) nunca acesse um indice inexistente.
    for i in range(0, 200, 1):
        tileIDImage[i] = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))

    # Carrega a imagem de cada peca pelo seu NOME (ex.: res/tiles/pellet.gif)
    # e a associa ao NUMERO correspondente, usando o crossref como tradutor.
    # Pecas sem .gif (ou listadas em NO_GIF_TILES) viram um quadrado vazio,
    # em vez de derrubar o jogo.
    for name, number in tileID.items():
        if number in NO_GIF_TILES:
            tileIDImage[number] = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            continue
        tile_path = os.path.join(SCRIPT_PATH, "res", "tiles", name + ".gif")
        if os.path.exists(tile_path):
            tileIDImage[number] = get_image_surface(tile_path)
        else:
            tileIDImage[number] = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))

    for y in range(0, TILE_HEIGHT, 1):
        for x in range(0, TILE_WIDTH, 1):
            if tileIDImage[tileID['pellet-power']].get_at((x, y)) == (0, 0, 0, 255):
                tileIDImage[tileID['pellet-power']].set_at((x, y), (255, 184, 174, 255))
            if tileIDImage[tileID['pellet']].get_at((x, y)) == (0, 0, 0, 255):
                tileIDImage[tileID['pellet']].set_at((x, y), IMG_PELLET_COLOR)

            for i in range(100, 200, 1):
                if tileIDImage[i].get_at((x, y)) == IMG_EDGE_LIGHT_COLOR:
                    tileIDImage[i].set_at((x, y), thisLevel.edgeLightColor)
                elif tileIDImage[i].get_at((x, y)) == IMG_FILL_COLOR:
                    tileIDImage[i].set_at((x, y), thisLevel.fillColor)
                elif tileIDImage[i].get_at((x, y)) == IMG_EDGE_SHADOW_COLOR:
                    tileIDImage[i].set_at((x, y), thisLevel.edgeShadowColor)


# ============================================
# INICIALIZAÇÃO DOS OBJETOS DO JOGO
# ============================================
thisGame = game()
thisLevel = level()
player = pacman()
thisFruit = fruit()
ghosts = {}
for i in range(0, 6, 1):
    ghosts[i] = ghost(i)
path = path_finder()

# Instancia o seu sistema de Quiz
quiz_system = QuizSystem()

# Corrige o tamanho da janela e inicializa o level
# Cria a janela do jogo. A flag SCALED faz com que, em tela cheia, o jogo
# seja escalado preservando a proporcao (com barras pretas se necessario),
# em vez de ficar distorcido. Se a placa de video nao suportar SCALED, cai
# para o modo normal.
fullscreen = False
USE_SCALED = pygame.SCALED   # 0 se SCALED nao funcionar nesta maquina
try:
    window = pygame.display.set_mode(thisGame.screenSize, pygame.SCALED)
except pygame.error:
    USE_SCALED = 0
    window = pygame.display.set_mode(thisGame.screenSize)
pygame.display.set_caption("Pacman Quiz")
screen = pygame.display.get_surface()

# Inicializa as fontes do Quiz
quiz_system.initialize_fonts()

# Carrega o Nível 1
thisLevel.LoadLevel(thisGame.GetLevelNum())
thisGame.SmartMoveScreen()

# Comeca na tela de digitar o nome do jogador
thisGame.SetMode(14)

def draw_name_entry(surf, screen_size, buffer):
    # Tela cheia preta pedindo o nome do jogador.
    surf.fill((0, 0, 0))
    fL = quiz_system.font_large
    fS = quiz_system.font_small
    cx = screen_size[0] // 2
    cy = screen_size[1] // 2

    title = fL.render("PAC-MAN QUIZ", True, (255, 255, 0))
    surf.blit(title, title.get_rect(center=(cx, cy - 100)))

    prompt = fS.render("Type your name and press ENTER:", True, (255, 255, 255))
    surf.blit(prompt, prompt.get_rect(center=(cx, cy - 40)))

    # cursor piscando
    cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
    shown = buffer + cursor
    name_surf = fL.render(shown if shown.strip() else cursor, True, (0, 255, 255))
    box_w = max(280, name_surf.get_width() + 40)
    box = pygame.Rect(0, 0, box_w, 52)
    box.center = (cx, cy + 10)
    pygame.draw.rect(surf, (30, 30, 80), box)
    pygame.draw.rect(surf, (255, 255, 0), box, 3)
    surf.blit(name_surf, name_surf.get_rect(center=box.center))

    hint = fS.render("(letters and numbers, up to 12 characters)", True, (170, 170, 170))
    surf.blit(hint, hint.get_rect(center=(cx, cy + 60)))


def draw_game_over(surf, screen_size, score, ranking, player_name):
    # Tela cheia preta: GAME OVER + sua pontuacao + ranking.
    surf.fill((0, 0, 0))
    fL = quiz_system.font_large
    fS = quiz_system.font_small
    cx = screen_size[0] // 2

    go = fL.render("GAME OVER", True, (255, 60, 60))
    surf.blit(go, go.get_rect(center=(cx, 55)))

    you = fS.render("%s - your score: %d" % (player_name or "Player", score), True, (255, 255, 0))
    surf.blit(you, you.get_rect(center=(cx, 100)))

    rank_title = fS.render("- RANKING (top 10) -", True, (0, 255, 255))
    surf.blit(rank_title, rank_title.get_rect(center=(cx, 145)))

    y = 180
    if not ranking:
        none = fS.render("(no scores yet)", True, (200, 200, 200))
        surf.blit(none, none.get_rect(center=(cx, y)))
    else:
        highlighted = False
        for idx, (sc, nm) in enumerate(ranking[:10], start=1):
            color = (255, 255, 255)
            if (not highlighted) and nm == player_name and sc == score:
                color = (0, 255, 0)   # destaca a sua entrada
                highlighted = True
            rank_s = fS.render("%2d." % idx, True, color)
            name_s = fS.render(str(nm)[:12], True, color)
            score_s = fS.render(str(sc), True, color)
            surf.blit(rank_s, (cx - 150, y))
            surf.blit(name_s, (cx - 110, y))
            surf.blit(score_s, (cx + 70, y))
            y += 28

    again = fS.render("Press ENTER to play again", True, (255, 255, 0))
    surf.blit(again, again.get_rect(center=(cx, screen_size[1] - 35)))


# ============================================
# LOOP PRINCIPAL DO JOGO
# ============================================
while True:
    # 1. PROCESSAR EVENTOS (Teclado, Sair)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            # F11: alterna entre tela cheia e janela
            if event.key == K_F11:
                fullscreen = not fullscreen
                flags = USE_SCALED
                if fullscreen:
                    flags = flags | pygame.FULLSCREEN
                pygame.display.set_mode(thisGame.screenSize, flags)
                screen = pygame.display.get_surface()
                continue

            if event.key == K_ESCAPE:
                # Em tela cheia, ESC apenas sai do fullscreen (mais seguro
                # durante uma apresentacao - evita fechar sem querer).
                if fullscreen:
                    fullscreen = False
                    pygame.display.set_mode(thisGame.screenSize, USE_SCALED)
                    screen = pygame.display.get_surface()
                    continue
                pygame.quit()
                sys.exit()

            # ----- MODO DIGITAR NOME -----
            if thisGame.mode == 14:
                if event.key == K_RETURN:
                    if name_input_buffer.strip():
                        current_player_name = name_input_buffer.strip()
                        name_input_buffer = ""
                        thisGame.StartNewGame()
                        thisGame.SmartMoveScreen()
                elif event.key == K_BACKSPACE:
                    name_input_buffer = name_input_buffer[:-1]
                else:
                    ch = event.unicode
                    if (ch and ch.isprintable() and ch not in ("\r", "\n", "\t")
                            and len(name_input_buffer) < 12):
                        name_input_buffer += ch

            # ----- MODO QUIZ: PERGUNTA NA TELA (jogo pausado) -----
            elif thisGame.mode == 12:
                answer = None
                if event.key == K_a:
                    answer = 'A'
                elif event.key == K_b:
                    answer = 'B'
                elif event.key == K_c:
                    answer = 'C'
                elif event.key == K_d:
                    answer = 'D'

                if answer:
                    # Verifica a resposta e passa a mostrar o feedback (Correct/Wrong).
                    # O power-up (se acertou) so e aplicado quando o feedback termina.
                    quiz_system.check_answer(answer)
                    thisGame.SetMode(13)  # Modo 13 = mostrando feedback

            # ----- MODO JOGANDO (Normal) -----
            elif thisGame.mode == 1:
                if event.key == K_LEFT:
                    player.reqDirX = -1
                    player.reqDirY = 0
                elif event.key == K_RIGHT:
                    player.reqDirX = 1
                    player.reqDirY = 0
                elif event.key == K_UP:
                    player.reqDirX = 0
                    player.reqDirY = -1
                elif event.key == K_DOWN:
                    player.reqDirX = 0
                    player.reqDirY = 1

            # ----- MODO "READY" -----
            elif thisGame.mode == 0 or thisGame.mode == 4:
                 if event.key == K_RETURN:
                    thisGame.SetMode(1)
            
            # ----- MODO "GAME OVER" (joga de novo -> pede novo nome) -----
            elif thisGame.mode == 3:
                if event.key == K_RETURN:
                    name_input_buffer = ""
                    thisGame.SetMode(14)

    # 2. ATUALIZAR LÓGICA DO JOGO (Movimentação)
    
    # Só atualiza a lógica se o jogo não estiver no modo "Ready", "Morrendo", "Quiz", etc.
    if thisGame.mode == 1:
        player.Move()
        for i in range(0, 4):
            ghosts[i].Move()
        thisFruit.Move()
        thisGame.SmartMoveScreen()

    elif thisGame.mode == 0:  # "Ready"
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 100:
            thisGame.SetMode(1)

    elif thisGame.mode == 2:  # "Morrendo"
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 100:
            thisGame.lives -= 1
            if thisGame.lives == -1:
                add_score_to_ranking(current_player_name, thisGame.score)
                thisGame.SetMode(3)  # Game Over
            else:
                thisGame.SetMode(4)  # Reinicia Posições

    elif thisGame.mode == 4: # Reiniciando Posições
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 60:
            thisGame.SetMode(0) # Volta pra "Ready"
            thisLevel.Restart()

    elif thisGame.mode == 5:  # Comeu um fantasma: pausa breve e volta ao jogo
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 25:
            thisGame.SetMode(1)
            # se o power-up ainda esta ativo, retoma a musica de power-up
            if thisGame.ghostTimer > 0:
                thisGame.PlayBackgoundSound(snd_powerpellet)

    elif thisGame.mode == 6:  # Limpou o mapa (pegou todas as bolinhas)
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 100:
            thisGame.RestartSameLevel()  # mesmo mapa, fantasmas mais rapidos
            thisGame.SmartMoveScreen()

    elif thisGame.mode == 13:  # Mostrando feedback do quiz (Correct / Wrong)
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 90:  # ~1.5 segundos a 60 FPS
            if quiz_system.last_answer_correct:
                # ACERTOU -> ganha o power-up (fantasmas ficam vulneraveis)
                thisGame.ghostTimer = 360
                thisGame.ghostValue = 200
                snd_powerpellet.play()
                for i in range(0, 4):
                    if ghosts[i].state == 1:
                        ghosts[i].state = 2
            # ERROU -> nao acontece nada
            quiz_system.end_feedback()
            thisGame.SetMode(1)

    # 3. DESENHAR TUDO NA TELA
    screen.blit(img_Background, (0, 0))

    thisLevel.DrawMap()
    thisFruit.Draw()
    player.Draw()
    for i in range(0, 4):
        ghosts[i].Draw()
    
    thisGame.DrawScore()

    # Desenha o Quiz por cima de tudo (se estiver ativo)
    quiz_system.draw(screen, thisGame.screenSize)

    # Telas de nome (inicio/jogar de novo) e game over com ranking
    if thisGame.mode == 14:
        draw_name_entry(screen, thisGame.screenSize, name_input_buffer)
    elif thisGame.mode == 3:
        draw_game_over(screen, thisGame.screenSize, thisGame.score,
                       get_ranking(), current_player_name)

    pygame.display.flip()

    # 4. CONTROLAR O FPS
    clock.tick(60)