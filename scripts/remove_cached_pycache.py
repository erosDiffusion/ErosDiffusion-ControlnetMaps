import os
import subprocess

def main():
    root = os.getcwd()
    removed = 0
    for dirpath, dirnames, filenames in os.walk(root):
        if '__pycache__' in dirnames:
            d = os.path.join(dirpath, '__pycache__')
            # Make path relative for git
            rel = os.path.relpath(d, root)
            rel = rel.replace('\\', '/')
            print(f"Removing cached: {rel}")
            subprocess.run(['git', 'rm', '-r', '--cached', '--ignore-unmatch', rel])
            removed += 1
    if removed == 0:
        print('No tracked __pycache__ directories found.')

if __name__ == '__main__':
    main()
