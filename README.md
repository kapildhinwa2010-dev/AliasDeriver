# AliasDeriver

[![CI](https://github.com/kapildhinwa2010-dev/AliasDeriver/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/AliasDeriver/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/AliasDeriver/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/AliasDeriver/actions/workflows/codeql.yml)


Canonical names and transitive alias groups derived from equality facts.

**Part of the [Kapildhinwa2010-dev Toolkit](https://github.com/kapildhinwa2010-dev/Kapildhinwa2010-dev).**

## What it does

AliasDeriver is the IDENTITY layer of the fact-tool family. It derives
transitive alias closures over configurable equality predicates
("same_as" by default), canonicalizes any name to its group
representative, and lists alias groups. Storage extras live in
FactBase; rules in RuleEngine; path analysis in ChainReasoner.

## Install

```bash
pip install -r requirements.txt
```

## Quick start

```python
from aliasderiver import KnowledgeNet

net = KnowledgeNet()
net.add("bob", "same_as", "Robert")
net.add("Robert", "same_as", "Bobby")
print(net.canonicalize("Bobby"))  # "Bobby" (min of the group)
print(net.alias_groups())         # [["Bobby", "Robert", "bob"]]
```

## API

- add / query / facts / chain / interference - shared triple store
- derive_aliases() / derive_aliases_from(predicates) - closure maps
- canonicalize(name) - group representative (itself if unaliased)
- alias_groups() - sorted groups with more than one member

## Honest results and limitations

- The canonical representative is min() of the group - byte-order
  sorted, so it is deterministic but arbitrary in meaning (lowercase
  beats uppercase).
- Equality is assumed symmetric and transitive; conflicting facts are
  merged silently, no contradiction detection.
- Only equality-style predicates are handled; other predicates are
  ignored by the closure.

## License

MIT - see [LICENSE](LICENSE).
