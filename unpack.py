import os
import subprocess
import csv
import shutil
from pathlib import Path
uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])

outputdirectory = os.path.join(os.getcwd(), "Output")
assetdirectory = os.path.join(os.getcwd(), "Game-Sounds")
assetdata = {}

def clean():
	for key in assetdata:
		wemsdirectory = os.path.join(assetdirectory, key)
		if len(assetdata[key]) > 0:
			shutil.rmtree(wemsdirectory)

def unpack(bnk):
	subprocess.call([os.path.join(os.getcwd(), "bnkextr.exe"),bnk])


def dumpbnks():
	for filename in os.listdir(assetdirectory):
		f = os.path.join(assetdirectory, filename)
		assetdata[Path(f).stem] = {}
		if filename.endswith('.bnk'):
			unpack(f)
		elif filename.endswith('.txt'):
			# convert TSV to json
			with open(f) as file:

				tsv_file = csv.reader(file, delimiter="\t")

				for line in tsv_file:
					if len(line) > 6:
						if line[1] != "ID" and line[3] != "" and line[5] != "":
							assetdata[Path(f).stem][line[1]] = {
								"Name": line[2],
								"Audio source file": line[3],
								"Wwise Object Path": line[5].replace("\\Actor-Mixer Hierarchy\\Default Work Unit\\",""),
								"Notes": line[6],
							}

def outputandorganise():
	for key in assetdata:
		wemsdirectory = os.path.join(assetdirectory, key)
		data = assetdata[key]
		if len(data) > 0:
			for filename in os.listdir(wemsdirectory):
				wem = os.path.join(wemsdirectory, filename)
				wemmetadata = data[Path(wem).stem]
				#create path
				p = uppath(os.path.join(outputdirectory, wemmetadata["Wwise Object Path"]),1)
				Path(p).mkdir(parents=True, exist_ok=True)
				#convert wem to wav using vgmstream
				newwempath = os.path.join(p, wemmetadata["Name"])
				subprocess.call([os.path.join(os.getcwd(), "vgmstream/vgmstream.exe"),wem,"-o",newwempath+".wav"])
				#convert wav to ogg using ffmpeg
				subprocess.call([os.path.join(os.getcwd(), "ffmpeg.exe"),"-y","-i",newwempath+".wav","-c:a","libvorbis","-b:a","192k",newwempath+".ogg"])
	

def main():
	dumpbnks()
	outputandorganise()
	clean()

main()