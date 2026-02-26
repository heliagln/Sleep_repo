# Sleep Score

Contient les fichiers pour calculer le score du sommeil.

Les fichiers de ce dossier sont:
- **sleep_score.py**: Ce fichier sert à calculer directement le score de sommeil à partir d'un fichier Garmin des épisodes du sommeil et de l'âge du patient. Il suffit de faire la commande suivante:
```
bash <(python3 sleep_score.py path/to/sleep/csv -age 22)
```
- **sleep_score_all.py**: Ce fichier sert à calculer directement les scores journaliers de tous les fichiers Garmin des épisodes du sommeil et de l'âge du patient. Il suffit de faire la commande suivante:
```
bash <(python3 sleep_score_all.py path/to/sleep/folder/csv -age 22)
```
- **age.csv**: csv avec les catégories de tranches d'âge et les bornes supérieures (strictes) associées à ces tranches d'âges. Les bornes sont en années.
- **reco_sleep_quality.csv**: csv regroupant toutes les recommendations. Toutes ces recommendations proviennent du papier suivant:
 ```bibtex
@ARTICLE{Ohayon2017-am,
  title     = "National Sleep Foundation's sleep quality recommendations: first
               report",
  author    = "Ohayon, Maurice and Wickwire, Emerson M and Hirshkowitz, Max and
               Albert, Steven M and Avidan, Alon and Daly, Frank J and
               Dauvilliers, Yves and Ferri, Raffaele and Fung, Constance and
               Gozal, David and Hazen, Nancy and Krystal, Andrew and Lichstein,
               Kenneth and Mallampalli, Monica and Plazzi, Giuseppe and
               Rawding, Robert and Scheer, Frank A and Somers, Virend and
               Vitiello, Michael V",
  abstract  = "To provide evidence-based recommendations and guidance to the
               public regarding indicators of good sleep quality across the
               life-span.The National Sleep Foundation assembled a panel of
               experts from the sleep community and representatives appointed
               by stakeholder organizations (Sleep Quality Consensus Panel). A
               systematic literature review identified 277 studies meeting
               inclusion criteria. Abstracts and full-text articles were
               provided to the panelists for review and discussion. A modified
               Delphi RAND/UCLA Appropriateness Method with 3 rounds of voting
               was used to determine agreement.For most of the sleep continuity
               variables (sleep latency, number of awakenings >5 minutes, wake
               after sleep onset, and sleep efficiency), the panel members
               agreed that these measures were appropriate indicators of good
               sleep quality across the life-span. However, overall, there was
               less or no consensus regarding sleep architecture or nap-related
               variables as elements of good sleep quality.There is consensus
               among experts regarding some indicators of sleep quality among
               otherwise healthy individuals. Education and public health
               initiatives regarding good sleep quality will require sustained
               and collaborative efforts from multiple stakeholders. Future
               research should explore how sleep architecture and naps relate
               to sleep quality. Implications and limitations of the consensus
               recommendations are discussed.",
  journal   = "Sleep Health",
  publisher = "Elsevier BV",
  volume    =  3,
  number    =  1,
  pages     = "6--19",
  month     =  feb,
  year      =  2017,
  language  = "en"
}
```
Les recommendations pour le temps de sommeil proviennent du papier suivant:
```bibtex
@ARTICLE{Hirshkowitz2015-rh,
  title     = "National Sleep Foundation's sleep time duration recommendations:
               methodology and results summary",
  author    = "Hirshkowitz, Max and Whiton, Kaitlyn and Albert, Steven M and
               Alessi, Cathy and Bruni, Oliviero and DonCarlos, Lydia and
               Hazen, Nancy and Herman, John and Katz, Eliot S and
               Kheirandish-Gozal, Leila and Neubauer, David N and O'Donnell,
               Anne E and Ohayon, Maurice and Peever, John and Rawding, Robert
               and Sachdeva, Ramesh C and Setters, Belinda and Vitiello,
               Michael V and Ware, J Catesby and Adams Hillard, Paula J",
  abstract  = "OBJECTIVE: The objective was to conduct a scientifically
               rigorous update to the National Sleep Foundation's sleep
               duration recommendations. METHODS: The National Sleep Foundation
               convened an 18-member multidisciplinary expert panel,
               representing 12 stakeholder organizations, to evaluate
               scientific literature concerning sleep duration recommendations.
               We determined expert recommendations for sufficient sleep
               durations across the lifespan using the RAND/UCLA
               Appropriateness Method. RESULTS: The panel agreed that, for
               healthy individuals with normal sleep, the appropriate sleep
               duration for newborns is between 14 and 17 hours, infants
               between 12 and 15 hours, toddlers between 11 and 14 hours,
               preschoolers between 10 and 13 hours, and school-aged children
               between 9 and 11 hours. For teenagers, 8 to 10 hours was
               considered appropriate, 7 to 9 hours for young adults and
               adults, and 7 to 8 hours of sleep for older adults. CONCLUSIONS:
               Sufficient sleep duration requirements vary across the lifespan
               and from person to person. The recommendations reported here
               represent guidelines for healthy individuals and those not
               suffering from a sleep disorder. Sleep durations outside the
               recommended range may be appropriate, but deviating far from the
               normal range is rare. Individuals who habitually sleep outside
               the normal range may be exhibiting signs or symptoms of serious
               health problems or, if done volitionally, may be compromising
               their health and well-being.",
  journal   = "Sleep Health",
  publisher = "Elsevier BV",
  volume    =  1,
  number    =  1,
  pages     = "40--43",
  month     =  mar,
  year      =  2015,
  keywords  = "Lifespan sleep; National Sleep Foundation; RAND/UCLA
               Appropriateness Method; Sleep adequacy; Sleep by age; Sleep
               duration; Sleep sufficiency; Sleep time recommendations",
  language  = "en"
}
```
