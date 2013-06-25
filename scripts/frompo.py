#!/usr/bin/python

import argparse
import json
import os
import re

LANGUAGES = [
  "bg",
  "cs",
  "de",
  "el",
  "en-US",
  "es",
  "eu",
  "fr",
  "ga-IE",
  "hr",
  "hu",
  "it",
  "ja",
  "mk",
  "my",
  "nl",
  "pl",
  "pt-BR",
  "ro",
  "ru",
  "sk",
  "sr",
  "th",
  "tr",
  "ur",
  "zh-CN",
  "zh-TW"
]

_scary_path_regex = re.compile("(" + ("|".join(LANGUAGES)) + ")/LC_MESSAGES.*")

def parse_po(f, root):

  locale = _scary_path_regex.findall(root)
  if len(locale) == 0:
    raise Exception("{} does not have a locale?".format(root))
  locale = locale[0]

  s = {}
  header = True
  lastid = None
  for line in f:
    line = line.strip()
    if header:
      if line == "":
        header = False
      continue

    line = line.split(" ", 1)
    if len(line) == 2:
      if line[0] == "msgid":
        lastid = json.loads(line[1])
        s[lastid] = None
      elif line[0] == "msgstr":
        s[lastid] = json.loads(line[1])

  return s, locale

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Generate the final locale file that would be used by the app.")
  parser.add_argument("directories", nargs="+", help="The directories that the po files are from.")
  parser.add_argument("-o", "--output", help="The output file location.", required=True)
  args = parser.parse_args()

  s = {}
  for directory in args.directories:
    for root, d, files in os.walk(directory):
      for fname in files:
        if fname.endswith(".po"):
          with open(os.path.join(root, fname)) as f:
            strings, locale = parse_po(f, root)
            s.setdefault(locale, {}).update(strings)

  with open(args.output, "w") as f:
    json.dump(s, f)
    print "Done! Output to {}".format(args.output)