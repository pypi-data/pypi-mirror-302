"""
ע�����
1. ȷ��ĳ����λ��Ϊ0ʱ�����ʱ����Ϊ0������ignore�������ignore��������������λ�ƺ���������
2. Kx�Ĵ�С������Чλ�Ʊ�ŵ����ֵ
3. ��������F��FD��С��ͬ��FD�Ĵ�Сȡ�����Ƿ����ĳ�����������Ե������FD��СΪ6*1��i�˺�j�ˣ�
"""
import sympy as sp
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve, lsqr
import contextlib
import io

output_buffer = io.StringIO()


def expand_matrix_(matrix):
    """
    չ��������ÿ��Ԫ�ص��Ҳ���·����㡣

    ����:
    matrix (sympy.Matrix): ����ľ���

    ����:
    sympy.Matrix: ��չ��ľ���
    """
    # ��ȡԭʼ���������������
    rows, cols = matrix.shape

    # ����һ����СΪ (2*rows, 2*cols) �������
    expanded_matrix = sp.zeros(rows * 2, cols * 2)

    # ��ԭ�����Ԫ�ط����¾�����ʵ�λ��
    for i in range(rows):
        for j in range(cols):
            expanded_matrix[i * 2, j * 2] = matrix[i, j]

    return expanded_matrix


def colculate_k_e_(unit_num, unit_le, unit_EA, unit_EI, set_zeros_FN=False, set_zeros_Fs=False, set_zeros_M=False,
                   ignore_x=False, ignore_y=False, ignore_beta=False,
                   expand_matrix=False, reverse_M=False):
    """
    ���㵥Ԫ�ľֲ�����ϵ�µĸնȾ���
    """
    all_k_e = []
    for i in range(unit_num):
        k_e = sp.Matrix([
            [unit_EA[i] / unit_le[i], 0, 0, -unit_EA[i] / unit_le[i], 0, 0],
            [0, 12 * unit_EI[i] / unit_le[i] ** 3, 6 * unit_EI[i] / unit_le[i] ** 2, 0,
             -12 * unit_EI[i] / unit_le[i] ** 3,
             6 * unit_EI[i] / unit_le[i] ** 2],
            [0, 6 * unit_EI[i] / unit_le[i] ** 2, 4 * unit_EI[i] / unit_le[i], 0, -6 * unit_EI[i] / unit_le[i] ** 2,
             2 * unit_EI[i] / unit_le[i]],
            [-unit_EA[i] / unit_le[i], 0, 0, unit_EA[i] / unit_le[i], 0, 0],
            [0, -12 * unit_EI[i] / unit_le[i] ** 3, -6 * unit_EI[i] / unit_le[i] ** 2, 0,
             12 * unit_EI[i] / unit_le[i] ** 3,
             -6 * unit_EI[i] / unit_le[i] ** 2],
            [0, 6 * unit_EI[i] / unit_le[i] ** 2, 2 * unit_EI[i] / unit_le[i], 0, -6 * unit_EI[i] / unit_le[i] ** 2,
             4 * unit_EI[i] / unit_le[i]],
        ])
        # �����������
        if reverse_M:
            k_e[2, :] = -k_e[2, :]  # ��תM
            k_e[5, :] = -k_e[5, :]  # ��תM
        zero_row = sp.zeros(1, 6)
        if set_zeros_FN:
            # ��һ�к͵���������
            k_e[0, :] = zero_row
            k_e[3, :] = zero_row
        if set_zeros_Fs:
            k_e[1, :] = zero_row
            k_e[4, :] = zero_row
        if set_zeros_M:
            k_e[2, :] = zero_row
            k_e[5, :] = zero_row
        del_idx = []
        if ignore_x:
            del_idx.append(0)  # ��һ�к͵�һ��
            del_idx.append(3)
        if ignore_y:
            del_idx.append(1)
            del_idx.append(4)  # �ڶ��к͵ڶ���
        if ignore_beta:
            del_idx.append(2)  # �����к͵�����
            del_idx.append(5)

        # ��ԭ��������ȡʣ�µ��к��У��γ��µľ���
        need_idx = list(set(range(6)) - set(del_idx))
        k_e = k_e.extract(need_idx, need_idx)
        if expand_matrix:
            k_e = expand_matrix_(k_e)

        all_k_e.append(k_e)
        try:
            print(f"��Ԫ{i + 1}�ֲ��նȾ���Ϊ��\n{np.array(k_e).astype(float)}")
        except:
            print(f"��Ԫ{i + 1}�ֲ��նȾ���Ϊ��\n{np.array(k_e)}")
    return all_k_e


def colculate_Te(unit_num, alphas, ignore_x=False, ignore_y=False, ignore_beta=False, expand_matrix=False):
    """
    ����ת������
    """
    all_Te = []
    for i in range(unit_num):
        Te = sp.Matrix([
            [sp.cos(alphas[i]), sp.sin(alphas[i]), 0, 0, 0, 0],
            [-sp.sin(alphas[i]), sp.cos(alphas[i]), 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, sp.cos(alphas[i]), sp.sin(alphas[i]), 0],
            [0, 0, 0, -sp.sin(alphas[i]), sp.cos(alphas[i]), 0],
            [0, 0, 0, 0, 0, 1]
        ])
        del_idx = []
        if ignore_x:
            del_idx.append(0)  # ��һ�к͵�һ��
            del_idx.append(3)
        if ignore_y and not expand_matrix:
            del_idx.append(1)
            del_idx.append(4)  # �ڶ��к͵ڶ���
        if ignore_beta:
            del_idx.append(2)  # �����к͵�����
            del_idx.append(5)
        need_idx = list(set(range(6)) - set(del_idx))
        Te = Te.extract(need_idx, need_idx)
        all_Te.append(Te)
        try:
            print(f"��Ԫ{i + 1}��ת������Ϊ��\n{np.array(Te).astype(float)}")
        except:
            print(f"��Ԫ{i + 1}��ת������Ϊ��\n{np.array(Te)}")
    return all_Te


def colculate_ke(all_k_e, all_Te):
    """
    ����ȫ�ֵ�Ԫ�նȾ���
    """
    all_ke = []
    for i in range(len(all_k_e)):
        ke = all_Te[i].T * all_k_e[i] * all_Te[i]
        all_ke.append(ke)
        try:
            print(f"��Ԫ{i + 1}ȫ�ָնȾ���Ϊ��\n{np.array(ke).astype(float)}")
        except:
            print(f"��Ԫ{i + 1}ȫ�ָնȾ���Ϊ��\n{np.array(ke)}")
    return all_ke


def generate_lambda(all_lambda_str):
    """
    ���ɦ�ָʾ����
    """
    from yyyutils.data_structure_utils import StringUtils
    all_lambda_matrix = sp.Matrix(StringUtils.transform_input_to_t_list(all_lambda_str, " ", ","))
    try:
        print(f"���е�Ԫ�Ķ�λ����Ϊ��\n{np.array(all_lambda_matrix).astype(int)}")
    except:
        print(f"���е�Ԫ�Ķ�λ����Ϊ��\n{np.array(all_lambda_matrix)}")
    return all_lambda_matrix


def colculate_kx(all_ke, all_lambda):
    """
    ����ȫ�ֽṹ�նȾ���
    """
    # �ҵ�all_lambda�е����ֵ����size
    size = int(numeric_matrix_max(all_lambda))
    kx = sp.zeros(size, size)
    for i in range(1, kx.shape[0] + 1):
        for j in range(1, kx.shape[1] + 1):
            for k in range(len(all_ke)):
                lambda_k = all_lambda[k, :]
                kei = [idx for idx, val in enumerate(lambda_k) if val == i]
                kej = [idx for idx, val in enumerate(lambda_k) if val == j]
                if kei and kej:
                    for l in range(len(kei)):
                        for m in range(len(kej)):
                            kx[i - 1, j - 1] += all_ke[k][kei[l], kej[m]]
    try:
        print(f"ȫ�ֽṹ�նȾ���Ϊ��\n{np.array(kx).astype(float)}")
    except:
        print(f"ȫ�ֽṹ�նȾ���Ϊ��\n{np.array(kx)}")
    return kx


def colculate_F_Fe(unit_num, Fs, qs, ignore_x=False, ignore_y=False, ignore_beta=False, expand_matrix=False,
                   reverse_M=False):
    """
    �������Ԫ�ھֲ�����ϵ�µĹ̶���
    """
    all_F_Fe = []
    for i in range(unit_num):
        F = Fs[i]
        q = qs[i]
        Fsi1 = Mi1 = Fsj1 = Mj1 = Fsi2 = Mi2 = Fsj2 = Mj2 = sp.S(0)
        if F is not None:
            Fsi1 = F[0] * F[2] ** 2 * (3 * F[1] + F[2]) / (F[1] + F[2]) ** 3
            Mi1 = F[0] * F[1] * F[2] ** 2 / (F[1] + F[2]) ** 2
            Fsj1 = F[0] * F[1] ** 2 * (F[1] + 3 * F[2]) / (F[1] + F[2]) ** 3
            Mj1 = -F[0] * F[1] ** 2 * F[2] / (F[1] + F[2]) ** 2
        if q is not None:
            Fsi2 = q[0] * q[1] / (2 * q[2] ** 3) * (2 * q[2] ** 3 - 2 * q[2] * q[1] ** 2 + q[1] ** 3)
            Mi2 = q[0] * q[1] ** 2 / (12 * q[2] ** 2) * (6 * q[2] ** 2 - 8 * q[2] * q[1] + 3 * q[1] ** 2)
            Fsj2 = q[0] * q[1] ** 3 / (2 * q[2] ** 3) * (2 * q[2] - q[1])
            Mj2 = -q[0] * q[1] ** 3 / (12 * q[2] ** 2) * (4 * q[2] - 3 * q[1])
        if reverse_M:
            Mi1, Mj1, Mi2, Mj2 = -Mi1, -Mj1, -Mi2, -Mj2
        F_Fe = sp.Matrix([0, Fsi1 + Fsi2, Mi1 + Mi2, 0, Fsj1 + Fsj2, Mj1 + Mj2])

        del_idx = []
        if ignore_x:
            del_idx.append(0)
            del_idx.append(3)
        if ignore_y and not expand_matrix:
            del_idx.append(1)
            del_idx.append(4)
        if ignore_beta:
            del_idx.append(2)
            del_idx.append(5)
        need_idx = list(set(range(6)) - set(del_idx))
        F_Fe = F_Fe.extract(need_idx, [0])
        all_F_Fe.append(F_Fe)
        try:
            print(f"��Ԫ{i + 1}�ľֲ��̶���Ϊ��\n{np.array(F_Fe).astype(float)}")
        except:
            print(f"��Ԫ{i + 1}�ľֲ��̶���Ϊ��\n{np.array(F_Fe)}")
    return all_F_Fe


def colculate_FFe(all_F_Fe, all_Te):
    """
    ���㵥Ԫȫ�̶ֹ���
    """
    all_FFe = []
    for i in range(len(all_Te)):
        FFe = all_Te[i].T * all_F_Fe[i]

        all_FFe.append(FFe)
        try:
            print(f"��Ԫ{i + 1}��ȫ�̶ֹ���Ϊ��\n{np.array(FFe).astype(float)}")
        except:
            print(f"��Ԫ{i + 1}��ȫ�̶ֹ���Ϊ��\n{np.array(FFe)}")
    return all_FFe


def coculate_FE(all_FFe, all_lambda):
    """
    �����Ч�ڵ����
    """
    non_zero_elements = [x for x in all_lambda if x != 0]
    unique_non_zero_elements = sorted(set(non_zero_elements))
    print(f"���нڵ��0���Ϊ��\n{np.array(unique_non_zero_elements)}")
    FE = sp.zeros(len(unique_non_zero_elements), 1)
    for i in range(1, len(unique_non_zero_elements) + 1):
        for j in range(all_lambda.shape[0]):
            k = [idx for idx, val in enumerate(all_lambda[j, :]) if val == i]
            if k:
                FE[i - 1] += all_FFe[j][k[0]]
    FE = -FE
    try:
        print(f"��Ч�ڵ����Ϊ��\n{np.array(FE).astype(float)}")
    except:
        print(f"��Ч�ڵ����Ϊ��\n{np.array(FE)}")
    return FE


def coculate_F(FE, FD):
    """
    ������ڵ���ۺϽڵ����
    """
    F = FE + FD
    try:
        print(f"���ڵ��ۺϽڵ����Ϊ��\n{np.array(F).astype(float)}")
    except:
        print(f"���ڵ��ۺϽڵ����Ϊ��\n{np.array(F)}")
    return F


def solve_equation(K, F):
    if isinstance(K, sp.Matrix) or isinstance(F, sp.Matrix) or any(isinstance(elem, sp.Expr) for elem in K.flat) or any(
            isinstance(elem, sp.Expr) for elem in F.flat):
        return solve_symbolic(K, F)
    else:
        return solve_numeric(K, F)


def solve_symbolic(K, F):
    K = sp.Matrix(K)
    F = sp.Matrix(F)

    try:
        # ����ʹ�� SymPy �����Է��������
        X = K.solve(F)
    except sp.matrices.exceptions.NonInvertibleMatrixError:
        # ����������죬����ʹ�ù����棨Moore-Penrose α�棩
        K_pinv = K.pinv()
        X = K_pinv * F
        print("���棺�������죬ʹ�ù�������⡣������ܲ���Ψһ�⡣")

    return X


def solve_numeric(K, F):
    K = np.array(K, dtype=float)
    F = np.array(F, dtype=float).ravel()

    K_sparse = sparse.csc_matrix(K)

    try:
        # ����ʹ�� spsolve
        X = spsolve(K_sparse, F)
    except sparse.linalg.MatrixRankWarning:
        # ��� spsolve ʧ�ܣ�ʹ����С���˷����
        X, _, _, _ = lsqr(K_sparse, F)[:4]
        print("���棺����������죬ʹ����С���˷���⡣������ܲ���Ψһ�⡣")

    return X


def calculate_delta(F, kx):
    """
    ����λ��
    """
    print("��ʼ����λ��")
    delta = solve_equation(kx, F)
    try:
        print(f"���ڵ�λ��Ϊ��\n{np.array(delta).astype(float)}")
    except:
        print(f"���ڵ�λ��Ϊ��\n{np.array(delta)}")
    return delta


def coculate_F_(all_F_Fe, all_Te, all_ke, X, all_lambda, reverse_M=False):
    """
    �������Ԫ�˶���
    """
    all_F_ = []
    for i in range(len(all_F_Fe)):
        lambda_i = all_lambda[i, :]
        res = sp.zeros(len(lambda_i), 1)
        for j in range(len(lambda_i)):
            if lambda_i[j] != 0:
                res[j] = X[lambda_i[j] - 1]
        print(all_F_Fe[i])
        print(all_Te[i] * all_ke[i] * res)
        F_ = all_F_Fe[i] + all_Te[i] * all_ke[i] * res
        # if reverse_M:
        #     print("���棺ʹ��reverse_Mѡ�ֻ�ܱ�֤�ֲ�����ϵ�µĸ˶�������ȷ�ԣ�ǰ��Ľ�����ܲ�׼ȷ��")
        #     temp = F_.shape[0] // 2
        #     F_[temp - 1, :] = -F_[temp - 1, :]
        #     F_[2 * temp - 1, :] = -F_[2 * temp - 1, :]

        all_F_.append(F_)
        try:
            print(f"��Ԫ{i + 1}�ĸ˶���Ϊ��\n{np.array(F_).astype(float)}")
        except:
            print(f"��Ԫ{i + 1}�ĸ˶���Ϊ��\n{np.array(F_)}")
    return all_F_


def numeric_matrix_max(matrix):
    return np.max(np.array(matrix.tolist()).astype(float))


def main(unit_num, unit_le, unit_EA, unit_EI, alphas, all_lambda_str, subs_token, FD=None, Fs=None, qs=None,
         sub_dict=None,
         set_zeros_FN=False,
         set_zeros_Fs=False,
         set_zeros_M=False,
         ignore_x=False,
         ignore_y=False,
         ignore_beta=False,
         expand_matrix=False,
         coculate_X_F_forced=False, reverse_M=False):
    """
    ������
    :param unit_num: ��Ԫ����
    :param unit_le: ��Ԫ���Ȳ���
    :param unit_EA: ��ԪEA����
    :param unit_EI: ��ԪEI����
    :param alphas: ��Ԫ��X��нǲ���
    :param all_lambda_matrix: ָʾ����
    :param subs_token: �Ƿ��Ѿ��滻���ű���
    :param FD: �ڵ���ȫ������ϵ�µ�ֱ�Ӻ��ز���
    :param Fs: ��Ԫ����������
    :param qs: ��Ԫ�������ز���
    :param sub_dict: ���ű����滻�ֵ�
    :param set_zeros_FN: �Ƿ񲻿���������ע�⣬��������Ƿ񲻿���x����λ�ƣ�
    :param set_zeros_Fs: �Ƿ񲻿��Ǽ�����ע�⣬��������Ƿ񲻿���y����λ�ƣ�
    :param set_zeros_M: �Ƿ񲻿�����أ�ע�⣬��������Ƿ񲻿��Ǧ·���ת�ǣ�
    :param ignore_x: �Ƿ���������ͼ��䷽���λ��
    :param ignore_y: �Ƿ���Լ����ͼ��䷽���λ��
    :param ignore_beta: �Ƿ������غͼ��䷽���ת��
    :param expand_matrix:
    :return:
    """
    U_EA = [unit_EA[0]] * unit_num
    U_EI = [unit_EI[0]] * unit_num
    U_L = [unit_le[0]] * unit_num
    U_Fs = [None] * unit_num
    U_qs = [None] * unit_num
    all_lambda_matrix = generate_lambda(all_lambda_str)
    U_FD = sp.zeros(int(numeric_matrix_max(all_lambda_matrix)), 1)
    if FD is not None:
        for i in range(len(FD)):
            U_FD[FD[i][0] - 1] = FD[i][1]
    if Fs is not None:
        for i in range(len(Fs)):
            U_Fs[Fs[i][0] - 1] = Fs[i][1]
    if qs is not None:
        for i in range(len(qs)):
            U_qs[qs[i][0] - 1] = qs[i][1]
    print(U_FD)
    if len(unit_le) == 2:
        for item in unit_le[1]:
            U_L[item[0] - 1] = item[1]
    elif len(unit_le) != 1:
        print("��Ԫ���Ȳ��������������顣")
    if len(unit_EA) == 2:
        for item in unit_EA[1]:
            U_EA[item[0] - 1] = item[1]
    elif len(unit_EA) != 1:
        print("EA���������������顣")
    if len(unit_EI) == 2:
        for item in unit_EI[1]:
            U_EI[item[0] - 1] = item[1]
    elif len(unit_EI) != 1:
        print("EI���������������顣")
    print(f"��Ԫ���Ȳ���Ϊ��{U_L}")
    print(f"��ԪEA����Ϊ��{U_EA}")
    print(f"��ԪEI����Ϊ��{U_EI}")
    print(f"��Ԫ��X��нǲ���Ϊ��{alphas}")
    print(f"��Ԫ����������Ϊ��{U_Fs}")
    print(f"��Ԫ�������ز���Ϊ��{U_qs}")
    print(f"�ڵ�ֱ�Ӻ��ز���Ϊ��{U_FD}")

    print()
    all_k_e = colculate_k_e_(unit_num, U_L, U_EA, U_EI, set_zeros_FN, set_zeros_Fs, set_zeros_M, ignore_x, ignore_y,
                             ignore_beta, expand_matrix, reverse_M)
    all_Te = colculate_Te(unit_num, alphas, ignore_x, ignore_y, ignore_beta, expand_matrix)
    all_ke = colculate_ke(all_k_e, all_Te)
    kx = colculate_kx(all_ke, all_lambda_matrix)
    all_F_Fe = colculate_F_Fe(unit_num, U_Fs, U_qs, ignore_x, ignore_y, ignore_beta, expand_matrix,
                              reverse_M)  # �Ե�ԪΪ���㵥λ
    all_FFe = colculate_FFe(all_F_Fe, all_Te)
    FE = coculate_FE(all_FFe, all_lambda_matrix)  # �Խڵ�Ϊ���㵥λ
    F = coculate_F(FE, U_FD)  # �Ը�Ϊ���㵥λ
    if subs_token:
        X = calculate_delta(F, kx)  # ʹ���µĺ�����
        if X is not None:
            all_F_ = coculate_F_(all_F_Fe, all_Te, all_ke, X, all_lambda_matrix)
        else:
            print("�޷�����˶�������Ϊλ�Ƽ���ʧ�ܡ�")
    else:
        if coculate_X_F_forced:
            X = calculate_delta(F, kx)  # ʹ���µĺ�����
            if X is not None:
                all_F_ = coculate_F_(all_F_Fe, all_Te, all_ke, X, all_lambda_matrix)
            else:
                print("�޷�����˶�������Ϊλ�Ƽ���ʧ�ܡ�")
        else:
            print("����û���滻���ű������޷�������ڵ�λ�ƺ͸˶�����")

    print()


def subs_(subs_dict):
    """
    ���ֵ�������з��ű��������滻
    :param subs_dict: �������ű�������ֵ���ֵ�
    :return: �滻����ֵ�
    """
    global subs_token

    updated = True
    while updated:
        updated = False
        for key, value in subs_dict.items():
            if isinstance(value, sp.Expr):
                new_value = value.subs(subs_dict)
                if new_value != value:
                    subs_dict[key] = new_value
                    updated = True

    # ����ȫ�ֱ���
    globals().update({str(key): value for key, value in subs_dict.items()})
    subs_token = True


if __name__ == '__main__':
    # ���峣��
    INV = 1e20
    PI = sp.pi
    subs_token = False
    # ����������Ҫ�ķ��ű���
    EA, EA1, EA2, EA3, EI, EI1, EI2, EI3 = sp.symbols('EA EA1 EA2 EA3 EI EI1 EI2 EI3')
    L, L1, L2, L3, alpha1, alpha2, alpha3, alpha4, alpha5, alpha6 = sp.symbols(
        'L L1 L2 L3 alpha1 alpha2 alpha3 alpha4 alpha5 alpha6')
    F1, F2, F3, F4, F5, F6, a1, b1, a2, b2, a3, b3, a4, b4, a5, b5, a6, b6 = sp.symbols(
        'F1 F2 F3 F4 F5 F6 a1 b1 a2 b2 a3 b3 a4 b4 a5 b5 a6 b6')
    q2, l2, q1, l1, q3, l3, q4, l4, q5, l5, q6, l6 = sp.symbols('q2 l2 q1 l1 q3 l3 q4 l4 q5 l5 q6 l6')
    FD1, FD2, FD3, FD4, FD5, FD6 = sp.symbols('FD1 FD2 FD3 FD4 FD5 FD6')

    # sub_dict = {
    #     alpha1: 0, alpha2: PI / 2, alpha3: PI / 2, alpha4: -PI / 2, alpha5: -PI / 2, EA: mmax
    # }
    sub_dict = {
        EA: EA, EA1: EA1, EA2: EA2, EA3: EA3,
        EI: EI, EI1: EI1, EI2: EI2, EI3: EI3,
        L: L, L1: L1, L2: L2, L3: L3,
        alpha1: 0, alpha2: PI / 2, alpha3: PI / 4, alpha4: -PI / 2, alpha5: -PI / 2, alpha6: alpha6,
        F1: 20, a1: 3, b1: 3, F2: F2, a2: a2, b2: b2, F3: F3, a3: a3, b3: b3,
        F4: F4, a4: a4, b4: b4, F5: F5, a5: a5, b5: b5, F6: F6, a6: a6, b6: b6,
        q1: q1, l1: l1, q2: 6, l2: 4, q3: 6, l3: 4, q4: q4, l4: l4, q5: q5, l5: l5, q6: q6, l6: l6,
        FD1: 2, FD2: -3, FD3: FD3, FD4: FD4, FD5: FD5, FD6: FD6
    }
    subs_(sub_dict)

    # ������������������ű���
    # all_lambda_matrix = [
    #     [1, 0, 2, 1, 0, 3],
    #     [1, 0, 2, 0, 0, 0],
    #     [1, 0, 3, 0, 0, 0],
    #     [1, 0, 2, 0, 0, 0],
    #     [1, 0, 3, 0, 0, 0]
    # ]
    all_lambda_str = '0,0,1,0'
    with contextlib.redirect_stdout(output_buffer):
        main(
            unit_num=1,
            unit_EA=[EA],
            unit_EI=[EI],
            unit_le=[L],
            alphas=[0],
            sub_dict=sub_dict,
            qs=[(1, (q1, L, L))],
            all_lambda_str=all_lambda_str,
            subs_token=subs_token,
            coculate_X_F_forced=True,
            ignore_x=True,
            reverse_M=True
        )
    output = output_buffer.getvalue()
    print(output)

    save_to_file = input("�Ƿ񱣴�����output.txt�ļ�����y/n��")
    if save_to_file.lower() == 'y':
        prompt = input("�����뱾��ʵ������ƻ�������")
        with open('output.txt', 'a', encoding='GBK') as f:
            f.write(f"{prompt}\n")
            f.write(output)
        print("����ѱ��浽output.txt�ļ���")
    else:
        print("���δ���档")
"""
TODO:
1. ���Ӷ�λ������Ĺ̶�����֧��
2. �����������Ĺ̶�����֧��
3. ��������ͬʱ�����ǽ�ȫ������������ֲ���������ͬ�����ڲ��õ��ǽ��ֲ�����������ȫ����������ͬ��
"""
