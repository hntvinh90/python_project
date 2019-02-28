import sys, os
from PIL import Image

def main():
    argvs = sys.argv
    if len(argvs) == 1:
        print('Error of syntax: png2ico <PNG file 1> ... <PNG file n>')
    else:
        for path in argvs[1:]:
            if os.path.exists(path):
                if path[-4:] in ['.png', '.PNG']:
                    img = Image.open(path)
                    img.save(path[:-4] + '.ico')
                else:
                    print('The file named %s is not PNG file' %(path))
            else:
                print('The file named %s does not exist' %(path))

if __name__ == '__main__':
    main()