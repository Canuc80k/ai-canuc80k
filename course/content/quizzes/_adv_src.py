"""Hàm ghi nguồn dùng chung cho các bộ High 2, Extra 2, Max 2, Ultra 2 (tệp phụ, không phải một bộ câu hỏi).

Nguồn là (loại, nhãn, url). "Đề thi" khi giữ đúng ý và đáp án câu gốc, "Phỏng theo" khi đổi dữ kiện hoặc đổi dạng câu.
"""

_PRELIM = 'https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf'
_FINAL = 'https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf'
_USA = 'https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-{}-problems.pdf'


def Q(topic, q, a, d, why, code=None, src=None):
    card = {'topic': topic, 'q': q, 'a': a, 'd': d, 'why': why}
    if code:
        card['code'] = code
    if src:
        card['src'] = src
    return card


def CA(paper, n, page, kind='Đề thi'):
    return (kind, f'AI Olympiad Canada (CAIO) · Đề luyện vòng loại 2026–27 {paper} · Câu {n}',
            f'https://www.iaiocanada.com/assets/pdfs/2026-27-caio-national-qualifier-practical-competition-{paper.lower()}.pdf#page={page}')


def P(n, page, kind='Đề thi'):
    return (kind, f'NOAI 2026 Singapore · Vòng sơ loại · Câu {n}', f'{_PRELIM}#page={page}')


def F(n, page, kind='Đề thi'):
    return (kind, f'NOAI 2026 Singapore · Chung kết · Câu {n}', f'{_FINAL}#page={page}')


def N25(n, page, kind='Đề thi'):
    return (kind, f'NOAI 2025 Singapore · Trắc nghiệm · Câu {n}',
            f'https://learn.aisingapore.org/wp-content/uploads/2025/10/NOAI-2025-MCQ-Assessment-Questions.pdf#page={page}')


def U(round_, part, page, kind='Phỏng theo'):
    name = {'round-1': 'Vòng 1', 'round-2-day-1': 'Vòng 2 · Ngày 1', 'round-2-day-2': 'Vòng 2 · Ngày 2'}[round_]
    return (kind, f'USA-NA-AIO 2026 · {name} · {part}', f'{_USA.format(round_)}#page={page}')


def G(year, n, page, kind='Đề thi'):
    url = {2026: 'https://gate2026.iitg.ac.in/doc/download/2026/QPs/DA.pdf', 2024: 'https://gate2026.iitg.ac.in/doc/download/2024/DA24S1.pdf'}[year]
    return (kind, f'GATE {year} Ấn Độ · Khoa học dữ liệu và AI · Câu {n}', f'{url}#page={page}')


def E(year, n, kind='Đề thi'):
    return (kind, f'EPFL CS-433 · Final exam {year} · Câu {n}',
            f'https://github.com/epfml/ML_course/blob/master/exam/final-exam-{year}-solutions.pdf')


def BK(file, exam, part, page, kind='Đề thi'):
    return (kind, f'UC Berkeley CS189 · {exam} · {part}', f'https://people.eecs.berkeley.edu/~jrs/189/exam/{file}.pdf#page={page}')


def CS(n, part, page, kind='Đề thi'):
    return (kind, f'Stanford CS230 · Practice Midterm {n} · {part}', f'https://cs230.stanford.edu/section/6/Practice_{n}_Sol.pdf#page={page}')


def TO(exam, part, page, kind='Đề thi'):
    url = {'CSC411 · Midterm 2018': 'https://www.cs.toronto.edu/~guerzhoy/411_2018/doc/midterm_soln.pdf',
           'CSC321 · Midterm 2018': 'https://www.cs.toronto.edu/~rgrosse/courses/csc321_2018/exams/midterm_solutions.pdf',
           'CSC321 · Final 2018': 'https://www.cs.toronto.edu/~rgrosse/courses/csc321_2018/exams/final_solutions.pdf'}[exam]
    return (kind, f'Toronto {exam} · {part}', f'{url}#page={page}')


def UW493(part, page, kind='Đề thi'):
    return (kind, f'UW CSE 493G1 · Exam Spring 2025 · {part}',
            f'https://courses.cs.washington.edu/courses/cse493g1/exam-archive/cse493g1-25sp-exam-solutions.pdf#page={page}')


def MIT(exam, part, page, kind='Đề thi'):
    url = {'6.390 · Midterm Fall 2022': 'https://introml.mit.edu/_static/spring23/midterm/review/6390_fall_2022_midterm_solutions.pdf',
           '6.036 · Midterm Fall 2021': 'https://introml.mit.edu/_static/spring23/midterm/review/6_036_Midterm_Fall_2021_solutions.pdf',
           '6.036 · Midterm Spring 2022': 'https://introml.mit.edu/_static/spring23/midterm/review/Spring_2022_Midterm_Solutions.pdf',
           '6.036 · Midterm Fall 2019': 'https://introml.mit.edu/_static/spring23/midterm/review/midterm-fall2019-solutions.pdf'}[exam]
    return (kind, f'MIT {exam} · {part}', f'{url}#page={page}')


def C(exam, part, page, kind='Đề thi'):
    return (kind, f'CMU 10-601 · Exam {exam} Practice · {part}',
            f'https://www.cs.cmu.edu/~mgormley/courses/10601/handout/exam{exam}_practice_problems.pdf#page={page}')


_MIT867 = {
    'midterm_f01soln': ('af6e5e8e769e8e4561393320c9e93db6', 'Midterm 10/2003 (a)'),
    'midterm_f03soln': ('a5dae01d24632b23c2755e6eb7e0b4ad', 'Midterm 10/2003 (b)'),
    'midterm_f02soln': ('54259bd801ab4823d969bb836624cf59', 'Midterm 10/2002'),
    'midterm_f04soln': ('ca7a3e3f6a26bddd927fab0ea5a2d861', 'Midterm 10/2004'),
    'midterm_f06soln': ('ffb24092649a63cd06dd4c3443ae9f2a', 'Midterm 10/2006'),
    'final_f01soln': ('85d4ef5363a3445d33ca956c394beec6', 'Final 12/2001'),
    'final_f02soln': ('eb184a21ce698a4ea5c87ad77b3ea454', 'Final 12/2002'),
    'final_f03soln': ('0da3e361419509f57ef59bb4345fa2d5', 'Final 12/2003'),
    'final_f04soln': ('e49f26ee15eafbbdcba4c0f491af009e', 'Final 12/2004'),
}


def MI(file, part, page, kind='Đề thi'):
    h, label = _MIT867[file]
    return (kind, f'MIT 6.867 · {label} · {part}',
            f'https://ocw.mit.edu/courses/6-867-machine-learning-fall-2006/{h}_{file}.pdf#page={page}')
