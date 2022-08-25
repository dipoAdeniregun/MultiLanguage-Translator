#  write your code here
import sys


def decode_Caesar_cipher(s, n):
    alpha = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',.?!"
    s = s.strip()
    text = ''
    for c in s:
        text += alpha[(alpha.index(c) + n) % len(alpha)]
    print(text)


def main():
    args = sys.argv[1]
    opened_file = open(args)
    encoded_text = opened_file.read()
    decode_Caesar_cipher(encoded_text, -13)

if __name__ == '__main__':
    main()
