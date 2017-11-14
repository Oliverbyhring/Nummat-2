###################################
##### Tidsplan EDIT 14. november - velkommen tilbake skal du være, Even!
###################################

26. oktober - start

29. oktober - lest og forst�tt B splines quadrature + alle oppgaver

1. november - 2a-2d kj�rende

6. nov - Kj�rende kode 2e-2h. Even bortreist.

Tid for stokmod.

14. november - Fungerende kode for alle oppgaver

15. november - Even back

17. november - Optimalisert kode for alle oppgaver

21. november - ferdig skrevet i Latex

24. november - deadline


#############################################
UPDATE per 14. november:
Jeg begynte på numerisk igjen idag, og siste modul (area_integral.py) kjører,
og gir resultat skal være rett (har fått ganske grundig gjennomgang av Abd).

TO DO:
Alle moduler må renskrives, dvs. gode lesbare variabelnavn (vanskelig), og
kun engelske kommentarer som forklarer hvert steg godt.

Vi må optimalisere koden. Vet ikke helt hvordan vi skal angripe denne, men her
er det spline_quadrature som gjøre det meste av de "manuelle" utregningene og
antakelig mest å hente her.

Latex. Jeg spurte Abdullah om hva han forventer av svar på oppgavene om linje-,
og overflateintegral, dvs. 2f og 2h. Han skrev følgende:

"I oppgave 2e og 2g trenger du ingen drøfting. Det er bare å lage riktig figur
som du setter inn i rapporten. På 2f og 2h er det nok å bare skrive generell
 formel for linje- og overflate-integral, og så forklare at hvis du bruker
 numerisk kvadratur, så får du respektivt en enkel og dobbel sum som du beregner.
 Her er det også mer fokus på at koden gir riktig svar. "

 Min plan er å skrive inn kostebinderiet som skal i 2f og 2h, deretter legge inn
 figurplottene i Latex. Dernest å optimalisere kode, og finne ut om Latex-besvarelsen
 burde suppleres.

 Spørsmål?



###################################
##### Ting � passe p�
###################################
Tau er 1-indeksret i Optimal Quadrature og oppgaveteksten!!!
p = degree. Order k = p + 1
An open knot vector will have the first and last elements repeated p+1 times.

###################################
##### Kodeplan
###################################

2d)

	Prepare_Data returnerer:
w og xi initialisert
n
integrals_c, eksakte integraler som lagres i Spline_Quadrature
(Returnerer IKKE augmented Knot vector fordi vi ikke trenger denne)

	Assembly tar inn w og xi og returnerer:
F evaluert
dF evaluert

	Spline_Quadrature:
Lagrer eksakte integraler
kj�rer loop som bruker assembly i hver loop
itererer til vi n�r himmelen

###################################
##### Resources
###################################

https://docs.google.com/document/d/1_qiC80mygluc7YxwivCQ2touO0cV4QCjtIwwOKhWDrE/edit?usp=sharing

Splipy har f�lgende innebygd:
integrate(t0, t1)[source]
	Integrate all basis functions over a given domain

evalute_derivative(u, v[, d=(1, 1)])�
	Evaluate the derivative of the surface at the given parametric values.

Progmester Sivert, kan det brukes?
