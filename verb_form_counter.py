import glob
import json
import multiprocessing as mp
import os

from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag
from collections import defaultdict
from itertools import cycle

CLTK_DIR = "/home/connor/cltk_data/greek/text/tlg/plaintext"
OUT_DIR = "/home/connor/ling/LING 202/Project/Output"
COMPLETED_FILE = "/home/connor/ling/LING 202/Project/Output/completed.txt"

class VerbFormCounter():

	tagger = None
	lemmatizer = None

	def get_counts_from_file(self, filename, queue):
		print("Processing {}".format(filename))
		counts_dict = {}
		tagger = POSTag('greek')
		lemmatizer = LemmaReplacer('greek')

		with open(filename, 'r') as f:
			for line in f:
				line = tlg_plaintext_cleanup(
					line, rm_punctuation = True, rm_periods = True
				)
				results = tagger.tag_tnt(line)
				for word in results:
					type_info = word[1]
					if type_info is not 'Unk':
						counts_dict[type_info] = counts_dict.get(
							type_info, defaultdict(int)
						)
						[lemma] = lemmatizer.lemmatize(
							word[0], return_raw = True
						)
						counts_dict[type_info][lemma] += 1

		out_filename = os.path.basename(filename).replace(".TXT", ".json")
		with open(os.path.join(OUT_DIR, out_filename), 'w') as out_file:
			json.dump(counts_dict, out_file)

		queue.put(filename)

	def write_completed(self, queue):
		with open(COMPLETED_FILE, "a") as comp_file:
			while True:
				m = queue.get()
				if m == 'kill':
					break
				comp_file.write(str(m) + '\n')
				comp_file.flush()

	def get_total_counts(self):
		counts_dict = {}
		file_list = glob.glob(os.path.join(CLTK_DIR, "TLG*.TXT"))
		manager = mp.Manager()
		queue = manager.Queue()
		pool = mp.Pool(mp.cpu_count() + 2)

		watcher = pool.apply_async(self.write_completed, (queue,))

		with open(COMPLETED_FILE, "r") as comp_file:
			completed = comp_file.read().split("\n")
			file_list = list(set(file_list) - set(completed))

		jobs = []
		for filename in file_list:
			job = pool.apply_async(self.get_counts_from_file, (filename, queue))
			jobs.append(job)

		for job in jobs:
			job.get()

		queue.put('kill')
		pool.close()
		
if __name__ == "__main__":
	counter = VerbFormCounter()
	counter.get_total_counts()

