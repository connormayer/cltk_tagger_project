import json

from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from collections import defaultdict

FILENAMES = [
	("/home/connor/ling/LING 202/Project/Output/TLG0012.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0012.TXT"),
	("/home/connor/ling/LING 202/Project/Output/TLG0016.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0016.TXT"),
	("/home/connor/ling/LING 202/Project/Output/TLG0059.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0059.TXT"),
	("/home/connor/ling/LING 202/Project/Output/TLG0014.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0014.TXT"),
	("/home/connor/ling/LING 202/Project/Output/TLG0031.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0031.TXT"),
	("/home/connor/ling/LING 202/Project/Output/TLG0527.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0527.TXT"),
	("/home/connor/ling/LING 202/Project/Output/TLG0062.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0062.TXT"),
	("/home/connor/ling/LING 202/Project/Output/TLG0548.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0548.TXT"),
	("/home/connor/ling/LING 202/Project/Output/TLG0008.json",
		"/home/connor/cltk_data/greek/text/tlg/plaintext/TLG0008.TXT"),
]

class FormFreqAggregator():

	def get_verb_counts_by_category(self, filename):
		with open(filename, 'r') as f:
			freq_dict = json.loads(f.read())
			results_dict = {}
			results_dict['indicative'] = defaultdict(int)
			results_dict['non-indicative'] = defaultdict(int)

			for key, value in freq_dict.items():
				if key[0] == 'V':
					if key[3] == '-':
						continue
					elif key[4] == 'I':
						results_dict['indicative'][key[3]] += sum(value.values())
					else:
						results_dict['non-indicative'][key[3]] += sum(value.values())

			indicative_count = sum(results_dict['indicative'].values())
			nonindicative_count = sum(results_dict['non-indicative'].values())
			total_count = indicative_count + nonindicative_count
			print(filename)
			print("Indicative: {}".format(indicative_count / total_count))
			print("Non-indicative: {}".format(nonindicative_count / total_count))
			print("Present indicative: {}".format(
				results_dict['indicative'].pop('P') / indicative_count
			))
			print("Imperfect indicative: {}".format(
				results_dict['indicative'].pop('I') / indicative_count
			))
			print("Aorist indicative: {}".format(
				results_dict['indicative'].pop('A') / indicative_count
			))
			print("Other indicative: {}".format(
				sum(results_dict['indicative'].values()) / indicative_count
			))

			print("Non-indicative present: {}".format(
				results_dict['non-indicative'].pop('P') / nonindicative_count
			))
			print("Non-indicative aorist: {}".format(
				results_dict['non-indicative'].pop('A') / nonindicative_count
			))
			print("Non-indicative other: {}".format(
				sum(results_dict['non-indicative'].values()) / nonindicative_count
			))

	def compare_tag_word_counts(self, json_file, txt_file):
		with open(json_file, 'r') as f1:
			with open(txt_file, 'r') as f2:
				json_data = json.loads(f1.read())
				txt_file = tlg_plaintext_cleanup(f2.read(), rm_punctuation=True, rm_periods=True)

				word_count = 0
				for _, value in json_data.items():
					for _, value2 in value.items():
						word_count += value2

				print(json_file)
				print("Tagged words: {}".format(word_count))
				print("File words: {}".format(len(txt_file.split(" "))))
				print("Percent: {}".format(word_count/len(txt_file.split(" "))))

if __name__ == "__main__":
	aggregator = FormFreqAggregator()
	for json_file, txt_file in FILENAMES:
		aggregator.get_verb_counts_by_category(json_file)
		aggregator.compare_tag_word_counts(json_file, txt_file)
