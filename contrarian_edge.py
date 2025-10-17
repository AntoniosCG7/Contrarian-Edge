import customtkinter as ctk
import yfinance as yf
from datetime import datetime, timedelta
import threading
from collections import deque
import time
import gc

_matplotlib_loaded = False


def load_matplotlib():
    global _matplotlib_loaded, plt, FigureCanvasTkAgg, Figure
    if not _matplotlib_loaded:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        _matplotlib_loaded = True


class ContrarianEdgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Contrarian Edge")
        self.geometry("900x930")
        self.minsize(900, 930)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(
            (0, 1, 2), weight=1, uniform="cards", minsize=220
        )

        self.header = ctk.CTkLabel(
            self.main_container,
            text="Contrarian Edge",
            font=ctk.CTkFont(family="Bahnschrift", size=32, weight="bold"),
        )
        self.header.grid(
            row=0, column=0, columnspan=3, pady=(20, 6), padx=20, sticky="ew"
        )

        self.subtitle = ctk.CTkLabel(
            self.main_container,
            text="S&P 500 Long Entry Signal System",
            font=ctk.CTkFont(family="Bahnschrift", size=14),
        )

        self.subtitle.grid(
            row=1, column=0, columnspan=3, pady=(0, 3), padx=20, sticky="ew"
        )

        self.last_updated = ctk.CTkLabel(
            self.main_container,
            text="Last updated: Never",
            font=ctk.CTkFont(family="Bahnschrift", size=12),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.last_updated.grid(
            row=2, column=0, columnspan=3, pady=(0, 16), padx=20, sticky="ew"
        )

        market_data_section = ctk.CTkLabel(
            self.main_container,
            text="MARKET DATA",
            font=ctk.CTkFont(family="Bahnschrift", size=17, weight="bold"),
        )
        market_data_section.grid(
            row=3, column=0, columnspan=3, pady=(0, 10), sticky="w", padx=20
        )

        self.vix_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.vix_frame.grid(row=4, column=1, padx=4, pady=(0, 12), sticky="nsew")
        self.vix_frame.grid_columnconfigure(0, weight=1)

        self.vix_header = ctk.CTkLabel(
            self.vix_frame,
            text="VIX",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.vix_header.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        self.vix_value = ctk.CTkLabel(
            self.vix_frame,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=44, weight="bold"),
        )
        self.vix_value.grid(row=1, column=0, padx=18, pady=(0, 3), sticky="w")

        self.vix_change = ctk.CTkLabel(
            self.vix_frame,
            text="",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.vix_change.grid(row=2, column=0, padx=18, pady=(0, 6), sticky="w")

        self.vix_sentiment_badge = ctk.CTkLabel(
            self.vix_frame,
            text="",
            font=ctk.CTkFont(family="Bahnschrift", size=13, weight="bold"),
            corner_radius=5,
            width=75,
            height=22,
        )
        self.vix_sentiment_badge.grid(row=3, column=0, padx=18, pady=(0, 6), sticky="w")

        self.vix_description = ctk.CTkLabel(
            self.vix_frame,
            text="Short-term volatility",
            font=ctk.CTkFont(family="Bahnschrift", size=13),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.vix_description.grid(row=4, column=0, padx=18, pady=(0, 18), sticky="w")

        self.vix3m_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.vix3m_frame.grid(
            row=4, column=2, padx=(4, 20), pady=(0, 12), sticky="nsew"
        )
        self.vix3m_frame.grid_columnconfigure(0, weight=1)

        self.vix3m_header = ctk.CTkLabel(
            self.vix3m_frame,
            text="VIX3M",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.vix3m_header.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        self.vix3m_value = ctk.CTkLabel(
            self.vix3m_frame,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=44, weight="bold"),
        )
        self.vix3m_value.grid(row=1, column=0, padx=18, pady=(0, 3), sticky="w")

        self.vix3m_change = ctk.CTkLabel(
            self.vix3m_frame,
            text="",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.vix3m_change.grid(row=2, column=0, padx=18, pady=(0, 6), sticky="w")

        self.vix3m_sentiment_badge = ctk.CTkLabel(
            self.vix3m_frame,
            text="",
            font=ctk.CTkFont(family="Bahnschrift", size=13, weight="bold"),
            corner_radius=5,
            width=75,
            height=22,
        )
        self.vix3m_sentiment_badge.grid(
            row=3, column=0, padx=18, pady=(0, 6), sticky="w"
        )

        self.vix3m_description = ctk.CTkLabel(
            self.vix3m_frame,
            text="3-month volatility",
            font=ctk.CTkFont(family="Bahnschrift", size=13),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.vix3m_description.grid(row=4, column=0, padx=18, pady=(0, 18), sticky="w")

        self.spy_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.spy_frame.grid(row=4, column=0, padx=(20, 4), pady=(0, 12), sticky="nsew")
        self.spy_frame.grid_columnconfigure(0, weight=1)

        self.spy_header = ctk.CTkLabel(
            self.spy_frame,
            text="S&P 500",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.spy_header.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        self.spy_value = ctk.CTkLabel(
            self.spy_frame,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=44, weight="bold"),
        )
        self.spy_value.grid(row=1, column=0, padx=18, pady=(0, 3), sticky="w")

        self.spy_change = ctk.CTkLabel(
            self.spy_frame,
            text="",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.spy_change.grid(row=2, column=0, padx=18, pady=(0, 6), sticky="w")

        self.spy_sentiment_badge = ctk.CTkLabel(
            self.spy_frame,
            text="Index",
            font=ctk.CTkFont(family="Bahnschrift", size=13, weight="bold"),
            corner_radius=5,
            width=75,
            height=22,
            fg_color="#3b82f6",
            text_color="white",
        )
        self.spy_sentiment_badge.grid(row=3, column=0, padx=18, pady=(0, 6), sticky="w")

        self.spy_description = ctk.CTkLabel(
            self.spy_frame,
            text="Target for long positions",
            font=ctk.CTkFont(family="Bahnschrift", size=13),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.spy_description.grid(row=4, column=0, padx=18, pady=(0, 18), sticky="w")

        self.ratio_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.ratio_frame.grid(
            row=8, column=0, columnspan=3, padx=20, pady=(0, 12), sticky="nsew"
        )
        self.ratio_frame.grid_columnconfigure(0, weight=1)

        self.ratio_header = ctk.CTkLabel(
            self.ratio_frame,
            text="VIX/VIX3M Ratio",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.ratio_header.grid(row=0, column=0, padx=18, pady=(18, 6))

        self.ratio_value = ctk.CTkLabel(
            self.ratio_frame,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=44, weight="bold"),
        )
        self.ratio_value.grid(row=1, column=0, padx=18, pady=(0, 6))

        self.sentiment_badge = ctk.CTkLabel(
            self.ratio_frame,
            text="",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
            corner_radius=5,
            width=75,
            height=22,
        )
        self.sentiment_badge.grid(row=2, column=0, padx=18, pady=(0, 6))

        ratio_bar_container = ctk.CTkFrame(self.ratio_frame, fg_color="transparent")
        ratio_bar_container.grid(row=3, column=0, padx=18, pady=(6, 6), sticky="ew")
        ratio_bar_container.grid_columnconfigure(1, weight=1)

        self.ratio_min_label = ctk.CTkLabel(
            ratio_bar_container,
            text="0.80",
            font=ctk.CTkFont(family="Bahnschrift", size=11),
            text_color=("#6b7280", "#9ca3af"),
            width=35,
        )
        self.ratio_min_label.grid(row=0, column=0, padx=(0, 8))

        self.ratio_progress = ctk.CTkProgressBar(
            ratio_bar_container,
            height=12,
            corner_radius=6,
        )
        self.ratio_progress.grid(row=0, column=1, sticky="ew")
        self.ratio_progress.set(0.5)

        self.ratio_max_label = ctk.CTkLabel(
            ratio_bar_container,
            text="1.20",
            font=ctk.CTkFont(family="Bahnschrift", size=11),
            text_color=("#6b7280", "#9ca3af"),
            width=35,
        )
        self.ratio_max_label.grid(row=0, column=2, padx=(8, 0))

        ratio_zone_labels = ctk.CTkFrame(ratio_bar_container, fg_color="transparent")
        ratio_zone_labels.grid(row=1, column=1, pady=(4, 0), sticky="ew")
        ratio_zone_labels.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            ratio_zone_labels,
            text="Low Fear",
            font=ctk.CTkFont(family="Bahnschrift", size=12, weight="bold"),
            text_color=("#6b7280", "#9ca3af"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            ratio_zone_labels,
            text="Neutral",
            font=ctk.CTkFont(family="Bahnschrift", size=12, weight="bold"),
            text_color=("#eab308", "#eab308"),
        ).grid(row=0, column=1)

        ctk.CTkLabel(
            ratio_zone_labels,
            text="High Fear",
            font=ctk.CTkFont(family="Bahnschrift", size=12, weight="bold"),
            text_color=("#22c55e", "#22c55e"),
        ).grid(row=0, column=2, sticky="e")

        self.ratio_description = ctk.CTkLabel(
            self.ratio_frame,
            text="Fear/complacency gauge",
            font=ctk.CTkFont(family="Bahnschrift", size=13),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.ratio_description.grid(row=4, column=0, padx=18, pady=(6, 18))

        indicators_section = ctk.CTkLabel(
            self.main_container,
            text="TECHNICAL INDICATORS",
            font=ctk.CTkFont(family="Bahnschrift", size=17, weight="bold"),
        )
        indicators_section.grid(
            row=6, column=0, columnspan=3, pady=(0, 10), sticky="w", padx=20
        )

        self.rsi_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.rsi_frame.grid(row=7, column=0, padx=(20, 4), pady=(0, 12), sticky="nsew")
        self.rsi_frame.grid_columnconfigure(0, weight=1)

        self.rsi_header = ctk.CTkLabel(
            self.rsi_frame,
            text="RSI (14-Day)",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.rsi_header.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        self.rsi_value = ctk.CTkLabel(
            self.rsi_frame,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=44, weight="bold"),
        )
        self.rsi_value.grid(row=1, column=0, padx=18, pady=(0, 6), sticky="w")

        self.rsi_status = ctk.CTkLabel(
            self.rsi_frame,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.rsi_status.grid(row=2, column=0, padx=18, pady=(0, 6), sticky="w")

        self.rsi_description = ctk.CTkLabel(
            self.rsi_frame,
            text="S&P 500 momentum",
            font=ctk.CTkFont(family="Bahnschrift", size=13),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.rsi_description.grid(row=3, column=0, padx=18, pady=(0, 18), sticky="w")

        self.macd_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.macd_frame.grid(row=7, column=1, padx=4, pady=(0, 12), sticky="nsew")
        self.macd_frame.grid_columnconfigure(0, weight=1)

        self.macd_header = ctk.CTkLabel(
            self.macd_frame,
            text="MACD",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.macd_header.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        macd_value_container = ctk.CTkFrame(self.macd_frame, fg_color="transparent")
        macd_value_container.grid(row=1, column=0, padx=18, pady=(0, 6), sticky="w")

        self.macd_dot = ctk.CTkLabel(
            macd_value_container,
            text="●",
            font=ctk.CTkFont(family="Bahnschrift", size=26, weight="bold"),
        )
        self.macd_dot.grid(row=0, column=0, padx=(0, 8))

        self.macd_value = ctk.CTkLabel(
            macd_value_container,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=44, weight="bold"),
        )
        self.macd_value.grid(row=0, column=1)

        self.macd_status = ctk.CTkLabel(
            self.macd_frame,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.macd_status.grid(row=2, column=0, padx=18, pady=(0, 6), sticky="w")

        self.macd_description = ctk.CTkLabel(
            self.macd_frame,
            text="Trend momentum",
            font=ctk.CTkFont(family="Bahnschrift", size=13),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.macd_description.grid(row=3, column=0, padx=18, pady=(0, 18), sticky="w")

        self.ma200_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.ma200_frame.grid(
            row=7, column=2, padx=(4, 20), pady=(0, 12), sticky="nsew"
        )
        self.ma200_frame.grid_columnconfigure(0, weight=1)

        self.ma200_header = ctk.CTkLabel(
            self.ma200_frame,
            text="200-Day MA",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.ma200_header.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        ma200_value_container = ctk.CTkFrame(self.ma200_frame, fg_color="transparent")
        ma200_value_container.grid(row=1, column=0, padx=18, pady=(0, 6), sticky="w")

        self.ma200_dot = ctk.CTkLabel(
            ma200_value_container,
            text="●",
            font=ctk.CTkFont(family="Bahnschrift", size=26, weight="bold"),
        )
        self.ma200_dot.grid(row=0, column=0, padx=(0, 8))

        self.ma200_value = ctk.CTkLabel(
            ma200_value_container,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=44, weight="bold"),
        )
        self.ma200_value.grid(row=0, column=1)

        self.ma200_status = ctk.CTkLabel(
            self.ma200_frame,
            text="--",
            font=ctk.CTkFont(family="Bahnschrift", size=14, weight="bold"),
        )
        self.ma200_status.grid(row=2, column=0, padx=18, pady=(0, 6), sticky="w")

        self.ma200_description = ctk.CTkLabel(
            self.ma200_frame,
            text="Long-term trend",
            font=ctk.CTkFont(family="Bahnschrift", size=13),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.ma200_description.grid(row=3, column=0, padx=18, pady=(0, 18), sticky="w")

        signal_section = ctk.CTkLabel(
            self.main_container,
            text="ACTIONABLE SIGNAL",
            font=ctk.CTkFont(family="Bahnschrift", size=17, weight="bold"),
        )
        signal_section.grid(
            row=9, column=0, columnspan=3, pady=(0, 10), sticky="w", padx=20
        )

        self.signal_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.signal_frame.grid(
            row=10, column=0, columnspan=3, padx=20, pady=(0, 12), sticky="ew"
        )
        self.signal_frame.grid_columnconfigure(0, weight=1)

        signal_header_container = ctk.CTkFrame(
            self.signal_frame, fg_color="transparent"
        )
        signal_header_container.grid(row=0, column=0, pady=(20, 6))

        self.signal_dot = ctk.CTkLabel(
            signal_header_container,
            text="●",
            font=ctk.CTkFont(family="Bahnschrift", size=24),
            text_color="#22c55e",
        )
        self.signal_dot.grid(row=0, column=0, padx=(0, 10))

        self.signal_action = ctk.CTkLabel(
            signal_header_container,
            text="BUY",
            font=ctk.CTkFont(family="Bahnschrift", size=44, weight="bold"),
        )
        self.signal_action.grid(row=0, column=1)

        signal_meta_container = ctk.CTkFrame(self.signal_frame, fg_color="transparent")
        signal_meta_container.grid(row=1, column=0, pady=(6, 8))

        self.signal_confidence = ctk.CTkLabel(
            signal_meta_container,
            text="Confidence: 75%",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.signal_confidence.grid(row=0, column=0, padx=(0, 16))

        self.signal_details = ctk.CTkLabel(
            signal_meta_container,
            text="3/4 indicators bullish",
            font=ctk.CTkFont(family="Bahnschrift", size=13, weight="bold"),
        )
        self.signal_details.grid(row=0, column=1)

        self.signal_bar = ctk.CTkProgressBar(self.signal_frame, height=10)
        self.signal_bar.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.signal_bar.set(0)

        self.signal_description = ctk.CTkLabel(
            self.signal_frame,
            text="Consider buying S&P 500 ETFs (SPY, VOO, IVV) when conditions align.",
            font=ctk.CTkFont(family="Bahnschrift", size=13, weight="bold"),
            wraplength=1000,
        )
        self.signal_description.grid(row=3, column=0, pady=(0, 20))

        chart_section = ctk.CTkLabel(
            self.main_container,
            text="TREND ANALYSIS",
            font=ctk.CTkFont(family="Bahnschrift", size=17, weight="bold"),
        )
        chart_section.grid(
            row=11, column=0, columnspan=3, pady=(0, 10), sticky="w", padx=20
        )

        self.chart_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, border_width=2
        )
        self.chart_frame.grid(
            row=12, column=0, columnspan=3, padx=20, pady=(0, 12), sticky="nsew"
        )
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_rowconfigure(1, weight=1)

        self.chart_header = ctk.CTkLabel(
            self.chart_frame,
            text="VIX/VIX3M RATIO TREND (60-DAY)",
            font=ctk.CTkFont(family="Bahnschrift", size=15, weight="bold"),
        )
        self.chart_header.grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")

        self.footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.footer_frame.grid(
            row=13, column=0, columnspan=3, padx=20, pady=(0, 20), sticky="ew"
        )
        self.footer_frame.grid_columnconfigure(0, weight=3)
        self.footer_frame.grid_columnconfigure(1, weight=1)

        self.refresh_button = ctk.CTkButton(
            self.footer_frame,
            text="Refresh Now",
            command=self.manual_refresh,
            font=ctk.CTkFont(family="Bahnschrift", size=13, weight="bold"),
            height=44,
            corner_radius=8,
            fg_color="#3b82f6",
            hover_color="#2563eb",
        )
        self.refresh_button.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        self.theme_button = ctk.CTkButton(
            self.footer_frame,
            text="Theme: Dark",
            command=self.toggle_theme,
            font=ctk.CTkFont(family="Bahnschrift", size=13, weight="bold"),
            height=44,
            corner_radius=8,
            fg_color="transparent",
            border_width=2,
            border_color="#3b82f6",
            text_color=("#3b82f6", "#3b82f6"),
            hover_color=("#e0e7ff", "#1e3a5f"),
        )
        self.theme_button.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.brand_tagline = ctk.CTkLabel(
            self.footer_frame,
            text="Contrarian Edge © 2025 — Turning Fear Into Opportunity",
            font=ctk.CTkFont(family="Bahnschrift", size=11, slant="italic"),
            text_color=("#6b7280", "#9ca3af"),
        )
        self.brand_tagline.grid(row=1, column=0, columnspan=2, pady=(6, 0))

        self.current_ratio = None
        self.previous_values = {}
        self.ratio_history = deque(maxlen=60)
        self.ratio_dates = deque(maxlen=60)

        self.chart_canvas = None
        self.last_chart_data = None

        self.auto_refresh_enabled = True
        self.fetch_data()
        self.schedule_refresh()

    def get_vix_sentiment(self, vix_value):
        if vix_value < 12:
            return "Very Low", "#6b7280"
        elif vix_value < 16:
            return "Low", "#6b7280"
        elif vix_value < 20:
            return "Normal", "#3b82f6"
        elif vix_value < 25:
            return "Elevated", "#3b82f6"
        elif vix_value < 30:
            return "High", "#3b82f6"
        elif vix_value < 40:
            return "Very High", "#3b82f6"
        else:
            return "Extreme", "#3b82f6"

    def get_ratio_sentiment(self, ratio_value):
        if ratio_value >= 1.10:
            return "Extreme Fear", "#3b82f6"
        elif ratio_value >= 1.05:
            return "High Fear", "#3b82f6"
        elif ratio_value >= 1.00:
            return "Fear", "#3b82f6"
        elif ratio_value >= 0.95:
            return "Neutral", "#3b82f6"
        elif ratio_value >= 0.90:
            return "Calm", "#6b7280"
        else:
            return "Very Calm", "#6b7280"

    def get_strategy_action(self, ratio_value):
        if ratio_value >= 1.05:
            return "STRONG BUY", "#22c55e"
        elif ratio_value >= 1.00:
            return "BUY", "#22c55e"
        elif ratio_value >= 0.95:
            return "WATCH", "#eab308"
        else:
            return "WAIT", "#6b7280"

    def calculate_rsi(self, prices, period=14):
        try:
            if len(prices) < period + 1:
                return None

            deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]

            avg_gain = sum(gains[:period]) / period
            avg_loss = sum(losses[:period]) / period

            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period

            if avg_loss == 0:
                return 100

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            print(f"Error calculating RSI: {e}")
            return None

    def calculate_macd(self, prices):
        try:
            if len(prices) < 26:
                return None, None

            def calculate_ema_series(data, period):
                multiplier = 2 / (period + 1)
                ema_values = []
                sma = sum(data[:period]) / period
                ema_values.append(sma)

                for i in range(period, len(data)):
                    ema = (data[i] - ema_values[-1]) * multiplier + ema_values[-1]
                    ema_values.append(ema)

                return ema_values

            ema_12_series = calculate_ema_series(prices, 12)
            ema_26_series = calculate_ema_series(prices, 26)

            macd_line_series = []
            for i in range(len(ema_26_series)):
                macd_value = ema_12_series[i + 14] - ema_26_series[i]
                macd_line_series.append(macd_value)

            macd_line = macd_line_series[-1]

            if len(macd_line_series) < 9:
                return macd_line, None

            signal_line_series = calculate_ema_series(macd_line_series, 9)
            signal_line = signal_line_series[-1]

            return macd_line, signal_line
        except Exception as e:
            print(f"Error calculating MACD: {e}")
            return None, None

    def validate_indicators(
        self, spy_price, rsi_value, macd_line, signal_line, ma200_value
    ):
        validation_passed = True
        warnings = []

        if rsi_value is not None:
            if rsi_value < 0 or rsi_value > 100:
                warnings.append(f"RSI out of valid range (0-100): {rsi_value:.2f}")
                validation_passed = False

            if rsi_value < 20 or rsi_value > 80:
                warnings.append(f"RSI at extreme level: {rsi_value:.2f}")

        if macd_line is not None and signal_line is not None:
            macd_diff = abs(macd_line - signal_line)
            if macd_diff > 100:
                warnings.append(f"Unusually large MACD divergence: {macd_diff:.2f}")

        if ma200_value is not None and spy_price is not None:
            price_vs_ma = ((spy_price - ma200_value) / ma200_value) * 100
            if abs(price_vs_ma) > 30:
                warnings.append(
                    f"S&P 500 {abs(price_vs_ma):.1f}% from 200-MA (unusual)"
                )

        if warnings:
            print("\n=== DATA VALIDATION WARNINGS ===")
            for warning in warnings:
                print(f"  ⚠ {warning}")
            print("=" * 40)

        return validation_passed

    def calculate_signal_strength(self, ratio, rsi, macd_crossover, above_ma200):
        score = 0
        signals = []
        entry_signals = 0

        if ratio >= 1.10:
            score += 40
            entry_signals += 1
            signals.append("[ENTRY] Extreme Fear - Prime Entry")
        elif ratio >= 1.05:
            score += 35
            entry_signals += 1
            signals.append("[ENTRY] High Fear - Strong Entry")
        elif ratio >= 1.00:
            score += 25
            entry_signals += 1
            signals.append("[ENTRY] Elevated Fear - Entry Signal")
        elif ratio >= 0.95:
            score += 10
            signals.append("[WATCH] Neutral - Monitor")
        else:
            score += 0
            signals.append("[WAIT] Low Fear - No Entry Signal")

        if rsi is not None:
            if rsi < 30:
                score += 30
                entry_signals += 1
                signals.append("[ENTRY] RSI Oversold - Strong Entry")
            elif rsi < 40:
                score += 20
                entry_signals += 1
                signals.append("[ENTRY] RSI Approaching Oversold")
            elif rsi < 50:
                score += 10
                signals.append("[WATCH] RSI Neutral-Low")
            elif rsi < 70:
                score += 5
                signals.append("[WATCH] RSI Neutral-High")
            else:
                score += 0
                signals.append("[WAIT] RSI Overbought - Wait")

        if macd_crossover == "bullish":
            score += 20
            entry_signals += 1
            signals.append("[ENTRY] MACD Bullish - Momentum Confirmed")
        elif macd_crossover == "neutral":
            score += 5
            signals.append("[WATCH] MACD Neutral")
        else:
            score += 0
            signals.append("[WAIT] MACD Bearish - Wait for Turn")

        if above_ma200:
            score += 20
            entry_signals += 1
            signals.append("[ENTRY] Above 200-MA - Bull Trend")
        else:
            score += 5
            signals.append("[WATCH] Below 200-MA - Caution")

        score = max(0, min(100, score))

        if score >= 85 and entry_signals >= 3:
            action = "STRONG BUY"
            color = "#22c55e"
        elif score >= 65 and entry_signals >= 2:
            action = "BUY"
            color = "#22c55e"
        elif score >= 40:
            action = "WATCH"
            color = "#eab308"
        else:
            action = "WAIT"
            color = "#6b7280"

        return action, score, color, signals, entry_signals

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

            current_chart_data = (tuple(self.ratio_history), ctk.get_appearance_mode())
            if (
                self.last_chart_data == current_chart_data
                and self.chart_canvas is not None
            ):
                return

            self.last_chart_data = current_chart_data

            load_matplotlib()

            if self.chart_canvas is not None:
                try:
                    widget = self.chart_canvas.get_tk_widget()
                    if widget.winfo_exists():
                        widget.destroy()
                except Exception as e:
                    print(f"Error destroying old chart widget: {e}")
                finally:
                    self.chart_canvas = None
                    gc.collect()

        except Exception as e:
            print(f"Error updating chart: {e}")
            return

        try:
            current_mode = ctk.get_appearance_mode().lower()
            text_color = "#ffffff" if current_mode == "dark" else "#000000"
            grid_color = "#333333" if current_mode == "dark" else "#e0e0e0"
            line_color = "#3b82f6"
            bg_color = "#2b2b2b" if current_mode == "dark" else "#dbdbdb"

            fig = Figure(figsize=(10, 3.5), facecolor=bg_color, dpi=90)
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
                linewidth=2.5,
                marker="o",
                markersize=5,
                markerfacecolor=line_color,
                markeredgecolor=bg_color,
                markeredgewidth=1.5,
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
                fontfamily="Bahnschrift",
                fontweight="600",
                labelpad=10,
            )
            ax.set_ylabel(
                "VIX/VIX3M Ratio",
                color=text_color,
                fontsize=10,
                fontfamily="Bahnschrift",
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

            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.chart_canvas.draw()
            canvas_widget = self.chart_canvas.get_tk_widget()
            canvas_widget.configure(background=bg_color)
            canvas_widget.grid(row=1, column=0, padx=14, pady=(0, 14), sticky="nsew")

            plt.close(fig)
        except Exception as e:
            print(f"Error creating/rendering chart: {e}")

    def fetch_data(self):
        try:
            self.refresh_button.configure(
                state="disabled", text="Fetching...", fg_color="#6b7280"
            )

            if len(self.ratio_history) == 0:
                try:
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=75)

                    vix = yf.Ticker("^VIX")
                    vix3m = yf.Ticker("^VIX3M")
                    vix_hist = vix.history(start=start_date, end=end_date)
                    vix3m_hist = vix3m.history(start=start_date, end=end_date)

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
                        )[-60:]

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
            rsi_value = None
            macd_line = None
            signal_line = None
            macd_crossover = "neutral"
            above_ma200 = False
            ma200_value = None

            try:
                print("\n=== FETCHING S&P 500 DATA ===")
                spy_data_full = yf.Ticker("^GSPC").history(period="1y")
                print(f"S&P 500 data rows: {len(spy_data_full)}")

                if not spy_data_full.empty and len(spy_data_full) > 0:
                    spy_price = float(spy_data_full["Close"].iloc[-1])
                    print(f"S&P 500 Price: ${spy_price:.2f}")

                    if spy_price <= 0 or spy_price > 100000:
                        print(f"Invalid S&P 500 price: {spy_price}")
                        spy_price = None
                    else:
                        prices_list = spy_data_full["Close"].tolist()

                        rsi_value = self.calculate_rsi(prices_list, period=14)

                        macd_line, signal_line = self.calculate_macd(prices_list)
                        if macd_line is not None and signal_line is not None:
                            if macd_line > signal_line:
                                macd_crossover = "bullish"
                            elif macd_line < signal_line:
                                macd_crossover = "bearish"

                        if len(prices_list) >= 200:
                            ma200_value = sum(prices_list[-200:]) / 200
                            above_ma200 = spy_price > ma200_value

                        rsi_str = f"{rsi_value:.2f}" if rsi_value is not None else "N/A"
                        ma200_str = (
                            f"{ma200_value:.2f}" if ma200_value is not None else "N/A"
                        )
                        print(f"RSI (Wilder's Smoothing): {rsi_str}")
                        print(f"MACD Crossover: {macd_crossover}")
                        print(f"MA200: {ma200_str}, Above: {above_ma200}")

                        print(f"\n=== TECHNICAL INDICATORS (Detailed) ===")
                        print(f"Current S&P 500: ${spy_price:.2f}")
                        print(
                            f"Last 5 S&P 500 prices: {[f'${p:.2f}' for p in prices_list[-5:]]}"
                        )
                        if rsi_value is not None:
                            print(f"RSI (14-day, Wilder's method): {rsi_value:.4f}")
                        if macd_line is not None and signal_line is not None:
                            macd_histogram = macd_line - signal_line
                            print(f"MACD Line: {macd_line:.4f}")
                            print(f"Signal Line: {signal_line:.4f}")
                            print(f"MACD Histogram: {macd_histogram:.4f}")
                        if ma200_value is not None:
                            price_vs_ma_pct = (
                                (spy_price - ma200_value) / ma200_value
                            ) * 100
                            print(f"200-Day MA: ${ma200_value:.2f}")
                            print(f"Price vs MA200: {price_vs_ma_pct:+.2f}%")
                        print("=" * 40)

                        self.validate_indicators(
                            spy_price, rsi_value, macd_line, signal_line, ma200_value
                        )
                else:
                    print("S&P 500 data is empty!")
                    spy_price = None
            except Exception as e:
                print(f"ERROR fetching S&P 500 data: {e}")
                import traceback

                traceback.print_exc()
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
                        spy_data_full["Close"].iloc[-2]
                        if len(spy_data_full) > 1
                        else spy_price
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

            ratio_min = 0.80
            ratio_max = 1.20
            ratio_clamped = max(ratio_min, min(ratio_max, ratio))
            progress_value = (ratio_clamped - ratio_min) / (ratio_max - ratio_min)
            self.ratio_progress.set(progress_value)

            if ratio >= 1.05:
                bar_color = "#22c55e"
            elif ratio >= 0.95:
                bar_color = "#eab308"
            else:
                bar_color = "#6b7280"

            self.ratio_progress.configure(progress_color=bar_color)

            if spy_price is not None:
                self.spy_value.configure(text=f"${spy_price:.2f}")
            else:
                self.spy_value.configure(text="N/A")

            vix_change_color = "#ef4444" if vix_change < 0 else "#22c55e"
            vix_arrow = "▼" if vix_change < 0 else "▲"
            self.vix_change.configure(
                text=f"{vix_arrow} {abs(vix_change):.2f} ({abs(vix_change_pct):.2f}%)",
                text_color=vix_change_color,
            )

            vix3m_change_color = "#ef4444" if vix3m_change < 0 else "#22c55e"
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
                text=ratio_sentiment, fg_color=bar_color, text_color="white"
            )

            if rsi_value is not None:
                self.rsi_value.configure(text=f"{rsi_value:.1f}")
                if rsi_value < 30:
                    rsi_status_text = "Oversold - Strong Entry Signal"
                    rsi_status_color = "#22c55e"
                elif rsi_value < 40:
                    rsi_status_text = "Approaching Oversold - Entry Zone"
                    rsi_status_color = "#22c55e"
                elif rsi_value < 50:
                    rsi_status_text = "Neutral-Low - Monitor"
                    rsi_status_color = "#3b82f6"
                elif rsi_value < 70:
                    rsi_status_text = "Neutral-High - No Entry"
                    rsi_status_color = "#6b7280"
                else:
                    rsi_status_text = "Overbought - Wait"
                    rsi_status_color = "#6b7280"
                self.rsi_status.configure(
                    text=rsi_status_text, text_color=rsi_status_color
                )
            else:
                self.rsi_value.configure(text="--")
                self.rsi_status.configure(text="Data unavailable", text_color="#6b7280")

            if macd_line is not None and signal_line is not None:
                if macd_crossover == "bullish":
                    self.macd_value.configure(text="BULLISH")
                    self.macd_dot.configure(text_color="#22c55e")
                    self.macd_status.configure(
                        text="Bullish Momentum Confirmed", text_color="#22c55e"
                    )
                elif macd_crossover == "bearish":
                    self.macd_value.configure(text="BEARISH")
                    self.macd_dot.configure(text_color="#f97316")
                    self.macd_status.configure(
                        text="Wait for Momentum Shift", text_color="#f97316"
                    )
                else:
                    self.macd_value.configure(text="NEUTRAL")
                    self.macd_dot.configure(text_color="#eab308")
                    self.macd_status.configure(
                        text="Neutral - Monitor", text_color="#eab308"
                    )
            else:
                self.macd_value.configure(text="--")
                self.macd_dot.configure(text_color="#6b7280")
                self.macd_status.configure(
                    text="Data unavailable", text_color="#6b7280"
                )

            if ma200_value is not None:
                if above_ma200:
                    self.ma200_value.configure(text="ABOVE")
                    self.ma200_dot.configure(text_color="#22c55e")
                    self.ma200_status.configure(
                        text="Bull Trend - Favorable Entry", text_color="#22c55e"
                    )
                else:
                    self.ma200_value.configure(text="BELOW")
                    self.ma200_dot.configure(text_color="#eab308")
                    self.ma200_status.configure(
                        text="Below 200-MA - Use Caution", text_color="#eab308"
                    )
            else:
                self.ma200_value.configure(text="--")
                self.ma200_dot.configure(text_color="#6b7280")
                self.ma200_status.configure(
                    text="Data unavailable", text_color="#6b7280"
                )

            signal_action, signal_score, signal_color, signals, entry_signals = (
                self.calculate_signal_strength(
                    ratio, rsi_value, macd_crossover, above_ma200
                )
            )

            signal_icons = {
                "STRONG BUY": "STRONG BUY",
                "BUY": "BUY",
                "WATCH": "WATCH",
                "WAIT": "WAIT",
            }
            display_action = signal_icons.get(signal_action, signal_action)
            self.signal_action.configure(text=display_action)
            self.signal_dot.configure(text_color=signal_color)
            self.signal_confidence.configure(
                text=f"Entry Score: {signal_score}/100", text_color=signal_color
            )
            self.signal_details.configure(
                text=f"{entry_signals}/4 entry signals active"
            )

            try:
                self.signal_bar.set(signal_score / 100.0)
                self.signal_bar.configure(progress_color=signal_color)
            except Exception:
                pass

            signal_descriptions = {
                "STRONG BUY": "Extreme fear detected with strong technical confirmation. Prime S&P 500 ETF entry opportunity.",
                "BUY": "Elevated fear with favorable technical setup. Good S&P 500 ETF entry opportunity.",
                "WATCH": "Moderate conditions. Monitor for stronger S&P 500 entry signals to develop.",
                "WAIT": "Insufficient fear/technical confirmation. Wait for better S&P 500 entry opportunity.",
            }
            self.signal_description.configure(
                text=signal_descriptions.get(
                    signal_action, "Analyzing market conditions..."
                )
            )

            print(f"\n=== CONTRARIAN LONG-ENTRY SIGNAL ===")
            print(f"Action: {signal_action}")
            print(f"Entry Score: {signal_score}/100")
            print(f"Active Entry Signals: {entry_signals}/4")
            print("Signal Breakdown:")
            for signal in signals:
                print(f"  • {signal}")
            print("=" * 40)

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

            if self.current_ratio >= 1.05:
                bar_color = "#22c55e"
            elif self.current_ratio >= 0.95:
                bar_color = "#eab308"
            else:
                bar_color = "#6b7280"

            self.sentiment_badge.configure(
                text=ratio_sentiment, fg_color=bar_color, text_color="white"
            )

        self.after(100, self.update_chart)


if __name__ == "__main__":
    app = ContrarianEdgeApp()
    app.mainloop()
