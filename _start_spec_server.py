#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""启动 spec_server，避免 Windows argv 编码损坏非 ASCII 路径。"""
import os
import sys
from pathlib import Path

# 强制 UTF-8
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

# 硬编码项目根目录（避免 argv 传递时 构 被损坏）
ROOT = r"D:\AI hub重构\home"
PORT = 8765

# 把脚本目录加入 path，import spec_server
SCRIPT_DIR = r"C:\Users\yrzhou9\.claude\skills\prototype-spec-annotator\scripts"
sys.path.insert(0, SCRIPT_DIR)

from spec_server import SpecHandler, HTTPServer
from pathlib import Path

root = Path(ROOT).resolve()
assert root.is_dir(), f"根目录不存在: {root}"
SpecHandler.root = root

server = HTTPServer(("127.0.0.1", PORT), SpecHandler)
sys.stderr.write("=" * 60 + "\n")
sys.stderr.write("Prototype Spec Annotator 本地服务\n")
sys.stderr.write(f"  根目录: {root}\n")
sys.stderr.write(f"  地址:   http://127.0.0.1:{PORT}\n")
sys.stderr.write("  保存端点: POST /save  (写入前自动备份到 history/)\n")
sys.stderr.write("  按 Ctrl+C 停止\n")
sys.stderr.write("=" * 60 + "\n")
sys.stderr.flush()
try:
    server.serve_forever()
except KeyboardInterrupt:
    sys.stderr.write("\n已停止\n")
    server.shutdown()
