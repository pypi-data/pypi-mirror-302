from abc import ABC, abstractmethod
import os
import logging
import traceback
from functools import partial
import pandas as pd
import gatools as ga


class Transformation(ABC):
    def __init__(self, *args, lazy=False, **kwargs):
        # Initialize transformation with arguments and parameters
        self.args = args
        self.kwargs = kwargs
        self.lazy = lazy
        self.df = None  # Dataframe produced by the transformation
        self.meta = {}  # Metadata produced by the transformation
        self.ctx = None  # Pipeline

        self.prev_df_fname = None  # Filename of the previous step's dataframe
        self.prev_df = None  # Dataframe from the previous step
        self.prev_meta = None

        # Parameters for step deletion and caching
        self.delete_step = False
        self.df_delete_cache = False

    @abstractmethod
    def process(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__

    def _run(self, ctx, ignore_failed=False):
        from flexpipe.pipeline import Pipeline

        self.ctx: Pipeline = ctx
        # Execute the transformation within the pipeline context
        skip = ctx.tracker.start_step(self)
        if skip:
            # Skip step if it is lazy and already done
            return ctx.tracker.steps[self.name]["end"]["state"]

        # Check last step
        val, last_step = ctx.tracker.check_last_step_state(self)
        if not val and not ignore_failed:
            x = f"Last step {last_step!r} failed, you should delete the step in tracker file or pass `ignore_failed`"
            log.error(x)
            raise RuntimeError(x)

        # # Load the previous dataframe if available
        # self.prev_df_fname = ctx.tracker.get_last_df()
        # if self.prev_df_fname and os.path.exists(self.prev_df_fname):
        #     self.prev_df = pd.read_csv(self.prev_df_fname, index_col=0)

        # if _fm := self.get_last_fname("meta_out_json"):
        #     self.prev_meta = ga.load_json(_fm)

        # Get the filename function for this step
        self.get_fname = partial(ctx.tracker.get_filename, _class=self)
        self.get_outdir = partial(ctx.tracker.get_outdir, _class=self)

        if os.path.exists(mfn := self.get_outdir() / "meta_out.json"):
            self.meta = ga.load_json(mfn)

        # Run the actual transformation process
        try:
            ret = self.process(*self.args, **self.kwargs) or {}
            meta = {**self.meta, **ret}
            # meta = ret or self.meta  # Use returned metadata or default to self.meta
        except Exception as _:
            log.error(
                f"An error occured during step {self.name!r}: {traceback.format_exc()}"
            )
            ctx.tracker.end_step(self, state="failed")
        else:
            # End the step, saving the dataframe and metadata
            ctx.tracker.end_step(self, df=self.df, meta=meta)
        finally:
            return ctx.tracker.steps[self.name]["end"]["state"]

    def get_last_fname(self, key):
        _, last_step = self.ctx.tracker.check_last_step_state(self)
        if last_step in self.ctx.tracker.steps:
            return self.ctx.tracker.steps[last_step]["end"].get(key)

    def get_key_fname(self, step, key):
        if step in self.ctx.tracker.steps:
            if x := self.ctx.tracker.steps[step]["end"].get(key):
                return x
        log.error(f"File {key!r} was not found in step {step!r}")

    def get_key_df(self, step, key):
        if fname := self.get_key_fname(step, key):
            return pd.read_csv(fname, index_col=0)


log = logging.getLogger(__name__)
