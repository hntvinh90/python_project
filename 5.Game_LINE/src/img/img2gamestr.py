import pygame, sys, os

def main():
    argvs = sys.argv
    if len(argvs)==1:
        print('Error of syntax: png2gamestr <PNG file 1> ... <PNG file n>')
    else:
        for path in argvs[1:]:
            if os.path.exists(path):
                if path[-4:] in ['.png', '.PNG']:
                    img = pygame.image.load(path)
                    with open(path+'.txt', 'w') as f:
                        f.write(str(pygame.image.tostring(img, 'RGBA')))
                    print(path, ':', img.get_rect(), 'Successfully!')
                else:
                    print('The file named %s is not PNG file' %(path))
            else:
                print('The file named %s does not exist' %(path))

if __name__ == '__main__':
    main()