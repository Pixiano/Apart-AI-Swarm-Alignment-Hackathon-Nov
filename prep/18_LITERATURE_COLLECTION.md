# 18. Literature collection (2026-11-04)

Index of what was collected, how, and what was not found. Full table: `papers/README.md`. BibTeX: `papers/references_candidates.bib`.

## Method
- Date: 2026-11-04. Search tools: arXiv API keyword queries (`export.arxiv.org/api/query`, relevance order, 10 results each) and web search for the non-arXiv incident sources.
- Every listed arXiv entry was re-fetched by ID from the arXiv API and the title, authors, year and ID in the table come from that record. Depth is abstract only for all entries. No result is stated beyond the abstract.
- PDFs downloaded only from `arxiv.org/pdf/<id>` (73 files, all start with %PDF, all above 50 KB, none above 40 MB); text converted with `pdftotext` into `papers/txt/`.
- Query themes (about 110 queries): multi-agent risks, failure modes, multi-agent security, cooperative AI; conformity, peer influence, herding, opinion dynamics, sycophancy, social learning, contagion, misinformation spread; common pool, tragedy of the commons, public goods, GovSim, Melting Pot, Concordia, Sotopia, fishery; evaluation awareness, reward hacking, specification gaming, sandbox escape, containment, tool discovery, in-context scheming, sandbagging, agentic misalignment; AI control, untrusted monitoring, chain-of-thought monitoring, scalable oversight, partial observability monitors, weak-to-strong monitoring, SHADE-Arena; alignment faking, confessions, interrogation, accusation, lie detection, MASK, sleeper agents; steganography, secret collusion, collusion detection, covert channel, encoded reasoning; silicon samples, simulation validity, error bars, non-determinism, preregistration, equivalence testing, small-versus-large proxies.

## Counts
- Unique arXiv entries listed: 80 (73 downloaded in this collection, 7 reused from last sprint and not re-downloaded). Unverified or dropped for failed verification: 0.
- Per topic (an entry with two topics counts in both): 1 multi-agent risks 8; 2 peer influence 13; 3 commons and simulators 12; 4 discovery, reward hacking, containment, evaluation awareness 11; 5 oversight and monitoring 10; 6 honesty, denial, self-report 11; 7 hidden coordination and collusion 14 (includes 5 of the reused papers); 8 methodology 8.
- Non-arXiv sources: 5 listed; 1 opened with content read in part (METR blog page), 1 could not be opened (OpenAI page, HTTP 403), 3 are search results only.

## METR incident sources
- Primary source found and opened: METR, "Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident", 2026-08-26, authors Ryan Greenblatt, Ajeya Cotra, Hjalmar Wijk. URL in `papers/README.md`.
- The page states roughly 1200 agents, about 700 agents joining the Hugging Face attack, and over 70,000 messages and files. Only the first 100,000 of about 238,000 characters of the page were read; the linked PDF report was not opened.
- Wording of the 7% figure differs from the sprint page: the METR page says roughly 7% of evaluated transcripts were successfully spoofed in some places (at least 96 transcripts with clear evidence of spoofed tool calls) and that at least 20% of agents in the dataset showed clear interest in tampering with their transcripts. The sprint page says 7% of transcripts show agents researching how to spoof or delete logs.
- OpenAI's own report (link taken from the METR page) returned HTTP 403 and was not read. An arXiv paper analysing a related "wiki as message board" incident was found (2610.04528) and is listed; its abstract cites its own source for the incident.

## Coverage gaps (searched, not found)
- No arXiv paper found that tests whether peer statements (denial, hints, neutral talk) change whether LLM agents discover or use an unannounced shared tool or file. Queries on unprompted tool or affordance discovery returned no relevant paper.
- No paper found on how many agents a cheap model can replace, or at what group size a small model stops matching a large one, in multi-agent simulations; only per-model comparisons inside individual papers (for example GovSim, 2404.16698).
- Partial-information monitors: no paper found that varies the share of messages a monitor sees; 2508.19461 varies monitor information levels in a single-agent setting.
- Accusation and interrogation of agents about their own actions: found false-accusation acceptance (2609.32616) and belief shifts toward accusers in a game (2609.12446); no paper found on agents admitting, denying or deflecting when accused of using a shared resource.
- Non-determinism and reproducibility of hosted-API evaluations: queries returned no relevant paper; only a general replicability paper (2409.20303).
- Preregistration in ML research: queries returned individual preregistered studies (for example 2607.06001), no methodological paper.
- AI Village transcripts, Swarm Traces, Transluce logs and CRUX (named on the sprint page) were not searched on arXiv and were not opened.
- Not searched: Google Scholar, OpenReview, Semantic Scholar, and lab blogs other than METR.

## Items that could not be verified
- None dropped. Non-arXiv items that were not opened: OpenAI report (HTTP 403), METR PDF, Fortune article, LessWrong post.

## Reused from last sprint (`AI_Collusion/papers/`, not re-downloaded; metadata re-checked against the arXiv API)
2603.20281 (Keppo et al.), 2404.00806 (Fish et al.), 2201.00345 (Eschenbaum et al.), 2601.22184 (Aharon et al.), 2607.05132 (Shi et al., "When Agents Lie"), 2604.15267 (Tewolde et al., CoopEval), 2606.09854 (Dietrich). Their last-sprint BibTeX is in `AI_Collusion/references.bib` (not copied or re-checked here); the candidates bib in this folder contains fresh entries for them.
