""" Functions related to the creation of the ERT of a venue. get_publications()
creates a file that maps publications (list of values) to venues (keys).
create_ert(venue, sample_size) concatenates the SRTs of a sample of publications
from the given venue. """


import json
from random import sample


def get_publications():
  """ For each venue found in 'json/dim/all/relevant_venues.json', gather all
  the publications that belong to it and dump them in a file. """
  venues = json.load(open('../data/json/dim/all/relevant_venues.json'))
  publications = {}
  for publication_id, venue in venues.items():
    if venue not in publications:
      publications[venue] = []
    publications[venue].append(publication_id)
  json.dump(
    publications, open('../data/json/dim/all/ert/venue_publications.json', 'w')
  )


def get_erts():
  """ For each venue in 'venue_publications' (the file created by
  get_publications()), call create_ert(). Dump the results in a file. """
  publications = json.load(open('../data/json/dim/all/venue_publications.json'))
  data = json.load(open('../data/json/dim/all/relevant_data.json'))
  erts = {venue: create_ert(ids, data) for venue, ids in publications.items()}
  json.dump(erts, open('../data/json/dim/all/ert/venue_erts.json', 'w'))


def create_ert(publications, data, sample_size=4):
  """ Given the publications of a venue and a sample size, concatenate the SRTs
  (i.e. title and abstract) of 'sample_size' random publications of the venue.
  Separate the texts of the publications with three slashes '///', so no ngrams
  are formed using tokens of different texts. Return the concantenated texts as
  well as a list with the IDs of the used publications. """
  if len(publications) <= sample_size:
    ids = publications
  else:
    ids = sample(publications, sample_size)
  ert = ''
  for id in ids:
    for text in data[id].values():
      if text is not None:
        ert += text + ' /// '
  return {'ert': ert, 'ids': ids}


if __name__ == "__main__":
  get_erts()