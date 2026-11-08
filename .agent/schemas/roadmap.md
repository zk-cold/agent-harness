# Definitions

## Roadmap Operations
Running `.agent/scripts/roadmap <backend> <target repo path>`, with the roadmap's backend, followed by one of:
- `add <title> <body> [<parent>]`: adding a roadmap item, as a sub-item of `<parent>` if given, and printing its ID.
- `close <item>`: closing an item and its open sub-items as not delivered.
- `complete <item>`: completing an item, closing its open sub-items as not delivered, then completing each ancestor whose sub-items are all closed.
- `edit <item> <title> [<body>]`: replacing an item's title, and its body if given.
- `show <item>`: showing an item, printing only its content written by the target repo's owner, members or collaborators.
- `list`: listing the open items authored by the target repo's owner, members or collaborators.
- `candidates`: listing candidates, the items `list` lists that have no open sub-items.
- `descendants <item>`: listing the items `list` lists that descend from `<item>`.

# Invariants

## Roadmap Backends
Each `.agent/scripts/roadmap-<backend>` must implement `## Roadmap Operations`.
