// NEPLv1 — en. 생성물: tools/render.py 가 NEPL-v1.en.md 에서 만든다. 손으로 고치지 않는다.
#set page(paper: "a4", margin: (x: 2.2cm, y: 2.4cm))
#set text(font: ("Noto Sans", "DejaVu Sans"), lang: "en", size: 10pt)
#set par(justify: false, leading: 0.68em)
#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 15pt)
#show heading.where(level: 2): set text(size: 11.5pt)

= NEWSNIPER Ethical Public License, Version 1 (NEPLv1)

Draft — not frozen; wording may change.

#strong[The Korean-language text is authoritative.] This English text is a convenience translation (clause 10.1).

This document is a #strong[template that may be applied to any repository as it stands.] Everything that varies between repositories — rightsholder, upstream work, separately licensed parts, governing law — is not written into the body but into the #strong[Application Notice] under clause 12.

#line(length: 100%, stroke: 0.4pt + gray)

== 0. About this licence — non-binding note

This licence is #strong[not an "open source" licence as defined by the Open Source Initiative, and not "free software" as defined by the Free Software Foundation.] Clause 5 restricts fields of endeavour (cf. OSD §6; FSF Freedom 0). That restriction is deliberate and will not be withdrawn. This licence is also #strong[not a Creative Commons licence] nor a modification of one; it is a standalone document and does not use the CC, MIT or BSD names or marks.

This clause 0 aids interpretation only and creates no rights or obligations.

#line(length: 100%, stroke: 0.4pt + gray)

== 1. Definitions

1.1 #strong["The Work"] means everything contained in the repository or distribution to which this licence is attached — documents, planning notes, scripts, diagrams, data, software, and derivatives thereof — excluding the #strong[Separately Licensed Parts] (clause 1.6).

1.2 #strong["Software Part"] means those portions of the Work that are executed or processed by machines: source code, object code, build scripts, configuration files and the like.

1.3 #strong["Textual Part"] means those portions of the Work that are not a Software Part: prose, planning notes, scripts, translations, diagrams, images, annotations and the like.

1.4 #strong["Upstream Work"] means any pre-existing work of which the Work is an adaptation, derivative, translation or arrangement, #strong[as listed in the Application Notice.] If the Application Notice lists none, the Work has no Upstream Work and #strong[clauses 4 and 6 do not apply.]

1.5 #strong["Upstream Rightsholder"] means the author of an Upstream Work personally, and any person or entity lawfully holding the economic copyright in it or an equivalent power to license it (including publishers and successors in title).

1.6 #strong["Separately Licensed Part"] means any part of the Work that carries its own licence notice or is so designated in the Application Notice. This licence has no effect on such a part; where there is a conflict, that part's own licence prevails.

1.7 #strong["Licensor"] means the holders of copyright in the Work who offer it under this licence, #strong[as identified in the Application Notice], together with other contributors.

1.8 #strong["You"] means the natural or legal person exercising rights under this licence.

1.9 #strong["Non-commercial"] means not primarily intended for or directed towards commercial advantage or monetary compensation. Recovery of actual costs (duplication, shipping, hosting), ordinary activity of a non-profit body, and sharing from a personal repository without advertising are non-commercial. Paid distribution, incorporation into an advertising- or subscription-funded service, and merchandising are commercial. In doubtful cases you may ask the Licensor.

1.10 #strong["Prohibited Use"] has the meaning given in clause 5.

1.11 #strong["Application Notice"] means the notice attached to the Work under clause 12.

#line(length: 100%, stroke: 0.4pt + gray)

== 2. Grant of rights

Subject to the conditions in clause 3 and to the limitation in clause 5, the Licensor grants You a #strong[worldwide, royalty-free, non-exclusive, perpetual] licence to:

2.1 #strong[As to the Software Part] — use, reproduce, modify, merge, publish, distribute and deploy it, in source or object form, with or without modification, #strong[including for commercial purposes].

2.2 #strong[As to the Textual Part] — reproduce, distribute, display, perform and translate it, and create adaptations of it, #strong[for non-commercial purposes only] and subject to the share-alike condition in clause 3.3. #emph[(Where the Application Notice permits commercial use of the Textual Part as well, that permission governs.)]

2.3 This grant extends only so far as the Licensor holds rights to grant. See clause 6.

#line(length: 100%, stroke: 0.4pt + gray)

== 3. Conditions

3.1 #strong[Attribution.] When distributing or publishing the Work or a derivative of it, You shall state, in a manner reasonable to the medium: the author named in the Application Notice; the name of this licence and where it may be obtained; and, if You have made changes, that changes were made. The form and placement of the notice may be adapted to the medium.

3.2 #strong[Preservation of notices.] You shall include a copy of this licence, the Application Notice and the copyright notices with the distribution. Where a Software Part is distributed in object form only, inclusion in documentation, an "about" screen, or an accompanying file suffices.

3.3 #strong[Share-alike — Textual Part only.] If You modify a Textual Part, or create an adaptation from one, and distribute the result, You shall distribute that result as a whole under this licence or a later version of it. This condition does not apply to the Software Part.

3.4 #strong[No implication of endorsement.] You shall not represent the Work as official material of an Upstream Work, or as approved, endorsed or sponsored by an Upstream Rightsholder. You shall not use the Licensor's name or marks to promote the Work without permission.

#line(length: 100%, stroke: 0.4pt + gray)

== 4. Accommodation for the Upstream Rightsholder

#emph[(Applies only where there is an Upstream Work — clause 1.4.)]

4.1 If You are an #strong[Upstream Rightsholder], clause 3.1 (attribution), clause 3.3 (share-alike) and the #strong[non-commercial limitation] in clause 2.2 do not apply to You. The Licensor separately grants each Upstream Rightsholder an #strong[additional permission] to incorporate, adapt and exploit the whole of the Work in the Upstream Work and its derivative works, #strong[without any obligation of attribution and including commercial exploitation.]

4.2 Even so, #strong[attribution is recommended.] The Licensor will assert no claim by reason of an Upstream Rightsholder's omission of attribution, and undertakes not to exercise moral rights to that extent (in jurisdictions where moral rights cannot be waived, this sentence is to be read as a covenant not to exercise them).

4.3 This accommodation #strong[does not override clause 5.] Prohibited Uses are not permitted to an Upstream Rightsholder either.

4.4 This accommodation is not conditioned on an Upstream Rightsholder accepting the other terms of this licence. An Upstream Rightsholder may rely on the additional permission in clause 4.1 alone.

#line(length: 100%, stroke: 0.4pt + gray)

== 5. Prohibited Uses — excluded from the scope of the grant

5.1 No permission granted by this licence #strong[extends to] the following uses. This is not a promise You make; it is a #strong[limitation on the scope of the grant itself], so that any such use is an unlicensed use and therefore an infringement of copyright.

(a) #strong[Crimes against humanity] — committing, attempting, ordering, soliciting, inducing, aiding or abetting any act described in Article 7 of the Rome Statute of the International Criminal Court, or using the Work to prepare, direct, conceal or justify such an act.

(b) #strong[War crimes] — as in (a), with respect to acts described in Article 8 of that Statute. Genocide (Article 6) and the crime of aggression (Article 8 bis) are likewise included.

(c) #strong[Crimes against children] — offences whose victim is a person under 18 years of age, in particular sexual exploitation and abuse of children, the production, possession or distribution of child sexual abuse material, child trafficking, forced child labour, and the use of children in armed conflict (by reference to the UN Convention on the Rights of the Child and its Optional Protocols, and to the law of the place of use).

5.2 Where the law of the place of use defines any of (a) to (c) more broadly, that law governs. Whether conduct falls within the wording of the instruments above is assessed independently of whether it has in fact been prosecuted before any international tribunal.

5.3 This limitation is #strong[permanent] and is not relaxed by clause 4, by the cure provision in clause 8, by the Application Notice, or by any other provision.

5.4 Use for academic research, journalism, human-rights documentation, education, law enforcement, or for recording, exposing, preventing or punishing the above crimes is #strong[not] a Prohibited Use.

#line(length: 100%, stroke: 0.4pt + gray)

== 6. Reservation of rights in the Upstream Work

#emph[(Applies only where there is an Upstream Work — clause 1.4.)]

6.1 The Work is an #strong[unofficial derivative work] based on the Upstream Work. All rights in the Upstream Work remain with its rightsholders.

6.2 This licence grants rights #strong[only in the Licensor's own creative contribution.] It grants no rights in elements originating in the Upstream Work, and the Licensor is in no position to grant such rights.

6.3 You are responsible for obtaining for Yourself any permission that the law of the place of use requires in respect of the Upstream Work before You use the Work.

6.4 If an Upstream Rightsholder requests the removal or withdrawal of all or part of the Work, the Licensor may comply, and doing so is not a breach of this licence. Rights already held by You in copies already distributed are not thereby extinguished retroactively.

#line(length: 100%, stroke: 0.4pt + gray)

== 7. No warranty; limitation of liability

7.1 The Work is provided #strong["as is"], without warranty of any kind, express or implied, including warranties of merchantability, fitness for a particular purpose and non-infringement.

7.2 To the fullest extent permitted by law, the Licensor shall not be liable for any damages arising from the use of, or inability to use, the Work.

7.3 #strong[However,] clauses 7.1 and 7.2 do not apply to damage caused by the Licensor's #strong[intent or gross negligence], to injury to life, body or health, or to any damage for which the governing law forbids exclusion. This clause is to be read down, so far as necessary, to conform to the mandatory rules of each jurisdiction (for example: §§305 ff. of the German Bürgerliches Gesetzbuch on standard terms; the Korean Act on the Regulation of Terms and Conditions; the UK Unfair Contract Terms Act 1977 and Consumer Rights Act 2015).

#line(length: 100%, stroke: 0.4pt + gray)

== 8. Breach and termination

8.1 If You breach a condition in clause 3, Your rights under this licence #strong[terminate automatically.]

8.2 If the breach is not one falling under clause 5, and You cure it within #strong[30 days] of becoming aware of it or being notified of it, Your rights are #strong[reinstated as if they had never terminated] — unless the Licensor has expressly and finally terminated them.

8.3 #strong[The cure in clause 8.2 does not apply to a breach of clause 5,] because such use lies outside the scope of the grant and no rights under this licence ever existed in respect of it.

8.4 The rights of third parties who have lawfully received copies from You are not affected by the termination of Your rights.

#line(length: 100%, stroke: 0.4pt + gray)

== 9. Governing law and severability

9.1 This licence is governed by the #strong[law stated in the Application Notice], or, failing such a statement, by the #strong[law of the Republic of Korea.] Where You are a consumer, the mandatory protections of the law of Your habitual residence are not displaced by this clause.

9.2 If any provision is invalid or unenforceable in a given jurisdiction, the remaining provisions are unaffected. An invalid provision shall be #strong[read down to the largest valid scope closest to its purpose.]

9.3 If the mandatory law of a jurisdiction voids a field-of-use restriction such as clause 5, that restriction shall nevertheless survive as a #strong[contractual covenant] to the extent it is valid.

#line(length: 100%, stroke: 0.4pt + gray)

== 10. Versions and translations

10.1 The #strong[Korean text is authoritative.] The English, Japanese and German texts are convenience translations; in case of divergence, the Korean text prevails.

10.2 The Licensor may publish later versions of this licence. Where the Application Notice states "NEPLv1 or any later version", You may choose any version. Where no version is stated, version 1 applies.

10.3 This licence document itself #strong[may be copied and distributed verbatim, and may be applied by anyone to their own work.] You may create modified versions, but if You do, #strong[You shall not use the name "NEWSNIPER Ethical Public License" or the abbreviation "NEPL".]

#line(length: 100%, stroke: 0.4pt + gray)

== 11. Spirit — non-binding postscript

Three things are asked of anyone who uses this licence. #strong[Do not pass off as your own what someone else made. Do not use it to harm people. And if you are standing on something, do not forget that it is there.]

This clause creates no rights or obligations.

#line(length: 100%, stroke: 0.4pt + gray)

== 12. Application Notice — how to apply this licence to your own work

Place a `LICENSE` (or `NOTICE`) file at the top of the repository and complete the following form. Items left blank are treated as "none".

#block(width: 100%, fill: luma(245), inset: 8pt, radius: 2pt, raw("NEWSNIPER Ethical Public License v1 — Application Notice\n\nWork:              <name / repository>\nLicensor:          <name or organisation> <contact (optional)>\nCopyright:         Copyright (c) <year> <name>\nVersion:           NEPLv1            (or \"NEPLv1 or any later version\")\nFull licence text: LICENSES/NEPL-v1.ko.md  (en / ja / de translations enclosed)\n\nUpstream Work:     <title, author, rightsholder — or \"none\"; if none, clauses 4 and 6 do not apply>\nSeparately Licensed Parts:\n                   <path> — <licence> (<copyright holder>)\n                   ...\nCommercial use of the Textual Part:  not permitted (default)  |  permitted (relaxing clause 2.2)\nGoverning law:     <country>   (default: Republic of Korea)"))

The Application Notice is treated as part of this licence, and #strong[no statement in it that would relax clause 5 has any effect.]

12.1 #strong[The one express, unconditional permission in this licence.] This licence #strong[says nothing whatsoever about the document format] in which it and the Application Notice are to be written or enclosed. Plain text, Markdown, HTML, PDF, reStructuredText, AsciiDoc, Typst, LaTeX, ODF, images, audio, braille — any of these will do; file names and extensions are free; several formats may be provided together. It suffices that a person can read it by ordinary means and that #strong[the wording is unaltered.] This permission is granted unconditionally, and no other clause limits it.

#line(length: 100%, stroke: 0.4pt + gray)

#emph[NEWSNIPER Ethical Public License v1 — draft. The final wording is subject to legal review. This document is not legal advice.]
