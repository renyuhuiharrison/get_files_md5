import hashlib   
import os
import io
import sys
from xml.dom.minidom import Document

def writeFileInfo(doc, filelist, filename, dirname, md5string):

    file = doc.createElement('file')
    filelist.appendChild(file)

    file.setAttribute("filename", filename)
    file.setAttribute("dir", dirname)
    file.setAttribute("md5", md5string)


def getFileMd5(filename):
    m = hashlib.md5()
    file = io.FileIO(filename,'r')
    bytes = file.read(1024)
    while(bytes != b''):
        m.update(bytes)
        bytes = file.read(1024) 
    file.close()
    return m.hexdigest()


def main():

    if 2 > len(sys.argv) :
        print("Please input the file name to save!")
        return

    saveFileName = sys.argv[1]

    doc = Document()
    filelist = doc.createElement('filelist')
    doc.appendChild(filelist)

    appName = os.path.basename(__file__)

    for root, dirs, files in os.walk("."):
        for f in files:
            full_file = os.path.join(root,f)
            dirname = os.path.dirname(full_file)

            if dirname == "." :
                dirname = ""
            else :
                dirname = dirname[2:]      #remove ./ in dirname

            dirname = dirname.replace("\\", '/')
            filename = os.path.basename(full_file)

            #the file does not written into the config
            if appName == filename or saveFileName == filename or "user.ini" == filename or "get_latest_gv.exe" == filename:
                continue
            
            

            writeFileInfo(doc, filelist, filename, dirname, getFileMd5(full_file))

    # save the config file
    with open(saveFileName, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))

main()