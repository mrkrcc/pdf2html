import re
from flask import Flask, request, jsonify
from os.path import isfile
import subprocess
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/pdf2html", methods=['POST', "GET"])
def pdf2html():
    path = request.args.get('path')
    print(path)
    fileName = path.rsplit("/", 1)[-1].split(".")[0]
    newFolder = path.rsplit("/", 1)[0] + "/" + fileName
    subprocess.run(['mkdir ' + newFolder], shell=True)
    subprocess.run(['pdftohtml -s -fontfullname ' + path + " " + newFolder + "/" + fileName +".html" ], shell=True)

    filePath =  newFolder + "/" + fileName + "-html.html"
    f = open(filePath, "r")
    file = f.read()
    f.close()
    try:
        file = BeautifulSoup(file, 'html.parser')
    except:
        import collections
        collections.Callable = collections.abc.Callable
        file = BeautifulSoup(file, 'html.parser')
    newPath = path.rsplit("/", 1)[0] + "/"
    newFileName = newPath + fileName + ".html"
    newFile = open( newFileName, "w" )
    temp = re.sub(r'bgcolor=.*?[0-9]\"', '', str(file))
    temp = re.sub(r'\<img.*?\>', '', str(temp))
    newFile.writelines( str(temp) )
    newFile.close()
    subprocess.run(['rm -rf ' + newFolder], shell=True)

    return "Converted to HTML"


if __name__ == '__main__':
    app.run( )
