# Contrarian Edge

**A long-only contrarian market timing system that identifies fear-driven entry opportunities using VIX/VXV ratio analysis and technical indicator confirmation.**

## Overview

Contrarian Edge generates actionable BUY or WAIT signals by detecting periods of excessive market fear (elevated VIX/VXV ratio) and confirming them with technical indicators. The system exclusively focuses on identifying long entry opportunities—no short or hedge recommendations.

**Core Philosophy:** _"Buy when fear peaks, wait when complacency reigns."_

## Key Features

### Real-Time Market Intelligence

- Live VIX, VIX3M, and S&P 500 monitoring with percentage/absolute change tracking
- 60-day VIX/VIX3M ratio trend visualization
- Visual progress bar showing current fear levels relative to historical ranges

### Technical Indicators

- **RSI (14-Day)**: Momentum analysis identifying oversold/overbought conditions
- **MACD**: Trend momentum with bullish/bearish crossover detection
- **200-Day MA**: Long-term trend validation and market regime identification

### Long-Only Signal System

Four signal states based on weighted scoring (0-100):

| Signal            | Score  | Criteria                 | Interpretation                               |
| ----------------- | ------ | ------------------------ | -------------------------------------------- |
| ✅ **STRONG BUY** | 85-100 | 3-4 entry signals active | Extreme fear + strong technical confirmation |
| 🟢 **BUY**        | 65-84  | 2+ entry signals active  | Elevated fear + favorable technical setup    |
| ⚪ **WATCH**      | 40-64  | 1-2 signals              | Moderate conditions—monitor for development  |
| ⚫ **WAIT**       | 0-39   | 0-1 signals              | Insufficient entry signals—patience required |

#### Entry Signal Components (X/4 Active)

1. **VIX/VXV Ratio ≥1.05** (40% weight): Core contrarian fear gauge
2. **RSI <40** (25% weight): Oversold conditions favor long entries
3. **MACD Bullish** (20% weight): Momentum confirmation for timing
4. **Above 200-MA** (15% weight): Bull market environment validation

### User Experience

- Dark/Light theme toggle
- Auto-refresh every 60 seconds
- Robust error handling with retry logic
- Optimized chart rendering (only updates when data changes)

## Strategy Logic

### Entry Signal Matrix

#### VIX/VXV Ratio (Primary Fear Gauge)

| Ratio     | Signal   | Interpretation                                      |
| --------- | -------- | --------------------------------------------------- |
| ≥1.10     | ✅ ENTRY | Extreme fear—prime contrarian opportunity (+40 pts) |
| ≥1.05     | ✅ ENTRY | High fear—strong entry signal (+35 pts)             |
| ≥1.00     | 🟢 ENTRY | Elevated fear—good opportunity (+25 pts)            |
| 0.95-1.00 | ⚪ WATCH | Moderate—monitor for development (+10 pts)          |
| <0.95     | ⚫ WAIT  | Low fear—insufficient signal (+0 pts)               |

#### RSI (Oversold Confirmation)

- **<30**: ✅ Oversold—strong entry (+30 pts)
- **30-40**: 🟢 Approaching oversold (+20 pts)
- **40-50**: ⚪ Neutral-low (+10 pts)
- **50-70**: ⚪ Neutral-high (+5 pts)
- **>70**: ⚫ Overbought—wait (+0 pts)

#### MACD (Momentum Confirmation)

- **Bullish Crossover**: ✅ Momentum confirmed (+20 pts)
- **Neutral**: ⚪ No clear momentum (+5 pts)
- **Bearish**: ⚫ Momentum against entry (+0 pts)

#### 200-Day MA (Trend Filter)

- **Above MA**: ✅ Bull trend—favorable environment (+20 pts)
- **Below MA**: ⚪ Bear trend—use caution (+5 pts)

### Example Scenarios

**✅ STRONG BUY (90/100):** Ratio 1.12 + RSI 28 + MACD Bullish + Above MA200 → 4/4 signals active  
**🟢 BUY (75/100):** Ratio 1.06 + RSI 38 + MACD Neutral + Above MA200 → 3/4 signals active  
**⚪ WATCH (50/100):** Ratio 0.97 + RSI 45 + MACD Bullish + Above MA200 → 2/4 signals active  
**⚫ WAIT (20/100):** Ratio 0.88 + RSI 72 + MACD Bearish + Above MA200 → 1/4 signals active

## Technical Specifications

### Data Sources

- **VIX**: CBOE Volatility Index (^VIX)
- **VIX3M**: CBOE 3-Month Volatility Index (^VIX3M)
- **S&P 500**: S&P 500 Index (^GSPC)

_Data provided by Yahoo Finance via yfinance library. Market data may be delayed 15-20 minutes._

### Indicator Calculations

- **RSI**: 14-period using Wilder's smoothing method
- **MACD**: 12/26-period EMA with 9-period signal line
- **200-Day MA**: Simple moving average of closing prices

## Disclaimer

**For informational and educational purposes only—not financial advice.**

This tool identifies potential long entry opportunities based on fear indicators and technical analysis. It should not be the sole basis for investment decisions. Always:

- Conduct thorough research and due diligence
- Consider your risk tolerance and investment timeline
- Consult with a qualified financial advisor
- Understand that past performance does not guarantee future results
- Use proper position sizing and risk management
- Develop your own exit strategies and stop-loss criteria

**Important**: Contrarian signals can experience significant drawdowns before reversing. Fear-driven conditions may persist or worsen. This is a market timing tool, not a complete trading system.

**Trading and investing involve substantial risk of loss.**

---

**Contrarian Edge** © 2025 — _Turning Fear Into Opportunity_
