import argparse
import json
import logging
import os
import re
import sys
from argparse import ArgumentParser
from collections import Counter
from importlib import import_module
from pathlib import Path
from pprint import pprint
from typing import Optional, Literal, Any, Type

from rich.progress import track

from adfluo import DatasetLoader, Extractor, Sample
from adfluo.dataset import ListLoader, SubsetLoader
from adfluo.extractor import ExtractionOrder
from adfluo.storage import CSVStorage, JSONStorage, PickleStorage, BaseFileBasedStorage
from adfluo.types import StorageFormat, StorageIndexing
from .utils import logger


class StoreNameValuePairs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = dict(v.split("=", 1) for v in values)
        for k, v in list(values.items()):
            if re.fullmatch(r'\".*\"', v):
                values[k] = str(v.strip('"'))
        setattr(namespace, self.dest, values)


class CLIParametersError(Exception):
    pass


def import_obj(class_path: str) \
        -> Optional[Extractor | type[DatasetLoader] | DatasetLoader | list[dict]]:
    # TODO: better error
    assert len(class_path.split(".")) > 1
    *module_path, obj_name = class_path.split(".")
    module_path = ".".join(module_path)

    sys.path.append(os.getcwd())
    mod = import_module(module_path)
    return getattr(mod, obj_name)


def load_dataset(dataset_name: str, dataset_args: Optional[dict[str, Any]]) -> DatasetLoader:
    # first trying to load from json (dataset is a path)
    dataset_path = Path(dataset_name)
    if dataset_path.is_file() and dataset_path.suffix == ".json":
        with open(dataset_path) as json_file:
            json_data = json.load(json_file)
            return ListLoader(json_data)

    else:
        obj = import_obj(dataset_name)
        if isinstance(obj, type) and issubclass(obj, DatasetLoader):
            return obj() if dataset_args is None else obj(**dataset_args)
        elif isinstance(obj, list):
            return ListLoader(obj)
        elif isinstance(obj, DatasetLoader):
            return obj
        elif obj is None:
            raise CLIParametersError(f"Couldn't import any dataset with name {dataset_name}")
        else:
            raise CLIParametersError(f"{dataset_name} isn't a valid dataset object or class")


class Command:
    COMMAND = "command"
    DESCRIPTION = "Command description"

    @staticmethod
    def init_parser(parser: ArgumentParser):
        pass

    @classmethod
    def main(cls, **kwargs):
        pass


class ExtractCommand(Command):
    COMMAND = "extract"
    DESCRIPTION = "Command description"

    @staticmethod
    def init_parser(parser: ArgumentParser):
        parser.add_argument("extractor", type=str,
                            help="Extractor instance in the current namespace")
        parser.add_argument("dataset", type=str,
                            help="Either a path to a json file "
                                 "that has a dataset layout, a list of samples, "
                                 "a DatasetLoader instance, or a DatasetLoader "
                                 "subclass")
        parser.add_argument("--dataset_args", "-ds", nargs="*",
                            action=StoreNameValuePairs,
                            help="If the dataset argument is a class, "
                                 "these are passed as the class's "
                                 "instantiation parameters")
        parser.add_argument("--hparams", "-hp", nargs="*",
                            action=StoreNameValuePairs,
                            help="If the extraction pipeline has hyper parameters, "
                                 "this is used to set them")
        action = parser.add_mutually_exclusive_group(required=False)
        action.add_argument("--output", "-o", type=Path,
                            help="Output file path or folder (depending on format)")
        action.add_argument("--test_samples",
                            action="store_true",
                            help="Just test that samples all can all provide "
                                 "the required input data")
        parser.add_argument("--feats", "-f", nargs="*", type=str,
                            help="Extract only for the specified features")
        parser.add_argument("--exclude_feats", "-ef", nargs="*", type=str,
                            help="Do not run extraction on specified features")
        parser.add_argument("--samples", "-s", nargs="*", type=str,
                            help="Extract only for the specified samples")
        parser.add_argument("--exclude_samples", "-es", nargs="*", type=str,
                            help="Do not run extraction on specified samples")
        parser.add_argument("--indexing",
                            choices=["feature", "sample"],
                            default="sample",
                            help="Storage indexing policy")
        parser.add_argument("--order",
                            choices=["feature", "sample"],
                            default="feature",
                            help="Extraction order (feature-wise or sample-wise)")
        parser.add_argument("--skip_errors",
                            action="store_true",
                            help="Errors while computing a feature for a sample are ignored.")
        parser.add_argument("--no_caching",
                            action="store_true",
                            help="Disable any form of caching (may impact performances "
                                 "but prevents memory overflows")
        parser.add_argument("--storage_format", "-sf", type=str,
                            choices=["csv", "json", "df", "pickle", "split-pickle", "hdf5"],
                            help="Storage format for the extracted features. "
                                 "If none is specified, will be autodetect from file extension")

        parser.add_argument("--hide_progress",
                            action="store_true",
                            help="Don't show progress bars during the extraction")

    @classmethod
    def storage_format_heuristic(cls, output_path: Path, storage_format: Optional[StorageFormat]):
        ext_mapping: dict[str, StorageFormat] = {
            "csv": "csv",
            "json": "json",
            "pkl": "pickle",
            "pckl": "pickle",
            "hdf5": "hdf5",
            "hf5": "hdf5"
        }
        if storage_format is not None:
            return storage_format
        else:
            ext = output_path.suffix.strip(".")
            return ext_mapping.get(ext)

    @classmethod
    def main(cls,
             extractor: str,
             dataset: str,
             dataset_args: Optional[list[str]],
             hparams: Optional[list[tuple[str, str]]],
             output: Path,
             feats: Optional[list[str]],
             exclude_feats: Optional[list[str]],
             samples: Optional[list[str]],
             exclude_samples: Optional[list[str]],
             indexing: StorageIndexing,
             order: ExtractionOrder,
             skip_errors: bool,
             no_caching: bool,
             storage_format: Optional[StorageFormat],
             test_samples: bool,
             hide_progress: bool,
             **kwargs):

        extractor: Extractor = import_obj(extractor)
        if not isinstance(extractor, Extractor):
            raise CLIParametersError(f"{extractor} isn't an extractor instance")
        elif extractor is None:
            raise CLIParametersError(f"Couldn't import extractor {extractor}")

        dataset: DatasetLoader = load_dataset(dataset, dataset_args)

        # setting up extractor hyperparameters
        hparams = dict(hparams) if hparams is not None else {}
        if not set(hparams.keys()) >= extractor.hparams:
            raise CLIParametersError(f"Extractor is missing hyperparameters value for hyperparameters: "
                                     f"{', '.join(extractor.hparams - set(hparams.keys()))}")
        elif extractor.hparams:
            extractor.set_hparams(hparams)

        if test_samples:
            error_count = 0
            for sample in track(dataset):
                sample: Sample
                for input_name in extractor.extraction_DAG.inputs:
                    try:
                        sample[input_name]
                    except Exception as err:
                        print(f"Got error '{type(err)} : {err}' on sample {sample.id} for "
                              f"when asked to provide input '{input_name}'")
                        error_count += 1

            print(f"Got {error_count} errors when testing {len(dataset)} samples from {dataset}")
            exit()

        # keeping only features that are specified in `feats`
        if feats:
            extractor.extraction_DAG.prune_features(keep_only=feats)
        if exclude_feats:
            extractor.extraction_DAG.prune_features(remove=exclude_feats)

        # wrapping the dataset with a subsetloader if only a subset of samples has been specified
        if samples:
            dataset = SubsetLoader(dataset, samples)
        if exclude_samples:
            excluded_samples = set(exclude_samples)
            dataset = SubsetLoader(dataset, [s.id for s in dataset if s.id not in excluded_samples])

        kwargs = {
            "extraction_order": order,
            "storage_indexing": indexing,
            "no_caching": no_caching,
            "skip_errors": skip_errors
        }

        if output is not None:
            storage_format = cls.storage_format_heuristic(output, storage_format)

        if output is None:
            extraction_method = extractor.extract_to_dict
        elif storage_format == "csv":
            extraction_method = extractor.extract_to_csv
        elif storage_format == "df":
            extraction_method = extractor.extract_to_df
        elif storage_format == "json":
            extraction_method = extractor.extract_to_json
        elif storage_format == "pickle":
            extraction_method = extractor.extract_to_pickle
        elif storage_format == "split-pickle":
            extraction_method = extractor.extract_to_pickle_files
        elif storage_format == "hdf5":
            extraction_method = extractor.extract_to_hdf5
        else:
            raise ValueError("Invalid extraction format")

        if storage_format == "split-pickle":
            kwargs["output_folder"] = output
        elif storage_format in {"csv", "json", "pickle", "hdf5"}:
            kwargs["output_file"] = output

        extractor.show_progress = not hide_progress

        # final call to extraction routine
        output_dict = extraction_method(dataset, **kwargs)

        if output is None:
            pprint(output_dict)


class ShowCommand(Command):
    COMMAND = "show"
    DESCRIPTION = "Show informations about an extractor or a dataset"

    @staticmethod
    def init_parser(parser: ArgumentParser):
        # TODO: add dataset args
        parser.add_argument("extractor_or_dataloader", type=str,
                            help="An Extractor instance, or a Dataloader instance or class from the current namespace. "
                                 "Eg: myproject.script.extractor, or myproject.dataloaders.MyDataLoader")
        parser.add_argument("--dataset_args", "-ds", nargs="*",
                            action=StoreNameValuePairs,
                            help="If the dataset argument is a class, "
                                 "these are passed as the class's "
                                 "instantiation parameters")
        parser.add_argument("--test_inputs", "-in", nargs="*", type=str,
                            help="For a datasetloader, test if the following input names are working properly")
        parser.add_argument("--output_file", "-o", type=Path,
                            help="Output file path for the extraction DAG's plot")
        # TODO : option to show DAG tree if possible
        parser.add_argument("--dag", action="store_true",
                            help="If the ")

    @classmethod
    def main(cls,
             extractor_or_dataloader: str,
             dataset_args: Optional[dict[str, Any]],
             output_file: Optional[Path],
             test_inputs: Optional[list[str]],
             dag: bool,
             **kwargs):
        obj = import_obj(extractor_or_dataloader)
        if obj is None:
            logger.error(f"Couldn't import extractor or dataset class {extractor_or_dataloader}")
            exit(1)

        # TODO: attempt at loading from json

        if isinstance(obj, list):
            obj = ListLoader(obj)

        # converting datasetloader *class* to datasetloader *instance*
        if isinstance(obj, type) and issubclass(obj, DatasetLoader):
            obj = obj() if dataset_args is None else obj(**dataset_args)

        if isinstance(obj, Extractor):
            print(f"Info for extractor {extractor_or_dataloader}")

            print(f"{len(obj.extraction_DAG.inputs)} inputs required:")
            for input_name in obj.extraction_DAG.inputs:
                print(f"\t- {input_name}")

            print(f"{len(obj.extraction_DAG.inputs)} hyper-parameters required:")
            for hparam_name in obj.hparams:
                print(f"\t- {hparam_name}")

            print(f"{len(obj.extraction_DAG.features)} features specified:")
            for feat_name in obj.extraction_DAG.features:
                print(f"\t- {feat_name}")

            # TODO: if dag output is specified, print to PNG/else

        elif isinstance(obj, DatasetLoader):
            print(f"Info for dataset {extractor_or_dataloader}:")
            print(f"{len(obj)} samples")
            sample_ids = [sample.id for sample in obj]
            samples_counts = Counter(sample_ids)
            duplicates = sorted([sample_id
                                 for sample_id, count in samples_counts.items()
                                 if count > 1])
            if duplicates:
                print(f"WARNING: The following samples ids are duplicate: "
                      f"{', '.join(duplicates)}")
            print("Testing loading of all samples...")
            samples_it = iter(obj)
            error_count = 0
            valid_samples = set()
            for _ in track(range(len(obj))):
                try:
                    sample = next(samples_it)
                    valid_samples.add(sample.id)
                except StopIteration:
                    break
                except Exception as err:
                    print(f"WARNING: On sample {sample.id} got error {err}")
                    error_count += 1
            print(f"Got {len(obj) - error_count} valid samples and {error_count} errors")

            if test_inputs is not None and test_inputs:
                print("Testing inputs for samples")

                for input_name in test_inputs:
                    error_count = 0
                    print(f"Testing input {input_name}...")
                    samples_it = iter(obj)
                    for _ in track(range(len(obj))):
                        try:
                            sample = next(samples_it)
                        except StopIteration:
                            break
                        except Exception:
                            pass

                        try:
                            _ = sample[input_name]
                        except Exception as err:
                            print(f"WARNING: On sample {sample.id} got error {err}")
                            error_count += 1
                    print(f"Got {len(valid_samples) - error_count} valid samples and {error_count} errors")

        else:
            print("Unsupported object: should be either a dataloader instance or class, "
                  "or an extractor instance")


class MergeCommand(Command):
    COMMAND = "merge"
    DESCRIPTION = "Merge two or more extraction results into one"

    @staticmethod
    def init_parser(parser: ArgumentParser):
        parser.add_argument("inputs", type=Path, nargs="+",
                            help="Input paths to extractions that you want to merge together.")
        parser.add_argument("--output", "-o", type=Path, required=True,
                            help="Output file path or folder (depending on format)")
        parser.add_argument("--indexing",
                            choices=["feature", "sample"],
                            default="sample",
                            help="Storage indexing policy for both inputs and output")
        parser.add_argument("--storage_format", "-sf", type=str,
                            choices=["csv", "json", "df", "pickle", "split-pickle", "hdf5"],
                            help="Storage format for both the inputs and output extractions files. "
                                 "If none is specified, will be autodetect from output file extension")

    @classmethod
    def main(cls,
             inputs: list[Path],
             output: Path,
             indexing: StorageIndexing,
             storage_format: Optional[StorageFormat],
             **kwargs):
        storage_format = ExtractCommand.storage_format_heuristic(output, storage_format)
        if storage_format is None:
            return logger.error("Couldn't determine a storage format")

        storage_class: Type[BaseFileBasedStorage]
        if storage_format in {"csv", "json"}:
            storage_class = CSVStorage if storage_format == "csv" else JSONStorage
            writemode = "w"
        else:
            if storage_format == "pickle":
                storage_class = PickleStorage
                writemode = "wb"
            else:
                return logger.error(f"Storage format {storage_format} not yet supported for this command")

        with output.open(writemode) as out_f:
            storage = storage_class(indexing, out_f)
            for input_path in inputs:
                logger.info(f"Merging {input_path}")
                storage.load_from_file(input_path)

            logger.info(f"Writing merged extraction to {output}")
            storage.write()


commands = [ExtractCommand,
            ShowCommand,
            MergeCommand]

argparser = ArgumentParser()
argparser.add_argument("-v", "--verbose",
                       action="store_true",
                       help="Verbose mode")
subparsers = argparser.add_subparsers()
for command in commands:
    parser = subparsers.add_parser(command.COMMAND)
    parser.set_defaults(func=command.main)
    command.init_parser(parser)


def main():
    args = argparser.parse_args()
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    # Invoking the right subfunction
    try:
        # calling the right command with Namespace converted to kwargs
        args.func(**vars(args))
    except CLIParametersError as err:
        logger.error(str(err))
        exit(1)


if __name__ == '__main__':
    main()
