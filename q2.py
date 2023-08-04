import copy
import sys


def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()

    return line


ALPHABET_SIZE = 26


def reverse_string(string):
    return string[::-1]


def string_match_prefix(string, r, l):
    len_string = len(string)
    return r < len_string and (string[r] == string[r - l] or string[r] == '.' or string[r - l] == '.')


def string_match_suffix(string, r, l):
    len_string = len(string)
    return r < len_string and (string[r] == string[r - l])


def z_algorithm_prefix(combined_str):
    len_combined = len(combined_str)
    z_lst = [None] * len_combined
    left = 0
    right = 0

    for i in range(1, len_combined):
        # Base case or Case 1
        if i > right:
            left = i
            right = i
            while string_match_prefix(combined_str, right, left):
                right += 1
            z_lst[i] = right - left
            right -= 1

        else:
            k = i - left
            if z_lst[k] < right - i + 1:
                z_lst[i] = z_lst[k]
            else:
                left = i
                while string_match_prefix(combined_str, right, left):
                    right += 1
                z_lst[i] = right - left
                right -= 1

    return z_lst


def z_algorithm_suffix(combined_str):
    len_combined = len(combined_str)
    z_lst = [None] * len_combined
    left = 0
    right = 0

    for i in range(1, len_combined):
        # Base case or Case 1
        if i > right:
            left = i
            right = i
            while string_match_suffix(combined_str, right, left):
                right += 1
            z_lst[i] = right - left
            right -= 1

        else:
            k = i - left
            if z_lst[k] < right - i + 1:
                z_lst[i] = z_lst[k]
            else:
                left = i
                while string_match_suffix(combined_str, right, left):
                    right += 1
                z_lst[i] = right - left
                right -= 1

    return z_lst

def bad_character(string):
    m = len(string)
    bad_char_table = [None] * m
    bad_char_table[0] = [-1] * ALPHABET_SIZE

    for i in range(1, m):
        bad_char_table[i] = copy.deepcopy(bad_char_table[i - 1])
        if string[i - 1] == '.':
            for j in range(ALPHABET_SIZE):
                bad_char_table[i][j] = i - 1
        else:
            bad_char_table[i][ord(string[i - 1]) - 97] = i - 1

    return bad_char_table


def good_suffix(string):
    m = len(string)
    good_suffix_lst = [-1] * (m + 1)

    z_suffix = z_algorithm_suffix(reverse_string(string))
    z_suffix.reverse()

    for p in range(m - 1):
        j = m - z_suffix[p]
        good_suffix_lst[j] = p

    return good_suffix_lst


def matched_prefix(string):
    m = len(string)
    matched_prefix_lst = [0] * (m + 1)
    z_prefix = z_algorithm_prefix(string)

    matched_prefix_lst[0] = m

    z_prefix.reverse()

    current_max = -1
    for i in range(len(z_prefix) - 1):
        current_max = max(current_max, z_prefix[i])
        matched_prefix_lst[m - i - 1] = current_max

    return matched_prefix_lst


def boyer_moore(txt, pat):
    if len(pat) == 0 or len(txt) == 0 or len(txt) < len(pat):
        return []

    matches = []

    # preprocessing
    bad_char_table = bad_character(pat)
    good_suffix_lst = good_suffix(pat)
    matched_prefix_lst = matched_prefix(pat)

    shift = 0

    m = len(pat)

    while shift <= len(txt) - m:
        pat_point = m - 1
        # compare for matches
        while pat_point > -1 and (pat[pat_point] == txt[shift + pat_point] or pat[pat_point] == '.'):
            pat_point -= 1
        if pat_point == -1:
            # pattern match substring so put to matches (1-indexed)
            matches.append(str(shift + 1))
            shift += m - matched_prefix_lst[1]
        else:
            # give 1 as max in case there is no bad character and so shift 1 place
            bad_char_shift = max(1, pat_point - bad_char_table[pat_point][ord(txt[shift + pat_point]) - 97])
            # finding good suffix for shifting
            if good_suffix_lst[pat_point + 1] == -1:
                suffix_shift = pat_point - matched_prefix_lst[pat_point + 1]
            else:
                suffix_shift = pat_point - good_suffix_lst[pat_point + 1]
            shift += max(bad_char_shift, suffix_shift)

    return matches


if __name__ == '__main__':
    t = read_file(sys.argv[1])
    p = read_file(sys.argv[2])

    text = ''
    pattern = ''

    if len(t) > 0:
        text = t[0]

    if len(p) > 0:
        pattern = p[0]

    res = boyer_moore(text, pattern)


    with open('output_q2.txt', 'w') as f:
        f.write('\n'.join(res))

