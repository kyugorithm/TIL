[Meeting Minutes] Initial Discussion on Implementing New Video ML QC Process

1. Meeting Objectives
• Discuss the detailed implementation methods for the newly proposed video ML QC process.
• Determine methods to verify ML QC results (e.g., leveraging OStream, new implementation within CMS).
• Define player implementation approaches, required resources, responsible teams, and timelines.
• Enhance mutual understanding and alignment among teams regarding the new QC process.

2. Key Discussion Points
• [Hansol] Shared background and objectives:
  ◦ Aim to decide specific implementation details following the proposal for an ML-based video QC process.
  ◦ Key decisions include: 
	① OStream vs. CMS implementation, 
	② Player implementation approach (possible reuse of OStream code), 
	③ Defining development resources (team responsibilities, schedule, location).
  ◦ [Joey] Noted potential lack of prior synchronization and differences in understanding among teams.

• Current QC Process and Role of OStream:
  ◦ [Aspyn] OStream player is currently used by the MO team for Post-QC (quality check of transcoded videos served to customers).
  ◦ [Joey/Ping] Proposed ML QC seems aligned with Pre-QC (checking original file specifications/quality), requiring significant new development if integrated with OStream.
  ◦ [Aspyn] Highlighted the need to distinguish clearly between Pre-QC and Post-QC, preferring to view Post-QC results via OStream (similar to the actual customer environment).

• Proposed ML QC Integration and Requirements:
  ◦ ML QC Items: Defined by MO (led by Aspyn, Valley) and delivered to the ML team. Around 30 items including pixel issues, logo detection, etc.
  ◦ Failure Handling: Remastering or requesting re-supply from CP (primarily CP re-supply).
  ◦ Result Verification Requirements: Similar to Baton player, allowing ML QC report items to link directly to the relevant timecode for visual confirmation. Perfect accuracy is not mandatory but should be practical. Current manual Excel-based verification is inefficient.
  ◦ ML Model Accuracy & Manual Review: Current ML model may yield false positives. MO team should manually review ML results before proceeding. (Formal agreement with MO team pending.)

• Implementation Method Discussions (OStream vs. CMS vs. In-house Development):
  ◦ Leveraging OStream:
    ▪ Advantages: Existing player available, alignment with current Post-QC workflow.
    ▪ Considerations: Requires cooperation with GSN (player development), associated costs.
    ▪ [Enoch] Short-term possibility: If ML team provides JSON-formatted results (timecode, messages), timecode-linked playback through a separate panel within OStream (similar to current VMAF/QVBR display) may be feasible.

  ◦ CMS-based Player Development:
    ▪ Advantages: Independent from OStream, customizable UI/UX specifically for QC purposes.
    ▪ Considerations: New player development needed.

  ◦ [Ping/Joey] In-house PoC Development:
    ▪ Given current low ML model reliability, an interim solution before formal OStream or CMS implementation.
    ▪ Quickly implement basic functionality (timecode navigation) using a simple API and open-source web player.
    ▪ Low technical barriers by utilizing existing MP4 files (SD/HD) generated from the current pipeline.
    ▪ Potential start around May-June.

• Redefined Process Flow Discussion:
  ◦ Pre-QC (ML) → Pass → Transcoding → Post-QC
  ◦ [Joey/Hansol] Option 1: Original file → Transcode only highest quality version first → ML QC (26 items) → Verify via player (MO team) → If Pass: transcode all formats / If Fail: request re-supply from CP.
    ▪ Benefit: Reduces unnecessary transcoding costs/time, efficient ML model feedback loop.
  ◦ [Ping] Key Consideration: Ideally block transcoding upon Pre-QC failure in the long run, but initially focus on verification and feedback without blocking due to ML model accuracy concerns (Hansol agreed).

• [Wooner] Project Urgency: Management request to complete within the year. Immediate need for a verification tool (player) to utilize currently developed ML models.

3. Summary of Discussions/Consensus
• Agreed on the necessity of ML-based QC implementation and achieving the completion goal within the year.
• Given the current ML model accuracy, creating an efficient review environment (player) for ML results and model improvement is a priority. The player must support timecode-based navigation.
• Implementation location for result verification (OStream, CMS, in-house PoC) has various pros and cons. Short-term, an in-house PoC (simple player + API) is a strongly considered solution.
• Ideal process involves blocking transcoding at the Pre-QC stage upon detection of issues, but realistically starting with initial transcoding (single high-quality version) followed by ML QC result review.
• Recognized current gaps in understanding between teams about Pre-QC/Post-QC definitions, specific ML QC roles, and OStream utilization scope. Clarification needed going forward.

4. Future Plans / Action Items
1. ML Team: Define and share ML QC result data format (JSON format including timecodes, error types, messages).
2. All Teams: Design and propose optimal solutions for short-term verification player implementation.
