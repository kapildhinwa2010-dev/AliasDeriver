import pytest

from aliasderiver import Fact, KnowledgeNet


def test_fact_basic():
    fact = Fact("alice", "same_as", "bob")
    assert fact.as_tuple() == ("alice", "same_as", "bob")


def test_fact_rejects_empty():
    with pytest.raises(ValueError):
        Fact("", "same_as", "bob")


def test_add_and_len():
    net = KnowledgeNet()
    assert net.add("a", "same_as", "b") is True
    assert net.add("a", "same_as", "b") is False
    assert len(net) == 1


def test_query_pattern():
    net = KnowledgeNet()
    net.add("a", "same_as", "b")
    net.add("b", "same_as", "c")
    assert len(net.query(subject="a")) == 1
    assert len(net.query(obj="c")) == 1


# --- alias derivation (AliasDeriver-specific) ---


def test_derive_aliases_transitive():
    net = KnowledgeNet()
    net.add("x", "same_as", "y")
    net.add("y", "same_as", "z")
    aliases = net.derive_aliases()
    assert aliases["x"] == aliases["y"] == aliases["z"]


def test_derive_aliases_ignores_other_predicates():
    net = KnowledgeNet()
    net.add("x", "knows", "y")
    assert net.derive_aliases() == {}


def test_canonicalize():
    net = KnowledgeNet()
    net.add("bob", "same_as", "robert")
    net.add("robert", "same_as", "rob")
    assert net.canonicalize("rob") == "bob"
    assert net.canonicalize("alice") == "alice"


def test_alias_groups():
    net = KnowledgeNet()
    net.add("a", "same_as", "b")
    net.add("b", "same_as", "c")
    net.add("x", "same_as", "y")
    groups = net.alias_groups()
    assert ["a", "b", "c"] in groups
    assert ["x", "y"] in groups
    assert len(groups) == 2


def test_alias_groups_empty_for_unaliased():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    assert net.alias_groups() == []


def test_derive_aliases_from_custom_predicates():
    net = KnowledgeNet()
    net.add("a", "equals", "b")
    net.add("b", "same_as", "c")
    aliases = net.derive_aliases_from(["same_as", "equals"])
    assert aliases["a"] == aliases["b"] == aliases["c"]


def test_derive_aliases_from_rejects_empty():
    net = KnowledgeNet()
    with pytest.raises(ValueError):
        net.derive_aliases_from([])