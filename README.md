# Submission README

## Track Chosen
Track A: Fictional Domain Packet

## What I Built
I built a lightweight Streamlit dashboard ("SignalDesk Workflow Health Check") that highlights exactly what's working and what's suspicious in the workflow usage data. It focuses on isolating the effects of two recent changes: the August 4th prompt update and the August 7th review policy change.

## Who It Is For
The fictional product team managing SignalDesk, to help them quickly cut through data noise and make better next decisions.

## Data Or Source Used
The provided `product_usage_events.csv` dataset.

## Assumptions I Made
- `user_rating` and `acceptance_rate` are the truest indicators of workflow health, far outranking the model's self-reported `median_confidence`.
- The traffic spike on August 5th (from a demo account) is noise that should be excluded from performance baselines.

## Data Issues Or Caveats I Noticed
- **Inconsistent casing:** The Product team's name was inconsistently cased (e.g., "product" vs "Product").
- **Missing/invalid values:** Some ratings were missing, and confidence scores were occasionally entered as text ("n/a").
- **Duplicates:** There were duplicate rows (e.g., on Aug 5th for Lead Summary) that needed deduplication.

## What I Would Do Next With More Time
I would build an automated anomaly detection check into this dashboard that runs daily. It would alert the team immediately if `flag_rate` spikes unexpectedly (as it did on Aug 7) or if non-production test accounts flood the data stream, preventing these issues from persisting unnoticed.
