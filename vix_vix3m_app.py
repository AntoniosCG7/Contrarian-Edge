import customtkinter as ctk
import yfinance as yf
from datetime import datetime, timedelta
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
import time


class VIXMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VIX/VIX3M Monitor")
        self.geometry("1500x900")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=60, pady=50)
        self.main_container.grid_columnconfigure((0, 1), weight=1)
        self.main_container.grid_columnconfigure(2, weight=2)

        self.header = ctk.CTkLabel(
            self.main_container,
            text="VIX/VIX3M Monitor",
            font=ctk.CTkFont(family="Bahnschrift", size=48, weight="bold"),
        )
        self.header.grid(row=0, column=0, columnspan=3, pady=(0, 4))

        self.subtitle = ctk.CTkLabel(
            self.main_container,
            text="Real-time market volatility sentiment tracker",
            font=ctk.CTkFont(family="Segoe UI", size=17),
        )
        self.subtitle.grid(row=1, column=0, columnspan=3, pady=(0, 4))

        self.last_updated = ctk.CTkLabel(
            self.main_container,
            text="Last updated: Never",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.last_updated.grid(row=2, column=0, columnspan=3, pady=(0, 20))

        self.vix_frame = ctk.CTkFrame(
            self.main_container, corner_radius=8, border_width=2, width=320, height=280
        )
        self.vix_frame.grid(row=3, column=0, padx=(0, 8), pady=(0, 8), sticky="nw")
        self.vix_frame.grid_columnconfigure(0, weight=1)
        self.vix_frame.grid_propagate(False)

        self.vix_header = ctk.CTkLabel(
            self.vix_frame,
            text="VIX",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.vix_header.grid(row=0, column=0, padx=28, pady=(28, 10), sticky="w")

        self.vix_value = ctk.CTkLabel(
            self.vix_frame,
            text="--",
            font=ctk.CTkFont(family="Consolas", size=52, weight="bold"),
        )
        self.vix_value.grid(row=1, column=0, padx=28, pady=(0, 6), sticky="w")

        self.vix_change = ctk.CTkLabel(
            self.vix_frame,
            text="",
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
        )
        self.vix_change.grid(row=2, column=0, padx=28, pady=(0, 10), sticky="w")

        self.vix_sentiment_badge = ctk.CTkLabel(
            self.vix_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8,
            width=85,
            height=28,
        )
        self.vix_sentiment_badge.grid(
            row=3, column=0, padx=28, pady=(0, 10), sticky="w"
        )

        self.vix_description = ctk.CTkLabel(
            self.vix_frame,
            text="Short-term volatility",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.vix_description.grid(row=4, column=0, padx=28, pady=(0, 28), sticky="w")

        self.vix3m_frame = ctk.CTkFrame(
            self.main_container, corner_radius=8, border_width=2, width=320, height=280
        )
        self.vix3m_frame.grid(row=3, column=1, padx=(8, 0), pady=(0, 8), sticky="nw")
        self.vix3m_frame.grid_columnconfigure(0, weight=1)
        self.vix3m_frame.grid_propagate(False)

        self.vix3m_header = ctk.CTkLabel(
            self.vix3m_frame,
            text="VIX3M",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.vix3m_header.grid(row=0, column=0, padx=28, pady=(28, 10), sticky="w")

        self.vix3m_value = ctk.CTkLabel(
            self.vix3m_frame,
            text="--",
            font=ctk.CTkFont(family="Consolas", size=52, weight="bold"),
        )
        self.vix3m_value.grid(row=1, column=0, padx=28, pady=(0, 6), sticky="w")

        self.vix3m_change = ctk.CTkLabel(
            self.vix3m_frame,
            text="",
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
        )
        self.vix3m_change.grid(row=2, column=0, padx=28, pady=(0, 10), sticky="w")

        self.vix3m_sentiment_badge = ctk.CTkLabel(
            self.vix3m_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8,
            width=85,
            height=28,
        )
        self.vix3m_sentiment_badge.grid(
            row=3, column=0, padx=28, pady=(0, 10), sticky="w"
        )

        self.vix3m_description = ctk.CTkLabel(
            self.vix3m_frame,
            text="3-month volatility",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.vix3m_description.grid(row=4, column=0, padx=28, pady=(0, 28), sticky="w")

        self.spy_frame = ctk.CTkFrame(
            self.main_container, corner_radius=8, border_width=2, width=320, height=280
        )
        self.spy_frame.grid(row=4, column=0, padx=(0, 8), pady=(8, 0), sticky="nw")
        self.spy_frame.grid_columnconfigure(0, weight=1)
        self.spy_frame.grid_propagate(False)

        self.spy_header = ctk.CTkLabel(
            self.spy_frame,
            text="S&P 500",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.spy_header.grid(row=0, column=0, padx=28, pady=(28, 10), sticky="w")

        self.spy_value = ctk.CTkLabel(
            self.spy_frame,
            text="--",
            font=ctk.CTkFont(family="Consolas", size=52, weight="bold"),
        )
        self.spy_value.grid(row=1, column=0, padx=28, pady=(0, 6), sticky="w")

        self.spy_change = ctk.CTkLabel(
            self.spy_frame,
            text="",
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
        )
        self.spy_change.grid(row=2, column=0, padx=28, pady=(0, 10), sticky="w")

        self.spy_sentiment_badge = ctk.CTkLabel(
            self.spy_frame,
            text="Index",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8,
            width=85,
            height=28,
            fg_color="#3b82f6",
            text_color="white",
        )
        self.spy_sentiment_badge.grid(
            row=3, column=0, padx=28, pady=(0, 10), sticky="w"
        )

        self.spy_description = ctk.CTkLabel(
            self.spy_frame,
            text="Market reference",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.spy_description.grid(row=4, column=0, padx=28, pady=(0, 28), sticky="w")

        self.ratio_frame = ctk.CTkFrame(
            self.main_container, corner_radius=8, border_width=2, width=320, height=280
        )
        self.ratio_frame.grid(row=4, column=1, padx=(8, 0), pady=(8, 0), sticky="nw")
        self.ratio_frame.grid_columnconfigure(0, weight=1)
        self.ratio_frame.grid_propagate(False)

        self.ratio_header = ctk.CTkLabel(
            self.ratio_frame,
            text="RATIO",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.ratio_header.grid(row=0, column=0, padx=28, pady=(28, 10), sticky="w")

        self.ratio_value = ctk.CTkLabel(
            self.ratio_frame,
            text="--",
            font=ctk.CTkFont(family="Consolas", size=52, weight="bold"),
        )
        self.ratio_value.grid(row=1, column=0, padx=28, pady=(0, 6), sticky="w")

        strategy_container = ctk.CTkFrame(self.ratio_frame, fg_color="transparent")
        strategy_container.grid(row=2, column=0, padx=28, pady=(0, 10), sticky="w")

        self.strategy_dot = ctk.CTkLabel(
            strategy_container,
            text="●",
            font=ctk.CTkFont(family="Arial", size=28, weight="bold"),
            width=25,
        )
        self.strategy_dot.grid(row=0, column=0, padx=(0, 3), pady=(0, 3))

        self.strategy_action = ctk.CTkLabel(
            strategy_container,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        )
        self.strategy_action.grid(row=0, column=1)

        self.sentiment_badge = ctk.CTkLabel(
            self.ratio_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8,
            width=85,
            height=28,
        )
        self.sentiment_badge.grid(row=3, column=0, padx=28, pady=(0, 10), sticky="w")

        self.ratio_description = ctk.CTkLabel(
            self.ratio_frame,
            text="VIX/VIX3M sentiment",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.ratio_description.grid(row=4, column=0, padx=28, pady=(0, 28), sticky="w")

        self.chart_frame = ctk.CTkFrame(
            self.main_container, corner_radius=8, border_width=2
        )
        self.chart_frame.grid(
            row=3, column=2, rowspan=2, padx=(16, 0), pady=(0, 0), sticky="nsew"
        )

        self.chart_header = ctk.CTkLabel(
            self.chart_frame,
            text="VIX/VIX3M RATIO TREND (60-DAY)",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.chart_header.grid(row=0, column=0, padx=28, pady=(24, 8), sticky="w")

        self.footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.footer_frame.grid(row=5, column=0, columnspan=3, pady=(20, 0), sticky="ew")
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.button_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.refresh_button = ctk.CTkButton(
            self.button_frame,
            text="Refresh Now",
            command=self.manual_refresh,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            height=50,
            corner_radius=12,
            fg_color="#3b82f6",
            hover_color="#2563eb",
        )
        self.refresh_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.theme_button = ctk.CTkButton(
            self.button_frame,
            text="Theme: Dark",
            command=self.toggle_theme,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            height=50,
            corner_radius=12,
            fg_color="transparent",
            border_width=2,
            border_color="#3b82f6",
            text_color=("#3b82f6", "#3b82f6"),
            hover_color=("#e0e7ff", "#1e3a5f"),
        )
        self.theme_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        self.current_ratio = None
        self.previous_values = {}
        self.ratio_history = deque(maxlen=60)
        self.ratio_dates = deque(maxlen=60)

        self.auto_refresh_enabled = True
        self.fetch_data()
        self.schedule_refresh()

    def get_vix_sentiment(self, vix_value):
        if vix_value < 12:
            return "Very Low", "#22c55e"
        elif vix_value < 16:
            return "Low", "#84cc16"
        elif vix_value < 20:
            return "Normal", "#3b82f6"
        elif vix_value < 25:
            return "Elevated", "#f59e0b"
        elif vix_value < 30:
            return "High", "#f97316"
        elif vix_value < 40:
            return "Very High", "#ef4444"
        else:
            return "Extreme", "#dc2626"

    def get_ratio_sentiment(self, ratio_value):
        if ratio_value >= 1.10:
            return "Extreme Fear", "#dc2626"
        elif ratio_value >= 1.05:
            return "High Fear", "#ef4444"
        elif ratio_value >= 1.00:
            return "Fear", "#f97316"
        elif ratio_value >= 0.95:
            return "Neutral", "#3b82f6"
        elif ratio_value >= 0.90:
            return "Calm", "#84cc16"
        else:
            return "Very Calm", "#22c55e"

    def get_strategy_action(self, ratio_value):
        if ratio_value >= 1.05:
            return "STRONG BUY", "#22c55e"
        elif ratio_value >= 1.00:
            return "BUY", "#22c55e"
        elif ratio_value >= 0.90:
            return "WATCH", "#eab308"
        elif ratio_value >= 0.85:
            return "CAUTION", "#f97316"
        else:
            return "REDUCE/HEDGE", "#ef4444"

    def fetch_ticker_data(self, ticker_symbol, retries=3, delay=1):
        for attempt in range(retries):
            try:
                ticker = yf.Ticker(ticker_symbol)
                data = ticker.history(period="5d")
                if not data.empty and len(data) > 0:
                    return data
                if attempt < retries - 1:
                    print(f"Empty data for {ticker_symbol}, retrying in {delay}s...")
                    time.sleep(delay)
            except Exception as e:
                if attempt < retries - 1:
                    print(
                        f"Error fetching {ticker_symbol} (attempt {attempt + 1}/{retries}): {e}"
                    )
                    time.sleep(delay)
                else:
                    raise
        raise ValueError(
            f"No data available for {ticker_symbol} after {retries} attempts"
        )

    def update_chart(self):
        try:
            if len(self.ratio_history) < 2:
                return

            for widget in self.chart_frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()
        except Exception as e:
            print(f"Error updating chart: {e}")
            return

        try:
            current_mode = ctk.get_appearance_mode().lower()
            text_color = "#ffffff" if current_mode == "dark" else "#000000"
            grid_color = "#333333" if current_mode == "dark" else "#e0e0e0"
            line_color = "#3b82f6"
            bg_color = "#2b2b2b" if current_mode == "dark" else "#dbdbdb"

            fig = Figure(figsize=(7.0, 5.0), facecolor=bg_color, dpi=100)
            ax = fig.add_subplot(111)
            ax.set_facecolor(bg_color)

            ratios = list(self.ratio_history)
            dates = list(self.ratio_dates)
            x_vals = list(range(len(ratios)))

            if len(ratios) == 0 or len(x_vals) == 0:
                print("No data to plot")
                return

            print(f"\n=== CHART DATA ({len(ratios)} points) ===")
            for i, (date, ratio) in enumerate(zip(dates[-10:], ratios[-10:])):
                print(f"{date}: {ratio:.4f}")
            print("=" * 40)

            ax.fill_between(
                x_vals,
                ratios,
                1.0,
                where=[r >= 1.0 for r in ratios],
                alpha=0.15,
                color="#ef4444",
                interpolate=True,
            )
            ax.fill_between(
                x_vals,
                ratios,
                1.0,
                where=[r < 1.0 for r in ratios],
                alpha=0.15,
                color="#22c55e",
                interpolate=True,
            )

            ax.plot(
                x_vals,
                ratios,
                color=line_color,
                linewidth=3,
                marker="o",
                markersize=6,
                markerfacecolor=line_color,
                markeredgecolor=bg_color,
                markeredgewidth=2,
                alpha=1.0,
                zorder=3,
                antialiased=True,
            )

            ax.axhline(
                y=1.0, color="#ef4444", linestyle="--", linewidth=2, alpha=0.6, zorder=2
            )

            date_labels = [d.strftime("%m/%d") for d in dates]
            if len(date_labels) > 10:
                step = len(date_labels) // 8
                tick_positions = list(range(0, len(date_labels), step))
                ax.set_xticks(tick_positions)
                ax.set_xticklabels(
                    [date_labels[i] for i in tick_positions], rotation=45, ha="right"
                )
            else:
                ax.set_xticks(x_vals)
                ax.set_xticklabels(date_labels, rotation=45, ha="right")

            ax.set_xlabel(
                "Date",
                color=text_color,
                fontsize=10,
                fontfamily="Segoe UI",
                fontweight="600",
                labelpad=10,
            )
            ax.set_ylabel(
                "VIX/VIX3M Ratio",
                color=text_color,
                fontsize=10,
                fontfamily="Segoe UI",
                fontweight="600",
                labelpad=10,
            )
            ax.tick_params(axis="x", colors=text_color, labelsize=8, width=1, length=4)
            ax.tick_params(axis="y", colors=text_color, labelsize=9, width=1, length=4)
            ax.grid(
                True, alpha=0.2, color=grid_color, linewidth=1, linestyle="-", zorder=1
            )

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_color(grid_color)
            ax.spines["left"].set_color(grid_color)
            ax.spines["bottom"].set_linewidth(1.5)
            ax.spines["left"].set_linewidth(1.5)

            ax.margins(x=0.02, y=0.1)

            fig.tight_layout(pad=2.0, rect=[0, 0.03, 1, 1])

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.configure(background=bg_color)
            canvas_widget.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        except Exception as e:
            print(f"Error creating/rendering chart: {e}")

    def fetch_data(self):
        try:
            self.refresh_button.configure(
                state="disabled", text="Fetching...", fg_color="#6b7280"
            )

            if len(self.ratio_history) == 0:
                try:
                    vix = yf.Ticker("^VIX")
                    vix3m = yf.Ticker("^VIX3M")
                    vix_hist = vix.history(period="2mo")
                    vix3m_hist = vix3m.history(period="2mo")

                    if not vix_hist.empty and not vix3m_hist.empty:
                        print(f"\n=== LOADING HISTORICAL DATA ===")
                        print(f"VIX history: {len(vix_hist)} days")
                        print(f"VIX3M history: {len(vix3m_hist)} days")

                        vix_hist = vix_hist[["Close"]].copy()
                        vix3m_hist = vix3m_hist[["Close"]].copy()

                        vix_hist.index = vix_hist.index.date
                        vix3m_hist.index = vix3m_hist.index.date

                        common_dates = sorted(
                            set(vix_hist.index) & set(vix3m_hist.index)
                        )

                        print(f"Common dates: {len(common_dates)}")

                        for i, date in enumerate(common_dates):
                            vix_val = vix_hist.loc[date, "Close"]
                            vix3m_val = vix3m_hist.loc[date, "Close"]

                            if vix_val > 0 and vix3m_val > 0:
                                ratio_val = vix_val / vix3m_val
                                self.ratio_history.append(ratio_val)
                                self.ratio_dates.append(date)

                                if i < 5 or i >= len(common_dates) - 5:
                                    print(
                                        f"  {date}: VIX={vix_val:.2f}, VIX3M={vix3m_val:.2f}, Ratio={ratio_val:.4f}"
                                    )
                                elif i == 5:
                                    print(
                                        f"  ... ({len(common_dates) - 10} more dates) ..."
                                    )

                        print(f"Loaded {len(self.ratio_history)} ratio data points")
                        if len(self.ratio_dates) > 0:
                            print(
                                f"Date range: {self.ratio_dates[0]} to {self.ratio_dates[-1]}"
                            )
                        print("=" * 40)
                except Exception as e:
                    print(f"Error loading historical data: {e}")

            vix_data = self.fetch_ticker_data("^VIX")
            vix3m_data = self.fetch_ticker_data("^VIX3M")

            vix_price = float(vix_data["Close"].iloc[-1])
            vix3m_price = float(vix3m_data["Close"].iloc[-1])

            if vix_price <= 0 or vix3m_price <= 0:
                raise ValueError("Invalid VIX/VIX3M price data")
            if vix_price > 200 or vix3m_price > 200:
                raise ValueError("VIX/VIX3M price seems abnormally high")
            if vix3m_price == 0:
                raise ValueError("VIX3M price is zero")

            ratio = vix_price / vix3m_price

            print(f"\n=== DATA FETCH ===")
            print(f"VIX: {vix_price:.2f}")
            print(f"VIX3M: {vix3m_price:.2f}")
            print(f"Ratio: {ratio:.4f}")
            print(f"Date: {datetime.now().date()}")
            print("=" * 40)

            spy_price = None
            try:
                spy_data = self.fetch_ticker_data("^GSPC", retries=2)
                spy_price = float(spy_data["Close"].iloc[-1])
                if spy_price <= 0 or spy_price > 100000:
                    print(f"Invalid S&P 500 price: {spy_price}")
                    spy_price = None
            except Exception as e:
                print(f"Could not fetch S&P 500 data: {e}")
                spy_price = None

            vix_prev = vix_data["Close"].iloc[-2] if len(vix_data) > 1 else vix_price
            vix3m_prev = (
                vix3m_data["Close"].iloc[-2] if len(vix3m_data) > 1 else vix3m_price
            )

            vix_change = vix_price - vix_prev
            vix_change_pct = (vix_change / vix_prev) * 100
            vix3m_change = vix3m_price - vix3m_prev
            vix3m_change_pct = (vix3m_change / vix3m_prev) * 100

            spy_change = 0
            spy_change_pct = 0
            spy_prev = spy_price
            if spy_price is not None:
                try:
                    spy_prev = (
                        spy_data["Close"].iloc[-2] if len(spy_data) > 1 else spy_price
                    )
                    spy_change = spy_price - spy_prev
                    spy_change_pct = (spy_change / spy_prev) * 100
                except:
                    pass

            self.current_ratio = ratio

            if len(self.ratio_history) > 2:
                recent_ratios = list(self.ratio_history)[-5:]
                avg_ratio = sum(recent_ratios) / len(recent_ratios)
                if abs(ratio - avg_ratio) > 0.15:
                    print(f"WARNING: Unusual ratio spike detected!")
                    print(f"  Current: {ratio:.4f}, Recent avg: {avg_ratio:.4f}")
                    print(f"  This might indicate bad data or a major market event")

            today = datetime.now().date()

            if len(self.ratio_dates) > 0 and self.ratio_dates[-1] == today:
                print(
                    f"Updating today's ratio: {self.ratio_history[-1]:.4f} -> {ratio:.4f}"
                )
                self.ratio_history[-1] = ratio
            else:
                print(f"Adding new day: {today} with ratio {ratio:.4f}")
                self.ratio_history.append(ratio)
                self.ratio_dates.append(today)

            self.vix_value.configure(text=f"{vix_price:.2f}")
            self.vix3m_value.configure(text=f"{vix3m_price:.2f}")
            self.ratio_value.configure(text=f"{ratio:.4f}")

            if spy_price is not None:
                self.spy_value.configure(text=f"${spy_price:.2f}")
            else:
                self.spy_value.configure(text="N/A")

            vix_change_color = "#22c55e" if vix_change < 0 else "#ef4444"
            vix_arrow = "▼" if vix_change < 0 else "▲"
            self.vix_change.configure(
                text=f"{vix_arrow} {abs(vix_change):.2f} ({abs(vix_change_pct):.2f}%)",
                text_color=vix_change_color,
            )

            vix3m_change_color = "#22c55e" if vix3m_change < 0 else "#ef4444"
            vix3m_arrow = "▼" if vix3m_change < 0 else "▲"
            self.vix3m_change.configure(
                text=f"{vix3m_arrow} {abs(vix3m_change):.2f} ({abs(vix3m_change_pct):.2f}%)",
                text_color=vix3m_change_color,
            )

            if spy_price is not None:
                spy_change_color = "#22c55e" if spy_change > 0 else "#ef4444"
                spy_arrow = "▲" if spy_change > 0 else "▼"
                self.spy_change.configure(
                    text=f"{spy_arrow} ${abs(spy_change):.2f} ({abs(spy_change_pct):.2f}%)",
                    text_color=spy_change_color,
                )
            else:
                self.spy_change.configure(
                    text="Data unavailable",
                    text_color="#6b7280",
                )

            strategy_action, dot_color = self.get_strategy_action(ratio)
            self.strategy_action.configure(text=strategy_action)
            self.strategy_dot.configure(text_color=dot_color)

            vix_sentiment, vix_color = self.get_vix_sentiment(vix_price)
            self.vix_sentiment_badge.configure(
                text=vix_sentiment, fg_color=vix_color, text_color="white"
            )

            vix3m_sentiment, vix3m_color = self.get_vix_sentiment(vix3m_price)
            self.vix3m_sentiment_badge.configure(
                text=vix3m_sentiment, fg_color=vix3m_color, text_color="white"
            )

            ratio_sentiment, ratio_color = self.get_ratio_sentiment(ratio)
            self.sentiment_badge.configure(
                text=ratio_sentiment, fg_color=ratio_color, text_color="white"
            )

            self.update_chart()

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_updated.configure(text=f"Last updated: {now}")

        except Exception as e:
            error_msg = str(e)
            print(f"Error fetching data: {error_msg}")

            if (
                "No VIX data available" in error_msg
                or "No VIX3M data available" in error_msg
            ):
                self.ratio_value.configure(text="N/A")
                self.sentiment_badge.configure(text="CLOSED", fg_color="#6b7280")
                self.last_updated.configure(text="Markets may be closed")
            elif "No S&P 500 data available" in error_msg:
                pass
            else:
                self.ratio_value.configure(text="ERROR")
                self.sentiment_badge.configure(text="ERROR", fg_color="#ef4444")
                self.last_updated.configure(text=f"Error: Unable to fetch data")
        finally:
            self.refresh_button.configure(
                state="normal", text="Refresh Now", fg_color="#3b82f6"
            )

    def manual_refresh(self):
        thread = threading.Thread(target=self.fetch_data, daemon=True)
        thread.start()

    def schedule_refresh(self):
        if self.auto_refresh_enabled:
            thread = threading.Thread(target=self.fetch_data, daemon=True)
            thread.start()
            self.after(60000, self.schedule_refresh)

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode().lower()
        new_mode = "Light" if current_mode == "dark" else "Dark"
        ctk.set_appearance_mode(new_mode)

        self.theme_button.configure(text=f"Theme: {new_mode}")

        if self.current_ratio is not None:
            ratio_sentiment, ratio_color = self.get_ratio_sentiment(self.current_ratio)
            self.sentiment_badge.configure(
                text=ratio_sentiment, fg_color=ratio_color, text_color="white"
            )

        self.update_chart()


if __name__ == "__main__":
    app = VIXMonitorApp()
    app.mainloop()
