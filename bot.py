import asyncio
from datetime import datetime
import json
import os
import pytz
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import httpx

# Токен вашего бота
TOKEN = "8975709751:AAGQrX27XnEM7TDCH_ENUOqWuuFSZQk2W0k"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список всех ваших серверов с их параметрами
SERVERS = [
    {
        "name": "🇪🇺 Обход⁴ (для видео)",
        "type": "json",
        "ping_url": "https://z7.nnmm.me",
        "data": {
            "dns": {
                "servers": ["77.88.8.8", "77.88.8.1"],
                "queryStrategy": "UseIPv4",
            },
            "routing": {
                "rules": [
                    {
                        "type": "field",
                        "protocol": ["bittorrent"],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "domain": ["domain:localhost"],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "ip": [
                            "127.0.0.0/8",
                            "169.254.0.0/16",
                            "224.0.0.0/4",
                            "213.219.212.4/32",
                            "255.255.255.255/32",
                        ],
                        "type": "field",
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "domain": [
                            "domain:rtbcdn.ru",
                            "domain:rutube.ru",
                            "domain:max.ru",
                            "domain:rutubelist.ru",
                        ],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "network": "udp,tcp",
                        "balancerTag": "Balancer",
                    },
                ],
                "balancers": [
                    {
                        "tag": "Balancer",
                        "selector": ["Auto1"],
                        "strategy": {
                            "type": "leastLoad",
                            "settings": {
                                "maxRTT": "8s",
                                "expected": 3,
                                "baselines": ["8s"],
                                "tolerance": 0.2,
                            },
                        },
                        "fallbackTag": "Fall",
                    }
                ],
                "domainMatcher": "hybrid",
                "domainStrategy": "IPIfNonMatch",
            },
            "inbounds": [
                {
                    "tag": "socks",
                    "port": 10808,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "settings": {"udp": True, "auth": "noauth"},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
                {
                    "tag": "http",
                    "port": 10809,
                    "listen": "127.0.0.1",
                    "protocol": "http",
                    "settings": {"allowTransparent": False},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
            ],
            "outbounds": [
                {
                    "tag": "Fall",
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": "176.109.87.102",
                                "port": 443,
                                "users": [
                                    {
                                        "id": "72fa03d0-dc22-4cb0-9cc7-ebd3e5bca44d",
                                        "encryption": "none",
                                        "flow": "xtls-rprx-vision",
                                    }
                                ],
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "tcpSettings": {"header": {"type": "none"}},
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "z7.nnmm.me",
                            "enableSessionResumption": False,
                            "fingerprint": "qq",
                            "alpn": ["http/1.1"],
                        },
                    },
                },
                {
                    "tag": "Auto1",
                    "protocol": "trojan",
                    "settings": {
                        "servers": [
                            {
                                "address": "zz26.tgnn.live",
                                "port": 443,
                                "password": "UrEuaLvtm_nst9j3XJKTFzA4qLjUzthU",
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "tcpSettings": {},
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "zz26.tgnn.live",
                            "enableSessionResumption": False,
                            "fingerprint": "firefox",
                            "alpn": ["http/1.1"],
                        },
                    },
                },
                {"tag": "DIRECT", "protocol": "freedom"},
                {"tag": "block", "protocol": "blackhole"},
            ],
            "burstObservatory": {
                "pingConfig": {
                    "timeout": "10s",
                    "interval": "40s",
                    "sampling": 3,
                    "httpMethod": "GET",
                    "destination": "https://www.gstatic.com/generate_204",
                    "connectivity": "",
                },
                "subjectSelector": ["Auto1"],
            },
            "remarks": "🇪🇺 Обход⁴ (для видео)",
        },
    },
    {
        "name": "🇷🇺 Обход³ 🐌 🐌 (Резерв)",
        "type": "json",
        "ping_url": "https://zz.tgnn.live",
        "data": {
            "dns": {
                "servers": ["1.1.1.1", "1.0.0.1"],
                "queryStrategy": "UseIPv4",
            },
            "routing": {
                "rules": [
                    {
                        "port": 443,
                        "type": "field",
                        "network": "udp",
                        "outboundTag": "BLOCK",
                    },
                    {
                        "type": "field",
                        "protocol": ["bittorrent"],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "domain": ["domain:localhost"],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "ip": [
                            "127.0.0.0/8",
                            "169.254.0.0/16",
                            "224.0.0.0/4",
                            "255.255.255.255/32",
                        ],
                        "type": "field",
                        "network": "tcp,udp",
                        "outboundTag": "DIRECT",
                    },
                ],
                "domainMatcher": "hybrid",
                "domainStrategy": "IPIfNonMatch",
            },
            "inbounds": [
                {
                    "tag": "socks",
                    "port": 10808,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "settings": {"udp": True, "auth": "noauth"},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
                {
                    "tag": "http",
                    "port": 10809,
                    "listen": "127.0.0.1",
                    "protocol": "http",
                    "settings": {"allowTransparent": False},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
            ],
            "outbounds": [
                {
                    "tag": "proxy",
                    "protocol": "trojan",
                    "settings": {
                        "servers": [
                            {
                                "address": "46.8.209.223",
                                "port": 443,
                                "password": "UrEuaLvtm_nst9j3XJKTFzA4qLjUzthU",
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "tcpSettings": {"header": {"type": "none"}},
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "zz.tgnn.live",
                            "enableSessionResumption": False,
                            "fingerprint": "qq",
                            "alpn": ["http/1.1"],
                        },
                    },
                },
                {"tag": "DIRECT", "protocol": "freedom"},
                {"tag": "BLOCK", "protocol": "blackhole"},
            ],
            "remarks": "🇷🇺 Обход³ 🐌 🐌 (Резерв)",
        },
    },
    {
        "name": "🇪🇺 Обход² 🐌",
        "type": "json",
        "ping_url": "https://z9.nnmm.me",
        "data": {
            "dns": {
                "servers": ["77.88.8.8", "77.88.8.1"],
                "queryStrategy": "UseIPv4",
            },
            "routing": {
                "rules": [
                    {
                        "type": "field",
                        "protocol": ["bittorrent"],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "domain": ["domain:localhost"],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "ip": [
                            "127.0.0.0/8",
                            "169.254.0.0/16",
                            "224.0.0.0/4",
                            "213.219.212.4/32",
                            "255.255.255.255/32",
                        ],
                        "type": "field",
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "domain": [
                            "domain:rtbcdn.ru",
                            "domain:rutube.ru",
                            "domain:max.ru",
                            "domain:rutubelist.ru",
                        ],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "network": "udp,tcp",
                        "balancerTag": "Balancer",
                    },
                ],
                "balancers": [
                    {
                        "tag": "Balancer",
                        "selector": ["Auto1"],
                        "strategy": {
                            "type": "leastLoad",
                            "settings": {
                                "maxRTT": "8s",
                                "expected": 1,
                                "baselines": ["8s"],
                                "tolerance": 0.2,
                            },
                        },
                        "fallbackTag": "Fall",
                    }
                ],
                "domainMatcher": "hybrid",
                "domainStrategy": "IPIfNonMatch",
            },
            "inbounds": [
                {
                    "tag": "socks",
                    "port": 10808,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "settings": {"udp": True, "auth": "noauth"},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
                {
                    "tag": "http",
                    "port": 10809,
                    "listen": "127.0.0.1",
                    "protocol": "http",
                    "settings": {"allowTransparent": False},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
            ],
            "outbounds": [
                {
                    "tag": "Fall",
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": "91.185.83.63",
                                "port": 443,
                                "users": [
                                    {
                                        "id": "72fa03d0-dc22-4cb0-9cc7-ebd3e5bca44d",
                                        "encryption": "none",
                                        "flow": "xtls-rprx-vision",
                                    }
                                ],
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "tcpSettings": {"header": {"type": "none"}},
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "z9.nnmm.me",
                            "enableSessionResumption": False,
                            "fingerprint": "qq",
                            "alpn": ["http/1.1"],
                        },
                    },
                },
                {
                    "tag": "Auto1",
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": "95.163.232.199",
                                "port": 443,
                                "users": [
                                    {
                                        "id": "72fa03d0-dc22-4cb0-9cc7-ebd3e5bca44d",
                                        "encryption": "none",
                                        "flow": "xtls-rprx-vision",
                                    }
                                ],
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "tcpSettings": {"header": {"type": "none"}},
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "z8.nnmm.me",
                            "enableSessionResumption": False,
                            "fingerprint": "random",
                            "alpn": ["http/1.1"],
                        },
                    },
                },
                {"tag": "DIRECT", "protocol": "freedom"},
                {"tag": "block", "protocol": "blackhole"},
            ],
            "burstObservatory": {
                "pingConfig": {
                    "timeout": "10s",
                    "interval": "40s",
                    "sampling": 3,
                    "httpMethod": "GET",
                    "destination": "https://www.gstatic.com/generate_204",
                    "connectivity": "",
                },
                "subjectSelector": ["Auto1"],
            },
            "remarks": "🇪🇺 Обход² 🐌",
        },
    },
    {
        "name": "🇪🇺 Обход¹",
        "type": "json",
        "ping_url": "https://de8.nnmm.me",
        "data": {
            "dns": {
                "servers": ["77.88.8.8", "77.88.8.1"],
                "queryStrategy": "UseIPv4",
            },
            "routing": {
                "rules": [
                    {
                        "type": "field",
                        "protocol": ["bittorrent"],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "domain": ["domain:localhost"],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "ip": [
                            "127.0.0.0/8",
                            "169.254.0.0/16",
                            "224.0.0.0/4",
                            "213.219.212.4/32",
                            "255.255.255.255/32",
                        ],
                        "type": "field",
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "domain": [
                            "domain:rtbcdn.ru",
                            "domain:rutube.ru",
                            "domain:max.ru",
                            "domain:rutubelist.ru",
                        ],
                        "outboundTag": "DIRECT",
                    },
                    {
                        "type": "field",
                        "network": "udp,tcp",
                        "balancerTag": "Balancer",
                    },
                ],
                "balancers": [
                    {
                        "tag": "Balancer",
                        "selector": ["Auto1"],
                        "strategy": {
                            "type": "leastLoad",
                            "settings": {
                                "maxRTT": "6s",
                                "expected": 5,
                                "baselines": ["6s"],
                                "tolerance": 0.2,
                            },
                        },
                        "fallbackTag": "Fall",
                    }
                ],
                "domainMatcher": "hybrid",
                "domainStrategy": "IPIfNonMatch",
            },
            "inbounds": [
                {
                    "tag": "socks",
                    "port": 10808,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "settings": {"udp": True, "auth": "noauth"},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
                {
                    "tag": "http",
                    "port": 10809,
                    "listen": "127.0.0.1",
                    "protocol": "http",
                    "settings": {"allowTransparent": False},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
            ],
            "outbounds": [
                {
                    "tag": "Auto1",
                    "protocol": "trojan",
                    "settings": {
                        "servers": [
                            {
                                "address": "de8.nnmm.me",
                                "port": 443,
                                "password": "UrEuaLvtm_nst9j3XJKTFzA4qLjUzthU",
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "tcpSettings": {},
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "de8.nnmm.me",
                            "enableSessionResumption": False,
                            "fingerprint": "qq",
                            "alpn": ["http/1.1"],
                        },
                    },
                },
                {
                    "tag": "Fall",
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": "213.219.212.12",
                                "port": 443,
                                "users": [
                                    {
                                        "id": "72fa03d0-dc22-4cb0-9cc7-ebd3e5bca44d",
                                        "encryption": "none",
                                        "flow": "xtls-rprx-vision",
                                    }
                                ],
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "tcpSettings": {"header": {"type": "none"}},
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "z2.nnmm.me",
                            "enableSessionResumption": False,
                            "fingerprint": "random",
                            "alpn": ["http/1.1"],
                        },
                    },
                },
                {"tag": "DIRECT", "protocol": "freedom"},
                {"tag": "block", "protocol": "blackhole"},
            ],
            "burstObservatory": {
                "pingConfig": {
                    "timeout": "6s",
                    "interval": "30s",
                    "sampling": 3,
                    "httpMethod": "GET",
                    "destination": "https://www.gstatic.com/generate_204",
                    "connectivity": "",
                },
                "subjectSelector": ["Auto1", "Fall"],
            },
            "remarks": "🇪🇺 Обход¹",
        },
    },
    {
        "name": "🌐 Белые списки 2",
        "type": "vless",
        "ping_url": "https://eh.vk.com",
        "data": (
            "vless://40795540-4829-478f-8a2c-b3a0f5db6649@importmsk.ru:443"
            "?flow=xtls-rprx-vision&encryption=none&security=reality&sni=eh.vk.com&fp=firefox&pbk=G7ahPRdtx_M8bxkIDU0hHtMbH6pn6dG91jweBVESSi0&type=tcp&headerType=none#%F0%9F%8C%90%20%D0%91%D0%B5%D0%BB%D1%8B%D0%B5%20%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%202"
        ),
    },
    {
        "name": "🇳🇱Нидерланды - БС",
        "type": "json",
        "ping_url": "https://wl2.wlrus.lol",
        "data": {
            "log": {"loglevel": "warning"},
            "dns": {"servers": ["1.1.1.1"], "queryStrategy": "UseIP"},
            "inbounds": [
                {
                    "tag": "socks",
                    "listen": "127.0.0.1",
                    "port": 10808,
                    "protocol": "socks",
                    "settings": {"auth": "noauth", "udp": True},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
                {
                    "tag": "http",
                    "listen": "127.0.0.1",
                    "port": 10809,
                    "protocol": "http",
                    "settings": {"allowTransparent": False},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
            ],
            "outbounds": [
                {
                    "tag": "🇳🇱Нидерланды - БС",
                    "remarks": "🇳🇱Нидерланды - БС",
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": "wl2.wlrus.lol",
                                "port": 443,
                                "users": [
                                    {
                                        "id": "7e7423fb-63c5-4e1d-9370-b9e8574b4ed4",
                                        "encryption": "none",
                                        "flow": "",
                                    }
                                ],
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "xhttp",
                        "xhttpSettings": {
                            "mode": "packet-up",
                            "host": "wl2.wlrus.lol",
                            "path": "/media/live/",
                            "extra": {
                                "mode": "packet-up",
                                "path": "/media/live/",
                                "xmux": {
                                    "cMaxReuseTimes": "128-256",
                                    "maxConcurrency": "8-16",
                                    "hKeepAlivePeriod": 15,
                                    "hMaxRequestTimes": "1000-2000",
                                    "hMaxReusableSecs": "1800-3600",
                                },
                                "headers": {
                                    "Accept": "*/*",
                                    "Cookie": (
                                        "session_id=dd056950878ee1b6acae099c566ffefa"
                                    ),
                                    "Origin": "https://wl2.wlrus.lol/",
                                    "Referer": "https://wl2.wlrus.lol/",
                                    "User-Agent": (
                                        "Mozilla/5.0 (Windows NT 10.0; Win64;"
                                        " x64; rv:151.0) Gecko/20100101"
                                        " Firefox/151.0"
                                    ),
                                    "Sec-Fetch-Dest": "empty",
                                    "Sec-Fetch-Mode": "cors",
                                    "Sec-Fetch-Site": "same-origin",
                                    "Accept-Language": (
                                        "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
                                    ),
                                },
                                "noSSEHeader": False,
                                "xPaddingKey": "_rnd",
                                "xPaddingBytes": "48-300",
                                "xPaddingHeader": "X-Cache",
                                "xPaddingMethod": "tokenish",
                                "uplinkHTTPMethod": "GET",
                                "xPaddingObfsMode": True,
                                "xPaddingPlacement": "queryInHeader",
                                "scMaxBufferedPosts": 512,
                                "scMaxEachPostBytes": 524288,
                                "scMaxConcurrentPosts": 2,
                                "scMinPostsIntervalMs": "50-150",
                            },
                        },
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "wl2.wlrus.lol",
                            "fingerprint": "firefox",
                            "alpn": ["h2", "http/1.1"],
                        },
                    },
                },
                {"tag": "direct", "protocol": "freedom"},
                {"tag": "block", "protocol": "blackhole"},
            ],
            "remarks": "🇳🇱Нидерланды - БС",
            "meta": {"serverDescription": "VLESS"},
        },
    },
    {
        "name": "🇳🇴Норвегия - БС",
        "type": "json",
        "ping_url": "https://wl.wlrus.lol",
        "data": {
            "log": {"loglevel": "warning"},
            "dns": {"servers": ["1.1.1.1"], "queryStrategy": "UseIP"},
            "inbounds": [
                {
                    "tag": "socks",
                    "listen": "127.0.0.1",
                    "port": 10808,
                    "protocol": "socks",
                    "settings": {"auth": "noauth", "udp": True},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
                {
                    "tag": "http",
                    "listen": "127.0.0.1",
                    "port": 10809,
                    "protocol": "http",
                    "settings": {"allowTransparent": False},
                    "sniffing": {
                        "enabled": True,
                        "routeOnly": False,
                        "destOverride": ["http", "tls", "quic"],
                    },
                },
            ],
            "outbounds": [
                {
                    "tag": "🇳🇴Норвегия - БС",
                    "remarks": "🇳🇴Норвегия - БС",
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": "wl.wlrus.lol",
                                "port": 443,
                                "users": [
                                    {
                                        "id": "7e7423fb-63c5-4e1d-9370-b9e8574b4ed4",
                                        "encryption": "none",
                                        "flow": "",
                                    }
                                ],
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "xhttp",
                        "xhttpSettings": {
                            "mode": "packet-up",
                            "host": "wl.wlrus.lol",
                            "path": "/media/live/",
                            "extra": {
                                "mode": "packet-up",
                                "path": "/media/live/",
                                "xmux": {
                                    "cMaxReuseTimes": "128-256",
                                    "maxConcurrency": "8-16",
                                    "hKeepAlivePeriod": 15,
                                    "hMaxRequestTimes": "1000-2000",
                                    "hMaxReusableSecs": "1800-3600",
                                },
                                "headers": {
                                    "Accept": "*/*",
                                    "Cookie": (
                                        "session_id=c82ad25936fa2f3776a6d0a1767d4799"
                                    ),
                                    "Origin": "https://wl.wlrus.lol/",
                                    "Referer": "https://wl.wlrus.lol/",
                                    "User-Agent": (
                                        "Mozilla/5.0 (Windows NT 10.0; Win64;"
                                        " x64; rv:151.0) Gecko/20100101"
                                        " Firefox/151.0"
                                    ),
                                    "Sec-Fetch-Dest": "empty",
                                    "Sec-Fetch-Mode": "cors",
                                    "Sec-Fetch-Site": "same-origin",
                                    "Accept-Language": (
                                        "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
                                    ),
                                },
                                "noSSEHeader": False,
                                "xPaddingKey": "_rnd",
                                "xPaddingBytes": "48-300",
                                "xPaddingHeader": "X-Cache",
                                "xPaddingMethod": "tokenish",
                                "uplinkHTTPMethod": "GET",
                                "xPaddingObfsMode": True,
                                "xPaddingPlacement": "queryInHeader",
                                "scMaxBufferedPosts": 512,
                                "scMaxEachPostBytes": 524288,
                                "scMaxConcurrentPosts": 2,
                                "scMinPostsIntervalMs": "50-150",
                            },
                        },
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "wl.wlrus.lol",
                            "fingerprint": "firefox",
                            "alpn": ["h2", "http/1.1"],
                        },
                    },
                },
                {"tag": "direct", "protocol": "freedom"},
                {"tag": "block", "protocol": "blackhole"},
            ],
            "remarks": "🇳🇴Норвегия - БС",
            "meta": {"serverDescription": "VLESS"},
        },
    },
]


def get_main_keyboard():
    """Нижняя клавиатура"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="🏓 Пинг серверов")
    builder.button(text="📦 Получить сервер")
    builder.button(text="ℹ️ О боте")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_servers_inline_keyboard(action_prefix):
    """Инлайн-клавиатура со списком серверов"""
    builder = InlineKeyboardBuilder()
    for idx, s in enumerate(SERVERS):
        builder.button(
            text=s["name"], callback_data=f"{action_prefix}_{idx}"
        )
    if action_prefix == "ping":
        builder.button(text="🌐 Пинговать все сразу", callback_data="ping_all")
    builder.adjust(1)
    return builder.as_markup()


def get_times_str():
    """Возвращает текущее время по МСК и ЕКБ"""
    tz_msk = pytz.timezone("Europe/Moscow")
    tz_ekb = pytz.timezone("Asia/Yekaterinburg")
    now = datetime.now(pytz.utc)
    time_msk = now.astimezone(tz_msk).strftime("%H:%M:%S")
    time_ekb = now.astimezone(tz_ekb).strftime("%H:%M:%S")
    return time_msk, time_ekb


async def measure_ping(url):
    """Измерение пинга до сервера (возвращает только успех/неуспех и реальный пинг)"""
    start_time = asyncio.get_event_loop().time()
    try:
        async with httpx.AsyncClient(timeout=6.0, http2=True) as client:
            response = await client.get(url)
            end_time = asyncio.get_event_loop().time()
            latency = int((end_time - start_time) * 1000)
            return True, latency
    except Exception:
        return False, 0


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 **Добро пожаловать!**\n\n"
        "Этот компактный помощник создан для управления конфигурациями и быстрой проверки доступности ваших узлов.\n"
        "Используйте удобные кнопки на клавиатуре ниже 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown",
    )


@dp.message(F.text == "ℹ️ О боте")
async def cmd_about(message: types.Message):
    await message.answer(
        "🛠 **Информация о системе:**\n\n"
        "• Статус сервиса: `🟢 Работает стабильно`\n"
        "• Платформа: `Render / Python 3.14`\n"
        "• Назначение: Мониторинг и выдача конфигов\n\n"
        "Все ноды защищены и оптимизированы под актуальные протоколы.",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown",
    )


@dp.message(F.text == "🏓 Пинг серверов")
async def menu_ping(message: types.Message):
    await message.answer(
        "🏓 Выберите сервер для проверки связи или запустите общий тест:",
        reply_markup=get_servers_inline_keyboard("ping"),
    )


@dp.message(F.text == "📦 Получить сервер")
async def menu_get_server(message: types.Message):
    await message.answer(
        "📦 Выберите нужный сервер для выгрузки конфигурации:",
        reply_markup=get_servers_inline_keyboard("get"),
    )


@dp.callback_query(F.data.startswith("ping_"))
async def callback_ping(callback: types.CallbackQuery):
    data_parts = callback.data.split("_")

    if data_parts[1] == "all":
        await callback.message.edit_text(
            "⏳ Выполняется комплексная проверка всех узлов, подождите..."
        )
        text_results = "📊 **Результаты проверки серверов:**\n\n"
        time_msk, time_ekb = get_times_str()

        for s in SERVERS:
            success, latency = await measure_ping(s["ping_url"])
            if success:
                text_results += f"✅ **{s['name']}**\n   └ Статус: `Доступен` (`{latency} ms`)\n\n"
            else:
                text_results += f"❌ **{s['name']}**\n   └ Статус: `Недоступен`\n\n"

        text_results += f"🕒 МСК: `{time_msk}` | ЕКБ: `{time_ekb}`"
        await callback.message.edit_text(text_results, parse_mode="Markdown")
    else:
        idx = int(data_parts[1])
        s = SERVERS[idx]
        await callback.message.edit_text(
            f"⏱ Проверяем узел *{s['name']}*...", parse_mode="Markdown"
        )

        success, latency = await measure_ping(s["ping_url"])
        time_msk, time_ekb = get_times_str()

        if success:
            res_text = (
                f"✅ **Сервер доступен!**\n"
                f"📌 {s['name']}\n"
                f"⏱ Задержка: `{latency} ms`\n\n"
                f"🕒 Время (МСК): `{time_msk}`\n"
                f"🕒 Время (ЕКБ): `{time_ekb}`"
            )
        else:
            res_text = (
                f"❌ **Сервер недоступен!**\n"
                f"📌 {s['name']}\n\n"
                f"🕒 Время (МСК): `{time_msk}`\n"
                f"🕒 Время (ЕКБ): `{time_ekb}`"
            )

        await callback.message.edit_text(res_text, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query(F.data.startswith("get_"))
async def callback_get_server(callback: types.CallbackQuery):
    idx = int(callback.data.split("_")[1])
    s = SERVERS[idx]
    time_msk, time_ekb = get_times_str()

    header_info = (
        f"📦 **Конфигурация сервера:**\n"
        f"📌 **{s['name']}**\n"
        f"🕒 МСК: `{time_msk}` | ЕКБ: `{time_ekb}`\n\n"
    )

    if s["type"] == "json":
        json_str = json.dumps(s["data"], ensure_ascii=False, indent=2)
        if len(json_str) > 4000:
            await callback.message.answer(header_info, parse_mode="Markdown")
            file_bytes = json_str.encode("utf-8")
            document = types.BufferedInputFile(
                file_bytes, filename=f"config_{idx+1}.json"
            )
            await callback.message.answer_document(
                document, caption="📄 Полный JSON файл конфигурации"
            )
        else:
            await callback.message.answer(
                f"{header_info}```json\n{json_str}\n```", parse_mode="Markdown"
            )
    elif s["type"] == "vless":
        await callback.message.answer(
            f"{header_info}<code>{s['data']}</code>", parse_mode="HTML"
        )

    await callback.answer()


async def main():
    print("Бот запущен и готов к работе...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
