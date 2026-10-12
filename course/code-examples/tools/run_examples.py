#!/usr/bin/env python3
"""Execute new lesson examples offline and verify their adjacent output fences.

Usage: python -B -X utf8 tools/run_examples.py content/phase-1/p1-01.md [--write]
Only new modules under this task's content/phase-N folders may be executed.
Each numbered example shares a namespace internally; every example starts in
a new process. A separate fresh process also executes all lesson blocks in
order. At most two execution processes can run across concurrent controllers.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import traceback
import uuid


WORK = Path(__file__).resolve().parents[1]
VERIFICATION = WORK / "verification"
RUNTIME = VERIFICATION / ".runtime"
LOCKS = VERIFICATION / ".execution-slots"
VERSION = "1.8"
ENVIRONMENT = {
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "BLIS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "PYTHONHASHSEED": "0",
    "MPLBACKEND": "Agg",
    "PYTHONIOENCODING": "utf-8",
    "HF_HUB_OFFLINE": "1",
    "TRANSFORMERS_OFFLINE": "1",
    "HF_DATASETS_OFFLINE": "1",
    "WANDB_MODE": "disabled",
}
EXAMPLE_HEADING = re.compile(r"^ {0,3}##[ \t]+Ví dụ[ \t]+(\d+)[ \t]*:[ \t]*(.*?)\s*$")
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})([^\r\n]*)[\r\n]*$")


def sha(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def atomic_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    try:
        temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        delays = (0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8)
        for attempt in range(len(delays) + 1):
            try:
                os.replace(temp, path)
                break
            except OSError as exc:
                sharing_conflict = isinstance(exc, PermissionError) or getattr(exc, "winerror", None) in {5, 32, 33}
                if not sharing_conflict or attempt == len(delays):
                    raise
                time.sleep(delays[attempt])
    finally:
        temp.unlink(missing_ok=True)


def parse_module(data: bytes) -> dict:
    text = data.decode("utf-8")
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    examples = []
    blocks = []
    fences = []
    current = None
    i = 0
    while i < len(lines):
        line = lines[i]
        heading = EXAMPLE_HEADING.match(line.rstrip("\r\n"))
        if heading:
            number = int(heading.group(1))
            if number != len(examples) + 1:
                raise ValueError(f"Example headings must be consecutively numbered from 1 (line {i + 1}).")
            current = {"number": number, "title": heading.group(2), "line": i + 1, "blocks": []}
            examples.append(current)
        elif re.match(r"^ {0,3}##[ \t]", line):
            current = None
        opener = FENCE_OPEN.match(line)
        if not opener:
            i += 1
            continue
        mark, info = opener.groups()
        language = info.strip().lower()
        closing = re.compile(r"^ {0,3}" + re.escape(mark[0]) + "{" + str(len(mark)) + r",}[ \t]*(?:\r?\n)?$")
        end = i + 1
        while end < len(lines) and not closing.match(lines[end]):
            end += 1
        if end == len(lines):
            raise ValueError(f"Unclosed fence at line {i + 1}.")
        fence = {
            "language": language,
            "start": offsets[i],
            "end": offsets[end + 1],
            "line": i + 1,
            "close_line": end + 1,
            "body": text[offsets[i + 1]:offsets[end]],
            "closing_has_eol": lines[end].endswith("\n"),
        }
        fences.append(fence)
        if language in {"python", "python3", "py"}:
            if current is None:
                raise ValueError(f"Python fence at line {i + 1} is outside a numbered '## Ví dụ N:' section.")
            block = {
                "id": len(blocks) + 1,
                "example": current["number"],
                "example_block": len(current["blocks"]) + 1,
                "line": i + 2,
                "code": fence["body"],
                "code_sha256": sha(fence["body"]),
                "fence": fence,
                "output": None,
            }
            current["blocks"].append(block)
            blocks.append(block)
        i = end + 1
    if not examples or not blocks:
        raise ValueError("The module must contain numbered examples and Python fences.")
    for example in examples:
        if not example["blocks"]:
            raise ValueError(f"Example {example['number']} has no Python code.")
    owned_outputs = set()
    for block in blocks:
        start = block["fence"]["end"]
        adjacent = next((f for f in fences if f["start"] >= start), None)
        if adjacent and adjacent["language"] == "output" and not text[start:adjacent["start"]].strip():
            block["output"] = adjacent
            owned_outputs.add(adjacent["start"])
    for fence in fences:
        if fence["language"] == "output" and fence["start"] not in owned_outputs:
            raise ValueError(f"Output fence at line {fence['line']} is not immediately adjacent to a Python fence.")
    eol = "\r\n" if b"\r\n" in data else "\n"
    return {"text": text, "examples": examples, "blocks": blocks, "eol": eol}


class ExecutionSlot:
    """Kernel file locks release automatically on crashes; no stale PID guessing."""

    def __init__(self, timeout: float):
        self.timeout = timeout
        self.handle = None
        self.index = None
        self.waited = 0.0

    def __enter__(self):
        LOCKS.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        while True:
            for index in range(2):
                path = LOCKS / f"slot-{index + 1}.lock"
                handle = path.open("a+b", buffering=0)
                if path.stat().st_size == 0:
                    handle.write(b"0")
                handle.seek(0)
                try:
                    if os.name == "nt":
                        import msvcrt
                        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except (OSError, BlockingIOError):
                    handle.close()
                    continue
                self.handle = handle
                self.index = index + 1
                self.waited = time.monotonic() - started
                return self
            if time.monotonic() - started >= self.timeout:
                raise TimeoutError(f"No execution slot became available within {self.timeout:g} seconds.")
            time.sleep(0.15)

    def __exit__(self, *_):
        if self.handle is not None:
            self.handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()


def install_offline_guard() -> dict:
    import builtins
    import socket
    policy = {"headless_pyplot_show": "Explicit no-op for pyplot.show in this headless runner; authored code remains unchanged and notebook show remains available.", "headless_pyplot_show_applied": False, "headless_pyplot_show_calls": 0}

    if os.name == "nt":
        import platform
        windows = sys.getwindowsversion()
        native_version = ".".join(map(str, windows.platform_version or windows[:3]))

        def native_windows_version(system="", release="", version="", supported_platforms=("win32", "win16", "dos")):
            if sys.platform not in supported_platforms:
                return system, release, version
            return "Microsoft", "Windows", native_version

        # Python 3.13 may fall back from WMI to a shell `ver` probe while NumPy
        # imports platform.machine(). Supply the same version through the
        # native Windows API; lesson subprocesses remain forbidden.
        platform._syscmd_ver = native_windows_version

    def denied(*_args, **_kwargs):
        raise RuntimeError("This lesson runner is offline: network connections and downloads are disabled.")

    socket.socket.connect = denied
    socket.socket.connect_ex = denied
    socket.create_connection = denied
    socket.getaddrinfo = denied

    def audit(event, _args):
        if event in {"socket.connect", "socket.getaddrinfo", "socket.sendto"}:
            denied()
        if event in {"subprocess.Popen", "os.system", "os.posix_spawn", "os.fork", "os.spawn"}:
            raise RuntimeError("Child processes are disabled so the shared two-process execution limit holds.")

    sys.addaudithook(audit)
    original_import = builtins.__import__

    def import_with_headless_show(name, globals=None, locals=None, fromlist=(), level=0):
        imported = original_import(name, globals, locals, fromlist, level)
        pyplot = sys.modules.get("matplotlib.pyplot")
        show = getattr(pyplot, "show", None)
        if show is not None and not getattr(show, "_run_examples_headless", False):
            def headless_show(*_args, **_kwargs):
                policy["headless_pyplot_show_calls"] += 1
            headless_show._run_examples_headless = True
            pyplot.show = headless_show
            policy["headless_pyplot_show_applied"] = True
        return imported

    # No Matplotlib import is performed by the controller. Patch only after
    # the lesson itself imports pyplot, including `from pyplot import show`.
    builtins.__import__ = import_with_headless_show
    return policy


def execute_program(request: dict, result_path: Path, gate_info: dict | None = None) -> int:
    result = {"status": "running", "started_utc": now(), "pid": os.getpid(), "blocks": [], **(gate_info or {})}
    atomic_json(result_path, result)
    result["runtime_policy"] = install_offline_guard()
    namespace = {"__name__": "__main__", "__file__": request["source_script"], "__package__": None, "__doc__": None, "__spec__": None, "__loader__": None, "__cached__": None}
    # One compile and one exec give the same module semantics as a downloaded
    # script. Blank source lines retain original Markdown traceback locations.
    parts = []
    cursor = 1
    for block in request["blocks"]:
        parts.append("\n" * (block["line"] - cursor))
        code = block["code"]
        if code and not code.endswith("\n"):
            code += "\n"
        parts.append(code)
        cursor = block["line"] + code.count("\n")
    try:
        compiled = compile("".join(parts), request["source"], "exec", dont_inherit=True)
    except BaseException:
        result.update({"status": "failed", "finished_utc": now(), "combined_script_compile_error": traceback.format_exc()})
        atomic_json(result_path, result)
        print(result["combined_script_compile_error"], file=sys.stderr, end="", flush=True)
        return 1

    saved_stdout = os.dup(1)
    saved_stderr = os.dup(2)
    current_index = -1
    active = None
    active_started = 0.0
    captured_out = captured_err = None

    def start_block(index):
        nonlocal current_index, active, active_started, captured_out, captured_err
        current_index = index
        block = request["blocks"][index]
        record = {key: block[key] for key in ("id", "example", "example_block", "line", "code_sha256")}
        out_path = result_path.with_name(f"{result_path.name}.block-{block['id']}.stdout")
        err_path = result_path.with_name(f"{result_path.name}.block-{block['id']}.stderr")
        record.update({"status": "running", "started_utc": now(), "stdout_path": str(out_path), "stderr_path": str(err_path), "stdout": "", "stderr": "", "stdout_sha256": sha(b""), "stderr_sha256": sha(b"")})
        result["blocks"].append(record)
        atomic_json(result_path, result)
        captured_out = out_path.open("w+b")
        captured_err = err_path.open("w+b")
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(captured_out.fileno(), 1)
        os.dup2(captured_err.fileno(), 2)
        active = record
        active_started = time.perf_counter()

    def finish_block(failed=False):
        nonlocal active, captured_out, captured_err
        if active is None:
            return
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(saved_stdout, 1)
        os.dup2(saved_stderr, 2)
        captured_out.seek(0)
        captured_err.seek(0)
        out = captured_out.read()
        err = captured_err.read()
        captured_out.close()
        captured_err.close()
        active.update({
            "status": "failed" if failed else "passed",
            "elapsed_seconds": round(time.perf_counter() - active_started, 6),
            "stdout": out.decode("utf-8"),
            "stderr": err.decode("utf-8"),
            "stdout_sha256": sha(out),
            "stderr_sha256": sha(err),
        })
        result["status"] = "failed" if failed else "running"
        atomic_json(result_path, result)
        Path(active["stdout_path"]).unlink(missing_ok=True)
        Path(active["stderr_path"]).unlink(missing_ok=True)
        active = None

    def trace_blocks(frame, event, _arg):
        if frame.f_code is not compiled:
            return None
        if event == "line":
            while current_index + 1 < len(request["blocks"]) and frame.f_lineno >= request["blocks"][current_index + 1]["line"]:
                finish_block()
                start_block(current_index + 1)
        return trace_blocks

    failed = False
    try:
        start_block(0)
        sys.settrace(trace_blocks)
        try:
            exec(compiled, namespace, namespace)
        except BaseException:
            failed = True
            traceback.print_exc()
        finally:
            sys.settrace(None)
            finish_block(failed)
        if not failed:
            while current_index + 1 < len(request["blocks"]):
                start_block(current_index + 1)
                finish_block()
    finally:
        os.dup2(saved_stdout, 1)
        os.dup2(saved_stderr, 2)
        os.close(saved_stdout)
        os.close(saved_stderr)
    result["status"] = "failed" if any(b["status"] == "failed" for b in result["blocks"]) else "passed"
    result["finished_utc"] = now()
    atomic_json(result_path, result)
    return 0 if result["status"] == "passed" else 1


def execute_child(result_path: Path) -> int:
    request = json.load(sys.stdin)
    # Compatibility for parents started before child-owned leases were added.
    if not request.get("child_owns_execution_slot"):
        return execute_program(request, result_path)
    queued = {"status": "waiting_for_execution_slot", "queued_utc": now(), "pid": os.getpid(), "blocks": []}
    atomic_json(result_path, queued)
    try:
        with ExecutionSlot(request["gate_timeout_seconds"]) as slot:
            gate_info = {"slot": slot.index, "gate_wait_seconds": round(slot.waited, 6), "execution_started_utc": now(), "slot_lease_owner": "execution child"}
            watchdog = threading.Timer(request["execution_timeout_seconds"], lambda: os._exit(124))
            watchdog.daemon = True
            watchdog.start()
            try:
                return execute_program(request, result_path, gate_info)
            finally:
                watchdog.cancel()
    except (OSError, TimeoutError) as exc:
        queued.update({"status": "controller_failure", "error": f"{type(exc).__name__}: {exc}", "finished_utc": now()})
        atomic_json(result_path, queued)
        return 1


def communicate_with_deadline(child, request_data: bytes, result_path: Path, execution_timeout: float, gate_timeout: float):
    first = True
    execution_seen = False
    deadline = time.monotonic() + gate_timeout + 5.0
    while True:
        try:
            out, err = child.communicate(request_data if first else None, timeout=0.25)
            return out, err, child.returncode == 124
        except subprocess.TimeoutExpired:
            first = False
        if not execution_seen and result_path.is_file():
            try:
                progress = json.loads(result_path.read_text(encoding="utf-8"))
                execution_start = progress.get("execution_started_utc")
                if execution_start:
                    elapsed = max(0.0, (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(execution_start)).total_seconds())
                    deadline = time.monotonic() + max(0.0, execution_timeout - elapsed)
                    execution_seen = True
            except (OSError, ValueError):
                pass
        if time.monotonic() >= deadline:
            child.kill()
            out, err = child.communicate()
            return out, err, True


def run_process(source: Path, blocks: list[dict], label: str, timeout: float, gate_timeout: float) -> dict:
    result_path = RUNTIME / f"{source.stem}-{os.getpid()}-{uuid.uuid4().hex}.json"
    request = {
        "source": str(source),
        "source_script": str(source.with_suffix(".py")),
        "blocks": [{key: b[key] for key in ("id", "example", "example_block", "line", "code", "code_sha256")} for b in blocks],
        "child_owns_execution_slot": True,
        "gate_timeout_seconds": gate_timeout,
        "execution_timeout_seconds": timeout,
    }
    record = {"label": label, "timeout_seconds": timeout, "blocks": [], "status": "failed"}
    child = None
    started = time.perf_counter()
    try:
        with contextlib.nullcontext():
            record["started_utc"] = now()
            env = os.environ.copy()
            env.update(ENVIRONMENT)
            child = subprocess.Popen(
                [sys.executable, "-B", "-u", "-X", "utf8", str(Path(__file__).resolve()), "--_child", str(result_path)],
                cwd=source.parent,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            record["pid"] = child.pid
            out, err, timed_out = communicate_with_deadline(child, json.dumps(request, ensure_ascii=False).encode("utf-8"), result_path, timeout, gate_timeout)
            if result_path.is_file():
                record.update(json.loads(result_path.read_text(encoding="utf-8")))
                for captured in record["blocks"]:
                    if captured["status"] == "running":
                        for stream in ("stdout", "stderr"):
                            partial_path = Path(captured[f"{stream}_path"])
                            partial = partial_path.read_bytes() if partial_path.is_file() else b""
                            captured[stream] = partial.decode("utf-8", errors="replace")
                            captured[f"{stream}_sha256"] = sha(partial)
                        captured["status"] = "timeout" if timed_out else "incomplete"
                        captured["capture_is_partial"] = True
            record.update({
                "returncode": child.returncode,
                "process_stdout": out.decode("utf-8", errors="replace"),
                "process_stderr": err.decode("utf-8", errors="replace"),
                "process_stdout_sha256": sha(out),
                "process_stderr_sha256": sha(err),
                "finished_utc": now(),
            })
            if timed_out:
                record["status"] = "timeout"
            elif child.returncode != 0:
                record["status"] = "failed"
            elif len(record["blocks"]) != len(blocks):
                record["status"] = "protocol_failure"
            elif record["process_stdout"]:
                record["status"] = "unattributed_stdout"
            elif record.get("status") != "passed":
                record["status"] = "protocol_failure"
    except (OSError, TimeoutError, ValueError) as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["status"] = "controller_failure"
        if child is not None and child.poll() is None:
            child.kill()
            child.communicate()
    finally:
        result_path.unlink(missing_ok=True)
        for block in blocks:
            for stream in ("stdout", "stderr"):
                result_path.with_name(f"{result_path.name}.block-{block['id']}.{stream}").unlink(missing_ok=True)
    record["elapsed_seconds_including_gate"] = round(time.perf_counter() - started, 6)
    print(f"{label}: {record['status']} ({record['elapsed_seconds_including_gate']:.2f}s total, {record.get('gate_wait_seconds', 0):.2f}s queue, slot {record.get('slot', '-')})", flush=True)
    for block in record["blocks"]:
        print(f"  block {block['id']}: stdout sha256={block['stdout_sha256']} ({len(block['stdout'].encode('utf-8'))} bytes)", flush=True)
        if block["stderr"]:
            print(f"  block {block['id']} stderr:\n{block['stderr']}", file=sys.stderr, end="" if block["stderr"].endswith("\n") else "\n", flush=True)
    if record.get("process_stderr"):
        print(record["process_stderr"], file=sys.stderr, end="" if record["process_stderr"].endswith("\n") else "\n", flush=True)
    if record.get("error"):
        print(record["error"], file=sys.stderr, flush=True)
    return record


def execute_suite(source: Path, module: dict, args, label: str) -> dict:
    isolated = [run_process(source, e["blocks"], f"{label}/example-{e['number']}", args.example_timeout, args.gate_timeout) for e in module["examples"]]
    whole = run_process(source, module["blocks"], f"{label}/whole-lesson", args.lesson_timeout, args.gate_timeout)
    issues = []
    if any(run["status"] != "passed" for run in isolated) or whole["status"] != "passed":
        issues.append("One or more executions failed.")
    isolated_blocks = {block["id"]: block for run in isolated for block in run["blocks"]}
    whole_blocks = {block["id"]: block for block in whole["blocks"]}
    for block in module["blocks"]:
        a, b = isolated_blocks.get(block["id"]), whole_blocks.get(block["id"])
        if a and b and a["stdout"] != b["stdout"]:
            issues.append(f"Block {block['id']} stdout differs between isolated example and whole lesson.")
    return {"status": "passed" if not issues else "failed", "issues": issues, "isolated": isolated, "whole_lesson": whole, "block_outputs": isolated_blocks}


def image_manifest(source: Path) -> list[dict]:
    """Only inspect this module's own id-qualified figures; never delete them."""
    figure_dir = source.parent / "fig"
    if not figure_dir.is_dir():
        return []
    images = []
    for path in sorted(figure_dir.glob(f"{source.stem}-*")):
        if path.is_file() and path.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}:
            images.append({"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path.read_bytes())})
    return images


def display_body(stdout: str) -> str:
    # A closing Markdown fence needs its own line. Receipts retain the exact
    # stdout bytes, including whether stdout had a final LF.
    normalized = stdout.replace("\r\n", "\n")
    return normalized if not normalized or normalized.endswith("\n") else normalized + "\n"


def output_issues(module: dict, suite: dict) -> list[str]:
    issues = []
    for block in module["blocks"]:
        executed = suite["block_outputs"].get(block["id"])
        if not executed:
            issues.append(f"Block {block['id']} has no captured output.")
            continue
        expected = display_body(executed["stdout"])
        actual = block["output"]["body"].replace("\r\n", "\n") if block["output"] else None
        if actual is None and expected:
            issues.append(f"Block {block['id']} is missing its adjacent output fence.")
        elif actual is not None and actual != expected:
            issues.append(f"Block {block['id']} output fence does not match captured stdout.")
    return issues


def execution_contract(module: dict) -> dict:
    return {
        "example_groups": [{"number": e["number"], "blocks": [b["id"] for b in e["blocks"]]} for e in module["examples"]],
        "blocks": [{
            "id": b["id"], "example": b["example"], "example_block": b["example_block"], "code_sha256": b["code_sha256"],
            "output_fence_sha256": sha(module["text"][b["output"]["start"]:b["output"]["end"]]) if b["output"] else None,
        } for b in module["blocks"]],
    }


def seal_prose(source: Path) -> int:
    receipt_path = VERIFICATION / f"{source.stem}.json"
    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes)
    if receipt.get("status") != "passed" or receipt.get("issues"):
        raise ValueError("A prose-only seal requires a passing execution receipt with no unresolved issues.")
    if Path(receipt["module"]).resolve() != source:
        raise ValueError("The existing receipt is bound to another source module.")
    source_bytes = source.read_bytes()
    module = parse_module(source_bytes)
    contract = execution_contract(module)
    old_groups = [{"number": e["number"], "blocks": e["blocks"]} for e in receipt["examples"]]
    if contract["example_groups"] != old_groups:
        raise ValueError("Example grouping changed; execute the module again.")
    old_blocks = [{key: b[key] for key in ("id", "example", "example_block", "code_sha256")} for b in receipt["blocks"]]
    current_blocks = [{key: b[key] for key in ("id", "example", "example_block", "code_sha256")} for b in contract["blocks"]]
    if current_blocks != old_blocks:
        raise ValueError("Executed code changed; execute the module again.")
    prior_contract = receipt.get("execution_contract") or receipt.get("prose_seal_contract")
    if prior_contract is not None and contract != prior_contract:
        raise ValueError("Code, example grouping or exact output-fence bytes changed; execute the module again.")
    suite = receipt.get("after_write_execution") or receipt["initial_execution"]
    if suite.get("status") != "passed" or suite.get("issues"):
        raise ValueError("The final execution suite is not passing.")
    if [b["id"] for b in suite["whole_lesson"]["blocks"]] != [b["id"] for b in module["blocks"]]:
        raise ValueError("Whole-lesson provenance is incomplete or out of order.")
    if len(suite["isolated"]) != len(module["examples"]):
        raise ValueError("Independent-example provenance is incomplete.")
    for run, example in zip(suite["isolated"], module["examples"]):
        if [b["id"] for b in run["blocks"]] != [b["id"] for b in example["blocks"]]:
            raise ValueError("Independent-example provenance differs from the example grouping.")
    observed = {}
    for run in [*suite["isolated"], suite["whole_lesson"]]:
        if run["status"] != "passed":
            raise ValueError("The receipt includes a failed execution.")
        for block in run["blocks"]:
            if block["status"] != "passed":
                raise ValueError("The receipt includes a failed code block.")
            for stream in ("stdout", "stderr"):
                if sha(block[stream]) != block[f"{stream}_sha256"]:
                    raise ValueError(f"Recorded {stream} hash does not match its captured bytes.")
            expected = next((b for b in module["blocks"] if b["id"] == block["id"]), None)
            if expected is None or block["code_sha256"] != expected["code_sha256"] or block["example"] != expected["example"] or block["example_block"] != expected["example_block"]:
                raise ValueError("Execution records disagree with current code/grouping.")
            if block["id"] in observed and observed[block["id"]]["stdout"] != block["stdout"]:
                raise ValueError("Recorded isolated and whole-lesson stdout disagree.")
            observed[block["id"]] = block
    if len(observed) != len(module["blocks"]):
        raise ValueError("The receipt is missing execution provenance for a block.")
    mismatches = output_issues(module, {"block_outputs": observed})
    if mismatches:
        raise ValueError("Output changed: " + "; ".join(mismatches))
    if "generated_images" in receipt and image_manifest(source) != receipt["generated_images"]:
        raise ValueError("Generated figure bytes changed; restore or execute them again.")
    new_sha = sha(source_bytes)
    execution_sha = receipt.setdefault("execution_source_sha256", receipt.get("source_after_write_sha256") or receipt["source_after_sha256"])
    previous_sha = receipt["source_after_sha256"]
    seal = {
        "sealed_utc": now(), "kind": "prose-only; no execution", "previous_source_sha256": previous_sha, "current_source_sha256": new_sha,
        "execution_source_sha256": execution_sha, "verifier_version": VERSION, "verifier_sha256": sha(Path(__file__).read_bytes()),
        "checked": ["exact code hashes", "example grouping", "recorded stdout/stderr hashes", "all output payloads", "generated figure hashes"],
        "exact_output_fence_bytes_checked": prior_contract is not None,
    }
    if prior_contract is None:
        seal["legacy_receipt_note"] = "The original receipt did not fingerprint output delimiter bytes. Output payloads match exact recorded stdout; current fence-byte fingerprints are established for subsequent seals."
    receipt.setdefault("prose_seals", []).append(seal)
    receipt["prose_seal_contract"] = contract
    receipt["source_after_sha256"] = new_sha
    if source.read_bytes() != source_bytes:
        raise RuntimeError("Source changed during prose validation; no receipt was sealed.")
    updated = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    commit_if_unchanged(receipt_path, receipt_bytes, updated)
    print(f"PROSE SEALED: {source}\nOriginal execution source sha256={execution_sha}\nCurrent source sha256={new_sha}\nReceipt: {receipt_path}\nNo execution was performed.", flush=True)
    return 0


def build_output_edits(module: dict, suite: dict) -> tuple[bytes, list[dict]]:
    eol = module["eol"]
    edits = []
    changes = []
    for block in module["blocks"]:
        stdout = suite["block_outputs"][block["id"]]["stdout"]
        body = display_body(stdout)
        existing = block["output"]
        if not body and not existing:
            continue
        longest = max((len(m.group(1)) for m in re.finditer(r"(?m)^ {0,3}(`+)", body)), default=0)
        fence = "`" * max(3, longest + 1)
        rendered = f"{fence}output{eol}" + body.replace("\n", eol) + fence
        if existing:
            if existing["closing_has_eol"]:
                rendered += eol
            start, end = existing["start"], existing["end"]
            if module["text"][start:end] == rendered:
                continue
            kind = "replaced"
        else:
            start = end = block["fence"]["end"]
            if block["fence"]["closing_has_eol"]:
                rendered = eol + rendered + eol
            else:
                rendered = eol + eol + rendered + eol
            kind = "inserted"
        edits.append((start, end, rendered))
        changes.append({"block": block["id"], "operation": kind, "stdout_sha256": sha(stdout), "stdout_bytes": len(stdout.encode("utf-8"))})
    text = module["text"]
    for start, end, rendered in sorted(edits, reverse=True):
        text = text[:start] + rendered + text[end:]
    return text.encode("utf-8"), changes


def commit_if_unchanged(source: Path, expected: bytes, replacement: bytes) -> None:
    """Compare source bytes immediately before atomic replacement; never blind-write."""
    temp = source.with_name(f".{source.name}.{os.getpid()}.{uuid.uuid4().hex}.output.tmp")
    try:
        temp.write_bytes(replacement)
        if source.read_bytes() != expected:
            raise RuntimeError("Source changed during execution; no outputs were written. Rerun against the author's latest revision.")
        os.replace(temp, source)
    finally:
        temp.unlink(missing_ok=True)


def permitted_source(argument: str) -> Path:
    source = Path(argument).resolve(strict=True)
    content = (WORK / "content").resolve()
    if not source.is_relative_to(content) or source.suffix.lower() != ".md" or not re.fullmatch(r"phase-\d+", source.parent.name) or source.parent.parent != content:
        raise ValueError(f"Only new {content}/phase-N/<id>.md modules are allowed.")
    for part in [source, source.parent, content]:
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise ValueError(f"Reparse-point source is not allowed: {part}")
    return source


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--_child":
        return execute_child(Path(sys.argv[2]))
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("module", help="New Markdown module under content/phase-N/.")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write", action="store_true", help="Insert/replace captured outputs, then run fresh verification again.")
    modes.add_argument("--seal-prose", action="store_true", help="Seal prose edits without execution after checking code/grouping/output against a passing receipt.")
    parser.add_argument("--example-timeout", type=float, default=90.0)
    parser.add_argument("--lesson-timeout", type=float, default=180.0)
    parser.add_argument("--gate-timeout", type=float, default=600.0)
    args = parser.parse_args()
    if min(args.example_timeout, args.lesson_timeout, args.gate_timeout) <= 0:
        parser.error("Timeouts must be positive.")
    if args.seal_prose:
        try:
            return seal_prose(permitted_source(args.module))
        except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
            print(f"PROSE SEAL FAILED: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
            return 1
    receipt = {
        "schema": "ai-course-code-execution-v1",
        "controller_version": VERSION,
        "controller_sha256": sha(Path(__file__).read_bytes()),
        "started_utc": now(),
        "status": "failed",
        "mode": "write-and-verify" if args.write else "verify",
        "python": {"executable": sys.executable, "version": sys.version},
        "environment": ENVIRONMENT,
        "network_policy": "Socket connections/DNS/UDP send and child process launches denied; HF offline flags set.",
        "windows_platform_probe": "platform._syscmd_ver uses sys.getwindowsversion().platform_version instead of launching shell ver; library imports keep native OS metadata without subprocesses.",
        "matplotlib_show_policy": "MPLBACKEND=Agg and an explicitly recorded pyplot.show no-op, installed lazily after lesson imports pyplot. No broad warning filter is applied; saved figure files remain on disk and are hashed.",
        "capture": "OS stdout/stderr file descriptors per block; exact UTF-8 bytes hashed and retained.",
        "output_fence_representation": "CRLF is rendered in the module's EOL style; missing stdout final LF is added only as Markdown closing-fence syntax. Raw stdout/hash remain exact in this receipt.",
        "execution_limit": {"maximum_active_children": 2, "mechanism": "msvcrt one-byte kernel file locks" if os.name == "nt" else "fcntl kernel file locks", "lease_owner": "execution child (survives a controller parent crash)", "directory": str(LOCKS)},
        "source_CAS": "Source byte comparison immediately before atomic os.replace; source hashes recorded before/after.",
        "issues": [],
    }
    receipt_path = None
    try:
        source = permitted_source(args.module)
        receipt_path = VERIFICATION / f"{source.stem}.json"
        RUNTIME.mkdir(parents=True, exist_ok=True)
        original = source.read_bytes()
        receipt.update({"module": str(source), "working_directory": str(source.parent), "source_before_sha256": sha(original)})
        receipt["images_before"] = image_manifest(source)
        module = parse_module(original)
        receipt["examples"] = [{"number": e["number"], "title": e["title"], "line": e["line"], "blocks": [b["id"] for b in e["blocks"]]} for e in module["examples"]]
        receipt["blocks"] = [{key: b[key] for key in ("id", "example", "example_block", "line", "code_sha256")} for b in module["blocks"]]
        suite = execute_suite(source, module, args, "initial")
        receipt["initial_execution"] = suite
        receipt["images_after_initial_execution"] = image_manifest(source)
        receipt["issues"].extend(suite["issues"])
        if suite["status"] != "passed":
            raise RuntimeError("Execution failed; no outputs were written.")
        if source.read_bytes() != original:
            raise RuntimeError("Source changed during execution; receipt is for the earlier snapshot. Rerun before writing or verifying.")
        if args.write:
            edited, changes = build_output_edits(module, suite)
            receipt["output_edits"] = changes
            if edited != original:
                commit_if_unchanged(source, original, edited)
            receipt["source_after_write_sha256"] = sha(edited)
            try:
                verified_module = parse_module(edited)
                after = execute_suite(source, verified_module, args, "after-write")
                receipt["after_write_execution"] = after
                receipt["images_after_write_execution"] = image_manifest(source)
                if receipt["images_after_initial_execution"] != receipt["images_after_write_execution"]:
                    receipt["issues"].append("This module's figure files differ across fresh repeated executions; remove SVG Date metadata and use a fixed hashsalt/seed.")
                receipt["issues"].extend(after["issues"])
                receipt["issues"].extend(output_issues(verified_module, after))
                for block_id, initial_output in suite["block_outputs"].items():
                    final_output = after["block_outputs"].get(block_id)
                    if final_output and final_output["stdout"] != initial_output["stdout"]:
                        receipt["issues"].append(f"Block {block_id} stdout changed across fresh repeated executions.")
                if source.read_bytes() != edited:
                    raise RuntimeError("Source changed during post-write verification. Rerun against the latest source.")
                if receipt["issues"]:
                    raise RuntimeError("Post-write output verification failed.")
            except BaseException:
                if edited != original and source.read_bytes() == edited:
                    commit_if_unchanged(source, edited, original)
                    receipt["output_edits_rolled_back"] = True
                raise
        else:
            receipt["issues"].extend(output_issues(module, suite))
        if not receipt["issues"]:
            receipt["status"] = "passed"
            receipt["execution_contract"] = execution_contract(parse_module(source.read_bytes()))
    except (OSError, ValueError, RuntimeError, UnicodeError) as exc:
        receipt["issues"].append(f"{type(exc).__name__}: {exc}")
    finally:
        receipt["finished_utc"] = now()
        if "module" in receipt:
            source = Path(receipt["module"])
            if source.is_file():
                receipt["source_after_sha256"] = sha(source.read_bytes())
                receipt["generated_images"] = image_manifest(source)
        if receipt_path is not None:
            atomic_json(receipt_path, receipt)
            print(f"Receipt: {receipt_path}", flush=True)
        for issue in receipt["issues"]:
            print(issue, file=sys.stderr, flush=True)
        print(f"RESULT: {receipt['status'].upper()}", flush=True)
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
