"""Ghép một bộ câu hỏi từ hai tệp nguồn theo danh sách mã (tệp phụ, không phải một bộ câu hỏi).

Mã 'A07' là câu thứ 7 (đếm từ 0) của nhóm tương ứng trong tệp thứ nhất, 'B03' là câu thứ 3 trong tệp thứ hai.
pick(...) trả về đúng các câu được chọn theo thứ tự đã ghi; rest(...) trả về các câu còn lại, giữ thứ tự gốc.
"""
import importlib.util
import pathlib

_HERE = pathlib.Path(__file__).parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, _HERE / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.GROUPS


def _card(a, b, code):
    src = {'A': a, 'B': b}[code[0]]
    return src[int(code[1:])]


def pick(file_a, file_b, chosen):
    a, b = _load(file_a), _load(file_b)
    out = {}
    for g, codes in chosen.items():
        assert len(set(codes)) == len(codes), (g, codes)
        out[g] = [_card(a[g], b[g], c) for c in codes]
    return out


def rest(file_a, file_b, chosen):
    a, b = _load(file_a), _load(file_b)
    out = {}
    for g, codes in chosen.items():
        taken = set(codes)
        out[g] = [c for k, c in enumerate(a[g]) if f'A{k:02d}' not in taken] + [c for k, c in enumerate(b[g]) if f'B{k:02d}' not in taken]
    return out
