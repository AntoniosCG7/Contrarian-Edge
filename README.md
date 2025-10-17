# Contrarian Edge

**A long-only contrarian market timing system that identifies fear-driven entry opportunities using VIX/VXV ratio analysis and technical indicator confirmation.**

## Overview

Contrarian Edge generates actionable BUY or WAIT signals by detecting periods of excessive market fear (elevated VIX/VXV ratio) and confirming them with technical indicators. The system exclusively focuses on identifying long entry opportunities for **S&P 500 exposure**—no short or hedge recommendations.

**Core Philosophy:** _"Buy when fear peaks, wait when complacency reigns."_

**What to Buy:** When you receive a BUY or STRONG BUY signal, consider purchasing S&P 500 ETFs such as SPY, VOO, IVV, or similar S&P 500 tracking funds.

**Holding Strategy:** Hold positions for 10-20 days or until the VIX/VIX3M ratio returns near 1.0 (indicating fear has normalized). Monitor the ratio daily and consider taking profits when it drops below 0.95 (complacency zone).

## Key Features

### Dual-Metric Signal System

- **Entry Score (0-100)**: Measures raw contrarian setup strength
- **Confidence (0-100%)**: Measures signal alignment and consistency
- **18 Intelligent Messages**: Nuanced guidance based on Entry Score vs Confidence alignment
- **Smart Decision Making**: Identifies conflicting signals vs strong alignment scenarios

### Real-Time Market Intelligence

- Live VIX, VIX3M, and S&P 500 monitoring with percentage/absolute change tracking
- 60-day VIX/VIX3M ratio trend visualization
- Visual progress bar showing current fear levels relative to historical ranges
- Enhanced signal breakdown with confidence indicators

### Technical Indicators

- **RSI (14-Day)**: Momentum analysis identifying oversold/overbought conditions
- **MACD**: Trend momentum with bullish/bearish crossover detection
- **200-Day MA**: Long-term trend validation and market regime identification

### Signal System

**Dual-metric approach** with separate Entry Score and Confidence analysis:

| Signal              | Entry Score | Confidence | Criteria                    | Interpretation                               | Action                  |
| ------------------- | ----------- | ---------- | --------------------------- | -------------------------------------------- | ----------------------- |
| ✅ **STRONG BUY**   | 85-100      | 70%+       | 3-4 entry signals active    | Extreme fear + strong technical confirmation | **Buy S&P 500 ETF**     |
| 🟢 **BUY**          | 65-84       | 60%+       | 2+ entry signals active     | Elevated fear + favorable technical setup    | **Buy S&P 500 ETF**     |
| 🟡 **MODERATE BUY** | 50-64       | 70%+       | 2+ signals + high alignment | Lower score but excellent signal alignment   | **Partial S&P 500 ETF** |
| ⚪ **WATCH**        | 40-64       | 50%+       | 1-2 signals                 | Moderate conditions—monitor for development  | Monitor                 |
| ⚫ **WAIT**         | 0-39        | <50%       | 0-1 signals                 | Insufficient entry signals—patience required | Wait                    |

#### Entry Score vs Confidence Separation

- **Entry Score (0-100)**: Measures raw contrarian setup strength
- **Confidence (0-100%)**: Measures signal alignment and consistency
- **Smart Decision Making**: High score + low confidence = conflicting signals, wait for clarity

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

### Complete Trading Strategy

**Entry:** Buy S&P 500 ETFs on BUY/STRONG BUY signals  
**Position Sizing:** Risk 1-3% of portfolio per trade (adjust based on signal strength)  
**Holding Period:** 10-20 days or until VIX/VIX3M ratio normalizes  
**Exit Signals:**

- **Take Profits:** When ratio drops below 0.95 (complacency zone)
- **Time Stop:** Exit after 20 days regardless of ratio
- **Emergency Stop:** If S&P 500 drops >8% from entry (risk management)

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

**✅ STRONG BUY (Entry: 90/100, Confidence: 85%):** Ratio 1.12 + RSI 28 + MACD Bullish + Above MA200 → 4/4 signals active → **"EXTREME FEAR + MAXIMUM CONFIDENCE - All signals aligned perfectly. Maximum allocation recommended."**

**🟢 BUY (Entry: 75/100, Confidence: 70%):** Ratio 1.06 + RSI 38 + MACD Neutral + Above MA200 → 3/4 signals active → **"ELEVATED FEAR + GOOD CONFIRMATION - Strong entry opportunity with solid technical backing."**

**🟡 MODERATE BUY (Entry: 55/100, Confidence: 80%):** Ratio 1.02 + RSI 42 + MACD Bullish + Above MA200 → 2/4 signals active → **"MODERATE SCORE + HIGH CONFIDENCE - Lower entry score but excellent signal alignment. Conservative entry with room to add on weakness."**

**⚪ WATCH (Entry: 45/100, Confidence: 75%):** Ratio 0.97 + RSI 45 + MACD Bullish + Above MA200 → 2/4 signals active → **"LOW SCORE + HIGH CONFIDENCE - Strong signal alignment but insufficient contrarian setup. Wait for fear levels to increase."**

**⚫ WAIT (Entry: 25/100, Confidence: 40%):** Ratio 0.88 + RSI 72 + MACD Bearish + Above MA200 → 1/4 signals active → **"INSUFFICIENT SETUP + MODERATE ALIGNMENT - Some signals present but insufficient for entry. Wait for better contrarian setup."**

### Intelligent Signal Messages

The system provides **18 different nuanced messages** based on Entry Score vs Confidence alignment:

#### Decision-Making Scenarios

| Entry Score | Confidence | Signal       | Message Example                                                                                                                         |
| ----------- | ---------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **85/100**  | **45%**    | WATCH        | "HIGH SCORE + MODERATE CONFIDENCE - Strong setup but some conflicting signals. Consider smaller position size."                         |
| **55/100**  | **85%**    | MODERATE BUY | "MODERATE SCORE + HIGH CONFIDENCE - Lower entry score but excellent signal alignment. Conservative entry with room to add on weakness." |
| **90/100**  | **80%**    | STRONG BUY   | "EXTREME FEAR + MAXIMUM CONFIDENCE - All signals aligned perfectly. Maximum allocation recommended."                                    |
| **45/100**  | **75%**    | WATCH        | "LOW SCORE + HIGH CONFIDENCE - Strong signal alignment but insufficient contrarian setup. Wait for fear levels to increase."            |

### Example Trade Scenario

**Day 1:** STRONG BUY signal (ratio 1.12) → Buy $10,000 of SPY at $450  
**Day 5:** Ratio drops to 1.05 → Hold (still in fear zone)  
**Day 12:** Ratio drops to 0.94 → **Take profits** (complacency zone reached)  
**Result:** SPY at $465 (+3.3% gain) + fear normalization = successful contrarian trade

**Alternative:** If ratio stays elevated >20 days, exit anyway (time stop)

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
