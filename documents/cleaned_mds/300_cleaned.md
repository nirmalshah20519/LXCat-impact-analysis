Contents lists available at [ScienceDirect](http://www.sciencedirect.com/science/journal/23521791)

# Nuclear Materials and Energy

journal homepage: [www.elsevier.com/locate/nme](https://www.elsevier.com/locate/nme)

# AMMONX: A kinetic ammonia production scheme for EIRENE implementation

S. Touchar[da](#page-0-0),[⁎](#page-0-1) , J. Mougeno[ta](#page-0-0) , C. Rond[a](#page-0-0) , K. Hassouni[a](#page-0-0) , X. Bonnin[b](#page-0-2)

- <span id="page-0-0"></span><sup>a</sup> *Université Paris 13, Sorbonne Paris Cité, LSPM, CNRS-UPR3407, 99 av. J.-B. Clément, 93430 Villetaneuse, France*
- <span id="page-0-2"></span><sup>b</sup> *ITER Organization, Route de Vinon sur Verdon, CS90 046, 13067 St Paul Lez Durance Cedex, France*

ARTICLE INFO

*Keywords:* Modeling Edge-plasma Ammonia formation Tokamak

#### ABSTRACT

Until recently the EIRENE suite handled hydrogen chemistry (*i.e.* H atoms, H2 molecules, and H2 <sup>+</sup> molecular ions and their isotopomers). Extensions also exist for hydrocarbon chemistry, including CxHy species (H is any hydrogen isotope), but no kinetic scheme including NHx chemistry had been implemented. After a benchmarking of available schemes and kinetic data, a reduced scheme including 50 reactive processes is presented here, implying a large set of N-bearing species (N, N2, N2 +, NHx radicals and ions). This mechanism is a part of a more complete scheme of 130 processes also including the metastable states of N2 and N. In a first time, this scheme has been validated by comparison with independent experimental works. In a second time the scheme was used in Eirene suite to model a type-case. First results confirm that under tokamak conditions, ammonia is produced in significative amount after N2 injection in the sub-divertor volume.

### **1. Introduction**

High performance plasma operation in ITER will require the routine injection of an extrinsic low atomic number impurity to provide cooling of the divertor plasma via radiative dissipation. The two principal candidate gases are neon and the molecular gas nitrogen N2. As reported in recent articles of research groups working within the Eurofusion consortium [\[1–3\]](#page-4-0), the use of N2 as a seed impurity in tokamak devices is subject to a nitrogen balance issue: a large fraction of the nitrogen injected for the radiative cooling of the plasma is not recovered as N2 upon regeneration using liquid helium operated cryopumps. This was clearly shown and confirmed in recent global gas balance experiments at ASDEX Upgrade (AUG) and JET [\[1\].](#page-4-0) The most probable loss channels are the implantation of nitrogen-containing ions into plasma-facing materials, nitrogen containing species co-deposition and ammonia formation [\[3,4\]](#page-4-1). The formation of large quantities of ammonia has consequences for several aspects of the ITER plant operation in terms of gas reprocessing and duty cycle. It is therefore important to assess early on what fraction of ammonia may be found in the ITER gas exhaust when N2 seeding is used.

The design of the ITER divertor and estimates of the required fuel throughput have relied for many years on simulations performed with the SOLPS plasma edge modeling suite [\[5\]](#page-5-0), a new version of which, SOLPS-ITER [\[6,7\]](#page-5-1), containing a more complete physics model, was launched in 2015 by the ITER Organization. The code uses the Monte Carlo neutral kinetic code EIRENE ([www.eirene.de](http://www.eirene.de)) as its main workhorse for solving the transport equations related to neutral atomic and molecular species, as well as for radicals and molecular ions. It has allowed reproducing the main trends of H2/D2 chemistry in tokamak devices [\[8\].](#page-5-2) EIRENE makes use of an optimized chemical kinetics model that describes both homogeneous gas phase chemistry and heterogeneous surface chemistry involved in the plasma-surface interaction (PSI). There was however no attempt to implement a chemical model in order to describe ammonia formation at the plasma-wall interface under tokamak edge-plasma conditions. In particular, the recent update of the AMJUEL module used for kinetic data source for EIRENE global model does not include an ammonia formation scheme [\[9\].](#page-5-3)

In the following of this paper, a global model for ammonia chemistry will be firstly described, indicating which resources were used to build it. In a second time a validation of the model in laboratory conditions, close to edge plasma ones, will be proposed. Finally, first results obtained for a test-case in SOLPS will be presented.

### **2. Construction of the NH3 kinetic model**

# *2.1. Construction of the global model*

To have a first approach of the N2/H2 chemistry, a first bibliographic study of the different N2/H2 schemes already validated was

*E-mail address:* [sylvain.touchard@lspm.cnrs.fr](mailto:sylvain.touchard@lspm.cnrs.fr) (S. Touchard).

<span id="page-0-1"></span><sup>⁎</sup> Corresponding author.

<span id="page-1-0"></span>**Table 1**Typical characteristic plasma parameters under the tokamak divertor.

undertaken. Among them, two studies have retained our attention:

- the series of papers from the group of the Instituto de Estructura de la Materia, IEM-CSIC in Madrid [10–12].
- the work of Sode et al. published in 2015 [13].

Both have been done in low pressure ranges (between 1 to 10 Pa), cold plasma electron temperature ranges (between 1 and 10 eV) and electron densities close to those relevant to the tokamak area under the divertor [14].

Other modelling works for    plasma chemistry are also available [15–17], but their conditions of validity are significantly far from ITER tokamak conditions. Most of them are for example validated from experiments conducted from 50 Pa to atmospheric pressure.

A first conclusion of this literature analysis was that building a comprehensive database for an    production scheme requires taking into consideration the global    plasma chemistry. Nevertheless, some assumptions can be made by considering plasma conditions in the divertor area, which are summarized in Table 1.

Thus, the following hypotheses have been put forward:

- The species to be taken into consideration in the model are H, H<sub>2</sub>, H<sup>+</sup>, H<sub>2</sub><sup>+</sup>, H<sub>3</sub><sup>+</sup>, N, N<sub>2</sub>, NH, NH<sub>2</sub>, NH<sub>3</sub>, N<sup>+</sup>, N<sub>2</sub><sup>+</sup>, NH<sup>+</sup>, NH<sub>2</sub><sup>+</sup>, NH<sub>3</sub><sup>+</sup>, NH<sub>4</sub><sup>+</sup>, N<sub>2</sub>H<sup>+</sup>. The contribution of short-lived radiative states in the ground state and metastable states as N<sub>2</sub>(A), N<sub>2</sub>(a'), N(<sup>2</sup>D) kinetics was also evaluated and considered when necessary.
- Considering the very low pressure, three-body collision processes were excluded.
- Except molecular nitrogen that is present in the feed gas, species containing more than 2 nitrogen atoms were not considered, which means that second order processes in nitrogen were not considered.

Following these assumptions, a database containing 130 reactions and 21 species was built up. This database has been implemented in the SOLPS-ITER code suite formalism under the new acronym AMMONX and contains the following processes:

- Ionization by collision between neutrals and electrons
- Neutrals dissociation by electron impact
- Dissociative recombination between ions and electrons
- Ion-neutral processes
- N2, N and H2 metastable-states chemistry
- Neutral/neutral chemistry.

The source of kinetic data used for these processes have been verified and evaluated regarding explored plasma conditions. Among the most used databases one can mention:

- the LxCat database [18], whose main references for cross-sections of collisional processes with electrons [19–21] are consistent with the values used by D. Reiter for processes involving N<sub>2</sub><sup>9</sup>
- the Anicich reviews [22,23] and Umist database [24] for ions/ neutral processes
- the work of Capitelli et al. [25] and NIST database [26] for neutral processes.

This new AMMONX database is available on the LSPM web site at the following address: <a href="https://www.lspm.cnrs.fr/ammonx">https://www.lspm.cnrs.fr/ammonx</a>. It is also now distributed as a standard part of the SOLPS-ITER code suite package.

#### 2.2. Towards a reduced mechanism

As computation time in Eirene increases strongly with the number of chemical processes, it has been useful to reduce this first mechanism to a smaller one containing as few reactions as possible, while still retaining the essential plasma kinetics. The process of the mechanism reduction was conducted along the following lines

- First step: Each species involved in the chemical model should be involved in at least one production and one loss processes. A reduced scheme involving 18 chemical species must therefore include at least 36 elementary processes. We identified for each chemical species the dominant production and loss processes, which end up with a first set of 30 chemical processes.
- Second step: the gas phase processes involving species that reacts on the surfaces and with characteristic times longer than the upper limit of the diffusion characteristic time have been disregarded. Such gas phase processes will be dominated by the surface processes and will have a little impact on the overall plasma kinetics. As a result of this second approximation step, almost all the processes involving only neutral ground state species were disregarded.
- Third step (general hypothesis): only processes with characteristic times comparable to the predominant production and consumption processes identified in Step 1 are selected. Characteristic times of the production and consumption process for each species are estimated assuming a nitrogen abundance of less than 4% (2% N<sub>2</sub> in most cases). We also assumed that nitrogen containing species as well as hydrogen-ions (H<sup>+</sup>, H<sub>2</sub><sup>+</sup> and H<sub>3</sub><sup>+</sup>) have similar densities. Due to the wide range of electron temperature, at least 2 or -3 production processes have to be considered for each species.

Finally, a reduced mechanism for use with Eirene is proposed with 42 reactions (hereafter referred to as model A). The validation of this mechanism is proposed in the following sections. Another scheme of 53 reactions (named model B) including processes with metastable states of    and N has been also generated, but it is still under validation by comparison with experimental results.

### 2.3. Necessity of considering processes occurring at the wall

Taking into account the plasmas considered in this study, the loss of molecular ions may take place through either electron-impact or heterogeneous dissociative recombination. In particular, due to the pressure range of the considered plasmas, heterogeneous dissociative recombination may be dominant in most cases, which induces a strong coupling between neutral and charged    species and thus significantly affects the concentration of neutral    that are involved in ammonia formation. The recombination probabilities for molecular ions were assumed to be unity in agreement with Capitelli et al. [25].

All the studies published in the literature on the chemical kinetics of ammonia formation in    plasmas suggest that ammonia formation takes place at least partly through a heterogeneous mechanism involving neutral radicalar    species. Consequently, we have included in our model the heterogeneous conversion reactions of neutral    that result in the formation of ammonia. This reaction set was strongly inspired by the one proposed in Ertl's work [27]. As the wall is supposed to be saturated with H adsorbed atoms,    (x=0-2) radicals are assumed to recombine with adsorbed H-atom to form    species by the well-known Eley–Rideal mechanism. The probabilities of these processes, approximately   , are taken from those proposed by Carrasco et al. [12].

<span id="page-2-0"></span>**Table 2** Characteristics of the plasma.

#### 3. Validation of the reduced mechanism

In order to evaluate the ability of our reduced mechanism to reproduce and explain the formation of ammonia    plasmas, we performed simulations of the plasmas obtained under the experimental conditions reported by Carrasco et al. [12] using a homemade quasi-homogeneous 0D model described elsewhere [28]. The studied conditions are summed up in Table 2 and are close to those observed in the vicinity of tokamak divertors [14].

For these conditions, the comparison of the variation of the calculated and measured [12] ammonia, nitrogen and hydrogen concentrations as function of the nitrogen content in the feed gas are reported in Fig. 1.

This graph shows a quite good agreement between the model and the experiment in these conditions, even if the formation of    seems to be slightly overestimated by our model for initial fractions of    higher than 0.02. It is worthy to mention here that the computed values for the electron temperature and density are 2.5 eV and 2.5   , respectively, which is consistent with the values measured by Carrasco et al. [12] (2.8 eV and 3.0   ).

Another result obtained in our calculations is the need to consider the ammonia formation on the walls in our initial mechanism. Indeed, the presence in our reduced chemical scheme of the process of dissociative recombination of    ions with electrons (reaction 1) cannot explain alone the    amounts measured experimentally, even if    ions are produced in significant amounts as reported in Fig. 2.

 (reaction 1)

In fact, the simulations performed without considering the surface processes involving neutral radicals, yield only negligible amounts of ammonia.

<span id="page-2-1"></span>Fig. 1. Evolution of the relative concentration of main by-products as a function of initial    fraction in the plasma – dots are experimental results and lines computed ones with the 42-reactions reduced model (model A).

<span id="page-2-2"></span>Fig. 2. Computed profiles of main ions for 0.5% of    in initial mixture, a power provided in the reactor volume of   , a mean pressure of    and a wall temperature of   .

These first results show that the reduced scheme developed in this study is able to yield a good estimate for the amount of ammonia produced in the plasma. It also gives the trends of the evolution of ammonia concentration as a function of nitrogen in the feed gas.

#### 4. First simulations of ND<sub>3</sub> formation in Eirene

Once our reduced mechanism was validated by the experiments available in the literature, we implemented it in the SOLPS-ITER package and we used it to predict the    and    species concentrations for an    gas injection into the ITER divertor. Tests cases are based on the test case ITER\_2588\_D+He+N and they are solved with code version SOLPS-ITER 3.0.6-51 (also known as the "SOLPS-ITER 3.0.6 master").

In order to illustrate the impact of nitrogen chemistry, we consider four test cases:

- Test Case 1: only N and N<sup>+</sup> species are included in the EIRENE chemistry, and we use the standard AMJUEL set of reactions (ALL-He\_el.amd file), plus neutral-neutral elastic collisions,
- Test Case 2: only the molecular N<sub>2</sub> species and its chemical reactions are added compared to Case 1 (ALL-He\_el.amd and N<sub>2</sub>-only.amd files),
- Test Case 3: AMMONX simplified model A (without metastables) is used (ALL-He\_el.amd and Ammonia\_add.amd files),
- Test Case 4: AMMONX model B with metastables is solved (ALL-He\_el.amd and Ammonia\_add\_metastables.amd files).

Compared to the standard ITER\_2588\_D+He+N case (available for SOLPS-ITER users), we locate the    gas puff under the divertor dome (blue line in Fig. 3), instead of the more standard gas puffing from the top of the machine. This situation is more representative of high-power ITER operation where divertor detachment control will require nitrogen seed impurities to be injected as close to the targets as possible, *i.e.* using the gas manifold located at the bottom of the vacuum vessel.

For test Case 1 the injected gas is N whereas a    gas is puffed for the other cases with a flux of 3.0.10 [20] atoms.s<sup>-1</sup>. At this stage, we consider that Eirene stand-alone cases, *i.e.* neutral trajectories and chemistry, are solved by the Eirene code on a fixed plasma background. The main D fuel is injected from the top of machine, while He is brought through the core boundary corresponding to the fusion rate.

A simplified surface mechanism has been implemented for surface processes which assumes that all ions are neutralized by collision with

<span id="page-3-0"></span><span id="page-3-1"></span>**Fig. 3.** Zoom on N (test Case 1) and N2 (test Cases 2-3-4) injection zone (blue line). (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.)

the wall; and that NDx radicals recombining at the wall (aggregating all surface chemistry into a simple prescription) are reemitted with the following distribution: 10% of N2, 30% of ND, 30% of ND2 and 30% of ND3.

The N atom densities (in m−3) predicted for each test case are presented in [Fig. 4.](#page-3-1) Adding N2 reactions reduces the N diffusion: the density of N atoms increases under the divertor whereas the density decreases above it. The lowest N density close to the X-point is found with Case 4.

[Fig. 5](#page-4-2) shows the particle density of N2 molecules (in m−3) for test Cases 2, 3 and 4. The AMMONX database (test Cases 3 and 4) predicts less diffusion of N2 above the divertor. Taking into account the metastable species, as for N, reduces the N2 diffusion above the divertor even further.

[Fig. 6](#page-4-3) illustrates the ND3 formation for test Cases 3 and 4, in which N and H initial amounts are close. Results clearly show ammonia formation under the divertor, but the total amount seems too high, certainly due to the strong wall chemistry assumption made above. Different test cases (not shown here) where only homogeneous phase ND3 formation reactions in the divertor volume are considered and wall chemistry is neglected yield only negligible amounts of ammonia formation. However, the current EIRENE wall chemistry model does not, at this time, allow us to do anything more detailed that a fixed perspecies recombination rate. In order to implement a more realistic wall

**Fig. 4.** N atoms particle density (m−3) for each case.

<span id="page-4-2"></span>**Fig. 5.** N2 molecules particle density (m−3) in test Cases 2, 3 and 4.

<span id="page-4-3"></span>**Fig. 6.** ND3 molecules particle density (m−3) in test Cases 3 and 4.

chemistry model, which actually predicts as opposed to impose a recombination rate into ammonia of nitrogen radicals impinging on the wall, modifications to EIRENE will be required, which will be the subject of future work.

# **5. Conclusions**

A new database named AMMONX including NHX formation processes has been achieved based on the AMJUEL formalism, for inclusion in the SOLPS-ITER code suite and as a stand-alone tool. Two reduced schemes of 42 and 53 processes respectively are proposed to model NH3/ND3 formation in plasma edge conditions under the divertor and have been validated by model/experiment comparison. We demonstrate the use of these new nitrogen chemistry datasets in EIRENE runs on a fixed SOLPS-ITER plasma background for typical ITER radiative divertor conditions. First simulations clearly predict ammonia formation in significant amounts under the divertor, however they are very sensitive to the details of the wall chemistry model used. Further refinements of the EIRENE wall chemistry capabilities are planned to improve the predictive power of such simulations.

## **Acknowledgments**

ITER is the Nuclear Facility INB no. 174. This paper explores new directions for tritium inventory management that are not yet introduced into the ITER technical baseline. The nuclear operator is not constrained by the results presented here. The views and opinions expressed herein do not necessarily reflect those of the ITER Organization.

## **References**

- <span id="page-4-0"></span>[1] [M. Oberkofler, D. Alegre, F. Aumayr, S. Brezinsek, T. Dittmar, K. Dobes, D. Douai,](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0001) [A. Drenik, M. Köppen, U. Kruezi, Ch. Linsmeier, C.P. Lungu, G. Meisl, M. Mozetic,](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0001) [C. Porosnicu, V. Rohde, S.G. Romanelli, Plasma-wall interactions with nitrogen](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0001) [seeding in all-metal fusion devices: formation of nitrides and ammonia, Fusion Eng.](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0001) [Des. 98–99 \(2015\) 1371–1374.](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0001)
- [2] [M. Oberkofler, G. Meisl, A. Hakola, A. Drenik, D. Alegre, S. Brezinsek, R. Craven,](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0002) [T. Dittmar, T. Keenan, S.G. Romanelli, R. Smith, D. Douai, A. Herrmann, K. Krieger,](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0002) [U. Kruezi, G. Liang, Ch. Linsmeier, M. Mozetic, V. Rohde, Nitrogen retention me](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0002)[chanisms in tokamaks with beryllium and tungsten plasma-facing surfaces, Phys.](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0002) [Scr. T167 \(2016\) 014077.](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0002)
- <span id="page-4-1"></span>[3] [L. Laguardia, R. Caniello, A. Cremona, D. Dellasega, F. Dell'Era, F. Ghezzi, G. Gittini,](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0003) [G. Granucci, V. Mellera, D. Minelli, F. Pallotta, M. Passoni, D. Ricci, E. Vassallo,](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0003) [Ammonia formation and W coatings interaction with deuterium/nitrogen plasmas](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0003) [in the linear device GyM, J. Nucl. Mater. 463 \(2015\) 680–683.](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0003)
- [4] [V. Rohde, M. Oberkofler, the ASDEX upgrade team, ammonia production in](http://refhub.elsevier.com/S2352-1791(18)30105-4/sbref0004)

- nitrogen seeded plasma discharges in ASDEX upgrade, J. Nucl. Mater. 463 (2015) 672–675.
- <span id="page-5-0"></span>[5] R.A. Pitts, X. Bonnin, F. Escourbiac, T. Hirai, J.P. Gunn, A.S. Kukushkin, M. Lehnen, V. Rozhansky, E. Sytova, G. De Temmerman, Physics basis for the ITER tungsten divertor, these proceedings.
- <span id="page-5-1"></span>[6] X. Bonnin, W. Dekeyser, R. Pitts, D. Coster, S. Voskoboynikov, S. Wiesen, Presentation of the new SOLPS-ITER code package for tokamak plasma edge modelling, Plasma Fusion Res. 11 (2016) 1403102.
- [7] S. Wiesen, D. Reiter, V. Kotov, M. Baelmans, W. Dekeyser, A.S. Kukushkin, S.W. Lisgo, R.A. Pitts, V. Rozhansky, G. Saibene, I. Veselova, S. Voskoboynikov, The new SOLPS-ITER code package, J. Nucl. Mater. 463 (2015) 480.
- <span id="page-5-2"></span>[8] D. Reiter, R.K. Janev, Atomic and molecular processes in plasma surface interactions and boundary plasma science, these proceedings.
- <span id="page-5-3"></span>[9] D. Reiter, The data file AMJUEL: additional atomic and molecular data for EIRENE, v. March 8, 2016 available on http://www.eirene.de/amjuel.pdf.
- <span id="page-5-4"></span>[10] E. Carrasco, M. Jimenez-Redondo, I. Tanarro, V.J. Herrero, Neutral and ion chemistry in low pressure dc plasmas of H<sub>2</sub> /N<sub>2</sub> mixtures: routes for the effcient production of NH<sub>3</sub> and NH<sub>4</sub><sup>+</sup>, Phys. Chem. Chem. Phys. 13 (2011) 19561–19572.
- [11] E. Carrasco, M. Jimenez-Redondo, I. Tanarro, V.J. Herrero, Chemistry in low-pressure cold plasmas: ions of astrophysical interest, Plasma Phys. Control. Fusion 54 (2012) 124019.
- <span id="page-5-15"></span>[12] E. Carrasco, I. Tanarro, V.J. Herrero, J. Cernicharo, Proton transfer chains in cold plasmas of    with small amounts of   . The prevalence of   , Phys. Chem. Chem. Phys. 15 (2013) 1699–1706.
- <span id="page-5-5"></span>[13] M. Sode, W. Jacob, T. Schwarz-Selinger, H. Kersten, Measurement and modeling of neutral, radical, and ion densities in H<sub>2</sub>-N<sub>2</sub>-Ar plasmas, J. Appl. Phys. 117 (2015) 083303.
- <span id="page-5-6"></span>[14] R.K. Janev, Basic properties of fusion edge plasmas and role of atomic and molecular processes, in: R.K Janev (Ed.), Atomic and Molecular Processes in Fusion Edge Plasmas, Springer Science and Business Media Inc., New York, 1995, pp. 1–13.
- <span id="page-5-7"></span>[15] B. Gordiets, C.M. Ferreira, M.J. Pinheiro, A. Ricard, Self-consistent kinetic model of low-pressure N<sub>2</sub>–H<sub>2</sub> flowing discharges: I. Volume processes, Plasma Sources Sci. Technol. 7 (1998) 363–378.

- [16] B. Gordiets, C.M. Ferreira, M.J. Pinheiro, A. Ricard, Self-consistent kinetic model of low-pressure N<sub>2</sub>-H<sub>2</sub> flowing discharges: II. Surface processes and densities of N, H, NH<sub>3</sub> species, Plasma Sources Sci. Technol. 7 (1998) 379–388.
- [17] J. Hong, S. Pancheshnyi, E. Tam, J.J Lowke, S. Prawer, A.B Murphy, Plasma catalytic synthesis of ammonia using functionalized-carbon coatings in an atmospheric-pressure non-equilibrium discharge, J. Phys. D 50 (2017) 154005.
- <span id="page-5-8"></span>[18] S. Pancheshnyi, S. Biagi, M.C. Bordage, G.J.M. Hagelaar, W.L. Morgan, A.V. Phelps, L.C. Pitchford, The LXCat project: electron scattering cross sections and swarm parameters for low temperature plasma modelling, Chem. Phys. 398 (2012) 148–153.
- <span id="page-5-9"></span>[19] Y. Itikawa, Cross sections for electron collisions with nitrogen molecules, J. Phys. Chem. Ref. Data 35 (2006) 31–53.
- <span id="page-5-17"></span>[20] J.-S. Yoon, M.-Y. Song, J.-M. Han, S.H. Hwang, W.-S. Chang, B. Lee, Y. Itikawa, Cross sections for electron collisions with hydrogen molecules, J. Phys. Chem. Ref. Data 37 (2008) 913–931.
- [21] V. Tarnovsky, H. Deutsch, K. Becker, Cross-sections for the electron impact ionization of    (x = 1-3), Int. J. Mass Spectrom. Ion Proc. 167–168 (1997) 69–78.
- <span id="page-5-10"></span>[22] V.G. Anicich, Evaluated bimolecular ion-molecule gas phase kinetics of positive ions for use in modeling planetary atmospheres, cometary comae, and interstellar clouds, J. Phys. Chem. Ref. Data 22 (1993) 1469–1569.
- [23] V.G. Anicich, An Index of the Literature for Bimolecular Gas Phase Cation-Molecule Reaction Kinetics, JPL Publication, 2003 2003, 03-19 NASA.
- <span id="page-5-11"></span>[24] D. McElroy, C. Walsh, A.J. Markwick, M.A. Cordiner, K. Smith, T.J. Millar, The UMIST database for astrochemistry 2012, Astron. Astrophys. 550 (2013) paper A36.
- <span id="page-5-12"></span>[25] M. Capitelli, C.M. Ferreira, B.F. Gordiets, A.I. Osipov, Plasma Kinetics in Atmospheric Gases, Springer-Verlag, Berlin, Heidelberg, 2000.
- <span id="page-5-13"></span>[26] NIST Chemical Kinetics Database Standard Reference Database 17, Version 7.0 (Web Version), Release 1.6.8 Data Version 2016.10 kinetics.nist.gov/.
- <span id="page-5-14"></span>[27] G. Ertl, Reactions at surfaces: from atoms to complexity (nobel lecture), Angew. Chem. Int. 47 (2008) 3524–3535.
- <span id="page-5-16"></span>[28] K. Hassouni, A. Gicquel, M. Capitelli, J. Loureiro, Chemical kinetics and energy transfer in moderate pressure H<sub>2</sub> plasmas used in diamond MPACVD processes, Plasma Sources Sci. Technol. 8 (1999) 494–512.