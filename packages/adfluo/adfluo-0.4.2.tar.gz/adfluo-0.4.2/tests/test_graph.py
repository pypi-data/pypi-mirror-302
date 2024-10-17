from typing import Any

import pytest

from adfluo import SampleProcessor
from adfluo.dataset import DictSample, ListLoader
from adfluo.exceptions import BadSampleException
from adfluo.extraction_graph import ExtractionDAG, SampleProcessorNode, BaseGraphNode
from adfluo.processors import Input, F, Feat
from tests.test_dsfeats import dataset


def test_two_pipeline_parallel():
    def a(arg): pass

    def b(arg): pass

    def c(arg): pass

    def d(arg): pass

    dag = ExtractionDAG()
    dag.add_pipeline(Input("input_b") >> F(a) >> F(b) >> Feat("feat_b"))
    dag.add_pipeline(Input("input_d") >> F(c) >> F(d) >> Feat("feat_d"))
    assert dag.features == {"feat_b", "feat_d"}
    assert dag.inputs == {"input_d", "input_b"}
    assert dag.feature_nodes["feat_b"].parents[0].processor == F(b)
    assert dag.feature_nodes["feat_d"].parents[0].processor == F(d)


def test_two_pipelines_simple_merge():
    def a(arg): pass

    def b(arg): pass

    def c(arg): pass

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test_input") >> F(a) >> F(b) >> Feat("feat_b"))
    dag.add_pipeline(Input("test_input") >> F(a) >> F(c) >> Feat("feat_c"))
    assert dag.features == {"feat_b", "feat_c"}
    assert dag.inputs == {"test_input"}
    assert dag.feature_nodes["feat_b"].parents[0].processor == F(b)
    assert dag.feature_nodes["feat_c"].parents[0].processor == F(c)
    assert (dag.feature_nodes["feat_b"].parents[0].parents[0].processor
            ==
            dag.feature_nodes["feat_c"].parents[0].parents[0].processor
            ==
            F(a))


def test_three_pipelines_simple_merge():
    def a(arg): pass

    def b(arg): pass

    def c(arg): pass

    def d(arg): pass

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test_input") >> F(a) >> F(b) >> Feat("feat_b"))
    dag.add_pipeline(Input("test_input") >> F(a) >> F(c) >> Feat("feat_c"))
    dag.add_pipeline(Input("test_input") >> F(a) >> F(d) >> Feat("feat_d"))
    assert dag.features == {"feat_b", "feat_c", "feat_d"}
    assert dag.inputs == {"test_input"}
    assert dag.feature_nodes["feat_b"].parents[0].processor == F(b)
    assert dag.feature_nodes["feat_c"].parents[0].processor == F(c)
    assert dag.feature_nodes["feat_d"].parents[0].processor == F(d)
    assert (dag.feature_nodes["feat_b"].parents[0].parents[0].processor
            ==
            dag.feature_nodes["feat_c"].parents[0].parents[0].processor
            ==
            dag.feature_nodes["feat_d"].parents[0].parents[0].processor
            ==
            F(a))


def test_branches_merge():
    def a(arg): pass

    def b(arg_a, arg_b): pass

    def c(arg_a, arg_b): pass

    def d(arg): pass

    dag = ExtractionDAG()
    dag.add_pipeline((Input("input_a") >> F(a) | Input("input_b")) >> F(b) >> F(d) >> Feat("feat_b"))
    dag.add_pipeline((Input("input_a") >> F(a) | Input("input_b")) >> F(c) >> F(d) >> Feat("feat_c"))
    assert dag.features == {"feat_b", "feat_c"}
    assert dag.inputs == {"input_a", "input_b"}
    assert dag.feature_nodes["feat_b"].parents[0].processor == F(d)
    assert dag.feature_nodes["feat_c"].parents[0].processor == F(d)
    assert dag.feature_nodes["feat_b"].parents[0].parents[0].processor == F(b)
    assert dag.feature_nodes["feat_c"].parents[0].parents[0].processor == F(c)
    assert (len(dag.feature_nodes["feat_b"].parents[0].parents[0].parents)
            ==
            len(dag.feature_nodes["feat_c"].parents[0].parents[0].parents)
            == 2)
    assert (dag.feature_nodes["feat_b"].parents[0].parents[0].parents
            ==
            dag.feature_nodes["feat_c"].parents[0].parents[0].parents)


def test_dependency_solving():
    def a(arg): pass

    def b(arg_a, arg_b): pass

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test_input") >> F(a) >> Feat("feat_a"))
    dag.add_pipeline((Input("test_input") | Feat("feat_a")) >> F(b) >> Feat("feat_b"))
    dag.solve_dependencies()
    assert dag.features == {"feat_b", "feat_a"}
    assert dag.inputs == {"test_input"}
    assert dag.feature_nodes["feat_a"].children[0].processor == F(b)
    assert dag.feature_nodes["feat_b"].parents[0].processor == F(b)


def test_unsolvable_feature():
    def a(arg): pass

    def b(arg): pass

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test_input") >> F(a) >> Feat("feat_a"))
    dag.add_pipeline(Feat("feat_c") >> F(b) >> Feat("feat_b"))
    with pytest.raises(ValueError):
        dag.solve_dependencies()


def test_feature_already_in_graph():
    def a(arg): pass

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test_input") >> F(a) >> Feat("feat_a"))
    with pytest.raises(AssertionError):
        dag.add_pipeline(Input("test_other_input") >> F(a) >> Feat("feat_a"))


def test_caching_simple():
    def add_one(n: int):
        return n + 1

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test_input") >> F(add_one) >> Feat("feat_a"))
    dag.add_pipeline(Input("test_input") >> F(add_one) >> Feat("feat_b"))
    sample = DictSample({"test_input": 1}, 0)
    assert dag.feature_nodes["feat_a"].parents[0] == dag.feature_nodes["feat_b"].parents[0]
    cached_node: SampleProcessorNode = dag.feature_nodes["feat_a"].parents[0]
    assert len(cached_node.children) == 2
    out = dag.feature_nodes["feat_a"][sample]
    assert out == 2
    assert len(cached_node.cache._samples_cache) == 1
    assert cached_node.cache._samples_cache["0"] == 2
    assert cached_node.cache._samples_cache_hits["0"] == 1

    out = dag.feature_nodes["feat_a"][sample]
    assert out == 2
    assert len(cached_node.cache._samples_cache) == 0


def test_caching_advanced():
    def add_one(n: int):
        return n + 1

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test_input") >> F(add_one) >> Feat("feat_a"))
    dag.add_pipeline(Input("test_input") >> F(add_one) >> Feat("feat_b"))
    dag.add_pipeline(Input("test_input") >> F(add_one) >> F(add_one) >> Feat("feat_c"))
    dag.add_pipeline(Input("test_input") >> F(add_one) >> F(add_one) >> Feat("feat_d"))
    sample_a = DictSample({"test_input": 1}, 0)
    sample_b = DictSample({"test_input": 2}, 1)
    assert dag.feature_nodes["feat_a"].parents[0] == dag.feature_nodes["feat_b"].parents[0]
    assert dag.feature_nodes["feat_c"].parents[0] == dag.feature_nodes["feat_d"].parents[0]
    cached_node: SampleProcessorNode = dag.feature_nodes["feat_a"].parents[0]
    assert len(cached_node.children) == 3
    out = dag.feature_nodes["feat_a"][sample_a]
    assert out == 2
    out = dag.feature_nodes["feat_a"][sample_b]
    assert out == 3
    assert len(cached_node.cache._samples_cache) == 2
    assert cached_node.cache._samples_cache["0"] == 2
    assert cached_node.cache._samples_cache["1"] == 3
    assert cached_node.cache._samples_cache_hits["0"] == 1

    out = dag.feature_nodes["feat_b"][sample_a]
    assert cached_node.cache._samples_cache_hits["0"] == 2


# TODO: make a cache test where the sample processors are checking that they shouldn't be called more
#  than once

def test_error_management():
    # todo : check that skip_error raises a badsample
    # todo : check that skip_error=false raises the right exception
    pass


def test_pruning():
    def a(n: int):
        return a + 1

    def b(n: int):
        return n ** 2

    def c(n: int):
        return n * 2

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test") >> F(a) >> Feat("plus_one"))
    dag.add_pipeline(Input("test") >> F(a) >> F(b) >> Feat("squared"))
    dag.add_pipeline(Input("test") >> F(a) >> F(c) >> Feat("double"))
    dag.solve_dependencies()
    assert dag.features == {"plus_one", "squared", "double"}
    dag.prune_features(keep_only=["plus_one"])

    assert dag.features == {"plus_one"}
    assert len(dag.nodes) == 3  # input, F(a), Feat(plus_one)
    assert len(dag.feature_nodes["plus_one"].parents[0].children) == 1

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test") >> F(a) >> Feat("plus_one"))
    dag.add_pipeline(Feat("plus_one") >> F(b) >> Feat("squared"))
    dag.add_pipeline(Feat("plus_one") >> F(c) >> Feat("double"))
    dag.solve_dependencies()

    assert dag.features == {"plus_one", "squared", "double"}
    dag.prune_features(keep_only=["plus_one"])

    assert dag.features == {"plus_one"}
    assert len(dag.nodes) == 3  # input, F(a), Feat(plus_one)
    assert len(dag.feature_nodes["plus_one"].parents[0].children) == 1

    dag = ExtractionDAG()
    dag.add_pipeline(Input("test") >> F(a) >> Feat("plus_one"))
    dag.add_pipeline(Feat("plus_one") >> F(b) >> Feat("squared"))
    dag.add_pipeline(Feat("plus_one") >> F(c) >> Feat("double"))
    dag.solve_dependencies()

    assert dag.features == {"plus_one", "squared", "double"}
    dag.prune_features(keep_only=["double"])

    assert dag.features == {"double"}
    for node in dag.nodes:
        print(str(node))
    assert len(dag.nodes) == 5  # input, F(a), Feat(plus_one), F(b), Feat("double")
    assert len(dag.feature_nodes["double"].parents[0].parents[0].children) == 1


def test_rombus_DAG():
    dag = ExtractionDAG()
    dag.add_pipeline(
        Input("input_a")
        >> F(lambda x: x + 3)
        >> (F(lambda x: x + 1) | F(lambda x: x / 2))
        >> F(lambda x, y: x + y)
        >> Feat("feat_a")
    )


def test_duplicate_feature():
    dag = ExtractionDAG()
    with pytest.raises(AssertionError, match="Duplicate name for feature name 'feat_a'"):
        dag.add_pipeline(
            Input("input_a")
            >> (Feat("feat_a") | Feat("feat_a"))
        )


def test_use_feature_before_creation():
    dag = ExtractionDAG()
    dag.add_pipeline(
        (Feat("feat_b") | Feat("feat_a"))
        >> F(lambda x, y: x * y)
        >> Feat("feat_c")
    )

    dag.add_pipeline(
        Input("input_a")
        >> F(lambda x: x + 3)
        >> Feat("feat_a")
    )
    dag.add_pipeline(
        Input("input_a")
        >> F(lambda x: x + 1)
        >> Feat("feat_b")
    )
    dag.solve_dependencies()


def test_inexisting_use_feature_before_creation():
    dag = ExtractionDAG()
    dag.add_pipeline(
        (Feat("feat_b") | Feat("feat_a"))
        >> F(lambda x, y: x * y)
        >> Feat("feat_c")
    )


def test_error_in_proc():
    def failing_proc(val: int) -> int:
        raise RuntimeError("Houston we have a problem")

    dag = ExtractionDAG()
    dag.add_pipeline(
        Input("data_a") >> F(failing_proc) >> Feat("feat_a")
    )
    dataloader = ListLoader(dataset)
    dag.set_loader(dataloader)
    sample = next(iter(dataloader))
    with pytest.raises(RuntimeError, match="Houston we have a problem"):
        dag.extract_sample_wise(sample, iter)


def test_badsample():
    class FailingProc(SampleProcessor):

        def process(self, val: int) -> int:
            if self.current_sample.id == "0":
                raise RuntimeError("Houston we have a problem")
            else:
                return val

    dag = ExtractionDAG()
    dag.add_pipeline(
        Input("data_a") >> FailingProc() >> Feat("feat_a")
    )
    dataloader = ListLoader(dataset)
    dag.set_loader(dataloader)
    BaseGraphNode.extraction_policy.skip_errors = True

    sample_0 = next(iter(dataloader))
    with pytest.raises(BadSampleException):
        # TODO : check for sample info in exception and stack data
        dag.feature_nodes["feat_a"][sample_0]

    feat_a = dag.extract_feature_wise("feat_a", iter)
    assert "0" not in feat_a
    BaseGraphNode.extraction_policy.skip_errors = False


def test_feature_default():
    class FailingProc(SampleProcessor):

        def process(self, val: int) -> int:
            if self.current_sample.id == "0":
                raise RuntimeError("Houston we have a problem")
            else:
                return val

    dag = ExtractionDAG()
    dag.add_pipeline(
        Input("data_a") >> FailingProc() >> Feat("feat_a", default=0)
    )
    dag.add_pipeline(
        Feat("feat_a") >> F(lambda x: x + 1) >> Feat("feat_b")
    )
    dataloader = ListLoader(dataset)
    dag.set_loader(dataloader)

    BaseGraphNode.extraction_policy.skip_errors = False

    sample_0 = next(iter(dataloader))
    with pytest.raises(RuntimeError, match="Houston we have a problem"):
        # TODO : check for sample info in exception and stack data
        dag.feature_nodes["feat_b"][sample_0]

    BaseGraphNode.extraction_policy.skip_errors = True
    feat_a = dag.extract_feature_wise("feat_b", iter)
    assert set(feat_a.values()) == set(range(1, 11))
