# AliasDeriver

AliasDeriver is a small Python library for storing simple subject–predicate–object facts and deriving alias groups from equality facts. The project is at version 0.1.0 and currently consists of a single Python module with a test suite; it is an in-memory library, not a command-line application or persistent graph database.

## Features

- `Fact` represents one triple and rejects empty or non-string subject, predicate, and object values.
- `KnowledgeNet` stores unique facts in memory. `add()` reports whether a fact was new; `query()` filters by subject, predicate, and/or object; `facts()` returns all facts in sorted order.
- `derive_aliases()` treats `same_as` facts as undirected equality edges and returns a mapping from every name in a connected component to its lexicographically smallest member.
- `derive_aliases_from(predicates)` derives the same kind of mapping using any supplied set of predicates as equality edges.
- `canonicalize(name)` returns the derived representative, or the input name when it is not part of an equality component. `alias_groups()` returns sorted groups containing more than one name.
- The fact store also provides `chain()` for a bounded walk along one predicate and `interference()` for ranking facts connected to a queried name by the module's co-occurrence count.

## Requirements

The project metadata declares Python 3.9 or later and NumPy 1.24 or later. The repository's `requirements.txt` also includes pytest for running tests.

## Install

From the repository root:

```bash
python -m pip install .
```

To install the repository's listed runtime and test requirements instead:

```bash
python -m pip install -r requirements.txt
```

There is no configured command-line entry point. Use the Python module API:

```python
from aliasderiver import KnowledgeNet

net = KnowledgeNet()
net.add("bob", "same_as", "Robert")
net.add("Robert", "same_as", "Bobby")

print(net.canonicalize("Bobby"))  # Bobby
print(net.alias_groups())         # [['Bobby', 'Robert', 'bob']]
```

The canonical name is selected with Python's `min()` over the component; it is a deterministic representative, not a claim about which name is authoritative.

## Tests and CI

On the inspected repository commit `a7b20a1af8db4562930a44ae1086a291f372e506`, the local test suite was run with `python -m pytest -q -p no:cacheprovider` and reported **11 passed**. This is a local test result, not a statement about the status of a GitHub Actions run.

The CI workflow is configured to run pytest, compile the module and tests, and perform an import smoke test on Python 3.10, 3.11, and 3.12. A separate workflow configures CodeQL analysis for Python. Workflow configuration alone does not establish the result of a remote run.

Run the tests locally with:

```bash
python -m pytest -q
```

## Limitations and scope

- Facts are held only in process memory; there is no persistence, file/database adapter, or command-line interface in the repository.
- Alias derivation uses connected components of selected predicates, assumes those facts express symmetric equality, and does not validate or resolve contradictory assertions.
- The canonical representative is chosen alphabetically/lexicographically by `min()`, not by domain-specific authority or preference.
- `chain()` follows one matching outgoing fact at each step (the first one stored) rather than exploring or returning all possible paths. `interference()` is a simple co-occurrence-based ranking, not a general reasoning or relevance model.
- No benchmark results are included.

## License

The repository includes an MIT License. See [LICENSE](LICENSE) for its terms.
