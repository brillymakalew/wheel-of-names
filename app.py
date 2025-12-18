import tkinter as tk
import math, random
import winsound

WIDTH, HEIGHT = 1200, 900
CENTER = WIDTH // 2
RADIUS = 330

class NeonWheel:
    def __init__(self, root):
        self.root = root
        root.title("🎰 NEON WHEEL OF NAMES")
        root.attributes("-fullscreen", True)

        root.bind("<Escape>", lambda e: root.destroy())

        self.canvas = tk.Canvas(root, bg="#050012")
        self.canvas.pack(fill="both", expand=True)

        self.names = []
        self.angle = 0
        self.speed = 0
        self.spinning = False
        self.light_phase = 0
        self.confetti = []

        self.ui()
        self.animate_lights()

    def ui(self):
        panel = tk.Frame(self.root, bg="#050012")
        panel.place(x=40, y=40)

        self.entry = tk.Entry(panel, font=("Consolas", 14), width=25)
        self.entry.grid(row=0, column=0)

        tk.Button(panel, text="ADD NAME", command=self.add,
                  bg="#00ffaa", fg="black",
                  font=("Consolas", 12, "bold")).grid(row=0, column=1, padx=10)

        tk.Button(panel, text="▶ START", command=self.start,
                  bg="#00ff00", fg="black",
                  font=("Consolas", 14, "bold")).grid(row=1, column=0, pady=10)

        tk.Button(panel, text="■ STOP", command=self.stop,
                  bg="#ff0055", fg="white",
                  font=("Consolas", 14, "bold")).grid(row=1, column=1)

    def add(self):
        n = self.entry.get().strip()
        if n:
            self.names.append(n)
            self.entry.delete(0, tk.END)
            self.draw()

    def draw(self):
        self.canvas.delete("wheel")
        if not self.names: return

        step = 360 / len(self.names)

        for i, name in enumerate(self.names):
            start = self.angle + i * step
            color = random.choice(["#ff00ff", "#00ffff", "#00ff55", "#ffaa00"])

            self.canvas.create_arc(
                CENTER-RADIUS, CENTER-RADIUS,
                CENTER+RADIUS, CENTER+RADIUS,
                start=start, extent=step,
                fill=color, outline="", tags="wheel"
            )

            ang = math.radians(start + step/2)
            x = CENTER + math.cos(ang) * RADIUS*0.65
            y = CENTER - math.sin(ang) * RADIUS*0.65

            self.canvas.create_text(
                x, y, text=name,
                fill="white",
                font=("Consolas", 14, "bold"),
                tags="wheel"
            )

        # Pointer
        self.canvas.create_polygon(
            CENTER-20, CENTER-RADIUS-10,
            CENTER+20, CENTER-RADIUS-10,
            CENTER, CENTER-RADIUS-45,
            fill="#ffff00", tags="wheel"
        )

    def animate_lights(self):
        self.canvas.delete("lights")
        for i in range(36):
            a = math.radians(i*10 + self.light_phase)
            x = CENTER + math.cos(a) * (RADIUS+30)
            y = CENTER - math.sin(a) * (RADIUS+30)
            c = "#ffff00" if i % 2 == self.light_phase % 2 else "#ff00ff"
            self.canvas.create_oval(x-6,y-6,x+6,y+6, fill=c, tags="lights")

        self.light_phase += 4
        self.root.after(90, self.animate_lights)

    def start(self):
        if not self.names: return
        self.speed = random.uniform(20, 25)
        self.spinning = True
        self.spin()

    def stop(self):
        self.spinning = False

    def spin(self):
        if self.speed > 0.15:
            self.angle += self.speed
            self.speed *= 0.995 if self.spinning else 0.965

            if self.speed < 1.8:
                self.angle += random.uniform(-1,1)

            winsound.Beep(900, 20)
            self.draw()
            self.root.after(30, self.spin)
        else:
            self.winner()

    def winner(self):
        step = 360 / len(self.names)
        idx = int((-self.angle % 360) / step)

        if random.choice([True, False]):
            idx = (idx + 1) % len(self.names)

        win = self.names[idx]
        winsound.Beep(1200, 300)
        self.canvas.create_text(
            CENTER, CENTER,
            text=f"🎉 {win} 🎉",
            fill="#00ffcc",
            font=("Consolas", 48, "bold")
        )
        self.spawn_confetti()

    def spawn_confetti(self):
        for _ in range(200):
            x = random.randint(0, WIDTH)
            y = random.randint(-HEIGHT, 0)
            c = random.choice(["#ff0","#0ff","#f0f","#0f0"])
            self.confetti.append([x,y,c])

        self.fall()

    def fall(self):
        self.canvas.delete("confetti")
        for p in self.confetti:
            p[1] += random.randint(4,8)
            self.canvas.create_oval(p[0],p[1],p[0]+6,p[1]+6,
                                    fill=p[2], tags="confetti")
        if self.confetti[0][1] < HEIGHT:
            self.root.after(50, self.fall)

if __name__ == "__main__":
    root = tk.Tk()
    NeonWheel(root)
    root.mainloop()
