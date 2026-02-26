import sys
import os
import random
import time
import platform
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont, QPainterPath

# =============================
# CONFIGURARE
# =============================

# --- HACK PENTRU UBUNTU/WAYLAND: Forțăm sistemul de ferestre clasic X11 ---
if platform.system() == "Linux":
    os.environ["QT_QPA_PLATFORM"] = "xcb"

FPS = 4
FRAME_TIME = 1000 // FPS  # milisecunde
MEME_INTERVAL = 6.0
FRAME_COUNT = 24
SCALE = 2.0

def resource_path(relative):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        possible_path = os.path.join(base_path, relative)
        if os.path.exists(possible_path): return possible_path
        return os.path.join(base_path, os.path.basename(relative))
    return os.path.join(os.path.abspath("."), relative)

# =============================
# MAIN CLASS (PyQt6)
# =============================
class DriftDancer(QWidget):
    def __init__(self):
        super().__init__()

        # --- MAGIA PENTRU TRANSPARENȚĂ PERFECTĂ PE LINUX ---
        # FramelessWindowHint: Fără margini
        # WindowStaysOnTopHint: Mereu deasupra
        # Tool: Ascunde aplicația din taskbar (opțional, dar bun pentru "desktop pets")
        flags = (Qt.WindowType.FramelessWindowHint |
                 Qt.WindowType.WindowStaysOnTopHint |
                 Qt.WindowType.Tool)
        if platform.system() == "Linux":
            flags |= Qt.WindowType.X11BypassWindowManagerHint
        self.setWindowFlags(flags)
        
        # Atributul critic care spune sistemului de operare că fundalul e gol
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.resize(500, 350)
        self.position_window()

        # Încărcare cadre (Frames)
        self.frames = []
        for i in range(FRAME_COUNT):
            path = resource_path(f"frames/frame_{i:02d}.png")
            if not os.path.exists(path):
                print(f"Eroare: Lipseste {path}")
                sys.exit(1)
            
            pixmap = QPixmap(path)
            # Scalare dacă e necesar
            if SCALE != 1.0:
                new_w = int(pixmap.width() / SCALE)
                new_h = int(pixmap.height() / SCALE)
                pixmap = pixmap.scaled(new_w, new_h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            self.frames.append(pixmap)

        self._drag_pos = None
        self.current_frame = 0
        self.smoke_particles = []
        
        # Sistem Meme
        self.last_meme_time = time.time()
        self.current_meme = None
        self.memelist = [
            "Is that a Supra?! A, stai, are rugină pe aripi.",
            "Semnalizarea a rămas fără lichid.",
            "Schimb pe E46 + diferență?",
            "S-a aprins martorul. E de la vreme.",
            "Băiatu', ai o cheie de 10? Dar un flex?",
            "Dacă nu scoate fum, înseamnă că e oprit.",
            "I paid for the whole speedometer, I'm gonna use it.",
            "Da, da, consumă 5 exterior. Dacă o împingi.",
            "Tractare? Iar?",
            "Suspensie sport sau telescoape scurse?",
            "Mai duce un sezon (cuzineții: 💀).",
            "Nu-s chele, sunt slickuri 👮🏻‍♂️.",
            "🥺👉👈 Mi-a scapat pedala de ambreiaj. 🚔",
            "M-am uitat pe sub ea... mai are un pic și cade.",
            "⚠️ CHECK ENGINE"
        ]

        # Timer pentru animație (Game Loop)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_loop)
        self.timer.start(FRAME_TIME)

    def position_window(self):
        # availableGeometry() găsește ecranul real utilizabil, ignorând taskbar-ul
        screen = QApplication.primaryScreen().availableGeometry()
        
        # Varianta bazată pe colțul dreapta-jos (ancorare perfectă):
        # Luăm punctul de start al ecranului (x, y) + Lățimea/Înălțimea totală - dimensiunea mașinii
        pos_x = screen.x() + screen.width() - 520  # 500 lățimea ferestrei + 20px margine
        pos_y = screen.y() + screen.height() - 360 # 350 înălțimea ferestrei + 10px margine jos
        
        # --- Dacă vrei varianta exactă cu procente (comentează liniile de sus și folosește-le pe astea): ---
        # pos_x = screen.x() + int(screen.width() * 0.80) # 80% spre dreapta
        # pos_y = screen.y() + int(screen.height() * 0.75) # 75% spre jos
        
        self.move(pos_x, pos_y)

    def update_loop(self):
        # 1. Update Cadru Mașină
        self.current_frame = (self.current_frame + 1) % FRAME_COUNT

        # 2. Update Fum
        if random.random() < 0.3:
            # Coordonate fum (ajustează dacă e nevoie)
            x = random.randint(180, 200)
            y = random.randint(230, 250)
            size = random.randint(10, 20)
            self.smoke_particles.append({
                "x": x, "y": y, "size": size,
                "vx": -3 - random.random() * 2,
                "vy": -1 - random.random() * 1,
                "life": 25
            })

        for p in self.smoke_particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
            p["size"] *= 0.95 # Se micșorează în timp
            if p["life"] <= 0 or p["size"] < 2:
                self.smoke_particles.remove(p)

        # 3. Update Meme
        if time.time() - self.last_meme_time > MEME_INTERVAL:
            self.last_meme_time = time.time()
            self.current_meme = random.choice(self.memelist)
        elif time.time() - self.last_meme_time > 4.0:
            # Ascunde mema după 4 secunde
            self.current_meme = None

        # Forțăm redesenarea ferestrei
        self.update()

    # Funcția de desenare (Aici randează PyQt6 grafica pe ecranul transparent)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 1. Desenăm Fumul
        # painter.setPen(Qt.PenStyle.NoPen)
        # painter.setBrush(QColor(150, 150, 150, 180)) # Gri cu puțină transparență alpha
        # for p in self.smoke_particles:
        #     painter.drawEllipse(QRectF(p["x"], p["y"], p["size"], p["size"]))

        # 2. Desenăm Mașina (Centrată pe lățime, așezată jos)
        car_pixmap = self.frames[self.current_frame]
        car_x = int((500 - car_pixmap.width()) / 2)
        car_y = int(350 - car_pixmap.height() - 20)
        painter.drawPixmap(car_x, car_y, car_pixmap)

        # 3. Desenăm Bula de Text (Dacă există)
        # 3. Desenăm Bula de Text (Design Premium)
        if self.current_meme:
            # Mutăm bula mult mai sus (y=10) și îi reducem înălțimea (h=55)
            # Astfel, nu va mai atinge deloc plafonul mașinii
            bubble_rect = QRectF(50, 10, 400, 55)
            
            # Umbră modernă, extrem de fină (Drop shadow)
            painter.setBrush(QColor(0, 0, 0, 60))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(bubble_rect.translated(2, 4), 18, 18)
            
            # Fundal Dark Mode tip "Frosted Glass" (Sleek UI)
            painter.setBrush(QColor(25, 25, 25, 235))
            
            # Contur subtil (BMW M Light Blue, grosime redusă pentru finețe)
            pen = QColor(0, 173, 239, 200) # Cyan/Blue electric
            painter.setPen(pen)
            painter.drawRoundedRect(bubble_rect, 18, 18)

            # Text: Curat, modern, premium
            painter.setPen(QColor(245, 245, 245)) # Alb-gri anti-oboseală
            
            # Folosim un font curat, sans-serif
            font = QFont("Helvetica Neue", 11, QFont.Weight.Bold)
            font.setStyleHint(QFont.StyleHint.SansSerif)
            painter.setFont(font)
            
            # Centrare perfectă matematică
            painter.drawText(bubble_rect, Qt.AlignmentFlag.AlignCenter, self.current_meme)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def _apply_macos_window_level(self):
        """Fix macOS NSPanel behaviour: don't hide on deactivate, float above other apps."""
        try:
            import objc
            from AppKit import NSFloatingWindowLevel
            ns_view = objc.objc_object(c_void_p=int(self.winId()))
            ns_window = ns_view.window()
            # Qt::Tool creates an NSPanel which hides itself when the app loses focus by default.
            # This is why the window disappears when you click Safari / any other app.
            ns_window.setHidesOnDeactivate_(False)
            ns_window.setLevel_(NSFloatingWindowLevel)
            # NSWindowCollectionBehaviorCanJoinAllSpaces = 1 << 0
            # NSWindowCollectionBehaviorStationary    = 1 << 4
            ns_window.setCollectionBehavior_(1 | 16)
        except Exception as e:
            print(f"[macOS] Could not set window level: {e}")

    # Permitem închiderea cu Escape
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dancer = DriftDancer()
    dancer.show()
    if platform.system() == "Darwin":
        dancer._apply_macos_window_level()
    sys.exit(app.exec())