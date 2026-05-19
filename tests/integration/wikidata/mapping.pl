resolve_name(Id, Name) :- wikidata_label(Id, Name), wikidata_person(Id).
place_of_birth(PersonId, Place) :- wikidata_place_of_birth(PersonId, PlaceId), wikidata_label(PlaceId, Place).
