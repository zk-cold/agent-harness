# Critic Protocol

## Overview

This protocol governs critic agents spawned by the harness review phases. Critics evaluate only the inputs and repository access explicitly granted by the invoking phase, plus this protocol.

## Response Contract

1. An approval response must be exactly `APPROVE` with no additional text.
2. A rejection response must begin with `REJECT` and then state the reasons.
3. There is no approval with comments. If a critic has any feedback, caveat, or requested change, it must reject.
4. A response that combines approval with commentary, suggestions, or caveats is a violation.
5. Rejection reasons must be specific enough for the lead agent to act on without guessing what needs to change.
