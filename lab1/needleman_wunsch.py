def get_score_and_alignment(
        seq_1: str, seq_2: str, 
        match_score: int = 1,
        mismatch_penalty: int = 1,
        gap_penalty: int = -1) -> tuple[int, list[tuple[str, str]]]:
    # 1. Создадим матрицу 
    matrix = [[float('-inf') for _ in range(len(seq_1)+1)] for _ in range(len(seq_2)+1)]

    # 2. Определим штрафы
    match_score = 1
    mismatch_penalty = -1
    gap_penalty = -1

    # 3. Заполним матрицу
    # Чтобы не захламлять основной цикл, первую строчку и первый столбец заполним отдельно
    matrix[0][0] = ([], 0, None)
    for i in range(1, len(seq_2)+1):
        matrix[i][0] = ([(i-1, 0)], matrix[i-1][0][1] + gap_penalty, ["up"])
    for j in range(1, len(seq_1)+1):
        matrix[0][j] = ([(0, j-1)], matrix[0][j-1][1] + gap_penalty, ["left"])

    # теперь можно)
    for i in range(1, len(seq_2)+1):
        for j in range(1, len(seq_1)+1):
            diag_score = matrix[i-1][j-1][1] + (match_score if seq_1[j-1] == seq_2[i-1] else mismatch_penalty)
            max_score = max(matrix[i-1][j][1] + gap_penalty,
                            matrix[i][j-1][1] + gap_penalty,
                            diag_score)
            ancestors = [] # запоминаем откуда пришли
            read_ancestors = []
            if matrix[i-1][j][1] + gap_penalty == max_score:
                ancestors.append((i-1, j))
                read_ancestors.append("up")
            if matrix[i][j-1][1] + gap_penalty == max_score:
                ancestors.append((i, j-1))
                read_ancestors.append("left")
            if diag_score == max_score:
                ancestors.append((i-1, j-1))
                read_ancestors.append("diag")
                
            matrix[i][j] = (ancestors, max_score, read_ancestors)

    def get_path(i, j, seq1, seq2):
        if matrix[i][j][2] is None: # условие остановки
            return [seq1[::-1]], [seq2[::-1]]
        seqs1, seqs2 = [], []
        for ancestor, ancestor_type in zip(matrix[i][j][0], matrix[i][j][2]):
            if ancestor_type == "up":
                seq1 += "-"
                seq2 += seq_2[i-1]
            elif ancestor_type == "left":
                seq1 += seq_1[j-1]
                seq2 += "-"
            elif ancestor_type == "diag":
                seq1 += seq_1[j-1]
                seq2 += seq_2[i-1]
            paths = get_path(*ancestor, seq1, seq2)
            seqs1 += paths[0]
            seqs2 += paths[1]
        return seqs1, seqs2

    seqs1, seqs2 = get_path(len(seq_2), len(seq_1), "", "")
    return matrix[len(seq_2)][len(seq_1)][1], list(zip(seqs1, seqs2))