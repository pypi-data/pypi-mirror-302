import json
import re
import os.path
import sys
import pkg_resources
from typing import Dict, Union, List, Tuple

from subdeloc_tools.modules import extract_subs
from subdeloc_tools.modules import pairsubs
from subdeloc_tools.modules import honorific_fixer
from subdeloc_tools.modules.types.types import MatchesVar
from modify_subs import find_key_by_string_wrapper as find_key_by_string

HONORIFICS_PATH = pkg_resources.resource_filename('subdeloc_tools', 'samples/honorifics.json')

class SubTools:
	honorifics = {}
	names = {}

	def __init__(self, main_sub: str, ref_sub: str, names_path: str, honorifics_name: str=HONORIFICS_PATH, output_name: str="edited.ass", load_from_lambda: bool=False):
		"""
		If load_from_lambda is True, names_path and honorifics_name should be the address to a public HTTP lambda. TODO
		"""
		self.main_sub = main_sub
		self.ref_sub = ref_sub
		self.output_name = output_name
		with open(honorifics_name, encoding='utf-8') as f:
			self.honorifics = json.load(f)
		with open(names_path, encoding='utf-8') as f:
			self.names = json.load(f)

	def print_to_file(self, data: dict, filename: str="result.json"):
		"""Writes the data to a JSON file."""
		with open(filename, "w", encoding="utf8") as output:
			json.dump(data, output, ensure_ascii=False, indent=2)

	def main(self) -> str:
		# Assuming pairsubs.pair_files is defined elsewhere and returns a list of subtitles
		res = pairsubs.pair_files(self.main_sub, self.ref_sub)
		s = self.search_honorifics(res)
		return honorific_fixer.fix_original(self.main_sub, s, self.output_name)


	def prepare_honor_array(self) -> List[str]:
		"""Prepares an array of all kanjis from the honorifics."""
		return [kanji for h in self.honorifics["honorifics"].values() for kanji in h["kanjis"]]

	def search_honorifics(self, subs: List[MatchesVar]) -> List[MatchesVar]:
		"""Searches for honorifics in the subtitles and processes them."""
		honor = self.prepare_honor_array()

		for sub in subs:
			for reference in sub["reference"]:
				for h in honor:
					if h in reference["text"]:
						self.check_sub(sub, h, reference["text"])
						break  # Exit loop after first match to avoid redundant checks

		return subs

	def check_sub(self, sub:MatchesVar, honor:str, reference_text:str) -> bool:
		"""Checks and replaces honorifics in the subtitles."""
		honorific = find_key_by_string(self.honorifics, honor, "kanjis")

		if not honorific:
			return False

		for name, name_value in self.names.items():
			if name_value in reference_text:
				for orig in sub["original"]:
					if name in orig["text"]:
						# Perform replacements for name and honorifics
						orig["text"] = re.sub(name, f"{name}-{honorific}", orig["text"], flags=re.I)
						
						for alternative in self.honorifics["honorifics"][honorific]["alternatives"]:
							orig["text"] = re.sub(alternative, "", orig["text"], flags=re.I)

						orig["text"] = orig["text"].strip()
		return True

	@classmethod
	def get_default_honorifics_file(self):
		with open(HONORIFICS_PATH, encoding='utf-8') as f:
			return json.load(f)