import logging
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional, Any

from django.core.cache import cache as default_cache
from django.core.exceptions import ImproperlyConfigured
from rest_framework.request import Request
from rest_framework.throttling import BaseThrottle

if TYPE_CHECKING:
    from rest_framework.views import APIView

from multirate_throttling import multirate_throttling_config, use_constance

logger = logging.getLogger(__name__)


@dataclass
class Rate:
    num_requests: int
    unit: str
    duration: int = field(init=False)

    duration_secs = {"s": 1, "m": 60, "h": 3_600, "d": 86_400, "w": 604_800}

    def __post_init__(self):
        self.duration = self.duration_secs[self.unit.lower()]


class MultiRateThrottle(BaseThrottle):
    cache = default_cache
    timer = time.time
    use_prefix = use_constance
    config = multirate_throttling_config
    cache_format = "throttle_%(scope)s_%(unit)s_%(ident)s"
    prefix = "THROTTLE_RATE"
    whitelist_param = "THROTTLE_RATE_WHITE_LIST"
    scope = None

    def __init__(self):
        self.ip: Optional[str] = None
        self.cache_identifier: Optional[str] = None
        self.config_name: Optional[str] = None
        self.rates_str = self.get_rates()
        self.rates = self.parse_rates(self.rates_str)

    @property
    def white_list(self) -> List[str]:
        white_list = getattr(self.config, self.whitelist_param, [])
        if isinstance(white_list, str):
            white_list = [item.strip() for item in white_list.split(",")]
        return white_list

    @property
    def rates_config(self) -> Any:
        return self.config if self.use_prefix else self.config.DEFAULT_THROTTLE_RATES

    def get_config_name(self) -> str:
        if not getattr(self, "scope", None):
            msg = (
                "You must set either `.scope` or `.rate` for '%s' throttle"
                % self.__class__.__name__
            )
            raise ImproperlyConfigured(msg)

        config_name = f"{self.prefix}_{self.scope}".upper() if self.use_prefix else self.scope
        return config_name

    def get_rates(self) -> str:
        self.config_name = self.get_config_name()
        try:
            return getattr(self.rates_config, self.config_name)
        except AttributeError:
            msg = (
                f"No default throttle rates set for '{self.scope}' scope "
                f"in config ({self.config_name})"
            )
            raise ImproperlyConfigured(msg)

    def parse_rates(self, rates_str: Optional[str]) -> List[Rate]:
        if not rates_str:
            return []

        rate_list = [rate for value in rates_str.split(",") if (rate := value.strip())]
        unique_rates = {}
        for rate in rate_list:
            try:
                num_str, period = rate.split("/")
                num_requests = int(num_str)
                unit = period[0]
                unique_rates[unit] = Rate(num_requests, unit)
            except (ValueError, IndexError, KeyError):
                logger.error(
                    f"Throttle misconfiguration: {self.scope} => "
                    f"wrong rate '{rate}' in '{rates_str}'"
                )
        rates = list(unique_rates.values())
        return rates

    def get_request_data(self, request: Request):
        self.ip = self.get_ident(request)

    def get_cache_identifier(self, request: Request) -> Optional[str]:
        return self.ip

    def get_cache_key(self, unit: str) -> Optional[str]:
        return self.cache_identifier and self.cache_format % {
            "scope": self.scope,
            "ident": self.cache_identifier,
            "unit": unit,
        }

    def process_rates(self) -> Optional[Rate]:
        now = self.timer()
        throttled = []
        for rate in self.rates:
            key = self.get_cache_key(rate.unit)
            if key is None:
                continue

            history = self.cache.get(key, [])
            while history and history[-1] <= now - rate.duration:
                history.pop()

            if len(history) < rate.num_requests:
                history.insert(0, now)
                self.cache.set(key, history, rate.duration)
            else:
                throttled.append(rate)

        max_throttled_rate = max(throttled, key=lambda r: r.duration, default=None)
        return max_throttled_rate

    def is_whitelisted(self) -> bool:
        return self.ip in self.white_list

    def allow_request(self, request: Request, view: "APIView") -> bool:
        self.get_request_data(request)

        if self.is_whitelisted():
            return self.throttle_success()

        self.cache_identifier = self.get_cache_identifier(request)
        if throttled_rate := self.process_rates():
            return self.throttle_failure(throttled_rate)

        return self.throttle_success()

    def throttle_success(self) -> bool:
        return True

    def throttle_failure(self, rate: Rate) -> bool:
        logger.warning(
            f"** THROTTLING ENABLED ** '{self.scope}': {rate.num_requests}/{rate.unit} => "
            f"{self.cache_identifier}"
        )
        return False
