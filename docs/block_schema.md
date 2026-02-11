Block format:

prev_hash | timestamp | agent | type | payload | hash | signature

Fields:
- prev_hash  : previous block hash
- timestamp  : unix time (UTC)
- agent      : signer identity
- type       : observation | proposal | verdict
- payload    : message content
- hash       : SHA256(prev_hash + fields)
- signature  : RSA signature of hash
