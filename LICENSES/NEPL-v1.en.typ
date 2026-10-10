// NEPLv1 — en. 생성물: tools/render.py 가 NEPL-v1.en.md 에서 만든다. 손으로 고치지 않는다.
#set page(paper: "a4", margin: (x: 2.2cm, y: 2.4cm))
#set text(font: ("Noto Sans", "DejaVu Sans"), lang: "en", size: 10pt)
#set par(justify: false, leading: 0.68em)
#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 15pt)
#show heading.where(level: 2): set text(size: 11.5pt)

= NEWSNIPER Ethical Public License, Version 1 (NEPLv1)

Draft, second revision — not frozen; wording may change.

#strong[This is a translation; the Korean text is authoritative] (clause 10.1).

This document is a #strong[template that may be applied to any repository as it stands.] Everything that varies between repositories — rightsholder, upstream work, separately licensed parts, governing law, optional conditions — is not written into the body but into the #strong[Application Notice] under clause 12.

#line(length: 100%, stroke: 0.4pt + gray)

== 0. About this licence

0.1 #strong[Non-binding note.] This licence is #strong[not an "open source" licence as defined by the Open Source Initiative, and not "free software" as defined by the Free Software Foundation.] Clause 5 restricts fields of endeavour (cf. OSD §6; FSF Freedom 0). That restriction is deliberate and will not be withdrawn. This licence is also #strong[not a Creative Commons licence] nor a modification of one; it is a standalone document and does not use the CC, MIT or BSD names or marks. This clause aids interpretation only and creates no rights or obligations.

0.2 #strong[Nature and acceptance.] This licence is a #strong[unilateral grant of permission] made by the Licensor to the world at large. You need not accept this licence in order to receive or possess a copy of the Work. However, nothing outside this licence gives You any title to use the Work; accordingly, if You reproduce, distribute, adapt or communicate the Work to the public, or do anything else that only the grant in clause 2 makes lawful, You thereby accept all the terms of this licence, including the limitation in clause 5 and clauses 7 and 9. Unless You exercise rights under this licence, You are under no obligation. This clause does not alter the character of clause 5 as a #strong[limitation on the scope of the grant] (clause 5.1).

0.3 #strong[Patents — not granted.] #strong[This licence grants no patent rights whatsoever.] If the use of the Work requires a patent licence, You are responsible for obtaining one Yourself. This clause is neither a promise to assert, nor a waiver of, any patent held by the Licensor.

0.4 The Licensor shall enclose the full text of this licence and the Application Notice with every distribution of the Work, so that You may read them before use (clause 3.2).

#line(length: 100%, stroke: 0.4pt + gray)

== 1. Definitions

1.1 #strong["The Work"] means everything contained in the repository or distribution to which this licence is attached — documents, planning notes, scripts, diagrams, data, software, and derivatives thereof — excluding the #strong[Separately Licensed Parts] (clause 1.6) and anything the Application Notice #strong[excludes from the grant].

1.2 #strong["Software Part"] means those portions of the Work that are #strong[written to direct the operation of a machine as such]: source code, object code, build scripts and configuration files. A file written in a typesetting or markup language in order to carry human-readable prose does not become a Software Part merely because a tool processes it.

1.3 #strong["Textual Part"] means those portions of the Work that are not a Software Part: prose, planning notes, scripts, translations, diagrams, images, annotations and the like.

1.3.1 #strong[Character is determined file by file.] A file not designated as a Software Part by the Application Notice is a Textual Part. Comments and strings inside a file that is a Software Part are Software Part along with that file. #strong[A file whose character is unclear is a Textual Part.] The character of output produced by running a Software Part follows the character of that output itself; but output generated from a Textual Part as input is a Textual Part.

1.4 #strong["Upstream Work"] means any pre-existing work of which the Work is an adaptation, derivative, translation or arrangement, #strong[as listed in the Application Notice.] If the Application Notice lists none, the Work has no Upstream Work and #strong[clauses 4 and 6 do not apply.]

1.5 #strong["Upstream Rightsholder"] means the author of an Upstream Work personally, and any person or entity lawfully holding the economic copyright in it or an equivalent power to license it (including publishers and successors in title).

1.6 #strong["Separately Licensed Part"] means any part of the Work that carries its own licence notice or is so designated in the Application Notice. This licence has no effect on such a part; where there is a conflict, that part's own licence prevails.

1.7 #strong["Licensor"] means the holders of copyright in the Work who offer it under this licence, being those #strong[identified in the Application Notice] and those who have #strong[contributed under clause 3.5].

1.8 #strong["You"] means the natural or legal person exercising rights under this licence.

1.9 #strong["Non-commercial"] means not primarily intended for or directed towards commercial advantage or monetary compensation.

(a) Recovery of actual costs (duplication, shipping, hosting), the ordinary activity of a non-profit body, and sharing from a personal repository without advertising are non-commercial.

(b) Paid distribution, incorporation into an advertising- or subscription-funded service, and merchandising are commercial.

(c) #strong[Machine learning.] Using the Work to train, fine-tune or retrieval-augment a machine-learning model is non-commercial #strong[only where both that model and any service using it are provided non-commercially.] Supplying it as training data for a model used in a product or service that is offered for a fee or funded by advertising or subscription is commercial; so is supplying the model's weights for a fee.

(d) In doubtful cases You may ask the Licensor in writing. #strong[The Licensor's reply is an opinion for guidance and does not bind the construction of this clause], nor does it give the Licensor an exclusive right to interpret this licence. Silence by the Licensor is neither consent nor refusal.

1.10 #strong["Prohibited Use"] has the meaning given in clause 5.

1.11 #strong["Application Notice"] means the notice attached to the Work under clause 12.

1.12 #strong["Licence Steward"] means the person who publishes and revises this licence document — the original publisher of this licence and any successor designated by them in writing. The Steward is distinct from the Licensor of any particular work (clause 1.7) and cannot be changed by an Application Notice.

#line(length: 100%, stroke: 0.4pt + gray)

== 2. Grant of rights

Subject to the conditions in clause 3 and to the limitation in clause 5, the Licensor grants You a #strong[worldwide, royalty-free, non-exclusive, perpetual and irrevocable] right as follows. The Licensor shall not revoke this grant at will; ceasing to distribute the Work, or making the repository private, does not affect the rights of anyone who lawfully obtained the Work under this licence beforehand. This grant terminates only as provided in clause 8.

2.1 #strong[As to the Software Part] — use, reproduce, modify, merge, #strong[communicate to the public (including making available online)], distribute, rent and deploy it, in source or object form, with or without modification, #strong[including for commercial purposes].

2.2 #strong[As to the Textual Part] — reproduce, distribute, rent, #strong[communicate to the public (including making available online, broadcasting and digital audio transmission)], display, publicly perform and translate it, and create adaptations of it and use those adaptations. This is #strong[for non-commercial purposes only.] #emph[(Where the Application Notice permits commercial use of the Textual Part, that permission governs. Where the Application Notice specifies share-alike, clause 3.3 applies.)]

2.3 This grant extends only so far as the Licensor holds rights to grant. See clause 6.

2.4 The names of the acts of use given in this clause are #strong[illustrative]; the grant extends to every exclusive right comprised in the copyright held by the Licensor. Where the law of the place of use calls a corresponding right by another name, the grant extends to that right also.

2.5 #strong[Consideration and downstream recipients.] Your performance of the conditions in clause 3 constitutes consideration for this grant. Even if, under a governing law requiring consideration, this grant were held not to be binding for want of it, the grant in clause 2 retains effect as a licence under copyright law, so that use within its scope is not an infringement. Each time You distribute the Work or a derivative of it, the recipient becomes a "You" in their own right under clause 1.8 and receives a licence #strong[directly from the Licensor] — that licence is not derived from Yours, and is unaffected if Your rights terminate under clause 8. You may not impose on recipients any restriction that this licence does not provide.

2.6 #strong[Nothing in this clause is to be construed as a grant of patent rights] (clause 0.3).

#line(length: 100%, stroke: 0.4pt + gray)

== 3. Conditions

3.1 #strong[Attribution.] When distributing or publishing the Work or a derivative of it, You shall state, in a manner reasonable to the medium: the author named in the Application Notice; the name of this licence and where it may be obtained; and, if You have made changes, that changes were made. The form and placement of the notice may be adapted to the medium.

3.2 #strong[Preservation of notices.] You shall include a copy of this licence, the Application Notice and the copyright notices with the distribution. Where a Software Part is distributed in object form only, inclusion in documentation, an "about" screen, or an accompanying file suffices.

3.3 #strong[Share-alike — optional condition.] #strong[This condition applies only where the Application Notice states "Share-alike: applies".] In that case, if You modify a Textual Part or create an adaptation from one and distribute the result, You shall distribute #strong[that adaptation] under this same licence. It does not apply to: the Software Part; a Separately Licensed Part (clause 1.6); or a mere aggregation of separate works that does not form a single work (it then applies only to the part that is this Work). #strong[If the Application Notice says nothing, this condition does not apply.]

3.4 #strong[No implication of endorsement.] You shall not represent the Work as official material of an Upstream Work, or as approved, endorsed or sponsored by an Upstream Rightsholder. You shall not use the Licensor's name or marks to promote the Work without permission.

3.5 #strong[Contributions.] If You submit a contribution to the Work, then in the absence of a separate written agreement that contribution is taken to be provided under this same licence, as a Software Part or a Textual Part according to its character. You represent that You are entitled so to provide it. #strong[You agree that the additional permission in clause 4 extends to Your contribution for the benefit of Upstream Rightsholders, and You accept the treatment of moral rights set out in clause 4.2 to the same extent] — provided that, in jurisdictions requiring a waiver or consent to be in writing, this takes effect only where You have done so in writing (including electronically). This clause does not affect Your status as an author.

#line(length: 100%, stroke: 0.4pt + gray)

== 4. Accommodation for the Upstream Rightsholder

#emph[(Applies only where there is an Upstream Work — clause 1.4.)]

4.1 If You are an #strong[Upstream Rightsholder], #strong[none of the conditions in clause 3] (3.1 attribution, 3.2 preservation of notices, 3.3 share-alike, 3.4 no implication of endorsement) and #strong[not the non-commercial limitation] in clause 2.2 apply to You. The Licensor grants each Upstream Rightsholder, irrespective of whether they accept any other term of this licence, a #strong[worldwide, royalty-free, non-exclusive, perpetual and irrevocable additional permission] over the whole of the Work — to incorporate, adapt and exploit it in the Upstream Work and its derivative works, without any obligation of attribution and including commercial exploitation. This additional permission is not an exclusive licence and is not an assignment of copyright. The second sentence of clause 3.4 (not using the Licensor's name or marks to promote the Work without permission) continues to apply.

4.1.1 Where an Upstream Rightsholder has incorporated the Work into the Upstream Work under clause 4.1, #strong[presenting the result as official material of the Upstream Work is not a representation prohibited by clause 3.4.]

4.1.2 An Upstream Rightsholder #strong[may sublicense] the additional permission in clause 4.1, to the extent necessary, to third parties whom they have authorised for the publication, translation, adaptation to other media, or merchandising of the Upstream Work. To that extent, Article 46(3) of the Korean Copyright Act and corresponding provisions in other jurisdictions do not apply.

4.1.3 The additional permission survives in favour of successors if the Licensor assigns the economic copyright or upon succession on death.

4.2 Even so, #strong[attribution is recommended.] As to moral rights, the following applies #strong[automatically], and #strong[the strongest step permitted by the law of the place of use] takes effect.

(a) #strong[Where waiver is permitted, the Licensor waives.] Within the scope of use defined in clause 4.1, the Licensor #strong[waives] the rights of attribution and integrity and any equivalent rights (e.g. Canadian Copyright Act s.14.1(2); UK CDPA s.87(2)).

(b) Where waiver is not permitted but #strong[consent is], the Licensor #strong[consents in advance] to such use and modification (e.g. Australian Copyright Act ss.195AW, 195AWA).

(c) Where neither waiver nor consent is permitted, the Licensor #strong[undertakes as a matter of contract not to exercise moral rights] within that scope, and #strong[agrees not to sue] in respect of them — e.g. Korean Copyright Act art. 14; Japanese Copyright Act art. 59; German UrhG §13; Austrian UrhG §19; Swiss URG art. 9.

(d) #strong[At every step above], this treatment is confined to the scope of use defined in clause 4.1 and does not extend to #strong[modifying or using the Work in a manner prejudicial to the Licensor's honour or reputation], nor to #strong[presenting the Work as the creation of a third party other than an Upstream Rightsholder.] This proviso is the minimum that mandatory law requires.

4.3 This accommodation #strong[does not override clause 5.] Prohibited Uses are not permitted to an Upstream Rightsholder either.

4.4 This accommodation is not conditioned on an Upstream Rightsholder accepting the other terms of this licence. An Upstream Rightsholder may rely on the additional permission in clause 4.1 alone.

#line(length: 100%, stroke: 0.4pt + gray)

== 5. Prohibited Uses — excluded from the scope of the grant

5.1 No permission granted by this licence #strong[extends to] reproduction, distribution, communication to the public, display, public performance or the making of adaptations for the following uses. The Licensor does not licence use for those purposes at all, and accordingly no title to use arises under this licence in respect of them.

(a) #strong[Crimes against humanity] — use in order to commit or attempt any act described in Article 7 of the Rome Statute of the International Criminal Court, or to #strong[order, solicit, induce], or to #strong[aid, abet or otherwise assist in or contribute to] its commission; use to prepare, direct or conceal such an act; or use to advocate, incite or justify it in a manner that constitutes an offence under the law of the place of use or under international law. The modes of participation are to be read by reference to Article 25(3) of that Statute.

(b) #strong[War crimes] — as in (a), with respect to acts described in Article 8 of that Statute.

(c) #strong[Genocide] (Article 6 of that Statute) and the #strong[crime of aggression] (Article 8 bis) — as in (a).

(d) #strong[Crimes against children] — as in (a), with respect to the sexual exploitation and abuse of persons under 18 years of age, the production, possession, distribution or public exhibition of child sexual abuse material, child trafficking, forced child labour, the use of children in armed conflict, and other offences against the life, body or sexual self-determination of children (by reference to the UN Convention on the Rights of the Child and its Optional Protocols, and to the law of the place of use).

5.2 Where the law of the place of use defines any of (a) to (d) #strong[more broadly, that law governs.] However, an extension whose purpose is not the protection of human rights but the suppression of freedom of expression, association or the press is not an extension for the purposes of this clause. Whether conduct falls within the wording of the instruments above is assessed independently of whether it has in fact been prosecuted before any international tribunal. "Place of use" means where You perform the act of use and where its effects are felt.

5.3 This limitation is #strong[permanent] and is not relaxed by clause 4, by the cure provision in clause 8, by the Application Notice, or by any other provision.

5.4 Use for academic research, journalism, human-rights documentation, education, #strong[lawful] law enforcement and judicial proceedings, personal commentary, criticism, satire or fiction that does not advocate or incite any act in clause 5.1, or use to record, expose, prevent, investigate, prosecute or punish those crimes, #strong[in conformity with the law of the place of use], is not a Prohibited Use.

This does not apply where the use itself constitutes, or contributes to the commission of, an act falling under clause 5.1, #strong[and that is so even where it bears the appearance of law enforcement, public order or national security. This clause does not prevail over clause 5.1.] Nor is this clause to be read as permitting conduct that the law of the place of use prohibits regardless of purpose (for example, the production, provision or possession of child sexual abuse material).

5.5 #strong[Legal character.] The limitation in clause 5.1 is #strong[primarily one upon the scope of the grant made by clause 2.] Only where the governing law does not recognise it as a limitation of scope, or characterises it as a contractual obligation, does it subsist as a #strong[contractual obligation] owed by You to the Licensor (clause 9.3). On either footing the Licensor may seek to restrain the use, recover damages, and have infringing articles destroyed.

#line(length: 100%, stroke: 0.4pt + gray)

== 6. Reservation of rights in the Upstream Work

#emph[(Applies only where there is an Upstream Work — clause 1.4.)]

6.1 The Work is an #strong[unofficial derivative work] based on the Upstream Work. All rights in the Upstream Work remain with its rightsholders.

6.2 This licence grants rights #strong[only in the Licensor's own creative contribution.] It grants no rights in elements originating in the Upstream Work, and the Licensor is in no position to grant such rights. #strong[The Textual Part may contain expression originating in the Upstream Work in a manner not readily separable, and the Licensor's permission alone does not make use lawful as against the Upstream Rightsholder.]

6.3 Before using the Work, You are responsible for #strong[judging for Yourself] whether that use requires permission in respect of the Upstream Work under the law of the place of use. Where that law limits the economic rights of the author — quotation, criticism, research, reporting and the like (e.g. Korean Copyright Act arts. 28 and 35-5) — no separate permission is required. The Licensor gives no warranty as to that judgement.

6.4 If an Upstream Rightsholder requests the removal or withdrawal of all or part of the Work, the Licensor may comply, and doing so is not a breach of this licence. #strong[Your rights in copies already distributed are not thereby extinguished.]

6.5 At the request of an Upstream Rightsholder the Licensor may #strong[cease future distribution] under this licence; such cessation is not a revocation of permissions already granted.

#line(length: 100%, stroke: 0.4pt + gray)

== 7. No warranty; limitation of liability

7.1 The Work is provided #strong["as is"], without warranty of any kind, express or implied, including warranties of merchantability, fitness for a particular purpose and non-infringement. Regard is to be had to the fact that the Work is provided #strong[free of charge] and that the Licensor has disclosed the defect in title in advance under clause 6.

7.2 To the fullest extent permitted by law, the Licensor shall not be liable for any damages arising from the use of, or inability to use, the Work.

7.3 #strong[However,] clauses 7.1 and 7.2 do not apply to: damage caused by intent or fraud on the part of the Licensor #strong[or the Licensor's legal representatives or persons used in performance]; damage caused by a #strong[gross want] of the care ordinarily to be observed by the Licensor; damage from injury to life, body or health, #strong[irrespective of the degree of fault]; liability under a warranty expressly assumed by the Licensor; and any damage for which the governing law #strong[or the mandatory law of the place of use] forbids exclusion. Where an obligation essential to the attainment of the purpose of the agreement is breached through slight negligence, the Licensor's liability is limited to the damage typically foreseeable in an agreement of this kind. Clauses 7.1 and 7.2 apply as read down to the extent the mandatory rules of the place of use require, the remainder continuing in effect. Examples of such mandatory rules are set out in #strong[Annex A].

#line(length: 100%, stroke: 0.4pt + gray)

== 8. Breach and termination

8.1 If You use the Work #strong[beyond the scope of the grant in clause 2] (including the non-commercial limitation in clause 2.2) or breach a condition in clause 3, Your rights under this licence #strong[terminate automatically.] Use beyond the scope of clause 2 was never licensed.

8.2 If the breach is not one falling under clause 5 and You #strong[cease] the breach, Your rights are #strong[provisionally reinstated] and continue unless and until the Licensor terminates them expressly and finally. Further, if You cure the breach within #strong[30 days of receiving notice of it from the Licensor], or, having received no notice, within #strong[30 days of first becoming aware of it], Your rights are #strong[reinstated as if they had never terminated, and that reinstatement does not depend on the Licensor's will.]

8.2.1 The Licensor may terminate Your rights finally only where the breach remains uncured after the cure period in clause 8.2, by notice in writing (including electronically) stating the grounds. A notice of termination given before or during the cure period has effect only as a notice under clause 8.2. Notice is to be given to the address stated in the Application Notice and is deemed received 7 days after dispatch.

8.2.2 #strong[If the Licensor does not give notice of a breach within 60 days of becoming aware of it, Your rights are definitively reinstated.]

8.3 #strong[The cure in clause 8.2 does not apply to a breach of clause 5,] because such use lies outside the scope of the grant and no rights under this licence ever existed in respect of it.

8.4 The rights of third parties who have lawfully received copies from You are not affected by the termination of Your rights (clause 2.5).

#line(length: 100%, stroke: 0.4pt + gray)

== 9. Governing law and severability

9.1 This licence is governed by the #strong[law stated in the Application Notice], or, failing such a statement, by the #strong[law of the Republic of Korea.] Where You are a consumer, the mandatory protections of the law of Your habitual residence are not displaced by this clause.

9.1.1 #strong[The existence, ownership and infringement of copyright, and the remedies for it, are governed by the law of the country for which protection is claimed] (the copyright law of the place of use). The choice of law in clause 9.1 concerns the contractual aspects of this licence. #strong[This licence makes no provision as to jurisdiction.]

9.2 If any provision is invalid or unenforceable in a given jurisdiction, the remaining provisions are unaffected. #strong[The place of an invalid provision is taken by the statutory rules of that jurisdiction.] Only where the law of that jurisdiction permits it do the Licensor and You agree to replace the provision with a valid one closest to its purpose. #strong[Where the mandatory law of that jurisdiction does not permit such reduction or replacement (for example, §306(2) of the German Civil Code), the provision is wholly ineffective in that jurisdiction.]

9.3 The limitation in clause 5 is primarily one upon the scope of the grant (clause 5.5); but where the mandatory law of a jurisdiction voids field-of-use restrictions, or a court #strong[characterises it as a contractual obligation], the restriction subsists as a contractual obligation to the extent it is valid.

#line(length: 100%, stroke: 0.4pt + gray)

== 10. Versions and translations

10.1 The #strong[Korean text is authoritative.] The English, Japanese and German texts are convenience translations; in case of divergence, the Korean text prevails.

10.2 #strong[Fixed versions.] New versions of this licence are published #strong[only by the Licence Steward (clause 1.12).] An individual Licensor may not publish a new version. #strong[Only the version stated in the Application Notice applies to a given work; no option such as "or any later version" is provided.] A Licensor who wishes to move to a new version must amend the Application Notice and distribute anew, without effect on permissions already granted. #strong[No version may delete the Prohibited Uses in clause 5 or narrow or relax their substantive scope; a document without such a restriction is not a version of this licence.]

10.3 This licence document itself #strong[may be copied and distributed verbatim, and may be applied by anyone to their own work.] You may create modified versions, but if You do, #strong[You shall not use the name "NEWSNIPER Ethical Public License" or the abbreviation "NEPL".] However, #strong[translating this licence into another language is permitted and such a translation may bear the name of this licence] — a translation shall state that it is a translation and that the Korean text is authoritative.

10.4 #strong[Extensions.] Where further clauses are needed to carry out the purpose of this licence, #strong[the Licence Steward (clause 1.12) may publish an "Extension" to be applied on top of this licence.] An Extension does not replace this licence and #strong[has effect only where it is applied together with it]; its name may combine the name of this licence with a suffix, and in that case the naming restriction in clause 10.3 does not apply. #strong[Extensions are optional] — an Extension binds a work only where the Application Notice names it, and where none is named there is none. And #strong[an Extension may do only two things: narrow the scope of the grant in clause 2, and add conditions.] An Extension may not delete any provision of this licence or weaken its protections, and #strong[the last sentence of clause 10.2 applies to Extensions as well.]

#line(length: 100%, stroke: 0.4pt + gray)

== 11. Spirit — non-binding postscript

Three things are asked of anyone who uses this licence. #strong[Do not pass off as your own what someone else made. Do not use it to harm people. And if you are standing on something, do not forget that it is there.]

This clause creates no rights or obligations.

#line(length: 100%, stroke: 0.4pt + gray)

== 12. Application Notice — how to apply this licence to your own work

Place a `LICENSE` (or `NOTICE`) file at the top of the repository and complete the following form. Items left blank are treated as "none".

#block(width: 100%, fill: luma(245), inset: 8pt, radius: 2pt, raw("NEWSNIPER Ethical Public License v1 — Application Notice\n\nWork:              <name / repository>\nLicensor:          <name or organisation>\nNotices to:        <address or e-mail>    (where notice under clause 8.2.1 is to reach)\nCopyright:         Copyright (c) <year> <name>\nVersion:           NEPLv1\nExtensions:        <none | e.g. NEPLv1-EP>   (clause 10.4 — none unless named)\nFull licence text: <path>\n\nUpstream Work:     <if any: title, author, rightsholder; otherwise \"none\" —\n                    clauses 4 and 6 then do not apply>\nSeparately Licensed Parts:\n                   <path> — <licence> (<copyright holder>)\nExcluded from the grant:\n                   <path or condition>    (clause 1.1 — may be omitted)\n\nSoftware Part:            <paths>   (files not listed are Textual Part — clause 1.3.1)\nCommercial use of the Textual Part:  not permitted (default)  |  permitted\nShare-alike (clause 3.3):            does not apply (default) |  applies\nGoverning law:     <country>              (default: Republic of Korea)"))

The Application Notice is treated as part of this licence, and #strong[no statement in it that would relax clause 5 has any effect.]

12.1 #strong[The one express, unconditional permission in this licence.] This licence #strong[says nothing whatsoever about the document format] in which it and the Application Notice are to be written or enclosed. Plain text, Markdown, HTML, PDF, reStructuredText, AsciiDoc, Typst, LaTeX, ODF, images, audio, braille — any of these will do; file names and extensions are free; several formats may be provided together. It suffices that a person can read it by ordinary means and that #strong[the wording is unaltered] — "wording" here means the numbering of the clauses and the sense of the words; differences of layout, line breaks, markup or typeface are not changes to the wording. This permission is granted unconditionally, and no other clause limits it.

12.2 #strong[Recommendation (non-binding).] In machine-readable metadata, the use of `LicenseRef-NEPL-1.0` is recommended. This is a recommendation; not following it is not a breach of clause 3 (clause 12.1).

#line(length: 100%, stroke: 0.4pt + gray)

== Annex A — For reference: examples of mandatory rules by jurisdiction (non-binding)

This Annex creates no rights or obligations; the list is illustrative and not exhaustive.

- #strong[Republic of Korea] — Act on the Regulation of Terms and Conditions, arts. 6, 7, 9; Civil Act art. 559
- #strong[Germany] — Civil Code (BGB) §§305 ff., §306(2), §307, §309 No. 7
- #strong[Austria] — Consumer Protection Act (KSchG) §6; General Civil Code (ABGB) §879(3)
- #strong[Switzerland] — Code of Obligations (OR) arts. 100, 101
- #strong[United Kingdom] — Unfair Contract Terms Act 1977; Consumer Rights Act 2015
- #strong[Japan] — Consumer Contract Act art. 8; Civil Code arts. 548-2 ff. (standard terms)
- #strong[Australia] — Competition and Consumer Act 2010 Sch. 2 (ACL) ss. 18, 23–25, 64
- #strong[Canada] — Copyright Act s.14.1(2); Civil Code of Québec arts. 1435–1437
- #strong[United States] — U.C.C. §§2-316, 2-719

#line(length: 100%, stroke: 0.4pt + gray)

#emph[NEWSNIPER Ethical Public License v1 — draft, second revision. The final wording is subject to legal review. This document is not legal advice.]
