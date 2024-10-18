import pytest
from django.core.exceptions import ImproperlyConfigured

from multirate_throttling.throttles import MultiRateThrottle, Rate


class TestRate:
    @pytest.mark.parametrize(
        "num_requests, unit, duration",
        [
            (1, "s", 1),
            (2, "s", 1),
            (3, "S", 1),
            (10, "m", 60),
            (10, "M", 60),
            (20, "h", 3_600),
            (20, "H", 3_600),
            (5, "d", 86_400),
            (6, "D", 86_400),
            (3, "w", 604_800),
            (6, "W", 604_800),
        ],
    )
    def test_init(self, num_requests, unit, duration):
        result = Rate(num_requests=num_requests, unit=unit)

        assert result.num_requests == num_requests
        assert result.unit == unit
        assert result.duration == duration == result.duration_secs[result.unit.lower()]
        assert result.duration_secs == {"s": 1, "m": 60, "h": 3_600, "d": 86_400, "w": 604_800}

    def test_init_with_wrong_unit(self):
        with pytest.raises(KeyError):
            Rate(num_requests=5, unit="X")


class TestMultiRateThrottle:
    @pytest.fixture
    def mock_rates(self, mocker):
        self.mock_get_rates = mocker.patch.object(MultiRateThrottle, "get_rates")
        self.mock_parse_rates = mocker.patch.object(MultiRateThrottle, "parse_rates")

    @pytest.mark.parametrize("is_constance_config", (True, False))
    def test_init(self, mocker, mock_rates, is_constance_config):
        test_scope = "test_scope"
        mocker.patch.object(MultiRateThrottle, "scope", test_scope)

        result = MultiRateThrottle()
        assert result.cache_format == "throttle_%(scope)s_%(unit)s_%(ident)s"
        assert result.prefix == "THROTTLE_RATE"
        assert result.scope == test_scope
        assert result.ip is None
        assert result.cache_identifier is None
        assert result.config_name is None
        assert result.rates_str == self.mock_get_rates.return_value
        assert result.rates == self.mock_parse_rates.return_value
        assert result.white_list == []
        self.mock_parse_rates.assert_called_once_with(self.mock_get_rates.return_value)

    @pytest.mark.parametrize(
        "scope, use_prefix, expected",
        (
            ("test_name", False, "test_name"),
            ("test_name", True, f"{MultiRateThrottle.prefix}_TEST_NAME"),
        ),
    )
    def test_get_config_name(self, mocker, mock_rates, scope, use_prefix, expected):
        mocker.patch.object(MultiRateThrottle, "use_prefix", use_prefix)
        mocker.patch.object(MultiRateThrottle, "scope", scope)

        result = MultiRateThrottle().get_config_name()

        assert result == expected

    @pytest.mark.parametrize("use_prefix", (True, False))
    def test_get_config_name_without_scope(self, mocker, mock_rates, use_prefix):
        mocker.patch.object(MultiRateThrottle, "use_prefix", use_prefix)

        with pytest.raises(ImproperlyConfigured):
            MultiRateThrottle().get_config_name()

    @pytest.mark.parametrize("value", ("some_rate", "other_rate, plus_one", ""))
    def test_get_rates(self, mocker, value):
        test_config_name = "test_config_name"
        test_config = mocker.Mock(**{test_config_name: value})

        mock_rates_config = mocker.patch.object(
            MultiRateThrottle,
            "rates_config",
            new_callable=mocker.PropertyMock,
            return_value=test_config,
        )
        mocker.patch.object(MultiRateThrottle, "parse_rates")
        mock_get_config_name = mocker.patch.object(
            MultiRateThrottle, "get_config_name", return_value=test_config_name
        )

        result = MultiRateThrottle()

        assert result.rates_str == value
        mock_rates_config.assert_called_once_with()
        mock_get_config_name.assert_called_once_with()

    def test_get_rates_value_not_in_config(self, mocker):
        test_config_name = "test_config_name"
        test_config = mocker.Mock(spec=[])

        mocker.patch.object(MultiRateThrottle, "config", test_config)
        mock_get_config_name = mocker.patch.object(
            MultiRateThrottle, "get_config_name", return_value=test_config_name
        )
        mock_parse_rate = mocker.patch.object(MultiRateThrottle, "parse_rates")

        with pytest.raises(ImproperlyConfigured):
            MultiRateThrottle()

        mock_get_config_name.assert_called_once_with()
        mock_parse_rate.assert_not_called()

    @pytest.mark.parametrize(
        "rate, expected",
        [
            (
                "10/day",
                [
                    Rate(num_requests=10, unit="d"),
                ],
            ),
            (
                "1/sec  ,  2/day   ",
                [Rate(num_requests=1, unit="s"), Rate(num_requests=2, unit="d")],
            ),
            (
                "2/s,4/m",
                [Rate(num_requests=2, unit="s"), Rate(num_requests=4, unit="m")],
            ),
            (
                "1/s, 2/m, 3/d, 4/w",
                [
                    Rate(num_requests=1, unit="s"),
                    Rate(num_requests=2, unit="m"),
                    Rate(num_requests=3, unit="d"),
                    Rate(num_requests=4, unit="w"),
                ],
            ),
            (
                "1/s, 2/m, 3/d,",
                [
                    Rate(num_requests=1, unit="s"),
                    Rate(num_requests=2, unit="m"),
                    Rate(num_requests=3, unit="d"),
                ],
            ),
            (
                "1/s, 2/s, 3/d, 4/d",
                [
                    Rate(num_requests=2, unit="s"),
                    Rate(num_requests=4, unit="d"),
                ],
            ),
            (",,,,", []),
            ("", []),
        ],
    )
    def test_parse_rates(self, mocker, rate, expected):
        mocker.patch.object(MultiRateThrottle, "get_rates", return_value=rate)

        throttle = MultiRateThrottle()

        assert throttle.rates == expected

    @pytest.mark.parametrize(
        "rate, expected",
        [
            ("10", []),
            ("5/", []),
            ("/", []),
            ("a/s", []),
            ("1/x", []),
            ("1/s, 10", [Rate(num_requests=1, unit="s")]),
            ("2/m, 5/", [Rate(num_requests=2, unit="m")]),
            ("3/d, /", [Rate(num_requests=3, unit="d")]),
            ("4/d, a/s", [Rate(num_requests=4, unit="d")]),
            ("a/s, 5/w, 1/x", [Rate(num_requests=5, unit="w")]),
        ],
    )
    def test_parse_rates_with_wrong_rates(self, mocker, rate, expected):
        mocker.patch.object(MultiRateThrottle, "get_rates", return_value=rate)

        throttle = MultiRateThrottle()

        assert throttle.rates == expected

    @pytest.mark.parametrize("ip", ["0.0.0.0", "1.2.3.4", None])
    def test_get_cache_identifier(self, mocker, mock_rates, ip):
        test_request = mocker.Mock()

        throttle = MultiRateThrottle()
        throttle.ip = ip

        result = throttle.get_cache_identifier(test_request)

        assert result == ip

    @pytest.mark.parametrize(
        "cache_identifier, unit",
        [
            ("0.0.0.0", "s"),
            ("xxxxxxxx", "d"),
            (None, "m"),
        ],
    )
    def test_get_cache_key(self, mock_rates, cache_identifier, unit):
        expected = cache_identifier and MultiRateThrottle.cache_format % {
            "scope": MultiRateThrottle.scope,
            "ident": cache_identifier,
            "unit": unit,
        }

        throttle = MultiRateThrottle()
        throttle.cache_identifier = cache_identifier

        result = throttle.get_cache_key(unit)

        assert result == expected

    def test_get_request_data(self, mocker, mock_rates):
        test_request = mocker.Mock()

        mock_get_ident = mocker.patch.object(MultiRateThrottle, "get_ident")

        throttle = MultiRateThrottle()
        throttle.get_request_data(test_request)

        throttle.ip = mock_get_ident.return_value

        mock_get_ident.assert_called_once_with(test_request)

    @pytest.mark.parametrize(
        "rates, history, expected_rate, expected_histories",
        [
            (
                [Rate(2, "s"), Rate(1, "m")],
                [99_950],
                Rate(1, "m"),
                ([100_000], None),
            ),
            (
                [Rate(3, "s"), Rate(2, "m"), Rate(1, "d")],
                [99_950, 99_925],
                Rate(1, "d"),
                ([100_000], [100_000, 99_950], None),
            ),
            (
                [Rate(2, "m"), Rate(2, "d")],
                [99_990, 99_980],
                Rate(2, "d"),
                (None, None),
            ),
            (
                [Rate(2, "s"), Rate(2, "d")],
                [],
                None,
                ([100_000], [100_000]),
            ),
            (
                [Rate(2, "m"), Rate(2, "w")],
                [99_995],
                None,
                ([100_000, 99_995], [100_000, 99_995]),
            ),
        ],
    )
    def test_process_rates(
        self, mocker, mock_rates, rates, history, expected_rate, expected_histories
    ):
        test_cache_keys = [f"cache_key_{rate.unit}" for rate in rates]
        mock_get_cache_key = mocker.patch.object(
            MultiRateThrottle, "get_cache_key", side_effect=test_cache_keys
        )
        mocker.patch.object(MultiRateThrottle, "timer", return_value=100_000)
        mock_cache = mocker.patch.object(MultiRateThrottle, "cache")
        mock_cache.get.side_effect = [history.copy() for _ in rates]
        self.mock_parse_rates.return_value = rates

        result = MultiRateThrottle().process_rates()

        assert result == expected_rate
        for call, rate in zip(mock_get_cache_key.call_args_list, rates):
            assert call.args == (rate.unit,)
        for call, cache_key in zip(mock_cache.get.call_args_list, test_cache_keys):
            assert call.args == (cache_key, [])

        cache_set_args = iter(call.args for call in mock_cache.set.call_args_list)
        for cache_key, rate, history in zip(test_cache_keys, rates, expected_histories):
            if history is not None:
                args = next(cache_set_args)
                assert args == (cache_key, history, rate.duration)

    def test_process_rates_without_cache_key(self, mocker, mock_rates):
        test_rate1 = Rate(num_requests=1, unit="s")
        test_rate2 = Rate(num_requests=5, unit="m")
        test_cache_key = "cache_key"

        mock_get_cache_key = mocker.patch.object(
            MultiRateThrottle, "get_cache_key", side_effect=[None, test_cache_key]
        )
        mocker.patch.object(MultiRateThrottle, "timer", return_value=100_000)
        mock_cache = mocker.patch.object(MultiRateThrottle, "cache")
        mock_cache.get.side_effect = ([99_999, 99_998], [99_999, 99_998])
        self.mock_parse_rates.return_value = [test_rate1, test_rate2]

        result = MultiRateThrottle().process_rates()

        assert result is None

        mock_get_cache_key.assert_called_with(test_rate2.unit)
        mock_cache.set.assert_called_with(
            test_cache_key, [100_000, 99_999, 99_998], test_rate2.duration
        )

    @pytest.mark.parametrize("throttled", [True, False])
    def test_allow_request(self, mocker, mock_rates, throttled):
        test_request = mocker.Mock()
        test_view = mocker.Mock()

        test_rate = Rate(0, "s")
        process_rates_result = test_rate if throttled else None

        mock_get_request_data = mocker.patch.object(MultiRateThrottle, "get_request_data")
        mock_cache_identifier = mocker.patch.object(MultiRateThrottle, "get_cache_identifier")
        mock_process_rates = mocker.patch.object(
            MultiRateThrottle, "process_rates", return_value=process_rates_result
        )
        mock_throttle_failure = mocker.patch.object(MultiRateThrottle, "throttle_failure")
        mock_throttle_success = mocker.patch.object(MultiRateThrottle, "throttle_success")

        expected = (
            mock_throttle_failure.return_value if throttled else mock_throttle_success.return_value
        )

        mock_is_white_listed = mocker.patch.object(
            MultiRateThrottle, "is_whitelisted", return_value=False
        )

        throttle = MultiRateThrottle()
        result = throttle.allow_request(test_request, test_view)

        assert result == expected

        assert throttle.cache_identifier == mock_cache_identifier.return_value
        mock_get_request_data.assert_called_once_with(test_request)
        mock_cache_identifier.assert_called_once_with(test_request)
        mock_process_rates.assert_called_once()
        if throttled:
            mock_throttle_failure.assert_called_once_with(test_rate)
        else:
            mock_throttle_success.assert_called_once()

        mock_is_white_listed.assert_called_once_with()

    def test_wait(self, mock_rates):
        assert MultiRateThrottle().wait() is None

    def test_throttled_success(self, mock_rates):
        assert MultiRateThrottle().throttle_success() is True

    def test_throttle_failure(self, mocker, mock_rates):
        test_rate = Rate(100, "m")
        test_scope = "test_scope"
        test_cache_identifier = "cache_identifier"

        mock_logger = mocker.patch("multirate_throttling.throttles.logger")

        throttle = MultiRateThrottle()
        throttle.scope = test_scope
        throttle.cache_identifier = test_cache_identifier

        assert throttle.throttle_failure(test_rate) is False

        mock_logger.warning.assert_called_once()
        log_msg = mock_logger.warning.call_args.args[0]
        assert "** THROTTLING ENABLED **" in log_msg
        assert throttle.scope in log_msg
        assert f"{test_rate.num_requests}/{test_rate.unit}" in log_msg
        assert f"{test_cache_identifier}" in log_msg

    @pytest.mark.parametrize("is_whitelisted", [True, False])
    def test_allow_request_return_true_if_is_whitelisted(self, mocker, mock_rates, is_whitelisted):
        test_request = mocker.Mock()
        test_view = mocker.Mock()

        mocker.patch.object(MultiRateThrottle, "is_whitelisted", return_value=is_whitelisted)
        mock_process_rates = mocker.patch.object(
            MultiRateThrottle, "process_rates", return_value=False
        )
        throttle = MultiRateThrottle()
        throttle.get_ident = mocker.Mock(return_value="some_ident")
        assert throttle.allow_request(test_request, test_view)
        (
            mock_process_rates.assert_called_once()
            if not is_whitelisted
            else mock_process_rates.assert_not_called()
        )

    def test_is_whitelisted(self, mocker, mock_rates):
        test_ip = "127.0.0.1"
        mocker.patch.object(
            MultiRateThrottle,
            "white_list",
            new_callable=mocker.PropertyMock,
            return_value=[test_ip],
        )
        throttle = MultiRateThrottle()
        throttle.ip = test_ip
        assert throttle.is_whitelisted()

    def test_is_whitelisted_false(self, mocker, mock_rates):
        test_ip = "127.0.0.1"
        unknown_ip = "127.0.0.2"
        mocker.patch.object(
            MultiRateThrottle,
            "white_list",
            new_callable=mocker.PropertyMock,
            return_value=[test_ip],
        )
        throttle = MultiRateThrottle()
        throttle.ip = unknown_ip
        assert not throttle.is_whitelisted()

    def test_rates_config_no_prefix(self, mocker):
        test_config = mocker.Mock(DEFAULT_THROTTLE_RATES=mocker.Mock(test_scope="1/s, 2/m, 3/d"))
        MultiRateThrottle.use_prefix = False
        MultiRateThrottle.config = test_config
        MultiRateThrottle.scope = "test_scope"
        throttle = MultiRateThrottle()
        assert throttle.rates_config == test_config.DEFAULT_THROTTLE_RATES

    def test_rates_config_with_prefix(self, mocker):
        test_config = mocker.Mock(THROTTLE_RATE_TEST_SCOPE="1/s, 2/m, 3/d")
        MultiRateThrottle.use_prefix = True
        MultiRateThrottle.config = test_config
        MultiRateThrottle.scope = "test_scope"
        throttle = MultiRateThrottle()
        assert throttle.rates_config == test_config

    @pytest.mark.parametrize(
        "white_list_value, expected_white_list",
        [
            (["a", "b", "c"], ["a", "b", "c"]),
            ("x,y,z", ["x", "y", "z"]),
            ("a , b", ["a", "b"]),
            ("x", ["x"]),
            ([], []),
        ],
    )
    def test_white_list(self, mocker, mock_rates, white_list_value, expected_white_list):
        test_white_list_value = white_list_value
        test_config = mocker.Mock(**{MultiRateThrottle.whitelist_param: test_white_list_value})
        MultiRateThrottle.config = test_config
        MultiRateThrottle.scope = "test_scope"
        throttle = MultiRateThrottle()
        assert throttle.white_list == expected_white_list
