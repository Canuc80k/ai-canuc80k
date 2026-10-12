"""Hàm ghi nguồn dùng chung cho các bộ Light 3, 4, 5 (tệp phụ, không phải một bộ câu hỏi)."""

_CBSE = {
    (10, '2025–26'): 'Curriculum26/SQP_MS_X/417_AI_SQP.pdf',
    (10, '2023–24'): 'Curriculum24/SQP_MS_X/417_AI_SQP.pdf',
    (10, '2022–23'): 'Curriculum23/SQP_MS_X/417_AI_SQP.pdf',
    (10, '2020–21'): 'Curriculum21/SQP_MS_X/417_AI_SQP.pdf',
    (12, '2022–23'): 'Curriculum23/SQP_MS_XII/843_AI_SQP.pdf',
    (12, '2025–26'): 'Curriculum26/SQP_MS_XII/843_AI_SQP.pdf',
}


def CB(grade, year, part, page, kind='Đề thi'):
    return (kind, f'CBSE Ấn Độ · Môn AI lớp {grade} · Đề mẫu {year} · Câu {part}',
            f'https://cbseacademic.nic.in/web_material/{_CBSE[(grade, year)]}#page={page}')


def HU(year, n, kind='Phỏng theo'):
    return (kind, f'AI Olympiad Hungary {year} · Vòng 1 · Câu {n}',
            f'https://github.com/hungarian-ai-olympiad/HAIO-Hungarian-AI-Olympiad/blob/main/{year}/nyari-orszagos/elmeleti/elso-fordulo.pdf')


def IA(n, page, kind='Đề thi'):
    return (kind, f'ISTQB CT-AI · Sample Exam A · Câu {n}',
            f'https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CT-AI_Sample-Exam-Questions_v1.1.pdf#page={page}')


def IG(n, page, kind='Đề thi'):
    return (kind, f'ISTQB CT-GenAI · Sample Exam A · Câu {n}',
            f'https://istqb.org/wp-content/uploads/sdm-uploads/ISTQB-CT-GenAI_Sample-Exam-A-Questions_v1.0.pdf#page={page}')


def P(n, page, kind='Đề thi'):
    return (kind, f'NOAI 2026 Singapore · Vòng sơ loại · Câu {n}',
            f'https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page={page}')


def N25(n, page, kind='Đề thi'):
    return (kind, f'NOAI 2025 Singapore · Trắc nghiệm · Câu {n}',
            f'https://learn.aisingapore.org/wp-content/uploads/2025/10/NOAI-2025-MCQ-Assessment-Questions.pdf#page={page}')


def C(exam, part, page, kind='Đề thi'):
    return (kind, f'CMU 10-601 · Exam {exam} Practice · {part}',
            f'https://www.cs.cmu.edu/~mgormley/courses/10601/handout/exam{exam}_practice_problems.pdf#page={page}')


def Q(topic, q, a, d, why, code=None, src=None):
    card = {'topic': topic, 'q': q, 'a': a, 'd': d, 'why': why}
    if code:
        card['code'] = code
    if src:
        card['src'] = src
    return card


def UW(term, n, page, kind='Đề thi'):
    label = {'24wi': 'Winter 2024', '24au': 'Autumn 2024', '25wi': 'Winter 2025'}[term]
    return (kind, f'UW CSE 446 · Midterm {label} · Câu {n}',
            f'https://courses.cs.washington.edu/courses/cse446/25sp/exams/pastexams/midterms/{term}-midterm-solutions.pdf#page={page}')


def E(year, n, kind='Đề thi'):
    return (kind, f'EPFL CS-433 · Final exam {year} · Câu {n}',
            f'https://github.com/epfml/ML_course/blob/master/exam/final-exam-{year}-solutions.pdf')


def G(year, n, page, kind='Đề thi'):
    url = {2026: 'https://gate2026.iitg.ac.in/doc/download/2026/QPs/DA.pdf', 2024: 'https://gate2026.iitg.ac.in/doc/download/2024/DA24S1.pdf'}[year]
    return (kind, f'GATE {year} Ấn Độ · Khoa học dữ liệu và AI · Câu {n}', f'{url}#page={page}')


def IA2(n, page, kind='Đề thi'):
    return (kind, f'ISTQB CT-AI 2.0 · Sample Exam A · Câu {n}',
            f'https://istqb.org/wp-content/uploads/2026/07/ISTQB_CTAI_V2.0_SampleExam-Questions-v2.2-1.pdf#page={page}')


def CA(paper, n, page, kind='Đề thi'):
    return (kind, f'AI Olympiad Canada (CAIO) · Đề luyện vòng loại 2026–27 {paper} · Câu {n}',
            f'https://www.iaiocanada.com/assets/pdfs/2026-27-caio-national-qualifier-practical-competition-{paper.lower()}.pdf#page={page}')
