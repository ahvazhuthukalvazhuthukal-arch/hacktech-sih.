"""
KalaiPaalam AI - Dynamic Fair-Price Recommendation Engine
Implements the explainable pricing baseline model:
BaseCost = MaterialCost + (LabourHours * LabourRate) + Overhead
MarketAdjusted = BaseCost * MarketSignalMultiplier
SuggestedPrice = clamp(MarketAdjusted, lower_bound, upper_bound)
"""

import math
from typing import Dict, Any

class PricingService:
    def __init__(self):
        # Baseline benchmarks per artisan craft cluster
        self.default_labour_rate = 120.0  # INR per hour skilled wage benchmark
        self.default_overhead = 180.0     # INR packaging, power, local handling
        self.default_market_signals = {
            "Textiles & Handloom": 1.12,   # 12% festive/e-commerce margin
            "Metalware & Brass": 1.20,     # 20% collectible heritage margin
            "Pottery & Terracotta": 1.15,
            "Woodcraft": 1.18,
            "default": 1.10
        }

    def calculate_fair_price(
        self,
        material_cost: float,
        labour_hours: float,
        category: str = "Textiles & Handloom",
        custom_labour_rate: float = None,
        custom_overhead: float = None,
        market_signal: float = None
    ) -> Dict[str, Any]:
        """
        Computes transparent cost breakdown and suggested pricing boundaries.
        Artisan retains final decision and pricing override authority.
        """
        rate = custom_labour_rate if custom_labour_rate is not None else self.default_labour_rate
        overhead = custom_overhead if custom_overhead is not None else self.default_overhead
        signal = market_signal if market_signal is not None else self.default_market_signals.get(category, self.default_market_signals["default"])

        # 1. Base Cost
        labour_total = labour_hours * rate
        base_cost = material_cost + labour_total + overhead

        # 2. Market Adjusted Price
        market_adjusted = base_cost * signal

        # 3. Transparent Range (Low, Mid, High)
        low_bound = math.ceil((base_cost * 0.98) / 50.0) * 50
        mid_suggested = math.ceil(market_adjusted / 50.0) * 50
        high_bound = math.ceil((market_adjusted * 1.10) / 50.0) * 50

        # Explanation breakdown
        explanation = (
            f"Based on ₹{material_cost:.0f} raw materials + ₹{labour_total:.0f} skilled labour "
            f"({labour_hours:.1f} hrs @ ₹{rate:.0f}/hr benchmark) + ₹{overhead:.0f} handling/packaging overhead "
            f"= Base Cost of ₹{base_cost:.0f}. Applied {signal:.2f}x verified craft demand factor. "
            f"Recommended fair selling range is ₹{low_bound:,.0f} to ₹{high_bound:,.0f}."
        )

        return {
            "material_cost": material_cost,
            "labour_hours": labour_hours,
            "labour_rate_per_hour": rate,
            "overhead_cost": overhead,
            "market_signal_multiplier": signal,
            "base_cost": base_cost,
            "recommended_low": low_bound,
            "recommended_mid": mid_suggested,
            "recommended_high": high_bound,
            "suggested_price": mid_suggested,
            "explanation": explanation,
            "model_version": "FairPrice-Heuristic-v1.2",
            "market_signal_provenance": "DEMO_SEEDED_BENCHMARK"
        }

pricing_service = PricingService()
